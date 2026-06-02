---
name: jb-browser-testing
description: "Use for JB browser-testing decisions: prefer PinchTab, choose agent-browser only when needed, and avoid playwriter/playwright-mcp."
skill_author: bjesuiter@gmail.com
---

# JB Browser Testing

## Rules

- **Primary**: Use the `jb-pinchtab-testing` skill / `pinchtab` CLI for browser debugging and testing whenever possible. It is more controllable and focused for JB workflows. Follow that skill's profile-selection rules before acting.
- **Fallback**: Use the `agent-browser` skill (by vercel) only when PinchTab is unavailable or clearly unsuitable for the task.
- **Avoid**: Do not use `playwriter`, `playwright-mcp`, or `playwright - opencode (built-in)` for JB browser debugging workflows.
