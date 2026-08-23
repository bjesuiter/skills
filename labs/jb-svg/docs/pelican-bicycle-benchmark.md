# Pelican bicycle benchmark source

Status: verified against the original author's repository and announcement.

## Canonical prompt

Simon Willison's `pelican-bicycle` repository gives the prompt as:

> `Generate an SVG of a pelican riding a bicycle`

The earliest commit in that repository already passes this exact string to each model. Willison's announcement on 25 October 2024 prints the same prompt and describes the exercise as his own LLM benchmark.

Primary sources:

- [README in `simonw/pelican-bicycle`](https://github.com/simonw/pelican-bicycle/blob/main/README.md#pelicans-on-a-bicycle)
- [Prompt in the initial script commit](https://github.com/simonw/pelican-bicycle/blob/f44768a3b5c280b25763b66af3166d2ca299b185/generate-svgs.sh#L35)
- [Willison's original announcement](https://simonwillison.net/2024/Oct/25/pelicans-on-a-bicycle/)

This wording is the source prompt, not an inferred reconstruction. Later variants such as "Draw a pelican riding a bicycle" are adaptations.

## Recommended lab prompt

Use the canonical sentence unchanged:

> `Generate an SVG of a pelican riding a bicycle`

Keeping it short preserves the benchmark's composition challenge and makes results comparable with Willison's corpus. Do not add visual techniques, a style, dimensions, or required anatomy to the prompt.

If the lab later gains a visual rubric, keep it separate from the prompt. Hugging Face's `pelican_bicycle` OpenEnv scorer checks for a pelican with a long beak and throat pouch, a bicycle with two similar wheels, a connecting frame and handlebars, and a plausible riding posture. Those checks are a later evaluation design, not part of Willison's original prompt.

Reference for the derivative rubric: [Hugging Face OpenEnv `pelican_svg`](https://huggingface.co/docs/openenv/environments/pelican_svg)
