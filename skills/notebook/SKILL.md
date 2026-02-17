---
name: Notebook
description: Local-first personal knowledge base for tracking ideas, projects, tasks, habits, and any object type you define. YAML-based with no cloud lock-in.
private: true
---

# Notebook Skill

Purpose: Track any object type you define such as ideas, projects, tasks, habits, books, and people.

**All operations use the `nb` CLI** — nb handles git commits, indexing, and file management automatically.

## Setup Workflow (First Time)

When no object types exist, guide JB through setup:

1. **Suggest a first type:**
   ```
   It looks like you have not defined any object types yet.
   Notebook works best when you define the types of things you want to track.

   What would you like to start with?
   1. Ideas for capturing thoughts and features
   2. Projects for long term work with goals
   3. Tasks for actionable items with due dates
   4. Something custom — tell me what you want to track
   ```

2. **Define the type:**
   - Preset choice: create with useful default fields
   - Custom: ask what to track and translate into fields
   ```bash
   nb notebook: type-add <typename> title:text status:select(raw|expanded|archived) priority:select(high|medium|low) tags:text notes:longtext
   ```

3. **Add first object:**
   ```bash
   nb notebook: add <typename> "Title" -t tag1,tag2 -p high
   ```

4. **Show workflow:**
   ```
   You now have:
   - Type: <typename> with N fields
   - 1 <typename> object: Title

   What would you like to do next?
   - nb notebook: list <typename> to see all items
   - nb notebook: expand <typename> title to add details
   - nb notebook: add <typename> to add another
   ```

## Quick Reference

### Defining Types

```bash
nb notebook: type-add <typename> <field1>:text <field2>:select(a|b|c) <field3>:number
```

Field types:
- `text` for short strings
- `longtext` for multi-line notes
- `select(a|b|c)` for one option from a list
- `number` for numeric values
- `date` for dates
- `list` for an array of strings

### Working with Objects

```bash
nb notebook: add <typename> "Title" [-t tag1,tag2 -p priority]
nb notebook: list <typename>
nb notebook: show <typename> <title>
nb notebook: expand <typename> <title>
nb notebook: edit <typename> <title> <field>:<value>
nb notebook: link <typename1>:<title1> <typename2>:<title2>
nb notebook: delete <typename> <title>
nb notebook: find "<query>"
nb notebook: stats
```

## nb Commands by Task

| Task | Command |
|------|---------|
| List all types | `nb notebook: list` |
| Add new type | `nb notebook: type-add <name> <fields>` |
| Add object | `nb notebook: add <type> "Title" [-t tags -p priority]` |
| List objects | `nb notebook: list <type>` |
| View object | `nb notebook: show <type> <title>` |
| Edit field | `nb notebook: edit <type> <title> <field>:<value>` |
| Expand/details | `nb notebook: expand <type> <title>` |
| Link objects | `nb notebook: link <type1>:<title1> <type2>:<title2>` |
| Delete object | `nb notebook: delete <type> <title>` |
| Search | `nb notebook: find "query"` |
| Stats | `nb notebook: stats` |

## Example Workflow

```bash
# 1. Define a type
nb notebook: type-add idea title:text status:select(raw|expanded|archived) priority:select(high|medium|low) tags:text notes:longtext

# 2. Add your first idea
nb notebook: add idea "Voice capture while driving" -t voice,automation -p high

# 3. Deepen it
nb notebook: expand idea "voice capture"

# 4. Link to other objects
nb notebook: add project "Home automation" -t household
nb notebook: link idea:"voice capture" project:"home automation"

# 5. Update as you work
nb notebook: edit idea "voice capture" status:expanded

# 6. View all ideas
nb notebook: list idea

# 7. Search
nb notebook: find "voice"
```

## Data Location

All data is stored in `~/.nb/notebook/` with git versioning handled by nb automatically.
