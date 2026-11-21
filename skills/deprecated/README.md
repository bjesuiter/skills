# Deprecated Skills

This page records retired skills, their replacements, and links to archived versions in Git.

## `full-send` and `full-stop`

Retired on 2026-11-21 after their workflows moved into the explicit PR modes of
the local-first skills. Use [`integrate pr`](../jb-in-progress/integrate/SKILL.md)
to finish and merge a PR, or [`prepare-merge pr`](../jb-in-progress/prepare-merge/SKILL.md)
to finish it and hand it back for review or merge.

Last available revision:
[`full-send`](https://github.com/bjesuiter/skills/tree/305f2f5d6bd72dfe10be1c9c3ce11f9eaddc4b93/skills/t3dotgg-tstack/full-send)
and [`full-stop`](https://github.com/bjesuiter/skills/tree/305f2f5d6bd72dfe10be1c9c3ce11f9eaddc4b93/skills/t3dotgg-tstack/full-stop).

## `jb-svg`

Archived on 2026-10-06 after JB preferred plain SVG generation in the pelican-bicycle comparison. Use plain SVG until a concrete roadblock warrants a small, focused custom skill. See the [decision](../../docs/adr/0001-use-plain-svg-until-a-roadblock.md) and the [last revision of the lab](https://github.com/bjesuiter/skills/blob/64e0029cd8d009857ca9579408b86e792c167305/research/jb-svg/README.md).

[Last archived version](https://github.com/bjesuiter/skills/tree/932c8f4040f058afa48878fc31fb15ab0c591bb2/deprecated-skills/jb-svg).

## `jb-pinchtab-testing`

Retired in favor of Vercel's [`agent-browser`](https://github.com/vercel-labs/agent-browser), which is now the primary browser-debugging tool through `jb-browser-testing`.

PinchTab required users and agents to select, start, and repeatedly target a profile-specific browser instance. That setup added unnecessary complexity for normal browser debugging. Agent-browser provides the workflow we need directly: headed debugging, named isolated sessions, persisted state with `--restore`, and authenticated-session support through its auth profiles, cookie import, and state files.

[Last archived version](https://github.com/bjesuiter/skills/tree/61255d7b33c60935201612240b8caf6629bb0ecc/deprecated-skills/jb-pinchtab-testing).

## `jb-adr`

Retired in favor of Matt Pocock's `domain-modeling` skill from [`mattpocock/skills`](https://github.com/mattpocock/skills). Decision confirmed on 2026-10-06.

`domain-modeling` covers our everyday ADR needs: sequentially numbered records in `docs/adr/`, context and rationale, and optional status, alternatives, and consequences. Its explicit criteria for when a decision merits an ADR reduce unnecessary documentation, while its domain-modeling workflow keeps terminology and decisions connected. A separate ADR skill adds redundant discovery context.

This is a practical replacement, not exact MADR compatibility: `jb-adr` prescribed structured MADR templates and an ADR index update; `domain-modeling` defaults to concise records. Projects requiring MADR should state their formatting and indexing conventions in their own `AGENTS.md`.

`jb-adr` is already absent from the active `skills/` directory and preference registry. Do not reinstall it for new work; use `domain-modeling` instead.

## `jb-tdd`

Retired in favor of Matt Pocock's [`tdd` skill](https://github.com/mattpocock/skills/tree/main/skills/engineering/tdd), which is the preferred test-driven development workflow.

[Last archived version](https://github.com/bjesuiter/skills/tree/61255d7b33c60935201612240b8caf6629bb0ecc/deprecated-skills/jb-tdd).
