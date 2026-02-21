# AGENTS.md - Skills Repository

Agent-specific instructions for working with this skills repository.

## Validation Workflow

When importing or modifying skills in this repo, always validate before committing:

### 1. Remove Broken Symlinks

Skills copied from local dev environments may contain symlinks that break outside that context:

```bash
cd /path/to/skills
find skills/ -type l -xtype l -delete
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

## Pre-Commit Checklist

Before committing skill changes:

- [ ] Remove broken symlinks: `find skills/ -type l -xtype l -delete`
- [ ] Validate discovery: `npx skills add . --list` (all skills appear)
- [ ] Test one install: `npx skills add . --skill <name> -a codex -y`
- [ ] Update README.md if skill list changed
- [ ] Commit with descriptive message

## Importing Skills from Other Repos

When copying skills from other locations (e.g., jb-home):

```bash
# 1. Copy skills
cp -r /source/path/skills/* skills/

# 2. Clean up symlinks
find skills/ -type l -xtype l -delete

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
- Remove broken ones: `find skills/ -type l -xtype l -delete`

**"Internal skills hidden"**
- Check if skill has `metadata.internal: true`
- Use `INSTALL_INTERNAL_SKILLS=1 npx skills add . --list` to see them

---

**Last validation:** 2026-02-17 (22 skills discovered successfully)
