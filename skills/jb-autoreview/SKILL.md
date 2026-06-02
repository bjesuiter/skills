---
name: jb-autoreview
description: Use when the user asks for autoreview, Codex/Claude second-model review, or final review of dirty changes, a branch, commit, or PR before ship.
---

# JB Autoreview

Generic structured closeout review for any git repo JB owns or works in.

This is a JB-generic fork of the OpenClaw/Steipete `autoreview` skill.

- Original URL: https://github.com/openclaw/agent-skills/blob/main/skills/autoreview/SKILL.md
- Upstream repository: https://github.com/openclaw/agent-skills
- Original author/source: Peter Steinberger / OpenClaw
- Fork intent: keep the portable review helper and review discipline, but remove OpenClaw-specific assumptions so the skill can run in any repo.

When asked to check for upstream updates, compare this skill and `scripts/autoreview` against the original URL/repository above.

## Use When

Use this skill when the user asks for:

- autoreview / auto review
- Codex review / Claude review / second-model review
- a final review before commit, merge, publish, or ship
- a review of local dirty changes, a branch, a commit, or a PR branch
- a structured review that should keep running until no accepted/actionable findings remain

This is a review workflow, not an approval gate. Treat output as advisory.

## Prerequisites

Required:

- `git`
- Python 3
- at least one review engine CLI, usually `codex`

Optional:

- `claude` for Claude reviews or review panels
- `gh` for PR base detection
- `droid` or `copilot` if intentionally using those engines

The helper resolves executables from absolute `PATH` entries outside the reviewed checkout, and rejects binaries inside the repo. This avoids accidentally running repo-provided fake tools.

## Helper Path

From this skill directory:

```bash
scripts/autoreview --help
```

If installed globally, resolve the script path from the skill directory before running it. Do not assume the current repo contains this skill.

## Pick Target

Let the helper auto-select when the user just says “autoreview”:

```bash
<autoreview-helper> --mode auto
```

Auto mode chooses:

- dirty worktree → local review
- non-main branch → branch review, using PR base via `gh pr view` when available, else `origin/main`
- clean `main` → fails with “no review target” because there is no diff to review

### Dirty Local Work

Use only for staged/unstaged/untracked work in the current checkout:

```bash
<autoreview-helper> --mode local
```

`--mode uncommitted` is accepted as an alias.

### Branch or PR Work

Use for committed branch work:

```bash
<autoreview-helper> --mode branch --base origin/main
```

If a PR exists, prefer its actual base:

```bash
base=$(gh pr view --json baseRefName --jq .baseRefName)
<autoreview-helper> --mode branch --base "origin/$base"
```

Optional review context is first-class:

```bash
<autoreview-helper> --mode branch --base origin/main --prompt-file /tmp/review-notes.md --dataset /tmp/evidence.json
```

### Single Commit

Use for an already committed change or landed commit:

```bash
<autoreview-helper> --mode commit --commit HEAD
```

For small stacks, review each commit explicitly or review the whole branch against its base.

## Engines

Codex is the default and usually the best closeout engine:

```bash
<autoreview-helper> --engine codex
```

Claude is available when requested:

```bash
<autoreview-helper> --engine claude
```

Do not silently switch engines or models. If the requested engine hits capacity, retry the same command a few times with the same engine/model.

## Parallel Tests

After formatting, it is OK to run focused tests and review in parallel:

```bash
<autoreview-helper> --parallel-tests "npm test -- --runInBand"
```

If tests or review cause code changes, rerun focused tests and rerun autoreview until the helper exits cleanly with no accepted/actionable findings.

## Review Panels

Multi-reviewer panels are opt-in only. Use them when explicitly requested or when risk justifies the extra spend:

```bash
<autoreview-helper> --panel
<autoreview-helper> --reviewers codex,claude
<autoreview-helper> --reviewers codex:gpt-5.1:high,claude:sonnet:max
```

## Guardrails

- Never blindly apply review output.
- Verify each finding by reading the actual code path and adjacent files.
- Read dependency docs/source/types when a finding depends on external behavior.
- Reject unrealistic edge cases, speculative risks, broad rewrites, and fixes that over-complicate the codebase.
- Prefer small fixes at the right ownership boundary.
- When an accepted finding reveals a repeated bug class, inspect the current review scope for sibling instances.
- Stop at touched surfaces, ownership boundaries, and clear follow-up territory.
- Do not push just to review. Push only when explicitly requested.
- Do not invoke nested reviewers from inside a review.
- Do not run an extra review just to get nicer wording after a clean helper result.
- Security findings should be concrete and actionable, not generic fear around shell/filesystem/network/auth code.

## Long-Running Reviews

Structured review can take up to 30 minutes.

Heartbeat lines like this are healthy progress:

```text
review still running: codex elapsed=120s pid=12345
```

Do not kill the helper just because it has been quiet for 2–5 minutes. Let it continue while heartbeats advance. Use `--stream-engine-output` only when live engine text is useful.

## Review Loop

1. Run the helper against the correct target.
2. Inspect accepted/actionable findings.
3. Verify each finding manually.
4. Reject non-issues with a brief explanation.
5. Fix accepted issues when in scope.
6. Rerun focused tests if fixes changed code.
7. Rerun the helper.
8. Stop when the helper exits 0 with no accepted/actionable findings.

## Final Report

Include:

- exact review command used
- tests/proof run
- findings accepted/rejected, briefly why
- the clean final helper result, or why a remaining finding was consciously rejected

If the final helper run exited 0 and produced no actionable findings, report that exact clean run as the closeout result.
