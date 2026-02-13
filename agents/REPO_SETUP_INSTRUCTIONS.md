# Repository Setup Instructions (Skills CLI)

This repo is structured to work cleanly with `npx skills`.

## 1) Required Structure

Use one of these patterns:

### Single-skill repo

```text
<repo>/
└── SKILL.md
```

### Multi-skill repo (used here)

```text
<repo>/
└── skills/
    ├── <skill-name>/
    │   └── SKILL.md
    └── <another-skill>/
        └── SKILL.md
```

> This repository uses the multi-skill layout under `skills/`.

## 2) SKILL.md Requirements

Every skill file must include YAML frontmatter:

```md
---
name: my-skill
description: What this skill does and when to use it
---
```

Required fields:
- `name` (stable, unique, lowercase-hyphen format recommended)
- `description`

## 3) Authoring Guidelines for Reliability

- Keep instructions agent-agnostic and markdown-only.
- Keep each skill focused on one capability.
- Prefer deterministic, stepwise instructions.
- Add explicit guardrails for risky operations.

## 4) Local Validation Checklist

From repository root:

```bash
# verify discovery
npx skills add . --list

# install a specific skill to an agent
npx skills add . --skill tdd -a codex -y

# optional: test global install
npx skills add . --skill tdd -g -a pi -y
```

## 5) Remote Validation (GitHub)

```bash
npx skills add bjesuiter/skills --list
npx skills add bjesuiter/skills --skill tdd -a codex -y
```

## 6) Optional: Internal/WIP Skills

Hide work-in-progress skills from normal discovery:

```yaml
metadata:
  internal: true
```

Install/list internal skills only when needed:

```bash
INSTALL_INTERNAL_SKILLS=1 npx skills add bjesuiter/skills --list
```

## 7) Maintenance

- Avoid renaming existing skill `name` values unless necessary.
- Keep backward-compatible behavior where possible.
- Run `npx skills add . --list` before each release/push.
