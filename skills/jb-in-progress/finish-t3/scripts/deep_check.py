#!/usr/bin/env python3
"""Read-only inventory of ignored worktree files; no dependencies beyond Git."""

import argparse
import json
import os
from pathlib import Path
import stat
import subprocess
import sys


def git(root, *args):
    return subprocess.check_output(
        ['git', '-C', str(root), *args], stderr=subprocess.PIPE
    )


def checkout(value):
    root = Path(value).resolve(strict=True)
    actual = Path(os.fsdecode(git(root, 'rev-parse', '--show-toplevel')).strip())
    if root != actual.resolve():
        raise ValueError('Specify checkout roots, not subdirectories')
    return root


def signature(info):
    return (info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns, info.st_ctime_ns)


def compare(source, destination):
    """Compare regular files without following a final symlink; detect concurrent edits."""
    flags = os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK
    with os.fdopen(os.open(source, flags), 'rb') as left:
        with os.fdopen(os.open(destination, flags), 'rb') as right:
            before = [os.fstat(left.fileno()), os.fstat(right.fileno())]
            if not all(stat.S_ISREG(item.st_mode) for item in before):
                raise ValueError('Not regular files')
            same = before[0].st_size == before[1].st_size
            if same:
                while True:
                    a, b = left.read(1024 * 1024), right.read(1024 * 1024)
                    if a != b:
                        same = False
                        break
                    if not a:
                        break
            after = [os.fstat(left.fileno()), os.fstat(right.fileno())]
            paths = [source.lstat(), destination.lstat()]
            if any(signature(a) != signature(b) or signature(b) != signature(c)
                   for a, b, c in zip(before, after, paths)):
                raise ValueError('File changed during comparison')
            return 'identical' if same else 'different'


def inspect(root, main, relative):
    parts = Path(relative).parts
    if Path(relative).is_absolute() or '..' in parts:
        raise ValueError('Unsafe Git path')
    # Do not traverse symlinked directories in either checkout.
    for base in (root, main):
        parent = base
        for part in parts[:-1]:
            parent /= part
            if parent.is_symlink():
                return 'symlink_parent'
    source, destination = root / relative, main / relative
    info = source.lstat()
    if not stat.S_ISREG(info.st_mode):
        return 'symlink' if stat.S_ISLNK(info.st_mode) else 'special_file'
    try:
        other = destination.lstat()
    except FileNotFoundError:
        return 'missing'
    if not stat.S_ISREG(other.st_mode):
        return 'type_mismatch'
    return compare(source, destination)


def scan(root, main):
    root, main = checkout(root), checkout(main)
    if root == main:
        raise ValueError('Worktree and main checkout must differ')
    def common(path):
        value = os.fsdecode(git(path, 'rev-parse', '--git-common-dir')).strip()
        return (path / value).resolve()
    if common(root) != common(main):
        raise ValueError('Checkouts must belong to the same Git repository')
    # Git's ls-files omits special files such as FIFOs. Walk without following
    # links, then ask Git to apply its ignore rules (tracked files stay excluded).
    paths = []
    def walk_error(error):
        raise error
    for directory, folders, files in os.walk(root, followlinks=False, onerror=walk_error):
        folders[:] = [name for name in folders if name != '.git']
        links = [name for name in folders if (Path(directory) / name).is_symlink()]
        folders[:] = [name for name in folders if name not in links]
        for name in files + links:
            path = Path(directory) / name
            if path == root / '.git':
                continue
            paths.append(os.fsencode(str(path.relative_to(root))))
    result = subprocess.run(
        ['git', '-C', str(root), 'check-ignore', '--stdin', '-z'],
        input=b''.join(path + b'\0' for path in paths),
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    if result.returncode not in (0, 1):
        raise ValueError('Cannot apply Git ignore rules')
    names = result.stdout
    findings = []
    for raw in sorted(set(names.split(b'\0')) - {b''}):
        relative = os.fsdecode(raw)
        try:
            status = inspect(root, main, relative)
        except (OSError, ValueError):
            # Do not emit exception text that could disclose contents or link targets.
            status = 'inspection_error'
        item = {'path': relative, 'status': status}
        if status != 'identical':
            item['disposition'] = 'review_required'
            if any(part in {'dist', 'build', 'node_modules', '.cache', '__pycache__'}
                   for part in Path(relative).parts[:-1]):
                item['hint'] = 'possible_reproducible_output; verify inputs and recipe'
        findings.append(item)
    return {
        'schema_version': 1,
        'worktree': str(root),
        'main_checkout': str(main),
        'ignored_files': findings,
        'review_required': sum(x['status'] != 'identical' for x in findings),
        'inspection_errors': sum(x['status'] == 'inspection_error' for x in findings),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--worktree', required=True)
    parser.add_argument('--main-checkout', required=True)
    args = parser.parse_args()
    try:
        result = scan(args.worktree, args.main_checkout)
    except (OSError, ValueError, subprocess.CalledProcessError):
        print(json.dumps({'error': 'Cannot inventory checkouts; verify roots and Git access'}))
        return 2
    print(json.dumps(result, indent=2, ensure_ascii=True))
    return 2 if result['inspection_errors'] else int(bool(result['review_required']))


if __name__ == '__main__':
    sys.exit(main())
