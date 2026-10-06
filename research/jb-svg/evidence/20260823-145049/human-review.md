# Human review of the pelican-bicycle battle

Reviewed by JB on 2026-10-06. Generated on 2026-08-23 using `gpt-5.6-sol` with high reasoning effort.

## Verdict

Baseline preferred. JB identified a glitch at the beak and broken-looking legs in `jb-svg`; the baseline looked better on those details.

- Entry A: `jb-svg`, [SVG](artifacts/pelican-bicycle/jb-svg/output.svg).
- Entry B: no-skill baseline, [SVG](artifacts/pelican-bicycle/baseline/output.svg).
- Screenshots: [beak and framing](beak-and-framing.png), [legs](legs.png).

## Evaluation limits

Both entries passed 8/8 structural checks. The [original automated judge](evaluations/pelican-bicycle.json) preferred A with scores of 94 and 93, praised A's feet and pedal contact, and criticized B's leg intersections. Human review disagreed. The original judge report is preserved unchanged, separately from this verdict.

The gallery displayed A enlarged and cropped while B fit entirely. This limits the fairness of the presentation and should be corrected before any future comparison. A single run cannot establish a general ranking of skill-based and plain SVG generation.

## Disposition

The [accepted decision](../../../../docs/adr/0001-use-plain-svg-until-a-roadblock.md) makes plain SVG the default. A future custom skill must address an observed roadblock and stay as small and concise as possible.

The manifest retains original source locations as provenance. Candidate instruction snapshots are stored as `instructions.md`; execution logs are omitted. Other local runs remain in the ignored `runs/` directory.
