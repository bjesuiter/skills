---
name: jb-worktree
description: Manage Git worktrees with the wtp CLI. Use when creating isolated branch worktrees, jumping between worktrees, bootstrapping per-worktree setup, or cleaning up merged branches.
homepage: https://github.com/satococoa/wtp
metadata: {"clawdbot":{"emoji":"🌳","requires":{"bins":["wtp"]},"install":[{"id":"brew","kind":"brew","formula":"satococoa/tap/wtp","bins":["wtp"],"label":"Install wtp (brew)"}]}}
skill_author: bjesuiter
---

# wtp Git Worktrees

Based on satococoa's `wtp` workflow: https://dev.to/satococoa/wtp-a-better-git-worktree-cli-tool-4i8l

Use `wtp` instead of raw `git worktree` when you want predictable paths, easier branch handling, setup hooks, and fast navigation.

## Why use it

- `wtp init` creates a starter `.wtp.yml` in the repo root
- `wtp add feature/auth` creates `../worktrees/feature/auth` automatically
- `wtp add` can create or reuse local/remote branches
- `.wtp.yml` can copy `.env`, create symlinks, and run bootstrap commands
- `wtp cd` and `wtp exec` make navigation and command execution easier
- `wtp remove --with-branch` cleans up both the worktree and its branch

## Install

```bash
brew install satococoa/tap/wtp
```

Alternative:

```bash
go install github.com/satococoa/wtp/v2/cmd/wtp@latest
```

## Quick start

```bash
# Create a starter .wtp.yml in the repository root
wtp init

# Create a worktree from an existing branch
wtp add feature/auth

# Create a new branch + worktree
wtp add -b feature/new-ui

# Create from a specific base ref
wtp add -b hotfix/login origin/main

# List all worktrees
wtp list

# Print the absolute path for a worktree
wtp cd feature/auth
wtp cd @

# Run a command inside a worktree
wtp exec feature/auth -- npm test

# Remove a worktree
wtp remove feature/auth

# Remove a worktree and delete its branch too
wtp remove --with-branch feature/auth
```

## Agent workflow

When the user asks to work in a separate branch or isolated checkout:

1. Check whether the repo already has `.wtp.yml`; if not, prefer `wtp init`
2. Check the current worktrees with `wtp list`
3. Create or open the target worktree with `wtp add ...`
4. Run commands inside it with either:
   - `cd "$(wtp cd <name>)" && ...`
   - `wtp exec <name> -- <command>`
5. When the work is done and merged, clean up with `wtp remove --with-branch <name>`

Prefer:
- `wtp add -b <branch>` for new work
- `wtp add <branch>` when the branch already exists locally or remotely
- `wtp exec <name> -- <command>` for one-off commands

Avoid force removal of dirty worktrees unless the user explicitly asks.

## `wtp init`

Use this first in repos that do not have a config yet:

```bash
wtp init
```

It creates `.wtp.yml` in the repository root with a starter configuration and example hooks. If `.wtp.yml` already exists, `wtp init` errors instead of overwriting it.

## Recommended `.wtp.yml`

`wtp init` gives you a starter file. Customize it like this when the project needs automatic setup for each new worktree:

```yaml
version: "1.0"
defaults:
  base_dir: "../worktrees"

hooks:
  post_create:
    - type: copy
      from: ".env"
      to: ".env"

    - type: symlink
      from: ".bin"
      to: ".bin"

    - type: command
      command: "npm ci"

    - type: command
      command: "npm run db:setup"
```

This is especially useful for repos that need local env files, shared tool directories, or bootstrap commands in every new worktree.

## Shell integration

For interactive shells, enable completions and navigation hooks:

```bash
eval "$(wtp shell-init zsh)"
# or
# eval "$(wtp shell-init bash)"
# wtp shell-init fish | source
```

Then `wtp cd feature/auth` can switch directly in the shell, and interactive `wtp add` can auto-switch into the new worktree.

## Useful patterns

```bash
# Return to the main worktree
wtp cd @

# Run tests in the main worktree
wtp exec @ -- npm test

# Force remove a dirty worktree only when you are sure
wtp remove --force feature/auth

# Remove worktree and force-delete its branch
wtp remove --with-branch --force-branch feature/auth
```

## Notes

- Default generated paths are based on branch names under `../worktrees`
- Remote-only branches are tracked automatically when unambiguous
- If multiple remotes contain the same branch name, create a local tracking branch first
- `wtp cd` is also useful in scripts because it prints the resolved absolute path
