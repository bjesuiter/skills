---
name: jb-browser-testing
description: "Use for JB browser debugging and testing: prefer Vercel's agent-browser, but use jb-chrome-mcp when requested or as its fallback; avoid Playwriter and Playwright MCP."
skill_author: bjesuiter@gmail.com
---

# JB Browser Testing

## Rules

- **Primary**: Use Vercel's `agent-browser` skill / CLI for browser debugging and testing. Before issuing CLI commands, load its installed, version-matched workflow with `agent-browser skills get core`.
- **Chrome DevTools MCP**: Use the `jb-chrome-mcp` skill when the user explicitly requests Chrome MCP/DevTools MCP. Otherwise, use it as the fallback when agent-browser is unavailable or clearly unsuitable—especially for inspecting the user's existing Chrome tabs or DevTools-specific diagnostics. Follow that skill's bootstrap and real-profile reattachment rules.
- **Visible debugging**: Use `agent-browser --headed` when inspecting visual behavior, reproducing UI issues, or when the user needs to interact with the browser window.
- **Prepared sessions**: Isolate work with a stable named `--session`. For a session that must survive relaunches (including an authenticated login), add `--restore`; reuse the same session name for every command. Check authenticated restoration with an appropriate `--restore-check-*` option when practical.
- **Credentials and state**: Prefer the agent-browser auth vault for stored login credentials. For existing authenticated browser data, import a user-provided file with `cookies set --curl <file>` or load a state file. Never put passwords, cookies, tokens, or exported state contents in commands, chat, repository files, or commits; state files are secrets.
- **Avoid**: Do not use `playwriter`, `playwright-mcp`, or `playwright - opencode (built-in)` for JB browser debugging workflows.
