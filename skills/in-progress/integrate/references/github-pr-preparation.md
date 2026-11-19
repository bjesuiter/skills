# GitHub PR preparation

Use the mode selected by the calling skill. Preparation has no merge step.

## Identify the change

Read repository instructions and confirm the intended GitHub repository,
worktree, source branch, target branch, and existing PR, if any. Use the PR's
actual target branch or the requested target for a new PR. Use the repository's
default only when neither specifies one. The request covers commits, pushes,
PR creation or updates, and a leased rewrite of the task's own branch after a
rebase where repository policy permits it. Check actual GitHub and harness
permissions before mutating remote state. In handoff mode, apply the calling
skill's auto-merge and queue checks before working on an existing PR.

Inspect staged, unstaged, and outgoing changes. Finish and commit only the
requested change, preserving unrelated work. Create a topic branch when
starting from the target branch. Use the repo's prescribed checks and review
workflow. Run the direct verification the change warrants within the session's
permissions. Request independent review through the permitted workflow and
resolve actionable findings before advancing.

## Refresh, verify, and publish

1. Fetch the target tip and confirm the live PR head and base ref. If someone
   updated the head or retargeted the PR, inspect that change before proceeding.
   Preserve concurrent contributions. Rebase the topic branch onto the current
   target tip when needed, using the repository's branch-update convention.
   Resolve conflicts according to intended behavior and ask about ambiguous
   behavior. Request a targeted re-review of any behavior changed by conflict
   resolution. Reuse earlier review only where the reviewed patch and its
   behavior still apply. Record the original reviewed SHA and the scope of
   any follow-up review.
2. Record the candidate head SHA and target tip SHA. Select checks and builds
   for the final diff and affected behavior. Record each command or observed
   result, the SHA or merge candidate it ran against, and the result or run
   link. When either SHA changes, reassess the diff, dependencies, configuration,
   and conflict resolutions. Rerun affected or missing checks and builds.
   Carry forward unaffected results with their original SHAs and a brief
   reason they still apply. Run the required full gate if impact is unclear.
3. Push only the intended branch and create or update the PR with the verified
   scope and proof summary. For an authorized rewrite after rebase, use an
   explicit `--force-with-lease=<ref>:<expected-remote-sha>` against the head
   you inspected. Re-read a rejected lease and reconcile the new head before
   trying again. Apply handoff mode's live queue checks before pushing.
   In T3 Code, link each created or updated PR with its full URL using
   `link_pull_request` or `link_pull_requests` immediately after publication.
4. Verify the live PR against the candidate. Use GitHub Actions when configured
   and confirm check runs cover the current head, GitHub's test merge commit,
   or the merge group as applicable. Confirm the tested merge candidate
   includes the verified target tip when the check covers the combined tree.
   Follow repository-required external
   checks too. Inspect review decisions and bot findings on the current diff.
   Fix genuine findings or failures, document the disposition of each finding,
   and repeat verification for the new candidate.

In T3 Code, use `watch_pull_request` when required checks or reviews are pending
and follow the watcher's continuation. On resumption, re-read the live PR
before acting. Unwatch at completion, handoff, or before asking the user.
Elsewhere, follow the harness's available wait mechanism. Pause for an actual
decision or permission blocker and report the pending state if the harness
cannot continue waiting.

## Readiness gate

Re-fetch the target branch and re-read the live PR immediately before reporting
readiness or merging. The gate passes when all of these hold:

- The PR is open and ready for review. The live head and target tip match
  the verified pair. The branch is up to date under the repository's policy,
  and GitHub reports the PR as mergeable.
- Proof covers the final diff. Required checks are satisfied under GitHub's
  rules and any repository-required builds or direct checks passed. No known
  failure or deferred required check remains.
- Required approvals are current, no human change request remains, and
  configured automated reviewers have finished with findings addressed.

When the base advances, refresh the branch and repeat the affected checks and
live gate. If a service cannot establish any required state, report it as
unverified. Leave the mode-specific action to the calling skill.
