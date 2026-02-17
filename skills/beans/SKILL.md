---
name: beans
description: Use the beans CLI to track issues/tasks alongside your code. Flat-file issue tracker that stores beans as markdown files in .beans/ directory. Integrates with Codex, OpenCode, and Claude Code via beans-prime.
homepage: https://github.com/hmans/beans
metadata: {"clawdbot":{"emoji":"🫘","requires":{"bins":["beans"]},"install":[{"id":"brew","kind":"brew","package":"hmans/beans/beans","label":"Install beans (brew)"}]}}
---

# beans - Flat-File Issue Tracker

A lightweight, flat-file issue tracker for humans and AI coding agents. Stores issues as markdown files in `.beans/` directory alongside your code.

## Why beans?

- **Simple** — No database, no server, just markdown files
- **AI-friendly** — Designed for AI coding agents
- **Git-friendly** — Lives alongside your code in `.beans/`
- **Portable** — Works with any editor/IDE

## Installation

```bash
# Via Homebrew
brew install hmans/beans/beans

# Via Go
go install github.com/hmans/beans@latest
```

## Setup

```bash
# Initialize beans in a project
beans init

# Verify setup
beans status
```

## Core Commands

### Create Beans
```bash
beans create "Implement user login"
# Creates new bean with auto-generated ID

beans create "Fix auth bug" --tag bug --tag urgent
# Creates bean with tags

beans create "Refactor API" --priority high
# Creates bean with priority
```

### List Beans
```bash
beans list                    # List all beans
beans list --open             # List only open beans
beans list --closed           # List closed beans
beans list --tag urgent       # Filter by tag
beans list --assignee me      # Filter by assignee
```

### Update Beans
```bash
beans open <id>               # Mark bean as open
beans close <id>              # Mark bean as closed
beans edit <id> --title "New title"
beans tag <id> --add bug --remove urgent
beans assign <id> --to me
```

### Show Bean Details
```bash
beans show <id>               # Show full bean details
beans show <id> --comments    # Include comments
```

### Comments
```bash
beans comment <id> "Added tests for this"
beans comment <id> --file commit-message.txt
```

### Search
```bash
beans search "login"          # Search in all beans
beans search --tag bug        # Search with filters
```

## beans prime

The `beans prime` command outputs project context for AI agents:

```bash
beans prime
# Outputs current beans, tags, and status for AI context
```

### Integration with OpenCode

Copy this plugin to your OpenCode config:

```typescript
// ~/.opencode/plugin/beans-prime.ts
import type { Plugin } from "@opencode-ai/plugin";

export const BeansPrimePlugin: Plugin = async ({ $, directory }) => {
  let prime = undefined;

  try {
    const hasBeans = await $`which beans`.quiet();
    const hasConfig = await $`test -f ${directory}/.beans.yml`.quiet();

    if (hasBeans.exitCode === 0 && hasConfig.exitCode === 0) {
      const result = await $`beans prime`.cwd(directory).quiet();
      prime = result.stdout.toString();
    }
  } catch (e) {
    // Silently skip if beans not available
  }

  return {
    "experimental.chat.system.transform": async (_, output) => {
      if (prime) output.system.push(prime);
    },
    "experimental.session.compacting": async (_, output) => {
      if (prime) output.context.push(prime);
    },
  };
};

export default BeansPrimePlugin;
```

### Integration with Codex

Set environment or add to AGENTS.md:

```bash
# In your repo's AGENTS.md:
IMPORTANT: before you do anything else, run `beans prime` and heed its output.
```

### Integration with Claude Code

Add to Claude Code's system prompt or context:

```bash
# Run before coding session
beans prime >> ~/.claude/context/beans.txt
```

## Workflow Example

```bash
# 1. Start work on a feature
beans create "Add dark mode support" --tag feature

# 2. Work on it, update progress
beans comment <bean-id> "Started working on color scheme"

# 3. Complete the feature
beans close <bean-id>
beans comment <bean-id> "Dark mode implemented for all views"
```

## Bean File Format

Beans are stored in `.beans/` as markdown:

```markdown
---
id: 12345678
title: "Implement user login"
status: open
tags: [feature, auth]
priority: high
assignee: developer
created: 2024-01-15T10:00:00Z
updated: 2024-01-15T14:30:00Z
---

## Description

Implement user login with email and password.

## Notes

- Use existing auth infrastructure
- Follow security best practices
```

## Configuration

Create `.beans.yml` in your project root:

```yaml
# .beans.yml
directory: .beans
format: markdown
templates:
  default: |
    ---
    id: {{.ID}}
    title: "{{.Title}}"
    status: open
    created: {{.Created}}
    ---

    {{.Description}}
```

## Tips

1. **Commit `.beans.yml`** — Share config with team
2. **Ignore `.beans/*.md`** — Keep beans local or commit based on preference
3. **Use tags consistently** — Create tag taxonomy early
4. **Run `beans prime`** — Before starting AI-assisted work

## Related Skills

- **nb** — Notebook management for ideas and references
- **github-pr** — PR workflow integration
- **prd** — Product Requirements Documents

## Links

- GitHub: https://github.com/hmans/beans
- Documentation: https://github.com/hmans/beans#readme
