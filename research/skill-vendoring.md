# Owning selected upstream skills

Researched: 2026-10-06. Scope: whether JB should copy favorite skills into this repository, customize them, and retire the preference registry. These sources address dependency ownership and skill authoring; the recommendation below applies them to this repository rather than claiming a measured comparison of registry versus copied skills.

## What the sources actually argue

- Russ Cox supports copying a small needed part of a dependency when the broader dependency carries unnecessary risk. The copied part becomes your maintenance responsibility, and copyright notices stay with it. The same essay argues against postponing upgrades indefinitely: accumulated changes make later upgrades harder, and you can rediscover bugs upstream already fixed. Even ordinary dependency upgrades deserve review. This supports selective ownership, not copying everything or blindly trusting updates. [Our Software Dependency Problem](https://research.swtch.com/deps)
- Anthropic explicitly favors concise skills that add information the model needs. Only skill metadata loads initially; the main instructions and references load when relevant. Shortening an unused reference has different implications from shortening an often-loaded instruction file. Their evaluation advice is to identify actual failures, create three representative scenarios, and write only enough instructions to address those failures. Removing words alone does not demonstrate improved behavior. [Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- Anthropic's Prithvi Rajasekaran describes trying to radically simplify an agent workflow and losing the earlier performance. It became difficult to identify which parts mattered. He switched to removing one component at a time and measuring the effect. His broader point is that instructions can encode assumptions about model weaknesses that become stale as models improve. This supports repeated pruning with behavior checks rather than one aggressive rewrite. [Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps)
- Chromium's maintainers prefer trackable upstream revisions when actively consuming upstream work. They document copied snapshots with source URLs and revisions, discourage reformatting because it obscures upstream diffs, and distinguish ordinary updates from a hard fork that is no longer updatable. A hard fork is treated as their own code. This is a useful contrast to wholesale rewriting: customization buys freedom but makes upstream comparison harder. [Adding third_party libraries](https://chromium.googlesource.com/chromium/src/+/main/docs/adding_to_third_party.md)
- Bioconductor's AI skill maintainers chose faithful summaries of upstream policy over local corrections. A drifted summary could produce incorrect package submission decisions. They record source revisions and map upstream chapters to derived files so refreshes are scoped. They rejected patch files as premature machinery that breaks on harmless upstream rewording. Local additions must be marked and dated. Their choice fits skills conveying someone else's rules; personal writing and workflow preferences have a different owner. [Mirror upstream Bioconductor policy rather than fork it](https://bioconductor.github.io/ai-agent-skills/docs/adr/0003-mirror-upstream-bioconductor-policy.html)
- Git supports selecting individual upstream commits and recording their origin with `cherry-pick -x`. Applying commits can conflict. This is a provenance aid when source history and paths remain compatible, not a general updater for a rewritten skill copied out of another repository. [git-cherry-pick documentation](https://git-scm.com/docs/git-cherry-pick)

## Pros for JB

These are implications of the sources above, not measured outcomes.

- You can align triggers, required tools, permissions, wording, and workflow decisions with how you actually work.
- A reviewed commit records your effective instructions together, making rollback and diagnosis easier.
- Upstream changes cannot silently replace a deliberate customization if your repository owns the installed copy.
- Small instruction-only skills are comparatively cheap to own when their useful content is stable.
- You can remove duplicated instructions and references that never improve your tasks.
- One canonical collection can reduce confusion about which variant is active, provided installation still has a single source of truth.

## Cons for JB

- You take over deciding whether fixes, compatibility changes, new examples, and changed best practices matter.
- Extensive shortening or restructuring makes an upstream text diff noisy. Useful ideas may need manual translation rather than a clean merge.
- Tool and API skills can stale faster than taste or review preferences. Copying Markdown does not copy responsibility for maintaining the CLI, package, or service it describes.
- Removing a detail that looks redundant may remove the instruction that prevented a specific failure. Keep a few real example tasks for each important adaptation.
- Helper scripts, templates, linked references, and dependencies can make a skill much larger than its main file suggests.
- Copies still need clear source and license records. A renamed skill should not erase where its content originated.
- Retiring a registry does not remove installation and selection needs. Profiles, scopes, and non-skill resources require a replacement or a reduced registry.

## Working recommendation

Own a curated subset and assign each skill an explicit maintenance policy. Start with the skills you often customize and can explain from experience. Treat stable personal workflows as JB-owned adaptations. Keep rapidly changing technical guidance close to its upstream source; keep summaries of external policy faithful to that policy.

For each copied skill, keep a small provenance file beside `SKILL.md`: upstream URL, exact source path, imported revision, license, last-reviewed upstream revision, meaningful local changes, and whether updates are mirrored, reviewed selectively, or intentionally discontinued. Keep this outside the instruction body so provenance does not consume context on every invocation.

Do not require every upstream change to become a local patch. Review changes since the last reviewed revision, record skipped changes, and port useful fixes. Keep three representative tasks for frequently used skills and compare behavior before accepting large cuts. Preserve scripts and uncommon detail as linked resources when they are still useful.

A repository can own the skill content while a smaller manifest continues to handle deployment. Replacing both content ownership and installation at once would combine two separate decisions.
