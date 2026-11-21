# Prepare a local branch

1. Identify the source, target worktree, intended remote and requested target
   branch (otherwise the repository default). Inspect all outgoing commits and
   preserve unrelated changes. Commit the intended work on the source. In
   preparation-only mode, use a topic branch if starting on the target.
2. Follow [verification](verification.md), starting with autoreview before
   rebasing. Fix findings and retain the successful review and its original SHA
   through rebases, including conflict resolution. Review subsequent changes
   beyond rebase reconciliation under repository policy.
3. Fetch the intended remote target. On success, prepare against a base that
   includes both the fetched tip and the local target. If they diverged, reconcile
   intended commits on a preparation branch and verify the combined result.
   On fetch failure, use the known local target tip and record the failure and
   base SHA. Leave the target branch and its worktree untouched during preparation.
4. Rebase the topic branch onto the selected base, clarify behaviorally ambiguous
   conflicts, and complete verification on the resulting tree. When integrating
   work already on the target, verify its outgoing commits directly against the
   remote base (last known upstream when offline). Never rebase the target.
5. Record readiness for this source and base, using the repository journal if
   available. Identify any required check or approval still outstanding.
