---
name: jb-browser-testing
description: Private browser testing rules for jb workflows. Prefer PinchTab via the jb-pinchtab-testing skill for browser debugging/testing, use agent-browser only when PinchTab is unsuitable, and do not use playwriter or playwright-mcp.
skill_author: bjesuiter@gmail.com
private: true
---

# JB Browser Testing

Private skill for personal use. Do not publish.

## Rules

- **Primary**: Use the `jb-pinchtab-testing` skill / `pinchtab` CLI for browser debugging and testing whenever possible. It is more controllable and focused for JB workflows. Follow that skill's profile-selection rules before acting.
- **Fallback**: Use the `agent-browser` skill (by vercel) only when PinchTab is unavailable or clearly unsuitable for the task.
- **Avoid**: Do not use `playwriter`, `playwright-mcp`, or `playwright - opencode (built-in)` for JB browser debugging workflows.
