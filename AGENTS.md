# Skills Repository

## Canonical locations

- Keep JB-maintained skills in `skills/jb/<skill-name>/`.
- Put imported skills maintained here in `skills/vendored/<skill-name>/`. Record the upstream source and revision and retain its license and notices.
- Put drafts in `skills/in-progress/<skill-name>/`. The Skills CLI discovers valid drafts by default. Add `metadata.internal: true` in the frontmatter to opt out of normal discovery.
- Record retired skills in `skills/deprecated/README.md`. Keep this directory for documentation only.
- `.agents/skills/` is local agent state, never a canonical source.

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
