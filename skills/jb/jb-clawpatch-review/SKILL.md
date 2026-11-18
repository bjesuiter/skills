---
name: jb-clawpatch-review
description: Use when the user mentions Clawpatch/clawpatch.ai, semantic feature review, repo-wide AI audit, persistent findings, or clawpatch init/map/review/report/fix/revalidate.
---

# JB Clawpatch Review

Use Clawpatch for semantic repo review with persistent findings and optional one-finding-at-a-time repairs.

Clawpatch is not a replacement for `jb-autoreview`: use `jb-autoreview` for final closeout review of a local diff, branch, commit, or PR; use this skill for feature-map-driven repo audits and tracked findings.

## Prerequisites

Required:

- `clawpatch`
- `git`
- a supported Clawpatch provider, usually local `codex`

Check setup:

```bash
clawpatch --help
clawpatch doctor
```

If provider/model/effort matters, pass them explicitly instead of changing silently:

```bash
clawpatch review --provider codex --model <model> --reasoning-effort high
```

## Core Workflow

Run from the repo root unless `--root <path>` is explicitly needed.

```bash
clawpatch init
clawpatch map
clawpatch review --limit 10
clawpatch report
```

Then inspect findings before acting:

```bash
clawpatch next
clawpatch show --finding <id>
```

Generate structured output when the agent needs to parse results:

```bash
clawpatch status --json
clawpatch report --json
clawpatch show --finding <id> --json
```

## Review Scope

Use batches for large repos:

```bash
clawpatch review --limit 10 --jobs 10
```

Narrow to a feature or project when the user asks for a specific area:

```bash
clawpatch review --feature <id>
clawpatch review --project <name-or-root>
```

Review changes since a ref when that is the requested scope:

```bash
clawpatch review --since origin/main
```

Append extra reviewer guidance with a prompt file:

```bash
clawpatch review --limit 10 --prompt-file /tmp/clawpatch-guidance.md
```

## Finding Handling

Treat every finding as advisory.

1. Read the finding:

   ```bash
   clawpatch show --finding <id>
   ```

2. Verify it by reading the real code path and adjacent files.
3. Reject speculative, low-value, unrealistic, or over-broad findings.
4. Triage verified status:

   ```bash
   clawpatch triage --finding <id> --status false-positive --note "Reason"
   clawpatch triage --finding <id> --status wont-fix --note "Reason"
   clawpatch triage --finding <id> --status uncertain --note "Reason"
   ```

5. For accepted issues, prefer small manual fixes unless the user explicitly asks Clawpatch to patch.

## Explicit Fix Workflow

Only fix one explicit finding at a time.

Before fixing:

- Confirm the finding is valid.
- Confirm the worktree is clean or intentionally dirty.
- Do not run `clawpatch fix` for multiple findings in one command.

```bash
clawpatch fix --finding <id>
```

After fixing:

```bash
git diff
clawpatch revalidate --finding <id>
```

Then run focused project checks from `.clawpatch/project.json` or repo conventions, for example:

```bash
npm test
npm run typecheck
npm run lint
```

If the fix is wrong or too broad, revert manually and explain why. Do not commit unless explicitly asked.

## Revalidation

Revalidate one finding after a manual or Clawpatch fix:

```bash
clawpatch revalidate --finding <id>
```

Revalidate a changed scope when the user asks for broader confirmation:

```bash
clawpatch revalidate --since origin/main
```

Use filters for batches:

```bash
clawpatch revalidate --status open --severity high --limit 10
```

## Guardrails

- Never blindly apply Clawpatch findings or patches.
- Always inspect code before accepting a finding.
- Always inspect `git diff` after `clawpatch fix`.
- Prefer manual fixes for nuanced product or architecture decisions.
- Keep fixes at the right ownership boundary; avoid broad refactors unless the bug class requires it.
- Do not push, commit, open PRs, or land changes unless explicitly requested.
- Do not run destructive git commands as part of this workflow.
- Keep `.clawpatch/` state as audit data; only remove it when the user requests cleanup.
- If Clawpatch reports provider/config trouble, run `clawpatch doctor --json` and fix setup before retrying review.

## Final Report

Include:

- exact Clawpatch commands run
- scope reviewed: feature/project/since ref/limit
- findings accepted, rejected, or triaged, with brief reasons
- fixes applied, if any
- revalidation result
- tests/checks run
- remaining open findings or next recommended command
