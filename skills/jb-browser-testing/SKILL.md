---
name: jb-browser-testing
description: Private browser testing rules for jb workflows. Prefer PinchTab via the jb-pinchtab-testing skill for browser debugging/testing, fall back to agent-browser, and avoid playwright-mcp.
skill_author: bjesuiter@gmail.com
private: true
---

# JB Browser Testing

Private skill for personal use. Do not publish.

## Rules

- **Primary**: Use the `jb-pinchtab-testing` skill / `pinchtab` CLI when possible. It controls PinchTab-managed browser profiles, so follow that skill's profile-selection rules before acting.
- **Fallback**: Use the `agent-browser` skill (by vercel) when PinchTab is unavailable or unsuitable.
- **Human-in-the-loop debugging fallback**: Use `playwriter` only when the user explicitly requests browser debugging with human involvement.
- **Avoid**: Do not use `playwright-mcp` OR `playwright - opencode (built-in)` because it is token heavy.
