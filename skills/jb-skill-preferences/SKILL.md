---
name: jb-skill-preferences
description: Manage JB's shared preferred AI skill registry in a GitHub Gist JSON5 file via gh CLI. Use to remember/update shared skill preferences, sync skillsets across machines, or install preferred skills for a topic into a Pi project.
private: true
skill_author: bjesuiter@gmail.com
---

# JB Skill Preferences

## Use when

- remember or update a preferred skill/skillset
- inspect JB's shared skill registry
- install preferred skills for a topic into the current Pi project
- keep AI skill choices synced across machines

## Registry target

Use exactly:
- filename: `jb-skill-preferences.json5`
- description: `JB shared preferred AI skill registry`
- gist: `https://gist.github.com/bjesuiter/98d5768dc360093affb8d8fdb064e45f`
- fallback search page: `https://gist.github.com/bjesuiter`

Treat the filename as canonical. Do not invent alternate filenames.

## Requirements

- `gh` installed and authenticated for gist read/write.
- Registry is JSON5, not JSON.
- Keep top-level `global` and `project` sections.
- Current topics: `global.core`, `global.experimental`, `project.designWork`, `project.devLibs`, `project.openclawDev`, `project.appleDev`.

## Registry shape

```json5
{
  version: 1,
  schema: {
    emptyArrays: "omit",
    wildcardSemantics: "wildcard: true means intentionally install all current and future skills from source",
    defaultSkillsCliArgs: ["-g", "--agent", "codex", "opencode", "pi", "-y"],
    groupedSkillsSemantics: "skills: [...] expands to repeated --skill flags",
  },
  global: {
    topics: {
      core: {
        description: "Always-installed general productivity skills",
        skills: [
          { source: "owner/repo", skill: "example-skill" },
          { source: "owner/repo-with-multiple", skills: ["skill-a", "skill-b"] },
          { source: "owner/all-skills", skill: "*", wildcard: true },
        ],
        notes: "Skills I want available globally",
      },
      experimental: {
        description: "Trial skills and Pi extensions",
        reviewAfter: "YYYY-MM-DD",
        skills: [],
      },
    },
  },
  project: {
    topics: {
      appleDev: {
        description: "Project-local Apple stack skills",
        skills: [{ source: "owner/repo", skill: "example-apple-skill" }],
        piExtensions: ["https://github.com/example/pi-extension"],
        notes: "Install for Apple platform projects",
      },
    },
  },
}
```

Rules:
- `global.topics.*` = globally installed preferences.
- `project.topics.*` = project-local preferences.
- Omit empty arrays (`prompts: []`, `extensions: []`, etc.).
- `description` = short topic summary; `notes` = freeform context.
- `reviewAfter` only for experimental topics; default window is three months.
- `skill: "name"` = one selected skill.
- `skills: ["a", "b"]` = multiple selected skills from the same repo; install with repeated `--skill` flags.
- `skill: "*"` requires `wildcard: true`.
- Do not add `cli: "skills@latest"`; latest is the default.
- Use `piExtensions` for Pi coding-agent-specific install sources; do not put them in generic `packages`.
- Use local absolute paths in `skills`/`extensions` only when explicitly requested.
- Preserve comments and field order when editing existing JSON5.

## Read registry

```bash
command -v gh
gh gist view https://gist.github.com/bjesuiter/98d5768dc360093affb8d8fdb064e45f --filename jb-skill-preferences.json5 --raw
```

If the pinned gist fails, find it by filename/description:

```bash
gh gist list --limit 100 --filter 'jb-skill-preferences\.json5|JB shared preferred AI skill registry'
```

## Create registry if missing

If adding/updating preferences and the registry does not exist, create a secret gist from a temp file using the schema above:

```bash
gh gist create /path/to/jb-skill-preferences.json5 -d 'JB shared preferred AI skill registry'
```

If only inspecting/installing, ask before initializing.

## Update preferences

1. Choose `global` for always-available skills, `project` for per-repo/topic skills; ask if unclear.
2. Choose/confirm the topic key, e.g. `appleDev`, `designWork`, `devLibs`, `openclawDev`, `browser-testing`.
3. Read the latest JSON5 from the gist.
4. Make the smallest update.
5. Deduplicate arrays. Prefer one `{ source, skills: [...] }` over repeated `{ source, skill }` for the same repo.
6. Ensure wildcard entries include `wildcard: true`.
7. Validate JSON5, then write back:

```bash
npx -y json5 -c /path/to/jb-skill-preferences.json5
gh gist edit https://gist.github.com/bjesuiter/98d5768dc360093affb8d8fdb064e45f --filename jb-skill-preferences.json5 /path/to/jb-skill-preferences.json5
```

## Install topic into current project

1. Read the registry.
2. Use `project.topics.<topic>` first.
3. If absent, say so. Only fall back to `global.topics.<topic>` if requested.
4. For skill entries:
   - `skill: "name"` → `--skill name`
   - `skills: ["a", "b"]` → `--skill a --skill b`
   - `skill: "*", wildcard: true` → `--skill '*'`
5. Install project-scope Pi extensions:

```bash
pi install -l <pi-extension-source>
```

6. Merge local `skills`, `prompts`, or `extensions` arrays into `.pi/settings.json` without removing unrelated settings.
7. Avoid duplicates. Warn before writing personal absolute paths into a shared repo.
8. After `.pi/settings.json` changes, tell the user to run `/reload` or restart Pi.

Use `pi install <source>` for global `piExtensions`.

## Example requests

- "Remember that Apple projects should use my ASC and SwiftUI skills."
- "Add my preferred GitHub skills to the shared registry as global preferences."
- "Install my preferred Apple skills into this project."
- "What preferred project skills do I already have for browser testing?"
