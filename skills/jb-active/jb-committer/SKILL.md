---
name: jb-committer
description: Use when the user asks to commit, commit-current, commit-only, group git changes, or draft commit messages.
---

# Committer

Inspect staged, unstaged, and untracked changes before committing. Group changes by logical purpose and write concise messages describing their semantic meaning. Create multiple commits when the work contains independent changes.

## Scope

- For `commit`, commit all coherent changes in the working tree.
- For `commit-current` or `commit-only`, commit only files related to the current conversation's change. Leave unrelated changes untouched.

## Beans

- Commit a related Beans file with its implementation.
- If the ticket is finished, mark it done before committing.
- If an unfinished ticket needs only a status update, commit that update separately.

## Finish

Push to the remote after creating the requested commits.
