---
"jb-skills": minor
---

Add local-first branch preparation and integration. Use `prepare-merge` to
prepare locally and `integrate` to merge locally and push. If fetching the
target fails, integration can finish locally with the push pending.

Use `prepare-merge pr` for GitHub PR handoff and `integrate pr` for a GitHub
merge. Install both skills for integration. Shared preparation now lives in
`prepare-merge`, which also works independently.
