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

## Included Skills (26)

### Core Development Workflows
- `jb-tdd` — Test-driven development workflow (red-green-refactor)
- `jb-refine-code` — Refactor pass focused on simplicity after changes
- `jb-beansloop` — Automated workflow using beans issue tracker
- `jb-committer` — Git commit grouping and commit message drafting
- `jb-release` — Generic release workflow; defers to repo-specific release instructions
- `jb-beans` — Flat-file issue tracker stored in `.beans/` directory

### Code Review & Quality
- `jb-autoreview` — Structured second-model autoreview via Codex/Claude for local, branch, commit, and PR diffs
- `jb-clawpatch-review` — Clawpatch semantic repo review, persistent findings reports, explicit fixes, and revalidation
- `security-check` — Red-team security review for code changes

### Browser & Web Testing
- `sweetlink` — Connect AI agent to a real browser tab
- `jb-browser-testing` — Browser testing workflows and patterns
- `jb-chrome-mcp` — Chrome DevTools MCP via `mcporter` for existing Chrome tabs
- `jb-pinchtab-testing` — Higher-level browser testing workflow for PinchTab-managed browsers via the PinchTab CLI

### Documentation & Research
- `jb-adr` — Create and manage Markdown Architectural Decision Records (MADR)
- `jb-docs-scraper` — Scrape documentation websites into markdown
- `jb-markit` — Convert files, URLs, and media into markdown with `markit`
- `summarize` — Summarize URLs, PDFs, images, audio, and YouTube
- `jb-mdn` — Query MDN Web Docs and browser compatibility through the official MDN MCP server using persistent `mcporter` config

### Development Tools
- `mcporter` — MCP server/tool management CLI
- `jb-bgproc` — Background process management via `bgproc`
- `jb-tuna-script` — Create executable scripts for the Tuna macOS launcher
- `jb-worktree` — Git worktree management via `wtp`

### Platform-Specific
- `xcode` — Build, test, and manage Xcode projects and Swift packages
- `mole-mac-cleanup` — Mac cleanup & optimization

### Utilities
- `nb` — Git-backed note management CLI
- `jb-skill-prefs` — Shared preferred skill registry and project skill installer via GitHub Gist

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
