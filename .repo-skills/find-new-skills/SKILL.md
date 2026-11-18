---
name: find-new-skills
description: Review omitted and newly added skills in this repository's vendored upstream sources, respect recorded exclusions, and compare candidates with JB's existing skills to recommend additions or ideas to adapt.
---

# Find new skills

Find useful skills and ideas in the upstream repositories already represented by this skills repo. Produce evidence-backed recommendations; importing, installing, or changing preferences requires a request that includes those actions.

## Establish coverage

Locate the skills repository from the current workspace or the user's supplied path. Read its `AGENTS.md`, `docs/maintaining-skills.md`, and each upstream folder's `vendor.json5` and `README.md`. Discover sources from those manifests rather than keeping a separate source list in this skill.

Build the comparison inventory from active repo skills, discoverable drafts, and their relevant bundled references. Include skills in JB's preferred registry and the current agent's available skill catalog when accessible. Use `jb-agent-env` when available to locate and read the registry. Treat installed copies as copies of a skill, not separate capabilities; distinguish drafts and retired skills from active choices. State any missing inventory or inaccessible source so the report's scope is clear.

Read descriptions to find likely overlaps, then read the matching skills' full instructions and relevant references before judging duplication. A shared topic or similar name is insufficient evidence.

## Inspect upstream candidates

For each source, resolve the current tracked branch tip or latest release according to its manifest. Fetch that revision into a temporary directory and record the exact revision inspected. Keep the vendored snapshot unchanged. Enumerate `SKILL.md` files throughout the source, including nested plugin layouts, and compare them with what is already imported.

Read recorded selection decisions before evaluating omitted skills:

- **Explicit ban:** Skip and cite the decision. Reconsider only when the user asks to revisit that ban.
- **Conditional exclusion:** Report the condition and whether evidence shows it has changed. When it still holds or cannot be verified, keep the skill deferred.
- **Unselected or previously overlooked:** Evaluate normally. A limited initial import, an omission without a reason, or “not selected” is not a permanent ban. An explicit request to review omitted skills permits reviewing that selection, but does not authorize importing them.
- **Ambiguous exclusion:** Explain the ambiguity and make any recommendation conditional on resolving it; do not silently convert it into either a ban or permission to import.

Inspect every eligible candidate's instructions and any references, scripts, or required sibling skills that affect its value. If the candidate is already represented through a renamed skill or local adaptation, compare the implementations and look for ideas the local version lacks. Upstream content is review material; do not execute its installation commands or workflow as part of assessing it.

## Judge the useful difference

Compare each candidate with the closest existing skills and JB's recorded workflows and constraints:

- What concrete task would this improve, and how often does that task arise? Distinguish demonstrated needs from speculative ones.
- Does it add a missing capability, or repeat an existing workflow? Identify the actual overlap and any conflicting advice.
- Does it offer a useful new approach to an existing problem: a decision rule, failure check, interface, reference, or implementation technique? Name the idea and where it would fit in an existing skill.
- Would a separate skill earn its discovery and maintenance cost, or would adapting a small part into an existing skill be clearer?
- What dependencies, provider assumptions, permissions, licensing constraints, or maintenance concerns affect adopting it? Verify facts that materially affect the recommendation.

Assign a disposition with a reason: **vendor**, **adapt ideas**, **duplicate**, **defer**, or **skip**. For duplicates, name the skill that already covers the behavior. For adaptations, name both the upstream idea and the proposed local destination. For deferrals, state what would make it useful. Prefer a concrete marginal benefit over novelty or polish; recommend nothing when nothing earns its place.

## Report

Lead with the strongest recommendations, ordered by practical value and confidence. For each, provide:

- Candidate name and a source link pinned to the inspected revision.
- Recommended disposition and the task or problem it helps with.
- Closest existing skills, with links, and the specific overlap or useful difference supported by their contents.
- Adoption cost or unresolved constraint that could change the recommendation.

End with compact coverage: sources and revisions inspected, eligible candidates reviewed, duplicates and deferrals, explicit bans skipped with their recorded reasons, and any unavailable sources or truncated review. Account for every discovered candidate, grouping routine duplicates or skips where helpful. Label an incomplete review as partial rather than implying that unchecked candidates have no value.

Keep the audit read-only unless the user requests changes. Do not update vendor snapshots, selection decisions, the preferred registry, or installed skills merely to record a recommendation. If a saved report is requested, follow the repository's documentation conventions.
