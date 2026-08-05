---
name: jb-agent-env
description: Manage JB's preferred agent environment from the shared Gist registry, including Markdown skills, Pi extensions, and CLIs. Use when adding, tagging, installing, updating, removing, or inspecting those resources.
private: true
skill_author: bjesuiter@gmail.com
---

# JB Agent Environment

This local skill is the **agent-environment registry editor and resource locator**.

The portable **install/bootstrap/update workflow** lives in the Gist setup document. Do not duplicate that full workflow here.

## Use when

- add a new preferred agent-environment resource to JB's registry
- update, remove, tag, or inspect registry resources
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
- Version 2+ uses top-level `resources` as the canonical flat registry.
- Preserve legacy top-level `global` and `project` compatibility views until the documented breaking removal.
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

1. Read the latest `jb-skill-preferences.json5` from the Gist.
2. Add or update exactly one top-level `resources` entry per installable skill, Pi extension, or CLI.
3. Set independent dimensions explicitly:
   - `kind`: `skill`, `piExtension`, or `cli`
   - `scope`: `global` or `project`
   - `lifecycle`: `stable` or `experimental`
   - `tags`: zero or more intended-use labels such as `devMachine`, `openclaw`, `appleDev`, or `webDev`
   - `installer`: the explicit command mechanism
4. Deduplicate identical resources by merging their tags; never copy an entry merely because it has another use case.
5. Keep legacy `global` and `project` views unchanged; they are compatibility-only and must not receive new entries.
6. Validate JSON5.
7. Write the updated registry back to the Gist.

```bash
npx -y json5 --validate /path/to/jb-skill-preferences.json5
gh gist edit https://gist.github.com/bjesuiter/98d5768dc360093affb8d8fdb064e45f \
  --filename jb-skill-preferences.json5 \
  /path/to/jb-skill-preferences.json5
```

## Entry rules

- `resources` is canonical; topic trees are deprecated compatibility views.
- Use one resource per selected skill or extension so tags remain independently editable.
- `scope` controls installation locality only; `tags` never imply an installer or scope.
- `lifecycle: "experimental"` entries require `reviewAfter`; stable entries do not.
- `skill: "name"` selects one skill; `skill: "*"` requires `wildcard: true`.
- A source-only skill install uses `installer: { type: "skillsCli", selection: "source" }` and omits `skill`.
- `kind: "piExtension"` requires `installer: { type: "pi" }`.
- `kind: "cli"` requires an explicit `installer.command`; do not infer it from the source.
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
- Keep `kind`, `scope`, `lifecycle`, and `tags` separate; tags are never categories.

## Example requests

- "Remember that Apple projects should use my ASC and SwiftUI skills."
- "Tag this skill for both devMachine and openclaw use."
- "Install the resource I just added to the registry."
- "What preferred resources are tagged openclaw?"
