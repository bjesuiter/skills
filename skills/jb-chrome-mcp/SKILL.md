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
4. `take_snapshot` before interacting
5. Use current `uid` values only from the latest snapshot.
6. Use `click`, `fill`, `press_key`, `navigate_page`, or `evaluate_script`
7. Use diagnostics tools when needed:
   - `list_console_messages`
   - `list_network_requests`
   - `get_network_request`
   - `performance_start_trace`
   - `performance_stop_trace`
   - `lighthouse_audit`

## Good defaults

- Prefer `mcporter call ... --args '{...}' --output json` for machine-readable responses.
- Prefer `take_snapshot` over screenshots when text structure is enough.
- Call `list_pages` first if the active tab is unclear.
- Use `select_page` with `bringToFront: true` before interactive actions when tab focus matters.
- For first live calls, prefer a timeout so the agent does not hang forever on a Chrome permission prompt:

```bash
timeout 20s mcporter call jb-chrome-mcp.list_pages --args '{}' --output json
```

- Avoid noisy recovery loops. Repeated MCP/browser restarts can trigger reconnect/login prompts and alerts. Try one recovery path, then pause and ask or report the verification gap.

## Common commands

First run:

```bash
./scripts/ensure-jb-chrome-mcp.sh
```

Then use the saved server.

List tabs:

```bash
mcporter call jb-chrome-mcp.list_pages --args '{}' --output json
```

Select a tab:

```bash
mcporter call jb-chrome-mcp.select_page --args '{"pageId":1,"bringToFront":true}' --output json
```

Take a text snapshot:

```bash
mcporter call jb-chrome-mcp.take_snapshot --args '{}' --output json
```

Click an element from the latest snapshot:

```bash
mcporter call jb-chrome-mcp.click --args '{"uid":"1_10","includeSnapshot":true}' --output json
```

Fill/type into an element:

```bash
mcporter call jb-chrome-mcp.fill --args '{"uid":"1_13","value":"text","includeSnapshot":true}' --output json
```

Evaluate JavaScript:

```bash
mcporter call jb-chrome-mcp.evaluate_script --args '{"function":"() => document.title"}' --output json
```

Show console messages:

```bash
mcporter call jb-chrome-mcp.list_console_messages --args '{}' --output json
```

Show network requests:

```bash
mcporter call jb-chrome-mcp.list_network_requests --args '{}' --output json
```

Start a performance trace:

```bash
mcporter call jb-chrome-mcp.performance_start_trace --args '{"reload":true,"autoStop":true}' --output json
```

Take a screenshot:

```bash
mcporter call jb-chrome-mcp.take_screenshot --args '{"fullPage":true,"filePath":"tmp/chrome-mcp.png"}' --output json
```

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
mcporter call jb-chrome-mcp.list_pages --args '{}' --output json
```

Use coordinates from the current Peekaboo snapshot, not stale notes. Success means `list_pages` returns the user's real Chrome tabs.

Attach-alert rule: when the current snapshot clearly shows Chrome asking to allow DevTools/MCP/browser automation attachment, click the visible **Allow** button once, then rerun `list_pages`. If the button is not visible or the prompt is ambiguous, stop and ask; do not silently switch to Playwright/Puppeteer.

## Secret handling

Never print tokens/passwords from page DOM, network logs, or inputs. For token checks, return shape only: present/absent, length, status code, account/org name.

## Troubleshooting

- If Chrome is not listening on `9222`, reopen `chrome://inspect/#remote-debugging` and turn it on again.
- If `list_pages` hangs, check Chrome for an **Allow** prompt and use attach prompt recovery above.
- If `list_pages` fails with `DevToolsActivePort`, ask the user to restart Chrome or the DevTools bridge, then retry once:

```bash
mcporter daemon restart
mcporter call jb-chrome-mcp.list_pages --args '{}' --output json
```

- If `list_pages` returns a connection error, retry with the persisted config form instead of ad-hoc stdio.
- If `--browserUrl` fails on `http://127.0.0.1:9222/json/version`, switch back to `--autoConnect`.
- If the wrong tab is active, run `list_pages` and `select_page` again.
- If browser automation is unavailable, report that as a verification gap instead of substituting isolated browser tooling.
