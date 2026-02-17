# bjesuiter/skills

Reusable agent skills compatible with the [`skills` CLI](https://github.com/vercel-labs/skills).

## Install

```bash
# List available skills
npx skills add bjesuiter/skills --list

# Install one skill
npx skills add bjesuiter/skills --skill jb-tdd -a codex -y

# Install all skills to all agents
npx skills add bjesuiter/skills --all
```

## Repository Layout

```text
skills/
├── agents/
│   └── REPO_SETUP_INSTRUCTIONS.md
└── skills/
    └── jb-tdd/
        └── SKILL.md
```

## Included Skills

- `jb-tdd` — test-driven development workflow (red-green-refactor)

## Local Validation

```bash
# From repo root
npx skills add . --list
```
