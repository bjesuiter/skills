# SVG battle rubric

Score the artifact, not the explanation.

- Brief compliance, 20 points. The SVG represents the requested subject, context, dimensions, and behavior.
- Visual craft, 25 points. Composition, proportion, spacing, hierarchy, stroke treatment, and color feel deliberate at the requested sizes.
- Geometry and scaling, 15 points. The `viewBox`, bounds, aspect ratio, transforms, and strokes scale without clipping or distortion.
- Accessibility and integration, 15 points. Semantics match the host context. The artifact handles inheritance, interaction, and reduced motion where applicable.
- Maintainability, 15 points. The markup uses clear primitives, paths, groups, IDs, reusable definitions, and precision without export residue.
- Safety and robustness, 10 points. References resolve, repeated instances remain safe, external dependencies are intentional, and the static fallback works.

Deduct for defects visible in the rendering even when structural checks pass. Deduct for structural defects that a static preview cannot show. Do not reward visual complexity by itself.
