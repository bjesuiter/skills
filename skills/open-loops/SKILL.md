---
name: open-loops
description: Find and report unfinished tasks, pending items, and open loops across sessions, memory, and notebooks. Use when JB asks about open tasks, what's pending, or to check for loose ends.
private: true
---

# Open Loops Skill

Track unfinished things across all available sources.

## Sources to Check

### 1. Current Session
Review the conversation for:
- Unanswered questions from JB
- Tasks mentioned but not completed
- Things that failed and weren't retried
- Promises made but not fulfilled

### 2. Background Agent Sessions
```bash
# List active sessions
```
Use `sessions_list` tool with `activeMinutes` to find recent sessions, then check their status.

### 3. Today's Memory
```bash
cat ~/.config/clawdbot-workspaces/jbclawd/memory/$(date +%Y-%m-%d).md
```
Look for:
- Items marked with `[ ]` (unchecked)
- Things noted as "TODO" or "pending"
- Unresolved issues

### 4. Long-term Memory
```bash
cat ~/.config/clawdbot-workspaces/jbclawd/MEMORY.md
```
Check for ongoing projects or commitments.

### 5. Agents Notebook
```bash
nb agents: list -a
# or search for open items
nb agents: search "TODO"
nb agents: search "pending"
nb agents: search "[ ]"
```

## Output Format

When reporting open loops, categorize by urgency:

```markdown
## 🔴 Blocked / Waiting
- [item] — waiting on [what]

## 🟡 In Progress
- [item] — status: [where we are]

## 🟢 Ready to Do
- [item] — can start now

## 📝 Noted for Later
- [item] — low priority / future
```

## Usage

When JB asks:
- "What's open?"
- "Any pending tasks?"
- "Open loops?"
- "What did we forget?"

Run through all sources and compile a summary.

## Storing Open Loops

If an open loop needs to persist beyond the session:
```bash
# Add to agents notebook
nb agents: add "open-loop-<slug>.md"
```

Or add to today's memory file for short-term tracking.
