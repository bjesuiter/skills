---
name: jb-skill-prefs
description: Use when adding, updating, removing, inspecting, or installing JB preferred skills from the shared Gist registry.
private: true
skill_author: bjesuiter@gmail.com
---

# JB Skill Prefs

This local skill is the **registry editor and resource locator**.

The portable **install/bootstrap/update workflow** lives in the Gist setup document. Do not duplicate that full workflow here.

## Use when

- add a new preferred skill or skillset to JB's registry
- update, remove, or inspect registry entries
- find the canonical registry/setup resources
- after editing the registry, install exactly the newly added entry if JB asks

## Canonical resources

Use exactly:

- Gist: `https://gist.github.com/bjesuiter/98d5768dc360093affb8d8fdb064e45f`
- registry filename: `jb-skill-preferences.json5`
- setup/install workflow filename: `jb-skill-preferences-setup.md`
- registry description: `JB shared preferred AI skill registry`
- fallback search page: `https://gist.github.com/bjesuiter`

Treat filenames as canonical. Do not invent alternates.

## Requirements

- `gh` installed and authenticated for gist read/write.
- Registry is JSON5, not JSON.
- Preserve top-level `global` and `project` sections.
- Preserve comments and field order when editing existing JSON5.

## Read resources

Read the registry:

```bash
gh gist view https://gist.github.com/bjesuiter/98d5768dc360093affb8d8fdb064e45f \
  --filename jb-skill-preferences.json5 \
  --raw
```

Read the install/update workflow:

```bash
gh gist view https://gist.github.com/bjesuiter/98d5768dc360093affb8d8fdb064e45f \
  --filename jb-skill-preferences-setup.md \
  --raw
```

If the pinned gist fails, find it by filename/description:

```bash
gh gist list --limit 100 --filter 'jb-skill-preferences\.json5|JB shared preferred AI skill registry'
```

## Registry editing workflow

1. Decide whether the entry belongs under `global` or `project`:
   - `global` = always-available/local-machine preferences.
   - `project` = per-repo/topic preferences.
   - Ask if unclear.
2. Choose or confirm the topic key, e.g. `core`, `experimental`, `appleDev`, `designWork`, `devLibs`, `openclawDev`, `browser-testing`.
3. Read the latest `jb-skill-preferences.json5` from the Gist.
4. Make the smallest possible update.
5. Deduplicate arrays. Prefer one `{ source, skills: [...] }` over repeated `{ source, skill }` entries for the same repo.
6. Validate JSON5.
7. Write the updated registry back to the Gist.

```bash
npx -y json5 -c /path/to/jb-skill-preferences.json5
gh gist edit https://gist.github.com/bjesuiter/98d5768dc360093affb8d8fdb064e45f \
  --filename jb-skill-preferences.json5 \
  /path/to/jb-skill-preferences.json5
```

## Entry rules

- `global.topics.*` = globally installed preferences.
- `project.topics.*` = project-local preferences.
- Omit empty arrays (`prompts: []`, `extensions: []`, etc.).
- `description` = short topic summary.
- `notes` = freeform context.
- `reviewAfter` only for experimental topics; default window is three months.
- `skill: "name"` = one selected skill.
- `skills: ["a", "b"]` = multiple selected skills from the same repo.
- `skill: "*"` requires `wildcard: true`.
- Do not add `cli: "skills@latest"`; latest is the default.
- Use `piExtensions` for Pi coding-agent-specific install sources; do not put them in generic `packages`.
- Use local absolute paths only when explicitly requested.

## Create registry if missing

If adding/updating preferences and the registry does not exist, create a secret gist from a temp file using the established schema:

```bash
gh gist create /path/to/jb-skill-preferences.json5 -d 'JB shared preferred AI skill registry'
```

If only inspecting or installing, ask before initializing.

## Installing after editing

If JB asks to install after adding a registry entry:

1. Read `jb-skill-preferences-setup.md` from the Gist.
2. Follow its **New-entry workflow: install exactly the skill just added** section.
3. Install exactly the newly added/changed entry, not the whole topic or registry, unless JB explicitly asks for that.

For full machine bootstrap/update, always defer to `jb-skill-preferences-setup.md`.

## Critical guardrails

- This local skill manages the registry; the Gist setup md manages installs/updates.
- Do not run full ensure/update mode when JB only asks to install a newly added skill.
- Never prune locally installed skills without explicit confirmation.
- Keep `global` and `project` semantics separate.

## Example requests

- "Remember that Apple projects should use my ASC and SwiftUI skills."
- "Add my preferred GitHub skills to the shared registry as global preferences."
- "Install the skill I just added to the registry."
- "What preferred project skills do I already have for browser testing?"
