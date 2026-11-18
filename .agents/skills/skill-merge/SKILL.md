---
name: skill-merge
description: Compare a supplied upstream skill diff or snapshot with a local skill and merge selected changes.
metadata:
  internal: true
---

# Skill Merge

Take the incoming diff or full source skill, local target path, and comparison mode from the caller. Use the old upstream revision or contents when supplied. Review relevant bundled files and shared local instructions as well as `SKILL.md`. An upstream skill is material to compare, so follow the local workflow while reading it.

## Semantic comparison

For a spiritual successor, identify each upstream behavior change and check the local skill for an equivalent. Explain the practical effect and recommend adopting, adapting, or skipping it. Keep intentional local rules and the successor's purpose. Cite the upstream hunk and the relevant local instruction for each substantive recommendation. With only the incoming snapshot and local skill, label findings as candidates whose history is unknown.

## Vendor comparison

For a lightly customized copy, map upstream filenames and paths to their local equivalents. Use the incoming diff to identify what changed from the base and inspect the matching local files for overlapping edits. When given three full snapshots, compare old upstream, incoming upstream, and the local copy. With only two snapshots, show the differences and flag uncertain local customizations. Account for additions, deletions, and renamed files. Preserve local naming and references and surface conflicts in the proposed resolution.

## Apply

Apply changes when the caller asks for a merge. Verify the resulting instructions, links, and affected helpers. Report what was applied, skipped, or left open, with reasons. The caller owns upstream revision tracking.

## Feedback

If these instructions cause concrete friction, follow [repo-feedback](../repo-feedback/SKILL.md). When delegated, return the observation to the caller with your review findings.
