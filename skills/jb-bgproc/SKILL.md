---
name: jb-bgproc
description: Use when starting, stopping, listing, cleaning, or inspecting long-running background processes via bgproc.
homepage: https://github.com/ascorbic/bgproc
metadata: {"clawdbot":{"requires":{"bins":["bgproc"]},"install":[{"id":"bun","kind":"bun","package":"bgproc","label":"Install bgproc (bun)","command":"bun i -g bgproc"}]}}
skill_author: bjesuiter
---

# bgproc CLI

Simple process manager for agents. All commands output JSON to stdout.

## Quick usage

```bash
bgproc start -n myserver -- npm run dev
```

## Commands

- start: Start a background process
- status: Get status of a background process (pid, open ports)
- logs: View logs for a background process
- stop: Stop a background process
- list: List all background processes
- clean: Remove dead processes and their logs

## start

```bash
bgproc start -n <name> [-f] [-t <seconds>] [-w [<seconds>]] [--keep] -- <command...>
```

Notes:
- `-n <name>`: Name the process (required)
- `-f`: Force start if name exists
- `-t <seconds>`: Timeout before considering start failed
- `-w [<seconds>]`: Wait for the process to become ready; optional seconds
- `--keep`: Keep logs after stop
- `--`: Separator before the command to run

## Other commands

```bash
bgproc status -n <name>
bgproc logs -n <name>
bgproc stop -n <name>
bgproc list
bgproc clean
```

## Tips

- Parse JSON output to extract pid, ports, and status fields.
- Use `bgproc clean` to remove stale entries and logs.
