---
name: jb-svg
description: Create, edit, or review hand-authored SVGs, including icons, diagrams, illustrations, responsive graphics, and SVG animation.
---

# JB SVG

Treat SVG as a small document with geometry, styles, semantics, and behavior. Produce readable source that renders cleanly at every intended size.

## Workflow

1. Inspect the surrounding code and determine how the SVG will be used: standalone file, inline HTML, framework component, CSS background, or `<img>` source. Match the project's syntax and styling conventions.
2. Establish the visual bounds and choose a simple coordinate system. Use `0 0 24 24` for conventional icons when it fits; use dimensions that make the actual geometry easy to reason about for other artwork.
3. Build the large shapes first. Prefer semantic primitives such as `<circle>`, `<rect>`, `<line>`, `<polyline>`, and `<polygon>`. Use `<path>` when the shape requires it.
4. Add styling, reusable definitions, accessibility, and optional motion according to the rules below.
5. Render the result. Inspect it at its smallest and largest intended sizes, then validate the markup. Finish only when the bounds, proportions, clipping, strokes, colors, and accessible name are correct in context.

## Geometry and scaling

- Give every SVG a `viewBox`. It defines the internal coordinate system independently of rendered CSS pixels.
- Keep geometry inside the `viewBox`, including half of every outward stroke. Add intentional breathing room instead of fixing accidental clipping with `overflow="visible"`.
- Preserve the intended aspect ratio. The default `xMidYMid meet` is usually right. Set `preserveAspectRatio` explicitly when cropping, alignment, or stretching is part of the design.
- Let the host control responsive size. Keep intrinsic `width` and `height` when they prevent layout shift, and allow CSS to override them. Avoid hard-coded dimensions in a reusable component unless its API calls for them.
- Align small, axis-bound icons to the rendered pixel grid. Odd-width strokes often need half-unit coordinates; judge the rendered result rather than forcing every coordinate to an integer.
- Prefer a few legible decimal places. Remove precision only after confirming that curves and joins still match.

## Shapes and paths

- Use the simplest element that describes the shape. A `<circle>` remains easier to tune than an exported circular path.
- Keep path commands readable while editing. `M`, `L`, `H`, `V`, `C`, `Q`, `A`, and `Z` cover ordinary work; uppercase commands use absolute coordinates and lowercase commands are relative.
- Use groups for meaningful shared transforms or styles, not as residue from a design-tool export.
- Set `fill="none"` on stroke-only shapes. Choose `stroke-linecap` and `stroke-linejoin` deliberately, especially for icons.
- Use transforms when they reveal repetition or symmetry. Flatten them only when the target tool requires it or the result becomes easier to maintain.

## Styling and reuse

- Use presentation attributes for stable defaults and CSS for states, themes, and animation. CSS overrides presentation attributes.
- Use `currentColor` when an icon should inherit its surrounding text color. Use CSS custom properties when a graphic exposes several themeable colors.
- Put gradients, masks, clip paths, filters, and reusable shapes in `<defs>`. Reference them with `url(#id)` or `<use>`.
- Make every referenced ID unique in the rendered document. In reusable components, namespace IDs or generate stable per-instance IDs so two copies cannot steal each other's gradient, mask, or clip path.
- Size filter regions deliberately. Default filter bounds often crop blurs and shadows.
- Keep standalone files self-contained and add `xmlns="http://www.w3.org/2000/svg"`. Avoid scripts, event handlers, remote assets, and embedded raster data unless the task needs them.

## Accessibility

Choose one treatment based on the SVG's role:

- Decorative inline SVG: set `aria-hidden="true"` and `focusable="false"`.
- Meaningful inline SVG: use `role="img"` and an accessible name, preferably `aria-labelledby` pointing to a unique `<title>` and optional `<desc>`.
- SVG loaded through `<img>`: put the accessible name in the `<img alt="...">`; internal `<title>` content does not replace `alt`.
- Interactive graphic: expose each control through native HTML when possible. If SVG elements must be interactive, supply keyboard behavior, focus handling, roles, names, and an adequate hit area.

Keep visible text as text when users must read, select, translate, or search it. Convert lettering to paths only when exact outlines matter more than those properties.

## Motion

Add motion only when requested or when it communicates state.

- Animate transforms and opacity when they can express the effect.
- Set `transform-origin` explicitly. For element-centered transforms, also set the appropriate `transform-box`, commonly `fill-box`.
- For draw-on animation, measure the path with `getTotalLength()` or normalize it with `pathLength="1"`, then animate `stroke-dashoffset` against a matching `stroke-dasharray`.
- Provide a useful static state and disable non-essential motion under `@media (prefers-reduced-motion: reduce)`.

## Cleanup and verification

- Remove editor metadata, empty elements, hidden leftovers, redundant attributes, and needless wrappers.
- Preserve semantic elements and editability during optimization. Do not convert every shape to a path or collapse everything into one opaque `d` string merely to save bytes.
- Parse standalone files with an XML-aware validator when available. Then render them in the real host, because valid XML can still have broken geometry, CSS, references, or accessibility.
- Check repeated component instances for ID collisions. Check hover, focus, reduced-motion, theme, and responsive states when the SVG uses them.
- If visual inspection is unavailable, say so and report which structural checks were completed.

## Minimal inline icon

```svg
<svg
  viewBox="0 0 24 24"
  width="24"
  height="24"
  fill="none"
  stroke="currentColor"
  stroke-width="2"
  stroke-linecap="round"
  stroke-linejoin="round"
  aria-hidden="true"
  focusable="false"
>
  <path d="M5 12h14M13 6l6 6-6 6" />
</svg>
```

## Source

The coordinate-system, path, CSS, dash animation, `<defs>`, and clipping guidance builds on Carmen Ansio's [SVG from Scratch](https://www.carmenansio.com/articles/svg-from-scratch/). Use the article when a task needs a worked explanation of those fundamentals.
