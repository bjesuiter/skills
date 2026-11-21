# bjesuiter/skills

JB's curated coding skills, compatible with the [`skills` CLI](https://github.com/vercel-labs/skills).

These skills represent workflows, tools, and patterns JB actively uses in development. They're designed to be agent-agnostic and work with any AI coding assistant that supports the skills format.

## Install

```bash
# List available skills
npx skills add bjesuiter/skills --list

# Install one skill
npx skills add bjesuiter/skills --skill jb-beans -a codex -y

# Install all discoverable skills to all agents
npx skills add bjesuiter/skills --all
```

Use an explicit skill name when you want a specific skill. Installing all discoverable skills can include drafts. For a reproducible installation, [install from a Git tag](.changeset/README.md#install-a-fixed-snapshot).

## Included Skills (37)

### Core Development Workflows
- `jb-stack-prefs` — JB's preferred stacks by use case, repository comparisons, and preference updates
- `jb-buying-judge` — One-at-a-time randomized anti-impulse-buying checks that distinguish a real need from a deliberate want
- `jb-decision-judge` — Proportionate adversarial decision review: steelman options, pressure-test a leaning, or check a chosen direction
- `jb-beansloop` — Automated workflow using beans issue tracker
- `jb-committer` — Git commit grouping and commit message drafting
- `jb-git-sync` — Request-only sync of configured Git repos, starting with `~/jb-home`
- `jb-local-release` — Local release workflow; prepares version/changelog/checks/commit/tag and defers to repo-specific instructions
- `jb-gh-release-with-attempts` — GitHub Actions release workflow using disposable release-attempt tags before canonical version tags
- `jb-beans` — Flat-file issue tracker stored in `.beans/` directory
- `linuxserver-image-scaffold` — Scaffold LinuxServer.io-style Docker image repos (Alpine/Ubuntu/both)

### Code Review & Quality
- `jb-autoreview` — Structured second-model autoreview via Codex/Claude for local, branch, commit, and PR diffs
- `jb-clawpatch-review` — Clawpatch semantic repo review, persistent findings reports, explicit fixes, and revalidation
- `jb-test-audit` — Test-value gate and evidence-driven audit workflow for low-value, duplicative, or implementation-coupled tests

### Browser & Web Testing
- `jb-browser-testing` — Browser testing workflows and patterns
- `jb-chrome-mcp` — Chrome DevTools MCP via `mcporter` for existing Chrome tabs

### Documentation & Research
- `jb-docs-scraper` — Scrape documentation websites into markdown
- `jb-markit` — Convert files, URLs, and media into markdown with `markit`
- `summarize` — Summarize URLs, PDFs, images, audio, and YouTube
- `jb-mdn` — Query MDN Web Docs and browser compatibility through the official MDN MCP server using persistent `mcporter` config
- `jb-obsidian-sync` — Clone and synchronize Obsidian Sync vaults for direct Markdown access without Obsidian Desktop

### Development Tools
- `jb-dev-env` — Secure dev environments with Varlock profiles and SOPS secrets decrypted through Bitwarden's SSH agent
- `mcporter` — MCP server/tool management CLI
- `jb-bgproc` — Consolidated background-process workflow, validated against `bgproc` 0.3.0; replaces the separate official `bgproc` skill
- `jb-tuna-script` — Create executable scripts for the Tuna macOS launcher
- `jb-worktree` — Git worktree management via `wtp`
- [`finish-t3`](skills/in-progress/finish-t3/SKILL.md) (draft) — Check OpenLoops and unsaved work, then finish a T3 worktree and archive; optional deep-check covers unique ignored data

### Platform-Specific
- `xcode` — Build, test, and manage Xcode projects and Swift packages
- `mole-mac-cleanup` — Mac cleanup & optimization

### Utilities
- `nb` — Git-backed note management CLI
- `jb-agent-env` — Shared preferred agent-environment registry for Markdown skills, Pi extensions, and CLIs via GitHub Gist

### tstack

- [`babysit-pr`](skills/t3dotgg-tstack/babysit-pr/SKILL.md) — Monitor pull requests through review and CI
- [`file-pr`](skills/t3dotgg-tstack/file-pr/SKILL.md) — Open a concise pull request
- [`leaving-pr-comments`](skills/t3dotgg-tstack/leaving-pr-comments/SKILL.md) — Write GitHub pull request comments
- [`modernize`](skills/t3dotgg-tstack/modernize/SKILL.md) — Identify and address outdated code and practices
- [`sol-loop`](skills/t3dotgg-tstack/sol-loop/SKILL.md) — Iterate on implementation with independent review
- [`takeover`](skills/t3dotgg-tstack/takeover/SKILL.md) — Take over a pull request, branch, or agent thread

### HumanLayer

- [`show-me`](skills/humanlayer-skills/show-me/SKILL.md) — Explain the current topic visually with diagrams, code sketches, and focused HTML artifacts

## In progress

- [`integrate`](skills/in-progress/integrate/SKILL.md) — Merge locally and push the target branch. Use `integrate pr` to merge through GitHub. Install `prepare-merge` alongside it. Awaiting testing. Discoverable through the Skills CLI.
- [`prepare-merge`](skills/in-progress/prepare-merge/SKILL.md) — Prepare a branch locally. Use `prepare-merge pr` to prepare a GitHub PR and leave it open. Awaiting testing. Discoverable through the Skills CLI.

## Retired skills

See the [retirement history](skills/deprecated/README.md) for replacements and archived versions.

## About

These skills are extracted from JB's personal development environment (`jb-home/src/jb-skills`) and made publicly available for the AI coding community. They represent real workflows used in production projects.

Some skills require specific CLIs to be installed (noted in each SKILL.md).
