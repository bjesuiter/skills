---
name: overnight-mode
description: Carry out unattended work using reversible defaults and a morning handoff.
disable-model-invocation: true
---

# Overnight mode

For an unattended run, create `~/.agents/OVERNIGHT` and state the work you are taking on. The marker applies to every session on this account that has the Stop hook configured. Leave it in place until the user ends overnight mode.

Resolve routine choices using the task, project conventions, and user preferences. Take reversible steps within scope and continue every independent part of the task. Record debatable choices, your assumptions, and how to undo each choice in the morning report. If a step requires approval or an unavailable human action, defer it and continue elsewhere.

Finish when the requested work is complete or all remaining work requires human action. Report completed work, verification, and the morning list. Describe each blocker as a declarative `NEEDS INPUT` item with the required action.

On an explicit request to end overnight mode or perform the morning handoff, remove `~/.agents/OVERNIGHT` and report the outcome and remaining items.

When asked to configure automatic enforcement, read [Stop hook setup](references/setup.md). The guard gives the agent up to two chances to act on a reversible next step or state a blocker before it allows the turn to end.
