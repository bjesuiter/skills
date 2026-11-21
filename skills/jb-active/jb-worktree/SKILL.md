---
name: jb-worktree
description: Use when creating, switching, bootstrapping, or cleaning Git worktrees, including T3 Code worktrees.
metadata:
  homepage: https://github.com/satococoa/wtp
  skill_author: bjesuiter
  clawdbot:
    emoji: "🌳"
    requires:
      bins: [wtp]
    install:
      - id: brew
        kind: brew
        formula: satococoa/tap/wtp
        bins: [wtp]
        label: Install wtp (brew)
---

# wtp Git Worktrees

Based on satococoa's `wtp` workflow: https://dev.to/satococoa/wtp-a-better-git-worktree-cli-tool-4i8l

Use `wtp` for worktrees it manages. For T3 Code worktrees, use the app's workspace tools for creation and the completion workflow below for cleanup.

## Worktree ownership

Before creating or finishing a worktree, inspect `git worktree list --porcelain` and the current app's workspace binding. Use `wtp list` to distinguish managed worktrees from external ones; a path under `~/.t3/worktrees/` is also a T3 hint.

- **wtp-managed:** follow the wtp workflow below.
- **T3-created or otherwise unmanaged:** remove directly with Git after the completion checks. Skip `wtp remove`, which cannot manage these worktrees.
- **New T3 workspace:** use the exposed app orchestration tools to bind the thread to its workspace. Creating a directory with `wtp` or Git, or changing the shell directory, does not update T3's thread binding. Use a handoff for the current thread and an explicitly bound launch when the user requests a separate thread.

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

For wtp-managed worktrees, when the user asks to work in a separate branch or isolated checkout:

1. Check whether the repo already has `.wtp.yml`; if not, prefer `wtp init`
2. Before creating or editing hooks, choose the install command with the package-manager policy below
3. Check the current worktrees with `wtp list`
4. Create or open the target worktree with `wtp add ...`
5. Run commands inside it with either:
   - `cd "$(wtp cd <name>)" && ...`
   - `wtp exec <name> -- <command>`
6. When the work is done and merged, follow the completion workflow below.

Prefer:
- `wtp add -b <branch>` for new work
- `wtp add <branch>` when the branch already exists locally or remotely
- `wtp exec <name> -- <command>` for one-off commands

Avoid force removal of dirty worktrees unless the user explicitly asks.

## Finish a worktree

1. Inspect the target's Git status and branch. Preserve pending changes and any local files that still need to be kept. Finish only after the requested merge and push are verified; for a merge into `main`, check that the feature tip is contained in `main` and that the resulting commits are on the intended remote. A squash or cherry-pick requires checking the equivalent changes instead of ancestry.
2. Stop only the dev servers and background processes associated with this worktree.
3. Run removal from a surviving checkout, such as the main checkout listed by `git worktree list --porcelain`. Keep subsequent commands' working directory outside the target.
4. Choose removal by ownership:
   - wtp-managed: `wtp remove --with-branch <name>`, using the name or relative path reported by wtp.
   - T3-created or otherwise unmanaged: `git worktree remove <absolute-path>`, then `git branch -d <branch>` once its merge is verified. If deletion refuses because the branch is checked out elsewhere or its merge cannot be established, retain it and report why.
5. Verify the target is absent from `git worktree list` and report the merge, push, and cleanup result. Delete a remote branch only when requested or required by the repository's workflow.

For T3, a shell-directory change leaves the thread bound to the removed workspace. Complete cleanup as the final workspace operation and tell the user which worktree was removed; new work needs a valid app workspace binding.

## `wtp init`

Use this first in repos that do not have a config yet:

```bash
wtp init
```

It creates `.wtp.yml` in the repository root with a starter configuration and example hooks. If `.wtp.yml` already exists, `wtp init` errors instead of overwriting it.

## Recommended `.wtp.yml`

`wtp init` gives you a starter file. Customize the `post_create` install command with this policy:

1. If `package.json` declares `packageManager`, treat it as authoritative and use that manager's install command.
2. Otherwise, choose from the lockfile:
   - `bun.lock` or `bun.lockb` → `bun install`
   - `pnpm-lock.yaml` → `pnpm install --frozen-lockfile`
   - `package-lock.json` → `npm ci`
3. If neither is present, inspect the project's setup documentation before adding an install hook.

Use this template and replace `<install command>` with the command selected by the policy above:

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
      command: "<install command>"

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
