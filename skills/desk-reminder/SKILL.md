---
name: desk-reminder
description: Track reminders for when JB is back at his desk. No specific time - triggered when JB says he's at his desk.
private: true
---

# Desk Reminder Skill

Track things to remind JB about when he's back at his desk.

## Adding a Reminder

When JB says "remind me at my desk" or similar:

1. Read the desk-reminders file:
   ```bash
   cat ~/.nb/agents/desk-reminders.md
   ```

2. Add the new reminder under today's date section:
   ```markdown
   ## YYYY-MM-DD
   
   - [ ] **Reminder title** — details
   ```

3. Commit and push:
   ```bash
   cd ~/.nb/agents && git add . && git commit -m "Desk reminder: <title>" 
   fish -c "cd ~/.nb/agents && git push"
   ```

## When JB is at His Desk

When JB says "I'm at my desk" or "back at desk":

1. Read desk-reminders.md
2. Report all unchecked items
3. Ask if he wants to handle any of them

## Completing Reminders

When a reminder is done:
- Mark it `[x]` instead of `[ ]`
- Or remove it entirely if no longer relevant

## File Location

`~/.nb/agents/desk-reminders.md`

Linked from `open-loops.md` for visibility.
