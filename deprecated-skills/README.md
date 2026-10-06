# Deprecated Skills

This directory preserves retired skills as historical reference only. It is intentionally outside `skills/`, so the `skills` CLI does not discover or install its contents when users run `npx skills add … --all`.

## `jb-pinchtab-testing`

Retired in favor of Vercel's [`agent-browser`](https://github.com/vercel-labs/agent-browser), which is now the primary browser-debugging tool through `jb-browser-testing`.

PinchTab required users and agents to select, start, and repeatedly target a profile-specific browser instance. That setup added unnecessary complexity for normal browser debugging. Agent-browser provides the workflow we need directly: headed debugging, named isolated sessions, persisted state with `--restore`, and authenticated-session support through its auth profiles, cookie import, and state files.

The legacy skill is retained at [`jb-pinchtab-testing/`](jb-pinchtab-testing/) for reference only. Do not install or use it for new work.

## `jb-adr`

Retired in favor of Matt Pocock's `domain-modeling` skill from [`mattpocock/skills`](https://github.com/mattpocock/skills). Decision confirmed on 2026-10-06.

`domain-modeling` covers our everyday ADR needs: sequentially numbered records in `docs/adr/`, context and rationale, and optional status, alternatives, and consequences. Its explicit criteria for when a decision merits an ADR reduce unnecessary documentation, while its domain-modeling workflow keeps terminology and decisions connected. A separate ADR skill adds redundant discovery context.

This is a practical replacement, not exact MADR compatibility: `jb-adr` prescribed structured MADR templates and an ADR index update; `domain-modeling` defaults to concise records. Projects requiring MADR should state their formatting and indexing conventions in their own `AGENTS.md`.

`jb-adr` is already absent from the active `skills/` directory and preference registry. Do not reinstall it for new work; use `domain-modeling` instead.

## `jb-tdd`

Retired in favor of Matt Pocock's [`tdd` skill](https://github.com/mattpocock/skills/tree/main/skills/engineering/tdd), which is the preferred test-driven development workflow.

The legacy skill is retained at [`jb-tdd/`](jb-tdd/) for reference only. Do not install or use it for new work.
