---
name: jb-stack-prefs
description: Apply JB's stack preferences when choosing technologies, comparing repositories, designing JavaScript library APIs, or recording updated preferences.
---

# JB stack preferences

Use JB's preferences to guide technology choices for the relevant use case. Read [web preferences](references/web.md) for SPAs, offline PWAs, Cloudflare websites and services, authentication, ORMs, and query builders.

Read [repository tooling preferences](references/repository-tooling.md) for linting, formatting, bundling, Vite, and test-runner selection.

Read [TypeScript CLI preferences](references/cli.md) for CLI frameworks, prompts, git hooks, and release tooling, including options under evaluation.

Read [Effect evaluation](references/effect.md) when considering Effect or proposing its adoption.

Read [JavaScript library API design](references/js-api-design.md) when designing or reviewing a public library API, including its types, lifecycle, and package exports.

## Apply preferences

- For new work, select the preferred stack for the use case, accounting for the project's constraints and JB's explicit instructions.
- For existing repositories, inspect dependencies and documented decisions before comparing them with these preferences. Explain differences and their implications; preserve established choices unless the task includes a stack change.
- Separate JB's current defaults from upstream maturity and maintenance. Check current official sources when release status, compatibility, or maintenance affects a recommendation. The recorded version choices describe JB's preference at the confirmation date.
- Call a choice legacy in JB's projects only when JB or a repository decision identifies it as superseded. A different stack alone is insufficient evidence. Record replacements with their use case when confirmed.
- Keep evaluating options and deliberate alternatives distinct from defaults.

## Maintain preferences

When a discussion produces a new recommendation, record its use case, rationale, relevant constraints, date, and source in the appropriate reference. Mark an agent recommendation as a candidate until JB endorses or adopts it; JB's explicit choices are confirmed preferences.

Update an existing entry when its preference changes. Preserve a superseded choice only when it helps explain existing repositories, and name its replacement and scope. Keep each preference in one reference and add a link here when introducing another use-case group.
