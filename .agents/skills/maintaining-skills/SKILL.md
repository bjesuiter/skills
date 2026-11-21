---
name: maintaining-skills
description: Maintain this skills repository when tracking upstream sources, importing or refreshing skills, validating changes, retiring skills, or preparing a release.
metadata:
  internal: true
---

# Maintaining skills

## Repository layout

- Keep JB-maintained skills in [skills/jb](../../../skills/jb/).
- Keep imported skills under `skills/<owner>-<repo>/`, one directory per upstream repository.
- Keep drafts under [skills/in-progress](../../../skills/in-progress/). The Skills CLI includes drafts in `--list` and `--all` unless their frontmatter sets `metadata.internal: true`.

## Upstream skills

For a first import, follow the [import reference](../update-vendored/references/importing.md). To check or refresh an existing import, use [update-vendored](../update-vendored/SKILL.md).

### Skill sources

Record upstream repositories worth exploring here. For vendored sources, follow the local README for skill selection and the vendor manifest for the pinned revision.

- [Warp common-skills](https://github.com/warpdotdev/common-skills/tree/main)
- [tstack](https://github.com/t3dotgg/tstack) · [Local vendor notes](../../../skills/t3dotgg-tstack/README.md)
- [HumanLayer skills](https://github.com/humanlayer/skills) · [Local vendor notes](../../../skills/humanlayer-skills/README.md)

## Validate changes

From the repository root, run `bun run check:skills` and confirm the expected skills are listed. To test installation, use a disposable project and an agent listed in [AGENTS.md](../../../AGENTS.md).

```bash
npx skills add /absolute/path/to/skills --skill jb-beans -a codex -y
```

## Retire a skill

Follow the retirement instructions in [AGENTS.md](../../../AGENTS.md) and verify that the retired name is absent from CLI discovery.

## Prepare a release

Follow the [Changesets release workflow](../../../.changeset/README.md). Consult the [decision records](../../../docs/adr/README.md) when a change touches an existing repository decision.
