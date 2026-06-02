# AGENTS.md - Skills Repository

Agent instructions for this multi-skill repository.

## Repo Layout

```text
.
├── AGENTS.md                 # Agent instructions
├── README.md                 # Public overview, install commands, skill list
├── meta/                     # Repo setup notes
├── skills/                   # Canonical public skills
│   └── <skill-name>/
│       ├── SKILL.md          # Required entrypoint
│       ├── references/       # Optional long-form docs/templates/examples
│       ├── scripts/          # Optional helpers
│       └── assets/           # Optional static files
└── .agents/skills/           # Local/private installed copies; not canonical
```

Create and edit public skills only under `skills/<skill-name>/`. Treat `.agents/skills/` as local agent state unless explicitly told otherwise.

## Creating a Skill

1. **Name it**
   - Use kebab-case: `jb-example-tool`.
   - Prefer `jb-` for personal workflow skills.
   - Match folder name and frontmatter `name` exactly.

2. **Create the entrypoint**

   ```text
   skills/<skill-name>/SKILL.md
   ```

   ```markdown
   ---
   name: <skill-name>
   description: Use when <specific trigger/situation>; mentions required CLI/tool if any.
   ---

   # Skill Title

   Use this skill when ...
   ```

3. **Keep `SKILL.md` focused**
   - When to use / not use
   - Prerequisites
   - Core workflow
   - Guardrails and failure modes
   - Expected deliverables

   Put bulky examples, API notes, templates, and helpers in `references/`, `scripts/`, or `assets/`, then link them from `SKILL.md` with relative paths.

4. **Update docs**
   - Add public skills to `README.md`.
   - Update the README skill count.
   - Document required CLIs/tools in the skill.

5. **Validate**
   - Run the validation workflow below before finishing, or state why it was not run.

## Validation Workflow

When importing or modifying skills in this repo, always validate before committing:

### 1. Remove Broken Symlinks

Skills copied from local dev environments may contain symlinks that break outside that context:

```bash
cd /path/to/skills
find -L skills/ -type l -delete
```

This removes any broken symbolic links before validation.

### 2. Run Skills CLI Discovery

Validate all skills are properly structured and discoverable:

```bash
npx skills add . --list
```

**Expected output:**
- Banner with "skills" logo
- "Available Skills" section listing all skills
- Each skill shows name + description
- No errors or missing skills

**What this validates:**
- ✅ YAML frontmatter is correct (`name`, `description`)
- ✅ SKILL.md files are in proper locations
- ✅ Multi-skill repo structure is recognized
- ✅ No broken file references

### 3. Test Installation (Optional)

Test that a skill can actually be installed:

```bash
npx skills add . --skill jb-tdd -a codex -y
```

This ensures the skill installs without errors.

When testing installs from this repo, clean up any skills installed only for testing afterwards. Do not leave test-installed skills in local/global agent skill directories unless the user explicitly wants to keep them.

## Pre-Commit Checklist

Before committing skill changes:

- [ ] Remove broken symlinks: `find -L skills/ -type l -delete`
- [ ] Validate discovery: `npx skills add . --list` (all skills appear)
- [ ] Test one install: `npx skills add . --skill <name> -a codex -y`
- [ ] Clean up skills installed only for install testing
- [ ] Update README.md if skill list changed
- [ ] Commit with descriptive message

## Post-Commit Local Skill Update

When committing one of JB's own workflow skills from this repo, update the installed local machine copy after the commit using the official preference-registry update rules.

Workflow:

1. Commit and push the repo change first.
2. Read the canonical setup workflow from the preference registry Gist:

   ```bash
   gh gist view https://gist.github.com/bjesuiter/98d5768dc360093affb8d8fdb064e45f \
     --filename jb-skill-preferences-setup.md \
     --raw
   ```

3. Follow the setup doc's new-entry/exact-entry install rules for the changed skill, using global scope unless JB specified otherwise.
4. Verify the installed skill reflects the committed change.
5. Do not leave repo-local test installs under `.agents/skills/`.

## Importing Skills from Other Repos

When copying skills from other locations (e.g., jb-home):

```bash
# 1. Copy skills
cp -r /source/path/skills/* skills/

# 2. Clean up symlinks
find -L skills/ -type l -delete

# 3. Validate
npx skills add . --list

# 4. Update README with new skill count/names

# 5. Commit
git add -A
git commit -m "feat: import X skills from Y"
```

## Troubleshooting

**"Skill not appearing in list"**
- Check YAML frontmatter has `name` and `description`
- Verify file is named `SKILL.md` (case-sensitive)
- Ensure skill is in `skills/<name>/SKILL.md` structure

**"Broken reference errors"**
- Look for symlinks: `find skills/ -type l`
- Remove broken ones: `find -L skills/ -type l -delete`

**"Internal skills hidden"**
- Check if skill has `metadata.internal: true`
- Use `INSTALL_INTERNAL_SKILLS=1 npx skills add . --list` to see them

---

**Last validation:** 2026-02-17 (22 skills discovered successfully)
