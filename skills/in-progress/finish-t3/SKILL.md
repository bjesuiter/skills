---
name: finish-t3
description: Finish a T3 Code worktree and archive its thread. By default, check OpenLoops and unsaved work. Use deep-check to also inspect unique ignored files or no-checks or skip-checks to skip both checks.
---

# Finish T3

Check that the thread's work is accounted for, remove the finished worktree,
then archive the thread. This skill performs no merge. Treat an invocation as
permission to finish and archive under the selected mode.

## 1. Identify the thread and mode

Use `t3_worktree_status` and `git worktree list --porcelain` to identify the
thread's worktree, branch, main checkout, and integration target. For another
thread, read it with `t3_thread_read` first and retain its environment and
workspace identity throughout.

- `no-checks` and `skip-checks` select the same mode. When explicitly requested
  (for example, `finish-t3 no-checks`), go directly to step 4 after identifying
  the worktree. Skip steps 2 and 3, including `deep-check`.
- `deep-check` adds the ignored-file check to the standard checks.
- With no mode specified, run the standard checks in steps 2 and 3.

## 2. Account for OpenLoops

Read the thread's conversation and relevant activity, including older pages
and truncated messages needed to account for its work. Identify outstanding
requests, promised actions, findings, deferred decisions, and follow-ups.
Check each against concrete evidence of its disposition:

- Completed work or a merged PR.
- An open PR carrying the work forward.
- A follow-up issue or new session with enough context to resume.
- A durable note recording the remaining work or a deliberate decision to
  defer or drop it.

A loop need not be completed to be handled. Record each disposition with its
PR, issue, session, or note location. A vague intention to handle it later is
still open. Use existing artifacts where possible. Resolve routine loose ends
within the authorized scope; use the repository's conventions for notes and
follow-ups. Ask for a decision only when a disposition needs user judgment or
an external action lacks authorization. Create a new session only when asked.
Every identified loop must have a concrete disposition before cleanup.

## 3. Check worktree preservation

Inspect tracked modifications (staged and unstaged) and untracked files with
`git status --porcelain=v1 --untracked-files=all`. Standard mode excludes
Git-ignored files, including ignored files absent from the main checkout.
Avoid reading their contents during this mode.

Refresh relevant remote refs and establish separately:

- Whether any local commits are absent from the intended remote. Check the
  actual branch/ref rather than assuming an upstream exists or is current.
- Whether any commits or equivalent changes remain outside the integration
  target. Use ancestry for normal merges; verify the merged PR and equivalent
  changes for squash/cherry-pick, including commits after the PR head.

Dirty/new files, unpushed commits, and unmerged changes require an explicit
preservation disposition. Commit/push only within the existing authorization;
otherwise retain the worktree and report what needs saving. An open PR can
handle an OpenLoop while its unmerged branch still needs retention. A verified
remote branch/PR may preserve those commits without a merge; retain that
branch and document its location. Never delete an unmerged branch as cleanup.
A note describing work is not a backup of its files or commits.

### Additional deep-check

Only when `deep-check` is requested, read and complete
[the deep-check procedure](references/deep-check.md) before cleanup. Leave
that reference and its script unloaded in standard mode.

## 4. Finish and archive

In standard and deep-check modes, proceed once every OpenLoop and preservation
finding has a verified disposition. In `no-checks` mode, retain the branch.
Complete repository-required finishing actions before removal.
Stop only processes associated with this worktree and clear its PR watches.

Run `git worktree remove <absolute-path>` from a surviving checkout; keep all
subsequent shell working directories outside the target. Remove only the
intended secondary worktree, retaining the main checkout. Use `git branch -d`
only for a verified merged branch; retain the branch if safe deletion refuses.
Force removal or force branch deletion requires explicit authorization. If
removal refuses because of ignored files in standard mode, report the refusal
and offer deep-check; do not silently expand the check or force deletion.

Verify the target is absent from `git worktree list`. Removal is the final
workspace operation: changing the shell directory does not rebind T3's thread.
Then call `t3_thread_organize` with `action: "archive"`, omitting `threadId`
for this thread or supplying the verified thread/environment for another one.
Archive only after cleanup succeeds. If tools are unavailable or an operation
fails, retain the thread as active and report the incomplete step.

Report the mode, removed worktree, retained branches, and archive outcome
concisely. In `no-checks` mode, state that OpenLoop and preservation checks
were skipped. Otherwise report their results and state that ignored files
were excluded in standard mode. Link mentioned artifacts and use the returned
T3 link when naming a thread.
