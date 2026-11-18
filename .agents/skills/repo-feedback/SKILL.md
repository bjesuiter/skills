---
name: repo-feedback
description: Report friction observed while running this repo's update-vendored or skill-merge workflows, and turn useful reports into regression checks.
metadata:
  internal: true
---

# Repo Feedback

When using `update-vendored` or `skill-merge`, capture concrete problems with the instructions. Examples include a broken command, an unclear decision, a missing prerequisite, repeated work, or a user correction. Continue the requested task when possible. A smooth run needs no feedback report.

## Report observed friction

Record each distinct issue as a Git-trackable Markdown file under `docs/agents/feedback/`. Create the directory on the first report. Name new files `YYYY-MM-DD-<skill>-<short-slug>.md`. Use a title and these fields:

- **Instruction** — skill, file and section, and the repo revision if known. Include whether the case was a check or refresh, or a vendor or semantic comparison, where relevant.
- **Expected and observed** — the smallest reproducible input and what actually happened. Distinguish an instruction problem from a tool, environment, or agent error when the evidence supports it.
- **Impact and workaround** — what was blocked or repeated, how the agent recovered, and any measured time or retries that help explain the impact.
- **Proposed change** — a narrow edit or an open question if the cause is uncertain.
- **Status** — start with `open`. Set it to `resolved` after verifying a fix and record the pass criterion and result.

Subagents return observations to the main agent, which owns writes. Search the directory for the same problem first. If a report exists, add the new occurrence with its date and revision. Use sanitized reproductions that can be committed. Link the files created or updated in the run's final response. Include them when asked to commit the feedback. Use the repo's [GitHub issue workflow](../../../docs/agents/issue-tracker.md) if the user asks to publish a report there.

## Check whether a change helped

When reviewing or fixing feedback, replay the original scenario with the same inputs, model, and environment before and after the instruction change where practical. Write down observable pass criteria first. For example, a check with upstream changes reports the correct targets and leaves the worktree untouched. A semantic review identifies the new behavior and preserves the successor's rules. A vendor review preserves local path mappings. Compare completion and user corrections first, then measured elapsed time, redundant commands or retries, and token use when available. Repeat timing runs when claiming a speedup, using the same changed skills for serial and parallel runs. Keep reproducible failures as regression cases when they cover a meaningful behavior.
