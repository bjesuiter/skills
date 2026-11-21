---
name: jb-mdn
description: Query MDN Web Docs through the official MDN MCP server using a persistent mcporter config, avoiding a direct MCP connection in the agent harness. Use when checking current web platform docs, CSS/HTML/JavaScript/Web API behavior, MDN browser compatibility data, Baseline support, or when the user asks whether a browser feature is supported.
metadata: {"clawdbot":{"emoji":"📚","requires":{"bins":["mcporter"]},"install":[{"id":"mcporter","kind":"node","package":"mcporter","bins":["mcporter"],"label":"Install mcporter"}]}}
---

# jb-mdn

Use the official MDN MCP server through a persistent `mcporter` server config for current web platform docs and browser compatibility, while avoiding a direct MCP connection in the agent harness.

Server URL: `https://mcp.mdn.mozilla.net/`
Configured name: `mdn`

## When to use

- Questions about CSS, HTML, JavaScript, DOM, Web APIs, browser features, or web standards.
- Browser compatibility, Baseline, or “can I use this?” checks.
- New or recently shipped platform features where model memory may be stale.
- Implementation work where exact MDN examples, syntax, or compatibility tables matter.

## Setup

Persist the official MDN MCP server in mcporter once per project or machine:

```fish
# Project-local config, preferred for repo-specific agent workflows
mcporter config add mdn https://mcp.mdn.mozilla.net/ --description "Official MDN Web Docs MCP server"

# Or global/home config when you want it everywhere
mcporter config add mdn https://mcp.mdn.mozilla.net/ --scope home --description "Official MDN Web Docs MCP server"
```

Verify:

```fish
mcporter config get mdn
mcporter list mdn --schema
```

## Quick commands

```fish
# Inspect available MDN MCP tools
mcporter list mdn --schema

# Search MDN
mcporter call mdn.search query="view transition"

# Fetch an MDN documentation page as markdown
mcporter call mdn.get-doc path="/en-US/docs/Web/CSS/Reference/At-rules/@view-transition"

# Fetch browser compatibility data by BCD key
mcporter call mdn.get-compat key="css.at-rules.view-transition"
```

Prefer `--output json` when parsing results programmatically:

```fish
mcporter call mdn.search query="popover attribute" --output json
```

## Workflow

1. **Search first** when you do not know the exact MDN path or BCD key.
2. **Fetch docs** with `get-doc` for syntax, examples, notes, and links.
3. **Fetch compatibility** with `get-compat` for support tables and Baseline claims.
4. **Cite what you used** in the final answer: MDN page path/URL and compatibility key when relevant.

## Tool names

The server currently exposes:

- `search` — search MDN documentation by query.
- `get-doc` — retrieve an MDN page as markdown. Takes a docs path or full URL.
- `get-compat` — retrieve MDN Browser Compatibility Data. Takes a BCD feature key like `api.fetch`, `javascript.builtins.Promise`, or `css.properties.display`.

## Guardrails

- Do not rely on memory for current browser support when MDN MCP can answer it.
- Treat the MDN MCP server as experimental; if a call fails, retry once, then fall back to `fetch_content` or web search and mention the fallback.
- Use the official remote HTTP server above, not an unofficial local MDN package, unless the user explicitly asks.
- Prefer a persistent `mcporter` config named `mdn`; do not wire MDN directly into Claude, Codex, Pi, Cursor, or other harness MCP configs unless the user explicitly asks.
