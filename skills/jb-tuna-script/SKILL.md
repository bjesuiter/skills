---
name: jb-tuna-script
description: Create simple executable scripts for the Tuna macOS launcher. Use when the user asks to add, write, create, or fix a Tuna script, Tuna launcher command, or script discoverable by Tuna.
---

# JB Tuna Script

Use this skill when creating small scripts that should appear in Tuna.

## Key facts

- Tuna scans executable scripts in `~/Library/Scripts` even in free mode.
- Custom script directories may be disabled unless Tuna Pro is active.
- Prefer creating the script directly in `~/Library/Scripts/<command-name>`.
- Do not research Tuna script locations again unless this path fails.

## Minimal script template

```bash
#!/usr/bin/env bash
# @tuna.name command-name
# @tuna.subtitle Short human-readable description
# @tuna.icon symbol:terminal
# @tuna.mode background
# @tuna.input none
# @tuna.output text

set -euo pipefail

export PATH="$HOME/.homebrew/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:$PATH"

exec command arg1 arg2
```

## Workflow

1. Choose a concise filename and Tuna name, usually the command name the user asked for.
2. Write the script at `~/Library/Scripts/<name>`.
3. Include Tuna metadata comments only as needed:
   - `@tuna.name` for display/search name.
   - `@tuna.subtitle` for a short explanation.
   - `@tuna.icon` optional; use an SF Symbol when obvious.
   - `@tuna.mode background` for wrappers that should just run.
   - `@tuna.input none` for no-argument scripts.
   - `@tuna.output text` when command output is useful.
4. Make it executable: `chmod +x ~/Library/Scripts/<name>`.
5. Verify by running `~/Library/Scripts/<name>` directly.

## Example: PinchTab dashboard

```bash
#!/usr/bin/env bash
# @tuna.name pinchtab
# @tuna.subtitle Open the PinchTab dashboard
# @tuna.icon symbol:rectangle.connected.to.line.below
# @tuna.mode background
# @tuna.input none
# @tuna.output text

set -euo pipefail

export PATH="$HOME/.homebrew/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:$PATH"

exec pinchtab dashboard
```

Expected path:

```text
~/Library/Scripts/pinchtab
```

Expected verification output:

```text
Dashboard: http://127.0.0.1:9867
  Token copied to clipboard — paste it on the login page.
  Opened in your browser.
```

## Guardrails

- Keep wrappers minimal; avoid inspecting unrelated existing scripts unless the requested behavior is complex.
- Use absolute/user-specific PATH entries when needed for Homebrew-installed CLIs.
- Prefer `exec <command>` so the script exits with the wrapped command's status.
