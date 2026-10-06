# Use plain SVG until a concrete roadblock

## Status

Accepted on 2026-10-06 by JB.

## Context

In the saved pelican-bicycle comparison, JB preferred the no-skill baseline. The `jb-svg` output had a beak junction glitch and broken-looking leg geometry. Both outputs passed all eight structural checks, while the automated judge narrowly favored `jb-svg`, 94 to 93. Those checks and scores did not capture the defects that mattered in human review.

This is one comparison with a gallery framing problem, not proof that every SVG skill performs worse. It provides no convincing benefit for keeping this broad skill active. The [archived research](../../research/jb-svg/README.md) preserves the artifacts and [human verdict](../../research/jb-svg/evidence/20260823-145049/human-review.md).

## Decision

Use plain SVG generation and editing without a dedicated SVG skill for now. Archive `jb-svg` and its evaluation lab as research, remove it from the active catalog and preference registry, and retire its installed copy.

Reconsider a custom skill only after encountering a concrete roadblock in real SVG work. Capture that failure, then write the smallest concise skill that addresses it. Retain only instructions that demonstrably help with the roadblock when compared with plain SVG.

## Consequences

SVG work proceeds with ordinary task instructions and visual inspection. Broad SVG guidance and competitor benchmarking are paused. The archived skill and lab remain available as reference if a future failure justifies a focused experiment.
