---
name: jb-bgproc
description: "Manage background processes with bgproc: start dev servers, wait for ports, inspect status/logs, restart, stop, and clean dead entries."
homepage: https://github.com/ascorbic/bgproc
metadata: {"clawdbot":{"requires":{"bins":["bgproc"]},"install":[{"id":"bun","kind":"bun","package":"bgproc","label":"Install bgproc (bun)","command":"bun i -g bgproc"}]}}
skill_author: bjesuiter
---

# Background Processes

Consolidated from the official `ascorbic/bgproc` skill and JB's process-management workflow. Validated against npm `bgproc@0.3.0` on Linux on 2026-10-06.

## Workflow

1. Choose a task-specific process name and start from the intended working directory.
2. For a server, wait for a listening port with a bounded timeout:

   ```bash
   bgproc start -n my-devserver -w 30 -- npm run dev
   ```

   This waits for port detection, not application health. Check the returned URL/endpoint separately when readiness requires more than a listening socket.
3. Inspect or restart the same process:

   ```bash
   bgproc status -n my-devserver
   bgproc logs -n my-devserver --tail 50
   bgproc logs -n my-devserver --errors
   bgproc restart -n my-devserver -w 30
   ```

4. Stop task-owned processes when finished, unless the user wants them left running:

   ```bash
   bgproc stop -n my-devserver
   ```

   A successful stop removes the registry entry and logs. Use `clean` for entries left behind by processes that exited independently.

## Command reference

```bash
# Start without waiting for a port
bgproc start -n my-worker -- node worker.mjs

# Limit process lifetime to five minutes
bgproc start -n my-worker -t 300 -- node worker.mjs

# Replace an existing named process; kills it first
bgproc start -n my-devserver -f -w 30 -- npm run dev

# Keep a process alive if port detection times out
bgproc start -n my-devserver -w 30 --keep -- npm run dev

# Restart using the stored command, directory, and lifetime timeout
bgproc restart -n my-devserver -w 30

# Logs are plain text; follow runs until interrupted
bgproc logs -n my-devserver --all
bgproc logs -n my-devserver --follow

# List processes, optionally restricted to a working directory
bgproc list
bgproc list --cwd
bgproc list --cwd /path/to/project

# Force-stop only when graceful termination is insufficient
bgproc stop -n my-devserver --force

# Clean a named dead entry and its logs
bgproc clean -n my-worker
```

`status`, `logs`, `stop`, `restart`, and `clean` also accept a positional process name. Examples here use `-n` consistently.

## Operational rules

- `-t SECONDS` on `start` limits process lifetime; it is not a startup timeout.
- `-w SECONDS` bounds the wait for a listening port. Without `--keep`, a wait timeout kills the process. Always specify seconds for a bounded wait.
- `--keep` applies only to port-wait timeout; it does not preserve logs or cancel the separate `-t` lifetime limit.
- Process-management commands emit JSON; `logs` emits plain text. Port-wait log streaming goes to stderr. Redact secrets before sharing either stream.
- Inspect existing names before force-replacing or stopping them. Limit cleanup to task-owned entries; `bgproc clean --all` affects every dead entry in the selected data directory.
- Port detection requires `lsof` and examines child processes. Supported platforms are macOS and Linux.
- For isolated validation, set `BGPROC_DATA_DIR` to a task-specific temporary directory so existing managed processes are untouched.
- Check `bgproc <command> --help` when behavior differs. Verify the installed package version through the package manager: this release's help banner incorrectly reports `v0.1.0`.
