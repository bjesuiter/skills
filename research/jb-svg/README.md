# Archived JB SVG research

Archived on 2026-10-06. Use plain SVG for current work. See the [accepted decision](../../docs/adr/0001-use-plain-svg-until-a-roadblock.md) and [human review](evidence/20260823-145049/human-review.md). The lab, including the previously uncommitted Glimpse integration, is retained for research.

This lab measures what an SVG skill changes. It keeps prompts identical, snapshots every candidate, checks the generated markup, renders previews, and can ask a blinded evaluator to compare the results.

Generated runs stay under `runs/` and are ignored by Git. Improvement proposals and promoted examples are kept because they are meant for review and possible commits.

## Start here

```bash
cd research/jb-svg

# Verify local dependencies and list cases
uv run lab.py doctor
uv run lab.py list

# Test the archived skill using a case id from cases/*.json
uv run lab.py test --case icon-button

# Compare jb-svg against a no-skill baseline on every case
uv run lab.py battle

# Compare arbitrary skill files or directories
uv run lab.py battle \
  --candidate jb-svg=../../deprecated-skills/jb-svg \
  --candidate rival=/absolute/path/to/another-skill
```

Every run prints its directory. After a battle, Glimpse opens `runs/<id>/gallery.html` in a native window. Closing that window ends its one-shot Glimpse session. Pass `--no-gallery` in CI or other headless runs. The evaluator result is stored in `runs/<id>/summary.md`.

Reopen a finished run with:

```bash
uv run lab.py gallery runs/<id>
```

The gallery integration needs the [`glimpse-cli`](https://www.npmjs.com/package/glimpse-cli) package on `PATH`:

```bash
npm install --global glimpse-cli
```

The npm install runs the native `glimpseui` build. If Bun installed the package without running dependency scripts, run `npm run build:macos` inside the installed `glimpseui` package once.

`--case` accepts a case `id`, not a free-form prompt. Run `uv run lab.py list` to see the available ids, or add a JSON case as described below.

## Improve the skill

Generate a proposal from an evaluated run:

```bash
uv run lab.py improve runs/<id> --candidate jb-svg
```

The command writes a complete candidate under `proposals/<timestamp>-jb-svg/`. It does not edit `deprecated-skills/jb-svg/SKILL.md`. Review the proposal and its rationale, then apply only changes supported by repeated failures.

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
uv run lab.py battle --model gpt-5.6-sol --reasoning-effort high

# Re-run the blinded judge for an existing run
uv run lab.py evaluate runs/<id> --model gpt-5.6-sol --reasoning-effort high

# Check standalone SVG files without a model
uv run lab.py check path/to/example.svg
```

`battle` uses the same model for every candidate. Candidate names are hidden from the evaluator, and rendered previews are attached in randomized order. The evaluator is still subjective. Treat the gallery, deterministic checks, and score report as separate evidence.

`test`, `battle`, `evaluate`, and `improve` default to `gpt-5.6-sol` with `high` reasoning effort. Use `--model` and `--reasoning-effort` to override either value. New runs record both settings in `manifest.json`.

## Add a case

Add one JSON file under `cases/` with these fields:

- `id`: stable kebab-case identifier
- `title`: short label
- `prompt`: the exact task every candidate receives
- `expect`: deterministic expectations such as `usage`, `currentColor`, or `reducedMotion`

Keep cases independent of `jb-svg` wording. A case should describe the desired artifact and its host context, not the implementation you expect.

## Paused research backlog

[Competitor research intake](docs/competitor-research.md) records the current candidate skills, unverified claims, safety concerns, and the steps for turning that research into a fair future benchmark.
