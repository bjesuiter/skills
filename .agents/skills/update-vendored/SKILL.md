---
name: update-vendored
description: Check this repository's vendored skills for upstream changes and review or refresh them with parallel per-skill reviews.
metadata:
  internal: true
---

# Update Vendored Skills

1. From the repository root, run `bun .agents/skills/update-vendored/scripts/update-vendored.ts --diffs`. If dependencies are missing, run `bun install --frozen-lockfile` first. Read the JSON Lines output, one record per local vendor directory. Process successful records even if another source returns `error` and the command exits nonzero.
2. Use `previous`, `latest`, and `changes` to review each source. An `unchanged` record means its recorded revision matches upstream. A `changed` record with empty `changes` means the revision moved without a diff in the checked skill directories. The script checks existing local imports against `skills/<skill-name>/` upstream. Verify the source path for `removed` or `missing` skill entries before proposing a change. For `unimported`, consult the [import reference](references/importing.md) and the local vendor directory's README to establish the selection.
3. Read the local vendor directory's README for local adaptations and successor mappings. Start one read-only subagent per upstream skill that needs review and run the reviews in parallel up to the available concurrency. Give each subagent the path to [skill-merge](../skill-merge/SKILL.md), the diff, old and incoming revisions, and its local targets. Review the imported copy in vendor mode and any mapped successors in semantic mode. Ask for findings and proposed changes. If delegation is unavailable, run the same reviews in the main agent.
4. Consolidate the findings in the main agent. Reconcile overlapping proposals when successors share instructions. On a check, report findings, proposed changes, and any unverified sources. When asked to refresh, apply the selected changes in the main agent. Use the [import reference](references/importing.md) for the pinned source and its notices, and apply requested successor changes separately from the vendor refresh. Account for the selected imports and successor findings before advancing the snapshot. Keep the prior snapshot while decisions remain open so the diff is available next run. Validate with `bun run check:skills`.

## Feedback

Ask reviewers to return any instruction friction with their findings. Follow [repo-feedback](../repo-feedback/SKILL.md) for concrete problems observed anywhere in the run.
