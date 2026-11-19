---
"jb-skills": minor
---

Add the discoverable finish-t3 draft in skills/in-progress to check thread OpenLoops and worktree preservation before cleanup and archiving. Its optional deep-check inspects unique ignored files for non-reproducible data; the skill performs no merge.

Include a read-only deep-check script that applies Git ignore rules and compares files against the main checkout, producing JSON findings for preservation review.

Load the detailed deep-check procedure only when that mode is requested.
