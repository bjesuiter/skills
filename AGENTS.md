# Skills Repository

## Canonical locations

- Public, installable skills belong in `skills/<skill-name>/`.
- `deprecated-skills/` is historical reference only and must not be made discoverable.
- `.agents/skills/` is local agent state, never a canonical source.

## Skill conventions

- Use kebab-case names; prefer the `jb-` prefix for JB workflow skills.
- The directory and `SKILL.md` frontmatter `name` must match.
- Keep `SKILL.md` concise. Put substantial examples, references, and helpers in sibling directories and link to them.
- When the active-skill set changes, update `README.md` and its count.

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
