# Human best practices

Recommendations for how JB runs agents. These are not agent instructions. Each entry comes from observed sessions, usually a skill-doctor run, and names its evidence.

## Model settings

### Watch for agents that stop after an implementation go-ahead

If an agent ends its turn after "implement" or "go" without changing a file, switch the model before raising effort. gpt-6.2-sol on low effort implemented reliably in local sessions, so low is acceptable for implementation work with it.

Evidence: skill-doctor, 2026-11-21. In Codex thread `01a1e49e`, four of six stops without a change happened on gpt-6.1-terra at medium effort. After the switch to gpt-6.1-sol at low effort, the agent changed files right away but still ended twice too early. In 20 gpt-6.2-sol sessions on low effort (17–21 Nov 2026, 145 user turns, about 40 go-aheads or change requests), it never ended a turn without making the change. Most of these turns record effort as `null`, which resolves to the config default of `low`. The evidence is thin: one Terra session, and the 6.2 sessions are mostly small repo and config changes.

### Check the handoff model and effort

A handoff thread inherits the parent's model and options unless you choose others. Check that the handoff runs with the model and effort you want for the next step.

Evidence: same session. The handoff to a new thread kept gpt-6.1-sol with low effort.
