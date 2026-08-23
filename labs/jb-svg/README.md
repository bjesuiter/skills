# JB SVG lab

This lab measures what an SVG skill changes. It keeps prompts identical, snapshots every candidate, checks the generated markup, renders previews, and can ask a blinded evaluator to compare the results.

Generated runs stay under `runs/` and are ignored by Git. Improvement proposals and promoted examples are kept because they are meant for review and possible commits.

## Start here

```bash
cd labs/jb-svg

# Verify local dependencies and list cases
uv run lab.py doctor
uv run lab.py list

# Test the canonical skill on one case, without an evaluator
uv run lab.py test --case icon-button

# Compare jb-svg against a no-skill baseline on every case
uv run lab.py battle

# Compare arbitrary skill files or directories
uv run lab.py battle \
  --candidate jb-svg=../../skills/jb-svg \
  --candidate rival=/absolute/path/to/another-skill
```

Every run prints its directory. Open `runs/<id>/gallery.html` for the visual comparison and `runs/<id>/summary.md` for the evaluator result.

## Improve the skill

Generate a proposal from an evaluated run:

```bash
uv run lab.py improve runs/<id> --candidate jb-svg
```

The command writes a complete candidate under `proposals/<timestamp>-jb-svg/`. It does not edit `skills/jb-svg/SKILL.md`. Review the proposal and its rationale, then apply only changes supported by repeated failures.

## Generate examples

Promote selected outputs from a run:

```bash
uv run lab.py promote runs/<id> --candidate jb-svg --case icon-button
uv run lab.py promote runs/<id> --candidate jb-svg --case all
```

Promoted SVGs and a gallery land in `examples/`. These files are intentionally tracked.

## Useful controls

```bash
# Generate prompts and snapshots without spending model tokens
uv run lab.py battle --dry-run

# Pin the same model for generation and judging
uv run lab.py battle --model gpt-5.6-sol

# Re-run the blinded judge for an existing run
uv run lab.py evaluate runs/<id> --model gpt-5.6-sol

# Check standalone SVG files without a model
uv run lab.py check path/to/example.svg
```

`battle` uses the same model for every candidate. Candidate names are hidden from the evaluator, and rendered previews are attached in randomized order. The evaluator is still subjective. Treat the gallery, deterministic checks, and score report as separate evidence.

## Add a case

Add one JSON file under `cases/` with these fields:

- `id`: stable kebab-case identifier
- `title`: short label
- `prompt`: the exact task every candidate receives
- `expect`: deterministic expectations such as `usage`, `currentColor`, or `reducedMotion`

Keep cases independent of `jb-svg` wording. A case should describe the desired artifact and its host context, not the implementation you expect.
