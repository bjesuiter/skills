---
name: integrate
description: Use when the user explicitly asks to "integrate this change" or "integrate this PR" and wants you to prepare and merge it through GitHub.
---

# Integrate

The explicit request authorizes merging the intended GitHub PR once it passes
the gate. Read and complete [GitHub PR preparation](references/github-pr-preparation.md)
in merge mode. Loading that reference from another skill grants no merge authority.

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
