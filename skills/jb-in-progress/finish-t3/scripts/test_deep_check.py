import os
from pathlib import Path
import subprocess
import tempfile
import unittest

from deep_check import scan


class DeepCheckTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.main = Path(self.temp.name) / 'main'
        self.work = Path(self.temp.name) / 'work'
        self.main.mkdir()
        self.git('init')
        (self.main / '.gitignore').write_text('ignored/\n')
        self.git('add', '.')
        self.git('-c', 'user.name=Test', '-c', 'user.email=test@example.org',
                 'commit', '-m', 'fixture')
        self.git('worktree', 'add', '-b', 'test-work', str(self.work))

    def git(self, *args):
        return subprocess.check_output(['git', '-C', str(self.main), *args],
                                       stderr=subprocess.PIPE)

    def put(self, base, name, content):
        path = base / 'ignored' / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
        return path

    def test_inventory_and_binary_comparison(self):
        for base in (self.main, self.work):
            self.put(base, 'same', b'\x00secret\xff')
        self.put(self.main, 'different', b'ab')
        self.put(self.work, 'different', b'ac')
        self.put(self.work, 'odd\nname', b'unique')
        self.put(self.work, 'dist/manual.db', b'irreplaceable')
        (self.work / 'ordinary-untracked').write_text('excluded')
        result = scan(self.work, self.main)
        items = {item['path']: item for item in result['ignored_files']}
        self.assertEqual(set(items), {'ignored/same', 'ignored/different',
                                     'ignored/odd\nname', 'ignored/dist/manual.db'})
        self.assertEqual(items['ignored/same']['status'], 'identical')
        self.assertEqual(items['ignored/different']['status'], 'different')
        self.assertEqual(items['ignored/odd\nname']['status'], 'missing')
        self.assertEqual(items['ignored/dist/manual.db']['disposition'], 'review_required')
        self.assertEqual(result['review_required'], 3)

    def test_symlinks_are_not_followed(self):
        self.put(self.work, 'nested/data', b'local')
        (self.main / 'ignored').mkdir()
        (self.main / 'ignored/nested').symlink_to(self.work / 'ignored/nested')
        (self.work / 'ignored/link').symlink_to('/no/such/file')
        result = scan(self.work, self.main)
        statuses = {item['status'] for item in result['ignored_files']}
        self.assertEqual(statuses, {'symlink_parent', 'symlink'})

    def test_special_files_and_invalid_checkout(self):
        self.put(self.work, 'placeholder', b'')
        os.mkfifo(self.work / 'ignored/pipe')
        result = scan(self.work, self.main)
        self.assertIn('special_file', [item['status'] for item in result['ignored_files']])
        with self.assertRaises(ValueError):
            scan(self.main, self.main)
        with self.assertRaises(ValueError):
            scan(self.work / 'ignored', self.main)


if __name__ == '__main__':
    unittest.main()
