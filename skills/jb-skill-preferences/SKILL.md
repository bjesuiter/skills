---
name: jb-skill-preferences
description: Manage JB's shared preferred AI skill registry in a dedicated GitHub Gist JSON5 file via gh CLI, and install topic-based preferred skills into the current Pi project. Use when the user wants to remember preferred skills, update shared skill preferences, sync skillsets across machines, or install preferred skills for a topic into a project.
private: true
skill_author: bjesuiter@gmail.com
---

# JB Skill Preferences

Author: bjesuiter

## When to use

Use this skill when the user wants to:
- remember a preferred skill or skillset for later
- update or review JB's shared preferred skill registry
- install preferred skills for a topic into the current Pi project
- keep preferred AI skill choices synced across machines

## Hardcoded registry target

Use this exact GitHub Gist registry target:
- filename: `jb-skill-preferences.json5`
- description: `JB shared preferred AI skill registry`
- bootstrap gist page: `https://gist.github.com/bjesuiter`
- exact gist URL: `https://gist.github.com/bjesuiter/98d5768dc360093affb8d8fdb064e45f`

Treat the filename as canonical. Do not invent alternate filenames.

## Requirements

- `gh` CLI must be installed.
- `gh` must be authenticated for read/write gist operations.
- The registry format is JSON5, not plain JSON.
- The registry must always have dedicated top-level `global` and `project` sections.
- Current topic keys are `global.topics.core`, `global.topics.experimental`, `project.topics.designWork`, `project.topics.devLibs`, `project.topics.openclawDev`, and `project.topics.appleDev`.

## Registry shape

Use this structure:

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
    },
  },
  project: {
    topics: {
      appleDev: {
        description: "Project-local Apple stack skills such as ASC, Xcode, SwiftUI",
        skills: [
          { source: "owner/repo", skill: "example-apple-skill" },
        ],
        piExtensions: [
          "https://github.com/example/pi-extension",
        ],
        notes: "Install for Apple platform projects",
      },
    },
  },
}
```

Guidance:
- `global.topics.*` stores preferences the user wants installed globally.
- `project.topics.*` stores preferences the user wants installed into project-local Pi config.
- Prefer portable `packages` entries for generic package-based resources.
- Use `piExtensions` for Pi coding-agent-specific install sources that should be installed with `pi install`.
- Use local absolute paths in `skills` or `extensions` only when the user explicitly wants machine-local resources.
- Omit properties whose value would only be an empty array, for example omit `prompts` instead of writing `prompts: []`.
- Use `description` for a short topic summary and `notes` for longer freeform context.
- Use `reviewAfter` on experimental topics. Default window: three months.
- Use `skill: "name"` for one selected skill from a repo.
- Use `skills: ["a", "b"]` for multiple selected skills from the same repo; the skills CLI supports this via repeated `--skill` flags.
- Add `wildcard: true` whenever `skill: "*"` is intentional.
- Do not add `cli: "skills@latest"`; latest is the default for the skills CLI.
- Preserve comments and field order when editing existing JSON5.

## Resolve the registry gist

1. Verify `gh` exists:

```bash
command -v gh
```

2. Find the gist by filename/description:

```bash
gh gist list --limit 100 --filter 'jb-skill-preferences\.json5|JB shared preferred AI skill registry'
```

3. If multiple gists match, prefer the one containing the exact file `jb-skill-preferences.json5`.

4. Read the registry file:

```bash
gh gist view <gist-id-or-url> --filename jb-skill-preferences.json5 --raw
```

## If the registry does not exist

- If the user asked to add, remember, or update preferred skills, create the gist.
- If the user only asked to install or inspect preferred skills, explain that the registry does not exist yet and ask whether to initialize it.

Create it from a local temp file using the schema above:

```bash
gh gist create /path/to/jb-skill-preferences.json5 -d 'JB shared preferred AI skill registry'
```

Default to a secret gist unless the user explicitly asks for a public one.

## Updating preferred skills

When the user wants to remember or update a preference:

1. Decide whether the entry belongs under `global` or `project`.
   - If the user says they always want it available across repos, use `global`.
   - If the user says it should be installed per repo/topic, use `project`.
   - If unclear, ask.
2. Choose or confirm the topic key, for example `appleDev`, `designWork`, `devLibs`, `openclawDev`, `browser-testing`.
3. Read the current JSON5 from the gist.
4. Make the smallest possible update.
5. Write the updated file back:

```bash
gh gist edit <gist-id-or-url> --filename jb-skill-preferences.json5 /path/to/jb-skill-preferences.json5
```

Keep arrays deduplicated. Prefer one `{ source, skills: [...] }` entry over repeated `{ source, skill }` entries for the same repo. If an entry uses `skill: "*"`, include `wildcard: true` to document that broad install as intentional.

## Installing preferred skills into the current project

When the user asks to install preferred skills for a topic into the current project:

1. Read the registry gist.
2. Look up `project.topics.<topic>` first.
3. If there is no project entry for the topic, mention that clearly. Only fall back to `global.topics.<topic>` if the user wants that behavior.
4. Install generic package sources with the package manager appropriate for that package.
   - For `skill: "name"`: pass `--skill name`.
   - For `skills: ["a", "b"]`: pass repeated flags, `--skill a --skill b`.
   - For `skill: "*", wildcard: true`: pass `--skill '*'`.
5. Install `piExtensions` with project scope:

```bash
pi install -l <pi-extension-source>
```

6. For local resource arrays like `skills`, `prompts`, or `extensions`, merge them into `.pi/settings.json` without removing unrelated settings.
7. Avoid duplicate entries.
8. If writing personal absolute paths into a shared repo, warn first.
9. After changing `.pi/settings.json`, tell the user to run `/reload` or restart Pi.

## Notes for Pi project setup

When editing `.pi/settings.json`, preserve existing keys and merge arrays carefully. A valid example:

```json
{
  "skills": ["~/.pi/skill-library/apple"],
  "extensions": [],
  "prompts": []
}
```

Use `pi install -l` for project-scope `piExtensions`; use `pi install <source>` for global `piExtensions`. Do not store Pi coding-agent-specific extension sources in generic `packages`; keep them under `piExtensions`.

## Example requests

- "Remember that Apple projects should use my ASC and SwiftUI skills."
- "Add my preferred GitHub skills to the shared registry as global preferences."
- "Install my preferred Apple skills into this project."
- "What preferred project skills do I already have for browser testing?"
