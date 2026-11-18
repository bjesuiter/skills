---
name: jb-beans
description: Use when a repository contains `.beans/` or the user mentions Beans, beans prime, flat-file issues, task tracking, or issue status changes.
---

# Beans

Use `beans` to manage Git-friendly Markdown issues stored in `.beans/`.

## Start with project guidance

Before working in a Beans-enabled repository, run:

```bash
beans prime
```

Follow its output. It defines the repository's workflow, issue model, statuses, and agent expectations and takes precedence over generic guidance here.

## Installation and binary safety

Install the Go CLI through Homebrew or Go:

```bash
brew install hmans/beans/beans
# or
go install github.com/hmans/beans@latest
```

Never install `beans` with npm or Bun. The package with that name is an unrelated legacy Node program. If Beans fails unexpectedly, especially with a `coffee-script` module error, diagnose command shadowing:

```bash
which -a beans
beans version
```

Use an absolute path to the working Homebrew or Go binary when necessary, then leave broader PATH repair outside the task.

## Agent workflow

Prefer `--json` whenever a command supports it. A typical lifecycle is:

```bash
# Discover actionable or existing work
beans list --json --ready
beans list --json -S "login"
beans show --json <id>

# Create and start work
beans create --json "Add login screen" -t feature -s todo -d "Build the initial login UI"
beans update --json <id> -s in-progress

# Record useful progress
beans update --json <id> --body-append "## Notes\n\nStarted implementation"

# Complete with a durable summary
beans update --json <id> -s completed \
  --body-append "## Summary of Changes\n\nImplemented and validated the feature."
```

Keep issue bodies current with reproduction details, decisions, checklists, progress, and final summaries. Use structured parent/blocking relationships instead of duplicating dependencies only in prose.

Use narrow body replacements or `--if-match` updates when concurrent edits could otherwise overwrite content. Run `beans check` after substantial configuration or relationship changes. Archive work only when the project workflow or user requests it.

## Discover current commands

Do not rely on a copied command catalog. Inspect the installed CLI because supported fields and flags can change:

```bash
beans --help
beans <command> --help
beans version
```

For advanced filtering and relationship traversal, inspect `beans graphql --help` and `beans graphql --schema`. Beans has no built-in `beans tui`; use the separate `beans-tui` tool when requested.

Project: https://github.com/hmans/beans
