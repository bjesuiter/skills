---
name: jb-chrome-mcp
description: Use mcporter to connect to Chrome DevTools MCP against a local Chrome with chrome://inspect/#remote-debugging enabled on 127.0.0.1:9222. Use when asked to use Chrome MCP/DevTools MCP via mcporter, inspect or automate existing Chrome tabs, or query console, network, screenshots, and performance through Chrome MCP.
homepage: https://github.com/ChromeDevTools/chrome-devtools-mcp
metadata: {"clawdbot":{"requires":{"bins":["mcporter"]},"install":[{"id":"node","kind":"node","package":"mcporter","bins":["mcporter"],"label":"Install mcporter (node)"}]}}
skill_author: bjesuiter@gmail.com
private: true
---

# JB Chrome MCP

Private skill for using Chrome DevTools MCP through `mcporter`.

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

Before the first `mcporter call`, run the bundled script:

```bash
./scripts/ensure-jb-chrome-mcp.sh
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

Note: the first live `mcporter call` may trigger a Chrome permission prompt for the DevTools MCP connection. Click **Allow** before expecting `list_pages` or other live calls to return.

## Preferred workflow

1. `list_pages`
2. `select_page`
3. `take_snapshot` before interacting
4. Use `click`, `fill`, `press_key`, `navigate_page`, or `evaluate_script`
5. Use diagnostics tools when needed:
   - `list_console_messages`
   - `list_network_requests`
   - `get_network_request`
   - `performance_start_trace`
   - `performance_stop_trace`
   - `lighthouse_audit`

## Good defaults

- Prefer `mcporter call ... --output json` for machine-readable responses.
- Prefer `take_snapshot` over screenshots when text structure is enough.
- Call `list_pages` first if the active tab is unclear.
- Use `select_page bringToFront=true` before interactive actions when tab focus matters.

## Common commands

First run:

```bash
./scripts/ensure-jb-chrome-mcp.sh
```

Then use the saved server.

List tabs:

```bash
mcporter call jb-chrome-mcp.list_pages --output json
```

Select a tab:

```bash
mcporter call jb-chrome-mcp.select_page pageId=1 bringToFront=true --output json
```

Take a text snapshot:

```bash
mcporter call jb-chrome-mcp.take_snapshot --output json
```

Click an element from the latest snapshot:

```bash
mcporter call jb-chrome-mcp.click uid=1_10 includeSnapshot=true --output json
```

Evaluate JavaScript:

```bash
mcporter call 'jb-chrome-mcp.evaluate_script(function: "() => document.title")' --output json
```

Show console messages:

```bash
mcporter call jb-chrome-mcp.list_console_messages --output json
```

Show network requests:

```bash
mcporter call jb-chrome-mcp.list_network_requests --output json
```

Start a performance trace:

```bash
mcporter call jb-chrome-mcp.performance_start_trace reload=true autoStop=true --output json
```

Take a screenshot:

```bash
mcporter call jb-chrome-mcp.take_screenshot fullPage=true filePath=tmp/chrome-mcp.png --output json
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

## Troubleshooting

- If Chrome is not listening on `9222`, reopen `chrome://inspect/#remote-debugging` and turn it on again.
- If `list_pages` returns a connection error, retry with the persisted config form instead of ad-hoc stdio.
- If `--browserUrl` fails on `http://127.0.0.1:9222/json/version`, switch back to `--autoConnect`.
- If the wrong tab is active, run `list_pages` and `select_page` again.
