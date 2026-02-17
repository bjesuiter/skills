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
    ├── agent-browser/
    ├── antigravity-quota/
    ├── apple-reminders/
    ├── beans/
    ├── bridle/
    ├── clawdcontrol/
    ├── desk-reminder/
    ├── github-pr/
    ├── housekeeping/
    ├── jb-tdd/
    ├── mcporter/
    ├── mole-mac-cleanup/
    ├── nb/
    ├── notebook/
    ├── open-loops/
    ├── openhue/
    ├── oracle/
    ├── refine/
    ├── security-check/
    ├── summarize/
    ├── sweetlink/
    ├── tmux/
    └── wacli/
```

## Included Skills (22)

### Development Tools
- `jb-tdd` — Test-driven development workflow (red-green-refactor)
- `beans` — Flat-file issue tracker stored in `.beans/` directory
- `github-pr` — Fetch, preview, merge, and test GitHub PRs locally
- `oracle` — Bundle a prompt + files for second-model review
- `security-check` — Red-team security review for code changes
- `refine` — Code refinement and review workflows

### Agent Management
- `bridle` — Unified configuration manager for AI coding assistants
- `clawdcontrol` — Control and manage Clawdbot via CLI
- `mcporter` — MCP server/tool management CLI
- `open-loops` — Find unfinished tasks and pending items

### Browser & Web
- `agent-browser` — Rust-based headless browser automation CLI
- `sweetlink` — Connect AI agent to real browser tab
- `summarize` — Summarize URLs, PDFs, images, audio, YouTube

### System & Productivity
- `tmux` — Remote-control tmux sessions
- `apple-reminders` — Create and manage Apple Reminders
- `desk-reminder` — Track reminders for when JB is at desk
- `mole-mac-cleanup` — Mac cleanup & optimization
- `housekeeping` — Self-cleaning and maintenance tasks

### Services & APIs
- `antigravity-quota` — Check Antigravity account quotas
- `openhue` — Control Philips Hue lights via OpenHue CLI
- `wacli` — Send WhatsApp messages and sync history

### Notes & Knowledge
- `nb` — Git-backed note management CLI
- `notebook` — Local-first personal knowledge base (YAML)

## Local Validation

```bash
# From repo root
npx skills add . --list

# Test install
npx skills add . --skill jb-tdd -a codex -y
```

## Source

These skills are maintained across JB's development environments. Some require specific CLIs to be installed.
