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
│   ├── AGENTS.md
│   └── REPO_SETUP_INSTRUCTIONS.md
└── skills/
    ├── agent-browser/
    ├── beans/
    ├── github-pr/
    ├── jb-tdd/
    ├── mcporter/
    ├── mole-mac-cleanup/
    ├── nb/
    ├── oracle/
    ├── refine/
    ├── security-check/
    ├── summarize/
    ├── sweetlink/
    └── tmux/
```

## Included Skills (13)

### Development Tools
- `jb-tdd` — Test-driven development workflow (red-green-refactor)
- `beans` — Flat-file issue tracker stored in `.beans/` directory
- `github-pr` — Fetch, preview, merge, and test GitHub PRs locally
- `oracle` — Bundle a prompt + files for second-model review
- `security-check` — Red-team security review for code changes
- `refine` — Code refinement and review workflows

### Browser & Web
- `agent-browser` — Rust-based headless browser automation CLI
- `sweetlink` — Connect AI agent to real browser tab
- `summarize` — Summarize URLs, PDFs, images, audio, YouTube

### System & Productivity
- `tmux` — Remote-control tmux sessions
- `mole-mac-cleanup` — Mac cleanup & optimization

### Agent Tools
- `mcporter` — MCP server/tool management CLI

### Notes & Knowledge
- `nb` — Git-backed note management CLI

## Local Validation

```bash
# From repo root
npx skills add . --list

# Test install
npx skills add . --skill jb-tdd -a codex -y
```

## Source

These skills are curated from JB's development workflows. Some require specific CLIs to be installed.
