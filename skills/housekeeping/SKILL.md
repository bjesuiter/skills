---
name: housekeeping
description: Self-cleaning skill. Check various locations for cleanup opportunities and run cleanup tasks. Use for routine maintenance.
private: true
aliases: [cleanup]
---

# Housekeeping Skill

Self-cleaning and maintenance for the system.

## Usage

When JB wants to clean up:
- "housekeeping"
- "cleanup"
- "self-cleaning"
- "run maintenance"

## Workflow

1. **Check** various locations for cleanup opportunities
2. **Report** brief details (one line per item)
3. **Ask** for confirmation
4. **Execute** specific cleanups or all if not specified

## Things to Check

### 1. nb openloops/~trash
- Count files in trash folder
- One-liner: "openloops/~trash: X file(s) to delete"

### 2. Session Logs (optional)
- Check for old session logs that can be pruned
- One-liner: "session logs: X old sessions"

### 3. Memory Files (optional)
- Check for very old memory files (older than 30 days)
- One-liner: "memory: X old files older than 30 days"

### 4. Temp Files (optional)
- Check for temporary files that can be removed
- One-liner: "temp: X files in /tmp/clawdbot/"

## Output Format

```
Housekeeping Report:

- openloops/~trash: 3 file(s) to delete
- session logs: 5 old sessions (>7 days)
- temp files: 12 files in /tmp/clawdbot/

Run cleanup? [yes/no/specify]
```

## User Interaction

1. **Report findings** with brief one-liners
2. **Ask for confirmation**
3. If user specifies (e.g., "only openloops trash"):
   - Run only that cleanup
4. If user confirms "yes":
   - Run all cleanup tasks

## Cleanup Commands

### OpenLoops Trash
```bash
# List count
ls ~/.nb/openloops/~trash/ | wc -l

# Delete all
rm ~/.nb/openloops/~trash/*

# Commit
cd ~/.nb/openloops && git add -A && git commit -m "housekeeping: clear trash"
```

### Session Logs
```bash
# Find old sessions
find ~/.config/clawdbot-workspaces/jbclawd/.claude/sessions -name "*.json" -mtime +7

# Prune old sessions (keep last 50)
ls -t ~/.config/clawdbot-workspaces/jbclawd/.claude/sessions/*.json | tail -n +51 | xargs rm
```

### Temp Files
```bash
# Find temp files
find /tmp/clawdbot -type f -mtime +1

# Remove old temp files
find /tmp/clawdbot -type f -mtime +1 -delete
```

## Safety

- Always report what will be cleaned
- Always ask for confirmation
- Never delete without asking
- If user specifies only certain cleanups, respect that

## Example

**User:** "housekeeping"

**Response:**
```
Housekeeping Report:

- openloops/~trash: 3 file(s) to delete
- session logs: 5 old sessions (>7 days)

Run cleanup? [yes/no/specify]
```

**User:** "yes"

**Response:**
```
✓ Cleared 3 files from openloops/~trash
✓ Pruned 5 old session logs

Housekeeping complete.
```

## Related

- [[open-loops]] — Track unfinished tasks
- [[desk-reminders]] — Things to do at desk
