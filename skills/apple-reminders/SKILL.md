---
name: apple-reminders
description: Create, list, and manage Apple Reminders via remindctl CLI. Use when user says "remind me", "Erinnerung:", or "Reminder:" to create reminders, or asks to list/check reminders.
---

# Apple Reminders

Use `remindctl` CLI to manage Apple Reminders.

## Commands

### Add Reminder
```bash
remindctl add --title "<reminder text>" --due "<date/time>"
```

**Date formats:**
- Natural language: `today 3pm`, `tomorrow 9am`, `next friday 2pm`
- ISO format: `2026-01-21T10:00:00`
- If date parsing fails → write to `memory/YYYY-MM-DD.md` as fallback

### List Reminders
```bash
remindctl show         # Show all reminders
remindctl list         # List reminder lists
remindctl list "Work"  # Show reminders in specific list
```

### Complete Reminder
```bash
remindctl complete "<reminder-id or title>"
```

### Delete Reminder
```bash
remindctl delete "<reminder-id or title>"
```

## Fallback

If `remindctl` fails or date parsing errors occur, write reminders to `memory/YYYY-MM-DD.md`:

```markdown
## Reminders
- [ ] Reminder text here
```

## Examples

- "remind me to call mom at 5pm" → `remindctl add --title "Call mom" --due "today 5pm"`
- "Erinnerung: Milch kaufen" → `remindctl add --title "Milch kaufen" --due "tomorrow 10am"`
- "Reminder: meeting tomorrow at 2" → `remindctl add --title "Meeting" --due "tomorrow 2pm"`
