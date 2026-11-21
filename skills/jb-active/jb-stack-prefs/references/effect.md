# Effect evaluation

Confirmed by JB on 2026-10-09 in the `jb-stack-prefs` discussion.

- Status: interested in evaluating Effect, also referred to as effect-ts or EffectTS, when a suitable project appears. It is not a default stack choice.
- Evaluation target: v4 as specified by JB on 2026-10-09. Verify current release status and compatibility when starting the evaluation.
- Concern: Effect's abstractions may spread throughout the project and shape its architecture. JB wants to understand that cost before adopting it broadly.
- Start with a bounded use case and explicit integration boundaries. Assess the benefit, how much surrounding code must adopt Effect, and how easily the experiment can be removed or isolated.
- Expand adoption only after JB has evaluated the results and chosen to use it more broadly.
