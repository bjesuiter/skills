# Stop hook setup

Install the skill with the Skills CLI for Claude Code, Codex, or both. The Stop hook requires Python 3 via `uv`. To enable it, merge the following entry into `hooks.Stop` in the appropriate file. Keep existing settings and register the guard once per agent.

| Agent | Project settings | User settings |
| --- | --- | --- |
| Claude Code | `.claude/settings.json` | `~/.claude/settings.json` |
| Codex | `.codex/hooks.json` | `~/.codex/hooks.json` |

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "uv run --no-project python '/absolute/path/to/overnight-mode/scripts/stop_guard.py'"
          }
        ]
      }
    ]
  }
}
```

Use the absolute path to the installed script. For a shared project config, put a copy of the script in the repo and use a project-root-relative command. Claude Code exposes `CLAUDE_PROJECT_DIR`. In a Git checkout, Codex can resolve the root with `git rev-parse --show-toplevel`. If Codex already defines hooks in `config.toml`, add the entry there to keep one source at that scope.

In Codex, review and trust the hook through `/hooks`. Project settings also require a trusted project. In Claude Code, open `/hooks` to verify the Stop entry. Restart existing sessions if they have not loaded the change.

The guard examines the tail of the final message through the `last_assistant_message` field supported by current Claude Code and Codex releases. Its question detection is heuristic. It leaves native permission prompts and mid-turn interactions to the agent and host. If the host doesn't run Stop hooks, the skill's unattended-work instructions still apply.

See [Claude Code hooks](https://code.claude.com/docs/en/hooks#stop) and the [Codex Stop event](https://github.com/openai/codex/blob/rust-v0.171.0/codex-rs/hooks/src/events/stop.rs).
