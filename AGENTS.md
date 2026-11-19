# Skills Repository

See [Maintaining skills](docs/maintaining-skills.md) when importing upstream skills, validating changes, or preparing a release.

## Canonical locations

- Keep JB-maintained skills in `skills/jb/<skill-name>/`.
- Put imported skills in `skills/<owner>-<repo>/<skill-name>/`. Update the source folder's [`vendor.json5`](.agents/skills/update-vendored/references/importing.md) after each import and retain the upstream license and notices.
- Keep a `README.md` in each local vendor directory. Record which skills to include or omit and consult it before refreshing the snapshot.
- Consider [giget](https://github.com/unjs/giget) for downloading upstream snapshots or subdirectories. Pin the import to a commit or release tag and include the upstream license and notices.
- Put drafts in `skills/in-progress/<skill-name>/`. The Skills CLI discovers valid drafts by default. Add `metadata.internal: true` in the frontmatter to opt out of normal discovery.
- Record retired skills in `skills/deprecated/README.md`. Keep this directory for documentation only.
- Keep repository-only workflows in `.agents/skills/` with matching links in `.claude/skills/` for Claude Code. Other entries in `.agents/skills/` are local agent state.

## Private skills

For requests about private skill previews, experiments, or personal workflows, use the separate private repository [bjesuiter/skills-private](https://github.com/bjesuiter/skills-private), cloned at `~/Develop/bjesuiter/skills-private`. Read its `AGENTS.md` before working there. Keep private skill contents and trial artifacts in that repository.

## SVG work

Use plain SVG until a concrete roadblock warrants a minimal custom skill. See [the accepted decision](docs/adr/0001-use-plain-svg-until-a-roadblock.md) before adding or reactivating SVG-specific guidance.

## Skill conventions

- Use kebab-case names; prefer the `jb-` prefix for JB workflow skills.
- The directory and `SKILL.md` frontmatter `name` must match.
- Keep `SKILL.md` concise. Put substantial examples, references, and helpers in sibling directories and link to them.
- When the active-skill set changes, update `README.md` and its count.
- When removing an active skill, also remove its resource entry from the `jb-agent-env` preference registry.

## Skill changes and releases

- Add a Changeset for changes to distributed skills or their layout. See [the release workflow](.changeset/README.md) for bump levels and Git tags.
- When retiring a skill, remove its directory and active references. Record the reason, replacement (if any), and last available revision in [the retirement history](skills/deprecated/README.md).
- Check that the retired name is absent from CLI discovery.

## Before committing skill changes

```bash
find -L skills/ -type l -delete
npx skills add . --list
```

If testing installation, use only the agents configured in `jb-agent-env` (`codex`, `opencode`, and `pi`) and remove test-only local installs afterwards.

## After committing a JB workflow skill

Push first, then read the official preference-registry setup workflow and use its exact-entry install process to update the installed copy (global unless JB says otherwise):

```bash
gh gist view https://gist.github.com/bjesuiter/98d5768dc360093affb8d8fdb064e45f \
  --filename jb-skill-preferences-setup.md \
  --raw
```

Verify the installed copy changed. Do not leave repo-local test installs in `.agents/skills/`.

## Runtime failures

Before diagnosing a reported skill failure deeply, check whether its relevant CLIs, MCP servers, packages, or other dependencies are stale.

## Agent skills

### Issue tracker

Use GitHub Issues in `bjesuiter/skills`. See [the issue tracker instructions](docs/agents/issue-tracker.md).

### Triage labels

Use the five standard [triage labels](docs/agents/triage-labels.md).

### Domain docs

Use the root `GLOSSARY.md` and `docs/adr/` for this single-context repository. See [the domain docs instructions](docs/agents/domain.md).

### Vendored skill updates

For an upstream skill update check or refresh, follow the repo-local [update-vendored skill](.agents/skills/update-vendored/SKILL.md).
