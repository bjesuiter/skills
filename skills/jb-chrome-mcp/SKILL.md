---
name: jb-chrome-mcp
description: Use when the user asks for Chrome MCP/DevTools MCP via mcporter, existing Chrome tabs, console/network inspection, screenshots, or performance traces.
homepage: https://github.com/ChromeDevTools/chrome-devtools-mcp
metadata: {"clawdbot":{"requires":{"bins":["mcporter"]},"install":[{"id":"node","kind":"node","package":"mcporter","bins":["mcporter"],"label":"Install mcporter (node)"}]}}
skill_author: bjesuiter@gmail.com
private: true
---

# JB Chrome MCP

Private skill for using Chrome DevTools MCP through `mcporter` against the user's existing Chrome session.

This skill defines JB-specific rules, bootstrap, safety, and recovery workflow only. For the full upstream tool catalog and exact arguments, read `references/chrome-devtools-mcp-tool-reference.md` instead of duplicating it here.

Hard rule: reattach to the existing Chrome profile only. Do not silently switch to isolated Chrome, Playwright, Puppeteer, the Codex in-app browser, AppleScript, `osascript`, GUI scripting, or macOS `open` for browser control unless the user explicitly asks for an isolated/new browser.

Screenshot/live UI bugs require this existing-Chrome path. `curl`, source inspection, Worker smoke tests, or local Playwright are supporting proof only; do not treat them as equivalent when the user showed a rendered browser problem or the page may depend on login/profile state.

## Prerequisites

Before using this skill:

1. Open `chrome://inspect/#remote-debugging` in Chrome.
2. Turn remote debugging on and allow incoming debugging connections in Chrome's dialog.
3. Confirm Chrome is listening on `127.0.0.1:9222`.
   - Expected listener: `Server running at: 127.0.0.1:9222`
   - Useful check: `lsof -nP -iTCP:9222 -sTCP:LISTEN`
4. Make sure `mcporter` is installed.

## Bootstrap rule

Do not ask the user to configure `mcporter` manually unless the bootstrap script fails.

Before the first `mcporter call`, run the bundled script. From this skills repo:

```bash
skills/jb-chrome-mcp/scripts/ensure-jb-chrome-mcp.sh
```

From an installed skill path:

```bash
/Users/bjesuiter/.agents/skills/jb-chrome-mcp/scripts/ensure-jb-chrome-mcp.sh
```

The script:

- verifies Chrome is listening on `127.0.0.1:9222`
- installs or updates a saved home-level `mcporter` server named `jb-chrome-mcp`
- configures `chrome-devtools-mcp` with `--autoConnect`

`--autoConnect` was more reliable for the `chrome://inspect/#remote-debugging` workflow than forcing `--browserUrl http://127.0.0.1:9222`.

After bootstrapping, verify the tool list if needed:

```bash
mcporter list jb-chrome-mcp --schema
```

This creates a saved home-level `mcporter` server named `jb-chrome-mcp`. That is what lets later calls use short names like `mcporter call jb-chrome-mcp.list_pages` instead of repeating the full `npx chrome-devtools-mcp ...` stdio config every time.

Note: the first live `mcporter call` may trigger a Chrome permission prompt for the DevTools MCP connection. If a live call hangs, check Chrome for an **Allow** prompt before changing config or restarting processes.

## Preferred workflow

1. `list_pages`
2. Confirm the list shows the user's real open tabs. If it shows a blank/default isolated Chrome, stop and say reattach failed.
3. `select_page`
4. `take_snapshot` before interacting. Use current `uid` values only from the latest snapshot.
5. Pick the tool from `references/chrome-devtools-mcp-tool-reference.md`:
   - Prefer `fill_form` for multi-field forms.
   - Use `handle_dialog` for page-level `alert`/`confirm`/`prompt`; use attach prompt recovery below only for native Chrome permission prompts.
   - For performance, use trace tools for performance metrics; Lighthouse excludes performance.
   - Do not use experimental-only tools (`click_at`, screencast) unless the server was configured with their required flags.

## Good defaults

- Prefer `mcporter call ... --args '{...}' --output json` for machine-readable responses.
- Prefer `take_snapshot` over screenshots when text structure is enough.
- Call `list_pages` first if the active tab is unclear.
- Use `select_page` with `bringToFront: true` before interactive actions when tab focus matters.
- For first live calls, use mcporter's built-in timeout so the agent gets a structured failure instead of hanging forever on a Chrome permission prompt:

```bash
mcporter call jb-chrome-mcp.list_pages --args '{}' --output json --timeout 20000
```

Do not wrap `mcporter` in shell `timeout` for normal use; it can kill the client without a useful MCP error.

- Avoid noisy recovery loops. Repeated MCP/browser restarts can trigger reconnect/login prompts and alerts. Try one recovery path, then pause and ask or report the verification gap.

## Command pattern

First run the bootstrap script, then use the saved server:

```bash
./scripts/ensure-jb-chrome-mcp.sh
mcporter call jb-chrome-mcp.<tool_name> --args '<json-args>' --output json --timeout 20000
```

Use `references/chrome-devtools-mcp-tool-reference.md` for tool names, parameters, examples, and flag requirements.

## Fallback for explicit browser URL mode

If `--autoConnect` is unavailable or you are connecting to an older/manual Chrome instance that exposes `/json/version`, use:

```bash
mcporter config add jb-chrome-mcp \
  --stdio npx \
  --arg -y \
  --arg chrome-devtools-mcp@latest \
  --arg --browserUrl \
  --arg http://127.0.0.1:9222 \
  --arg --no-usage-statistics \
  --scope home
```

## Attach prompt recovery

If `list_pages` hangs while Chrome shows an auth/attach/update prompt, handle the attach alert before falling back. Prefer Peekaboo to press an explicit Chrome **Allow** button when visible; otherwise wait for the human. Do not restart daemons or kill MCP processes just because the first output is slow.

```bash
PB="${PEEKABOO_BIN:-$HOME/bin/peekaboo}"
[ -x "$PB" ] || PB="$(command -v peekaboo)"
"$PB" permissions status --json
"$PB" see --app frontmost --path /tmp/chrome-attach.png --json --annotate
# If the UI shows Chrome "Allow remote debugging?", click only the visible Allow button.
"$PB" click --coords <allow_x>,<allow_y> --json
mcporter call jb-chrome-mcp.list_pages --args '{}' --output json --timeout 20000
```

Use coordinates from the current Peekaboo snapshot, not stale notes. Success means `list_pages` returns the user's real Chrome tabs.

Attach-alert rule: when the current snapshot clearly shows Chrome asking to allow DevTools/MCP/browser automation attachment, click the visible **Allow** button once, then rerun `list_pages`. If the button is not visible or the prompt is ambiguous, stop and ask; do not silently switch to Playwright/Puppeteer.

## Secret handling

Never print tokens/passwords from page DOM, network logs, or inputs. For token checks, return shape only: present/absent, length, status code, account/org name.

`get_network_request` can return request/response bodies inline. Prefer file output args from the reference for large or potentially sensitive bodies, then summarize only safe shape/status details.

Avoid debug logging by default. Do not enable `DEBUG=*`, `--logFile`, or verbose protocol logging unless explicitly debugging MCP internals and prepared to redact the output. Chrome DevTools MCP debug logs can include live URLs, request headers, cookies, auth tokens, post bodies, and other sensitive browser-session data from open tabs.

## Troubleshooting

- If Chrome is not listening on `9222`, reopen `chrome://inspect/#remote-debugging` and turn it on again.
- If `list_pages` hangs, check Chrome for an **Allow** prompt and use attach prompt recovery above.
- If `list_pages` fails with `DevToolsActivePort`, ask the user to restart Chrome or the DevTools bridge, then retry once:

```bash
mcporter daemon restart
mcporter call jb-chrome-mcp.list_pages --args '{}' --output json --timeout 20000
```

- If `list_pages` returns a connection error, retry with the persisted config form instead of ad-hoc stdio.
- If `--browserUrl` fails on `http://127.0.0.1:9222/json/version`, switch back to `--autoConnect`.
- If the wrong tab is active, run `list_pages` and `select_page` again.
- If browser automation is unavailable, report that as a verification gap instead of substituting isolated browser tooling.
