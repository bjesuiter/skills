---
name: nb
description: Create, list, search, edit, organize, bookmark, or synchronize notes and todos with the `nb` CLI. Use whenever the user asks to work with an nb notebook or nb-managed content.
---

# nb

Use the `nb` CLI for Git-backed notes, todos, bookmarks, and notebooks.

## Storage safety

Never edit, copy, move, delete, or commit files inside `~/.nb/*` directly. Always use `nb` commands so indexes and automatic Git history remain consistent. This applies to long notes and bulk operations too.

## Select a notebook

Inspect notebook context before mutating content:

```bash
nb notebooks
nb notebooks current
nb use <notebook>
```

Use the `nb <notebook>:` prefix when an operation should target a notebook other than the current one. Create a notebook only when requested or clearly required:

```bash
nb notebooks add <name>
```

## Core note workflow

```bash
# Create
nb add -t "Title" -c "Content"
nb <notebook>: add -t "Title" -c "Content"

# Inspect and search
nb list
nb show <id-or-title>
nb search "query"

# Update and organize
nb edit <id-or-title>
nb move <id> <notebook>:

# Synchronize configured remotes
nb sync
```

Quote titles containing spaces. Resolve ambiguous matches by listing or searching before editing, moving, or deleting. Let destructive commands prompt unless the user explicitly authorized non-interactive deletion.

## Todos and bookmarks

Use the dedicated command families rather than encoding these as ordinary notes:

```bash
nb todo add "Task"
nb todos open
nb todo do <id>

nb bookmark <url>
nb bookmark list
nb bookmark search "query"
```

Add tags, comments, or due dates when the request provides them. Use `nb sync` after changes only when synchronization is requested or established by the surrounding workflow.

## Discover current syntax

Do not rely on a copied flag catalog. Inspect the installed CLI for less-common operations such as tags, folders, Boolean search, imports, exports, Git checkpoints, renaming, or deletion:

```bash
nb help
nb help <command>
nb version
```

Project: https://github.com/xwmx/nb
