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
starting from the target branch. Take ownership through merge or handoff as
selected by the calling skill.

## Prove and independently review the change

An explicit PR-mode request authorizes task-scoped testing, including running
the app or dev server, browser and device checks, and screenshots. Where
repository instructions would otherwise require asking before a test method,
the request supplies that permission. Follow repository instructions for how to
test and honor harness approvals.

Use direct evidence for the behavior changed. For a bug, reproduce it and
rerun the same case after the fix where practical. Add a focused regression
test when existing coverage misses the behavior and the repo has a test setup.
For UI or runtime changes, observe the affected behavior in the running app
when that is what the change claims to fix. If material behavior cannot be
verified, use the blocker procedure below.

Use the repository's independent review workflow when specified. Otherwise use
`sol-loop` if available and runnable, with `jb-autoreview` as the fallback.
Self-review alone does not satisfy this step. If no independent review can be
completed, stop before pushing and report the blocker. Start the review before
rebasing and follow [verification](verification.md) to track proof and review
against the candidate.

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
2. Complete verification on the resulting candidate and target tip.
3. Push only the intended branch and create or update the PR with the verified
   scope and proof summary. For an authorized rewrite after rebase, use an
   explicit `--force-with-lease=<ref>:<expected-remote-sha>` against the head
   you inspected. Re-read a rejected lease and reconcile the new head before
   trying again. Apply handoff mode's live queue checks before pushing.
   Use the repository's filing workflow or `file-pr` when available. Follow the
   repository's title conventions, explain the problem and solution, include
   proof and the actual model and harness attribution, and check the title,
   body, and attachments for secrets or private details before publishing.
   In T3 Code, link each created or updated PR with its full URL using
   `link_pull_request` or `link_pull_requests` immediately after publication.
   Open the PR ready for review, or mark an existing draft ready after initial
   verification. Respect an explicit request to keep it in draft. In handoff
   mode, verify and report that draft and its outstanding checks or reviews.
   In merge mode, use the blocker procedure before changing the requested
   draft status. For a draft handoff, verify the live head, base, and draft
   status and report gates that still require a ready PR.
4. Verify the live PR against the candidate. Use GitHub Actions when configured
   and confirm check runs cover the current head, GitHub's test merge commit,
   or the merge group as applicable. Confirm the tested merge candidate
   includes the verified target tip when the check covers the combined tree.
   Follow repository-required external
   checks too. Inspect review decisions and bot findings on the current diff.
   Fix genuine findings or failures and verify each fix before pushing the new
   candidate. Respond to dismissed findings with a written reason and resolve
   the thread where supported. Use `leaving-pr-comments` when available. Address
   material advisory findings already received and wait only for required checks
   and reviewers.

In T3 Code, use `watch_pull_request` when required checks or reviews are pending
and follow the watcher's continuation. On resumption, re-read the live PR
before acting. Unwatch at completion, handoff, or before asking the user.
Elsewhere, use `pr-wait` when available and suitable for the required gates,
or the harness's available wait mechanism. Report the pending state if the
harness cannot continue waiting.

## Resolve blockers

Continue autonomously while the issue is within the request and can be resolved
with evidence. Use the harness question tool when proof is unavailable, the
gate cannot pass, the goal is materially ambiguous, or further action needs
permission. In T3 Code, unwatch before asking. Include the PR link if one
exists, the blocker, and the options with your recommendation first. If you
cannot get an answer, leave any PR
open and unmerged and lead the handoff with the decision needed. In handoff
mode, report when required human approval is the only remaining gate.

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
  required automated reviewers have finished with findings addressed.

When the base advances, refresh the branch and repeat the affected checks and
live gate. If a service cannot establish any required state, report it as
unverified. Leave the mode-specific action to the calling skill.
