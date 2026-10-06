# Competitor research intake

Status: captured for later verification and benchmark design.

Provenance: notes supplied by JB on 2026-08-23 from another agent's research. The repositories and `SKILL.md` files have not been independently checked in this lab. Star counts, install counts, licenses, security-audit claims, and implementation details may change.

## Candidate skills

### Upbrew SVG Creator Skill

Source: [upbrew-tech/svg-creator-skill](https://github.com/upbrew-tech/svg-creator-skill)

Reported strengths:

- General SVGs, illustrations, characters, icons, and animation.
- A required write, render, inspect, and fix loop.
- Recipes for composition, light, gradients, shadows, and characters.
- Reported as Apache-2.0 with 25 GitHub stars at intake time.

Reported concern:

- Do not install or run it unchanged. Its helper reportedly assumes Claude-specific paths and may install CairoSVG with `pip --break-system-packages`.
- Before a benchmark, inspect the current repository and extract a safe candidate that contains instructions only. Do not carry its dependency-install behavior into the lab.

### Jawwad's SVG Creator

Source: [svg-creator/SKILL.md in jawwadfirdousi/agent-skills](https://github.com/jawwadfirdousi/agent-skills/blob/main/svg-creator/skills/svg-creator/SKILL.md)

Reported strengths:

- SVG 2 and path syntax.
- Portable output without host CSS dependencies.
- Accessibility and security.
- Gradients, masks, filters, and animation.
- Validation and production cleanup.

Reported tradeoff:

- Strong technical reference, but less emphasis on a visual feedback loop.

### Icon Set Generator

Source: [Icon Set Generator on skills.sh](https://www.skills.sh/jezweb/claude-skills/icon-set-generator)

Reported strengths:

- A shared style contract for stroke, corner radii, and visual density.
- Reported at about 1,700 installations, 976 GitHub stars, and three passed security audits at intake time.

Reported boundary:

- Specialized for icon families. Compare it in an icon-set case, not as a general illustration skill.

## Candidates not shortlisted

- Quiver and similar SVG generator skills reportedly delegate to an external API. They do not test whether the skill improves the agent's own SVG work.
- ClawHub `text-to-svg` was reported as OpenClaw-compatible and audited, but too shallow to make a useful general competitor.
- `svg-art` was reported as useful for generated patterns, charts, and fractals, but not for free-form visual design.

## Working synthesis

The supplied recommendation combines four ideas:

- Carmen Ansio for coordinate systems and SVG fundamentals.
- Jawwad for correctness, portability, accessibility, and security.
- Upbrew for the render, inspect, and fix loop.
- Icon Set Generator for a measurable style contract across related icons.

Treat this as a hypothesis for improving `jb-svg`, not as evidence. A later benchmark should show which instructions change output quality and which only make the skill longer.

## Future benchmark

Do not add a test case from these notes alone. Resume with this sequence:

1. Fetch the current source for every shortlisted skill and record its commit SHA, license, exact `SKILL.md` path, and any linked instructions that affect behavior.
2. Remove or isolate installation commands, machine-specific paths, network mutations, and tool assumptions before using a candidate in the lab.
3. Decide whether the first comparison tests general illustration craft or icon-family consistency. These are different tasks and should become separate cases.
4. Write one neutral JSON case under `cases/`. Describe the artifact and host context without naming techniques taken from any candidate skill.
5. Run all candidates with the same pinned model. Inspect the blind gallery before revealing identities or reading the judge report.
6. Promote a rule into `jb-svg` only when repeated runs tie it to a specific improvement.

The lab already keeps every execution separate:

```text
runs/<timestamp>/
├── manifest.json
├── candidates/<candidate>/SKILL.md
├── artifacts/<case>/<candidate>/
├── evaluations/
├── gallery.html
└── summary.md
```

Run directories use a timestamp and add a numeric suffix on collision, so a later test never overwrites an earlier run.
