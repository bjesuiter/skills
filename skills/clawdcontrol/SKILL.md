---
name: clawdcontrol
description: Control and manage Clawdbot via its CLI. Run gateway commands, manage agents, send messages, and more.
metadata:
  clawdbot:
    emoji: "🦞"
    os: ["darwin", "linux"]
    requires:
      bins: ["clawdbot"]
    install:
      - id: clawdbot-cli
        kind: manual
        label: "Install clawdbot CLI (see Prerequisites)"
---

# ClawdControl Skill

Control and manage Clawdbot via its CLI. This skill documents all available `clawdbot` commands for gateway management, agent control, messaging, and more.

## Prerequisites

**The clawdbot CLI must be available in the system path for this skill to work!**

You can link it by calling `pnpm link` in your local copy of the git repo or installing it globally.

```bash
# From your local clawdbot repo
cd /path/to/clawdbot
pnpm link --global

# Or install globally via your package manager
pnpm add -g clawdbot
```

## Usage

All commands follow the pattern: `clawdbot <command> [options]`

```bash
clawdbot --help              # Show all commands
clawdbot <command> --help    # Get help for a specific command
```

## Commands Reference

### Global Options

| Option | Description |
|--------|-------------|
| `-V, --version` | Output version number |
| `--dev` | Dev profile (isolated state under `~/.clawdbot-dev`) |
| `--profile <name>` | Use a named profile |
| `--no-color` | Disable ANSI colors |
| `-h, --help` | Display help |

---

### setup — Initialize Clawdbot

Initialize `~/.clawdbot/clawdbot.json` and the agent workspace.

```bash
clawdbot setup [options]

Options:
  --workspace <dir>       Agent workspace directory (default: ~/clawd)
  --wizard                Run the interactive onboarding wizard
  --non-interactive       Run without prompts
  --mode <mode>           Wizard mode: local|remote
  --remote-url <url>      Remote Gateway WebSocket URL
  --remote-token <token>  Remote Gateway token
```

---

### onboard — Interactive Setup Wizard

Set up the gateway, workspace, and skills interactively.

```bash
clawdbot onboard [options]

Options:
  --workspace <dir>              Agent workspace directory
  --reset                        Reset config + credentials + sessions
  --non-interactive              Run without prompts
  --flow <flow>                  Wizard flow: quickstart|advanced
  --mode <mode>                  Wizard mode: local|remote
  --auth-choice <choice>         Auth method (token|claude-cli|apiKey|etc.)
  --gateway-port <port>          Gateway port
  --gateway-bind <mode>          Bind: loopback|lan|tailnet|auto
  --gateway-auth <mode>          Auth: off|token|password
  --install-daemon               Install gateway daemon
  --skip-providers               Skip provider setup
  --skip-skills                  Skip skills setup
  --node-manager <name>          Node manager: npm|pnpm|bun
  --json                         Output JSON summary
```

---

### configure — Update Configuration

Interactive wizard to update models, providers, skills, and gateway.

```bash
clawdbot configure|config [options]

Options:
  --section <name>  Configure only one section (repeatable):
                    workspace|model|gateway|daemon|providers|skills|health
```

---

### doctor — Health Checks

Health checks + quick fixes for the gateway and providers.

```bash
clawdbot doctor [options]

Options:
  --no-workspace-suggestions  Disable workspace memory suggestions
  --yes                       Accept defaults
  --repair                    Apply recommended repairs
  --force                     Apply aggressive repairs
  --non-interactive           Safe migrations only
  --generate-gateway-token    Generate gateway token
  --deep                      Scan system for extra gateway installs
```

---

### reset — Reset Configuration

Reset local config/state (keeps CLI installed).

```bash
clawdbot reset [options]

Options:
  --scope <scope>    config|config+creds+sessions|full
  --yes              Skip confirmation
  --dry-run          Print actions without removing files
```

---

### uninstall — Remove Clawdbot

Uninstall gateway service + local data (CLI remains).

```bash
clawdbot uninstall [options]

Options:
  --service    Remove gateway service
  --state      Remove state + config
  --workspace  Remove workspace dirs
  --app        Remove macOS app
  --all        Remove everything
  --yes        Skip confirmation
  --dry-run    Preview actions
```

---

### message — Send Messages

Send messages and provider actions.

```bash
clawdbot message [command]

Commands:
  send         Send a message
  poll         Send a poll
  react        Add/remove a reaction
  reactions    List reactions
  read         Read recent messages
  edit         Edit a message
  delete       Delete a message
  pin          Pin a message
  unpin        Unpin a message
  pins         List pinned messages
  permissions  Fetch channel permissions
  search       Search messages
  thread       Thread actions
  emoji        Emoji actions
  sticker      Sticker actions
  role         Role actions
  channel      Channel actions
  member       Member actions
  voice        Voice actions
  event        Event actions
  timeout      Timeout a member
  kick         Kick a member
  ban          Ban a member

Examples:
  clawdbot message send --to +15555550123 --message "Hi"
  clawdbot message poll --provider discord --to channel:123 --poll-question "Snack?" --poll-option Pizza --poll-option Sushi
  clawdbot message react --provider discord --to 123 --message-id 456 --emoji "✅"
```

---

### agent — Run Agent Turn

Run an agent turn via the Gateway.

```bash
clawdbot agent [options]

Options:
  -m, --message <text>     Message for the agent
  -t, --to <number>        Recipient in E.464
  --session-id <id>        Explicit session id
  --thinking <level>       Thinking level: off|minimal|low|medium|high
  --provider <provider>    Delivery: last|telegram|whatsapp|discord|slack|signal|imessage
  --local                  Run embedded agent locally
  --deliver                Send reply back to provider
  --json                   Output as JSON
  --timeout <seconds>      Agent timeout

Examples:
  clawdbot agent --to +15555550123 --message "status update"
  clawdbot agent --session-id 1234 --message "Summarize inbox" --thinking medium
  clawdbot agent --to +15555550123 --message "Summon reply" --deliver
```

---

### agents — Manage Isolated Agents

Manage isolated agents (workspaces + auth + routing).

```bash
clawdbot agents [command]

Commands:
  list        List configured agents
  add         Add a new isolated agent
  delete      Delete an agent and prune workspace/state
```

---

### daemon — Gateway Service Management

Manage the Gateway daemon service (launchd/systemd/schtasks).

```bash
clawdbot daemon [command]

Commands:
  status      Show daemon status + probe Gateway
  install     Install Gateway service
  uninstall   Uninstall Gateway service
  start       Start Gateway service
  stop        Stop Gateway service
  restart     Restart Gateway service

Examples:
  clawdbot daemon status
  clawdbot daemon install
  clawdbot daemon restart
```

---

### gateway — Run WebSocket Gateway

Run the WebSocket Gateway.

```bash
clawdbot gateway [options] [command]

Options:
  --port <port>              Gateway WebSocket port
  --bind <mode>              Bind mode: loopback|tailnet|lan|auto
  --token <token>            Shared auth token
  --auth <mode>              Auth mode: token|password
  --tailscale <mode>         Tailscale: off|serve|funnel
  --tailscale-reset-on-exit  Reset Tailscale on shutdown
  --force                    Kill existing listener on port
  --verbose                  Verbose logging
  --compact                  Compact WebSocket logs
  --raw-stream               Log raw model events to jsonl

Commands:
  call       Call a Gateway method
  health     Fetch Gateway health
  status     Show reachability + discovery + health
  discover   Discover gateways via Bonjour

Examples:
  clawdbot gateway --port 18789
  clawdbot --dev gateway
  clawdbot gateway --force
  clawdbot gateway status
```

---

### logs — Tail Gateway Logs

Tail gateway file logs via RPC.

```bash
clawdbot logs [options]

Options:
  --limit <n>        Max lines (default: 200)
  --max-bytes <n>    Max bytes (default: 250000)
  --follow           Follow log output
  --interval <ms>    Polling interval (default: 1000)
  --json             Emit JSON log lines
  --plain            Plain text output
  --url <url>        Gateway WebSocket URL
  --token <token>    Gateway token
  --timeout <ms>     Timeout (default: 10000)

Examples:
  clawdbot logs --follow
  clawdbot logs --limit 50 --json
```

---

### memory — Memory Search Tools

Memory search and indexing tools.

```bash
clawdbot memory [command]

Commands:
  status      Show memory search index status
  index       Reindex memory files
  search      Search memory files

Examples:
  clawdbot memory status
  clawdbot memory index
  clawdbot memory search "project ideas"
```

---

### models — Model Management

Model discovery, scanning, and configuration.

```bash
clawdbot models [command]

Commands:
  list             List configured models
  status           Show configured model state
  set              Set the default model
  set-image        Set the image model
  aliases          Manage model aliases
  fallbacks        Manage model fallback list
  scan             Scan OpenRouter free models
  auth             Manage model auth profiles

Examples:
  clawdbot models list
  clawdbot models status
  clawdbot models set anthropic/claude-sonnet-4-5
```

---

### nodes — Node Pairing Management

Manage gateway-owned node pairing.

```bash
clawdbot nodes [command]

Commands:
  status      List known nodes with status
  describe    Describe node capabilities
  list        List pending and paired nodes
  pending     List pending pairing requests
  approve     Approve a pairing request
  reject      Reject a pairing request
  rename      Rename a paired node
  invoke      Invoke a command on a node
  run         Run shell command on a node (mac)
  notify      Send notification (mac)
  camera      Capture camera media
  canvas      Capture/render canvas content
  screen      Capture screen recordings
  location    Fetch location

Examples:
  clawdbot nodes status
  clawdbot nodes list
  clawdbot nodes pending
  clawdbot nodes approve <code>
```

---

### sandbox — Container Management

Manage sandbox containers (Docker-based agent isolation).

```bash
clawdbot sandbox [command]

Commands:
  list        List containers and status
  recreate    Remove containers to force recreation
  explain     Explain effective sandbox/tool policy

Examples:
  clawdbot sandbox list
  clawdbot sandbox list --browser
  clawdbot sandbox recreate --all
  clawdbot sandbox explain
```

---

### tui — Terminal UI

Open a terminal UI connected to the Gateway.

```bash
clawdbot tui [options]

Options:
  --url <url>            Gateway WebSocket URL
  --token <token>        Gateway token
  --password <password>  Gateway password
  --session <key>        Session key
  --deliver              Deliver assistant replies
  --thinking <level>     Thinking level override
  --message <text>       Send initial message
  --timeout-ms <ms>      Agent timeout
  --history-limit <n>    History entries to load (default: 200)

Examples:
  clawdbot tui
  clawdbot tui --session mychat --deliver
```

---

### wake — Trigger Wake Event

Enqueue a system event and optionally trigger an immediate heartbeat.

```bash
clawdbot wake [options]

Options:
  --text <text>    System event text
  --mode <mode>    Wake mode: now|next-heartbeat
  --json           Output JSON
  --url <url>      Gateway WebSocket URL
  --token <token>  Gateway token
  --expect-final   Wait for final response

Examples:
  clawdbot wake --text "Check emails" --mode now
```

---

### cron — Cron Job Management

Manage cron jobs via Gateway.

```bash
clawdbot cron [command]

Commands:
  status      Show cron scheduler status
  list        List cron jobs
  add         Add a cron job
  rm          Remove a cron job
  enable      Enable a cron job
  disable     Disable a cron job
  runs        Show cron run history
  edit        Edit a cron job
  run         Run a cron job now

Examples:
  clawdbot cron list
  clawdbot cron add --schedule "0 * * * *" --command "status"
  clawdbot cron run <job-id>
```

---

### dns — DNS Helpers

DNS helpers for wide-area discovery (Tailscale + CoreDNS).

```bash
clawdbot dns [command]

Commands:
  setup       Set up CoreDNS to serve clawdbot.internal

Examples:
  clawdbot dns setup
```

---

### docs — Search Documentation

Search the live Clawdbot docs.

```bash
clawdbot docs [query...]

Examples:
  clawdbot docs "gateway configuration"
  clawdbot docs "model providers"
```

---

### hooks — Webhook Helpers

Webhook helpers and hook-based integrations.

```bash
clawdbot hooks [command]

Commands:
  gmail       Gmail Pub/Sub hooks (via gogcli)
```

---

### pairing — Secure DM Pairing

Secure DM pairing (approve inbound requests).

```bash
clawdbot pairing [command]

Commands:
  list        List pending pairing requests
  approve     Approve a pairing code

Examples:
  clawdbot pairing list
  clawdbot pairing approve <code>
```

---

### plugins — Plugin Management

Manage Clawdbot plugins/extensions.

```bash
clawdbot plugins [command]

Commands:
  list        List discovered plugins
  info        Show plugin details
  enable      Enable a plugin
  disable     Disable a plugin
  install     Install a plugin
  doctor      Report plugin load issues

Examples:
  clawdbot plugins list
  clawdbot plugins install npm:my-plugin
```

---

### providers — Provider Management

Manage chat provider accounts.

```bash
clawdbot providers [command]

Commands:
  list        List configured providers + auth profiles
  status      Show gateway provider status
  logs        Show recent provider logs
  add         Add or update a provider account
  remove      Disable or delete a provider account
  login       Link a provider account (WhatsApp Web)
  logout      Log out of a provider session

Examples:
  clawdbot providers list
  clawdbot providers login --verbose
  clawdbot providers status
```

---

### skills — Skill Management

List and inspect available skills.

```bash
clawdbot skills [command]

Commands:
  list        List all available skills
  info        Show detailed information about a skill
  check       Check which skills are ready vs missing requirements

Examples:
  clawdbot skills list
  clawdbot skills info github
  clawdbot skills check
```

---

### update — Update Clawdbot

Update Clawdbot to the latest version.

```bash
clawdbot update [options]

Options:
  --json               Output result as JSON
  --restart            Restart daemon after update
  --timeout <seconds>  Timeout per update step (default: 1200)

Notes:
  - For git installs: fetches, rebases, installs deps, builds, runs doctor
  - Skips update if working directory has uncommitted changes

Examples:
  clawdbot update
  clawdbot update --restart
```

---

### status — Show System Status

Show provider health and recent session recipients.

```bash
clawdbot status [options]

Options:
  --json          Output JSON
  --all           Full diagnosis
  --usage         Show provider usage/quota snapshots
  --deep          Probe providers (WA + Telegram + Discord + Slack + Signal)
  --timeout <ms>  Probe timeout
  --verbose       Verbose logging

Examples:
  clawdbot status
  clawdbot status --all
  clawdbot status --deep
  clawdbot status --usage
```

---

### health — Gateway Health

Fetch health from the running gateway.

```bash
clawdbot health [options]

Options:
  --json          Output JSON
  --timeout <ms>  Connection timeout
  --verbose       Verbose logging

Examples:
  clawdbot health
  clawdbot health --json
```

---

### sessions — List Sessions

List stored conversation sessions.

```bash
clawdbot sessions [options]

Options:
  --json              Output as JSON
  --verbose           Verbose logging
  --store <path>      Path to session store
  --active <minutes>  Only show sessions updated within N minutes

Examples:
  clawdbot sessions
  clawdbot sessions --active 120
  clawdbot sessions --json
```

---

### browser — Browser Management

Manage clawd's dedicated browser (Chrome/Chromium).

```bash
clawdbot browser [command]

Commands:
  status                    Show browser status
  start                     Start the browser
  stop                      Stop the browser
  reset-profile             Reset browser profile
  tabs                      List open tabs
  tab                       Tab shortcuts
  open <url>                Open URL in new tab
  focus <target-id>         Focus a tab
  close <target-id>         Close a tab
  profiles                  List all browser profiles
  create-profile <name>     Create a new profile
  delete-profile <name>     Delete a profile
  screenshot                Capture screenshot
  snapshot                  Capture snapshot (ai|aria format)
  navigate <url>            Navigate to URL
  resize <width> <height>   Resize viewport
  click <ref>               Click element by ref
  type <ref> <text>         Type into element
  press <key>               Press a key
  hover <ref>               Hover element
  drag <from> <to>          Drag from one ref to another
  select <ref> <option...>  Select option(s)
  upload <path>             Arm file upload
  fill --fields <json>      Fill form
  dialog --accept           Handle modal dialog
  wait --text <text>        Wait for condition
  evaluate --fn <js>        Evaluate JS function
  console                   Get console messages
  pdf                       Save page as PDF
  cookies                   Read/write cookies
  storage                   Read/write localStorage/sessionStorage
  set                       Browser environment settings

Examples:
  clawdbot browser status
  clawdbot browser start
  clawdbot browser open https://example.com
  clawdbot browser snapshot
  clawdbot browser screenshot --full-page
  clawdbot browser click 12 --double
  clawdbot browser type 23 "hello" --submit
  clawdbot browser navigate https://example.com
  clawdbot browser resize 1280 720
  clawdbot browser console --level error
```

---

## Quick Reference

| Task | Command |
|------|---------|
| View all commands | `clawdbot --help` |
| Get command help | `clawdbot <command> --help` |
| Start gateway | `clawdbot gateway` |
| Run agent | `clawdbot agent --to +123456789 --message "Hi"` |
| Send message | `clawdbot message send --to +123456789 --message "Hi"` |
| Check status | `clawdbot status` |
| List sessions | `clawdbot sessions` |
| Update clawdbot | `clawdbot update` |
| Manage providers | `clawdbot providers` |
| Manage skills | `clawdbot skills` |
| Run TUI | `clawdbot tui` |

## Documentation

- [CLI Docs](https://docs.clawd.bot/cli)
- [Gateway Docs](https://docs.clawd.bot/gateway)
- [Tools > Browser](https://docs.clawd.bot/tools/browser)
