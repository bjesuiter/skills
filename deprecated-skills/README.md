# Deprecated Skills

This directory preserves retired skills as historical reference only. It is intentionally outside `skills/`, so the `skills` CLI does not discover or install its contents when users run `npx skills add … --all`.

## `jb-pinchtab-testing`

Retired in favor of Vercel's [`agent-browser`](https://github.com/vercel-labs/agent-browser), which is now the primary browser-debugging tool through `jb-browser-testing`.

PinchTab required users and agents to select, start, and repeatedly target a profile-specific browser instance. That setup added unnecessary complexity for normal browser debugging. Agent-browser provides the workflow we need directly: headed debugging, named isolated sessions, persisted state with `--restore`, and authenticated-session support through its auth profiles, cookie import, and state files.

The legacy skill is retained at [`jb-pinchtab-testing/`](jb-pinchtab-testing/) for reference only. Do not install or use it for new work.
