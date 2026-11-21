---
name: integrate
description: Use when the user explicitly asks to integrate a change. Merge locally by default, or use GitHub when the user explicitly requests a PR merge.
---

# Integrate

An integration request authorizes the merge once preparation passes. Use
local mode for `integrate` or
`integrate local`. Use GitHub mode for `integrate pr` or an explicit request
to integrate a pull request.

Both paths use references bundled with the companion skill `prepare-merge`.
If a sibling path is unavailable, locate that skill through the catalog and
read the corresponding reference. Install both skills to use `integrate`.

## Local merge

Complete [local preparation](../../jb/prepare-merge/references/local-preparation.md).
Respect required PRs, approvals and branch protections. Proceed once the selected
candidate passes the required checks and review.

Use the repository's exclusive merge slot, when available, only for target
synchronization, merge and push. Recheck the source and local target, and fetch
the remote target before merging. If it has advanced, release the slot, refresh
preparation against the new base and retry with the original review. Refresh
proof for any changed source. If fetch fails, use the verified local base
after checking that the candidate still includes the local target.

Merge the verified candidate into the local target using repository convention.
The resulting tree must match the verified tree, otherwise recheck it outside
the slot before publication. For work already on the target, skip the merge
when its tip is the verified candidate.

After a successful fetch, push the exact verified integration commit to the
intended target ref with a normal push. Confirm the remote contains it. On a
rejected push, preserve the local merge, fetch and reconcile any remote advance,
then repeat affected verification before retrying. If a push result is
ambiguous, inspect the remote before retrying or claiming success.

If fetch failed, finish the local merge and report **merged locally, push
pending**. When resuming publication, fetch first and confirm the intended
outgoing commits. Push if still current, or reconcile and reverify against the
advanced target. Report the integration commit, checks, review and publication
state. A push attempted with an unknown outcome is **publication unconfirmed**.

## GitHub PR merge

Complete [GitHub PR preparation](../../jb/prepare-merge/references/github-pr-preparation.md)
in merge mode.

After the gate passes, re-read the live head and target branch tip immediately
before submitting the merge. If either differs from the verified pair, return
to preparation. Use the repository's allowed merge method and branch protection.
Bind the request to the verified head, for example with `gh pr merge
--match-head-commit <verified-head-sha>`. Never use an admin bypass.

If the repository requires a merge queue, submit the verified head through it
and wait for GitHub to confirm the outcome. Use auto-merge only if the configured
merge path requires it. Confirm that any pending merge still targets the
verified change. If the head or target branch changes before completion,
re-evaluate the gate and rely on the queue's checks for the new merge group
where they cover the affected proof. If the gate no longer passes, cancel the
pending merge if permitted and return to preparation. Resolve an ambiguous
merge response by reading the live PR before retrying.

Report the PR URL, verified head and base, merge commit, proof and review
outcomes, and decisions made on the user's behalf. If blocked, report the
actual PR state and what remains.

Adapted from Theo Browne's [full-send](https://github.com/t3dotgg/tstack) under
the [MIT License](LICENSE).
