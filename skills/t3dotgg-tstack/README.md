# tstack

Skills from [t3dotgg/tstack](https://github.com/t3dotgg/tstack). The pinned upstream revision and import date are in [vendor.json5](vendor.json5).

Include `babysit-pr`, `file-pr`, `full-send`, `full-stop`, `leaving-pr-comments`, `modernize`, `sol-loop`, and `takeover` when refreshing this import.

Keep `takeover` for agent-assisted work on open-source projects. JB uses it infrequently today.

Keep `babysit-pr` to follow up on human and bot reviews and catch conflicts or changes to the base branch while a PR is open. This is useful even without GitHub Actions.

Keep `modernize` for stale implementation worktrees with open PRs. It checks whether the original goal still needs work and what changed on the base branch before updating the PR.

Use `integrate` and `prepare-to-merge` as the names for JB's planned adaptations of `full-send` and `full-stop`. Both should use the same GitHub PR preparation and readiness checks. `integrate` merges once the gate passes. `prepare-to-merge` leaves the ready PR open for a human to merge. Tie evidence to the reviewed commits, rerun affected checks when the base advances, and request a targeted re-review if conflict resolution changes behavior.

### Upstream changes to successor skills

Use semantic comparison for these successors, including the shared preparation flow.

- `full-send` → [`integrate`](../jb/integrate/SKILL.md)
- `full-stop` → [`prepare-to-merge`](../jb/prepare-to-merge/SKILL.md)

Keep `leaving-pr-comments` for GitHub. When another channel needs attribution, consider a shared `public-agent-attribution` skill for messages an agent sends on JB's behalf, including email. Share the verified model or harness name and sender attribution rules, and let each channel choose its own format. Keep the GitHub callout in `leaving-pr-comments`.

Exclude `council` while JB has only one subscription that can provide a council member. Bring it back once two such subscriptions are available. Claude is the likely second one.
