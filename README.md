# bjesuiter/skills

JB's curated coding skills, compatible with the [`skills` CLI](https://github.com/vercel-labs/skills).

These skills represent workflows, tools, and patterns JB actively uses in development. They're designed to be agent-agnostic and work with any AI coding assistant that supports the skills format.

## Install

```bash
# List available skills
npx skills add bjesuiter/skills --list

# Install one skill
npx skills add bjesuiter/skills --skill jb-tdd -a codex -y

# Install all skills to all agents
npx skills add bjesuiter/skills --all
```

## Included Skills (21)

### Core Development Workflows
- `jb-tdd` — Test-driven development workflow (red-green-refactor)
- `jb-refine-code` — Refactor pass focused on simplicity after changes
- `jb-beansloop` — Automated workflow using beans issue tracker
- `committer` — Git commit message generation and conventions
- `beans` — Flat-file issue tracker stored in `.beans/` directory

### Code Review & Quality
- `security-check` — Red-team security review for code changes
- `oracle` — Bundle a prompt + files for second-model review
- `refine` — Code refinement and review workflows

### Browser & Web Testing
- `agent-browser` — Rust-based headless browser automation CLI
- `sweetlink` — Connect AI agent to real browser tab
- `jb-browser-testing` — Browser testing workflows and patterns

### Documentation & Research
- `jb-docs-scraper` — Scrape documentation websites into markdown
- `summarize` — Summarize URLs, PDFs, images, audio, YouTube

### Development Tools
- `github-pr` — Fetch, preview, merge, and test GitHub PRs locally
- `mcporter` — MCP server/tool management CLI
- `tmux` — Remote-control tmux sessions
- `bgproc` — Background process management

### Platform-Specific
- `xcode` — Build, test, and manage Xcode projects and Swift packages
- `mole-mac-cleanup` — Mac cleanup & optimization

### Utilities
- `nb` — Git-backed note management CLI
- `exe-dev` — exe.dev tooling and workflows

## Local Validation

```bash
# From repo root
npx skills add . --list

# Test install
npx skills add . --skill jb-tdd -a codex -y
```

## About

These skills are extracted from JB's personal development environment (`jb-home/src/jb-skills`) and made publicly available for the AI coding community. They represent real workflows used in production projects.

Some skills require specific CLIs to be installed (noted in each SKILL.md).
