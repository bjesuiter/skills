# Human best practices

Recommendations for how JB runs agents. These are not agent instructions. Each entry comes from observed sessions, usually a skill-doctor run, and names its evidence.

## Model settings

### Use reasoning effort medium or higher for implementation work

Low reasoning effort is fine for short questions and status checks. For implementation threads, spec work, and handoffs, use medium or higher.

Evidence: skill-doctor, pi-phoenix batch 1, 2026-11-21. In Codex thread `01a1e49e` (gpt-6.1-sol, `reasoningEffort: low`), the agent ended its turn six times after "implement" or "go" before it changed the first file. The Codex base instructions already tell it to continue after authorization, so an instruction change would not fix this. One session is not proof, but low effort is the most likely cause.

### Check the handoff model and effort

A handoff thread inherits the parent's model and options unless you choose others. If the parent ran with low effort, set a higher effort for the handoff.

Evidence: same session. The handoff to a new thread kept gpt-6.1-sol with low effort.
