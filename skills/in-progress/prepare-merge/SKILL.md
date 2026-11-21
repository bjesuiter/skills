---
name: prepare-merge
description: Use when the user asks to prepare a branch for merge. Prepare locally by default, or prepare and leave a GitHub PR open when requested.
---

# Prepare Merge

For `prepare-merge` or `prepare-merge local`, complete
[local preparation](references/local-preparation.md). Report the prepared head,
base, checks, review and any blocker. Note when the base was verified locally
after a failed fetch. Stop before merge or push.

## GitHub PR mode

Use this path for `prepare-merge pr` or an explicit request to prepare a pull
request. Complete [GitHub PR preparation](references/github-pr-preparation.md)
in handoff mode. Leave the PR open. Never merge, enable auto-merge, enter a
merge queue, push to the target branch, or delegate those actions.

Before working on an existing PR, before each push, and at handoff, check the
live PR for auto-merge and merge queue enrollment. Disable auto-merge and
dequeue the PR when active. With GitHub CLI, inspect `autoMergeRequest` via
`gh pr view` and use `gh pr merge --disable-auto <PR>` only to turn off an
active request. Inspect queue membership separately through GitHub's PR UI
or API. Verify both are off after making changes. If you
cannot establish or enforce that state, stop and report the blocker. Report
any settings or enrollment you changed.

After the final live check, unwatch the PR in T3 Code before handing it back
or asking the user for a decision. Report the PR URL, verified head and base,
proof, review outcomes, and remaining risks. Use the actual GitHub state:

- **Ready to merge** when the gate passes and the PR is open, ready for review,
  and free of automatic merge enrollment.
- **Waiting for required approval** when required human approval is the sole
  unresolved gate. Identify the outstanding approval.
- **Blocked** when anything else prevents readiness. State what you tried and
  what remains.
- **Already merged** if GitHub reports that someone else merged it.

Adapted from Theo Browne's [full-stop](https://github.com/t3dotgg/tstack) under
the [MIT License](LICENSE).
