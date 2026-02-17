---
title: Telegram Process Viewer - Pinned Progress Messages
created: 2026-01-16T19:48:00+01:00
updated: 2026-01-16T19:48:00+01:00
tags: [telegram, bot, progress, pinned-message, background-task]
status: completed
priority: medium
owner: agent
---

## Goal

Design a system for displaying background task progress in Telegram using pinned status messages that update in real-time.

## Research Summary

After researching Telegram bots that implement progress indicators, the most common patterns include:

1. **Pinned Message Updates** - Send a message, pin it, then update via `editMessageText`
2. **Inline Keyboards** - Add buttons for cancellation/status
3. **Chat Actions** - Use `sendChatAction` for typing/upload indicators
4. **Periodic Updates** - Update every N seconds with progress percentage

### Real-World Examples

- **File Download Bots** (e.g., @MCPlayerBot) - Show file size, downloaded MB, ETA
- **YouTube Downloaders** - Progress bar with percentage, speed, format info
- **Crypto Trading Bots** - Pin status with buy/sell alerts updating in place
- **Moderation Bots** - Pin "Scanning..." status during bulk operations
- **Backup Bots** - "Backing up X of Y files..." with file names

## Key Telegram API Methods

### Core Methods for Progress Messages

```python
# 1. Send initial status message
sendMessage(chat_id, text, parse_mode="Markdown")

# 2. Pin the message for visibility
pinChatMessage(chat_id, message_id, disable_notification=False)

# 3. Update the message with new progress
editMessageText(chat_id=chat_id, message_id=message_id, text=new_text)

# 4. Optional: Add inline keyboard for actions
editMessageReplyMarkup(chat_id, message_id, reply_markup=keyboard)

# 5. Unpin when done (or keep for history)
unpinChatMessage(chat_id, message_id)
```

### Additional Useful Methods

```python
# Show "typing..." or "uploading..." status
sendChatAction(chat_id, action="typing")

# Get message info to verify it exists
getMessage(chat_id, message_id)

# Delete the pinned message on completion
deleteMessage(chat_id, message_id)
```

## Implementation Details

### Progress Message Format

For best readability, use:
- **Monospace font** for numbers/bars (Markdown: `code` or `` ` ``)
- **Emojis** for status indicators
- **Consistent width** for progress bars
- **Timestamps** for long-running tasks

### Progress Bar Rendering

```
█░░░░░░░░░░░ 10%  ▓▓▓▓▓░░░░░░░ 50%
```

Unicode block characters:
- `█` - Full block
- `▓` - 3/4 block  
- `▒` - 1/2 block
- `░` - 1/4 block
- `□` - Empty block

### State Management

```python
class ProgressTracker:
    def __init__(self, bot, chat_id, task_name):
        self.bot = bot
        self.chat_id = chat_id
        self.task_name = task_name
        self.message_id = None
        self.start_time = None
        
    async def start(self, total_items):
        self.total = total_items
        self.current = 0
        self.start_time = time.time()
        
        # Send and pin initial message
        msg = await self.bot.send_message(
            self.chat_id,
            self._format_status(0),
            parse_mode="Markdown"
        )
        self.message_id = msg.message_id
        await self.bot.pin_chat_message(self.chat_id, self.message_id)
        
    async def update(self, current, info=""):
        self.current = current
        percent = (current / self.total) * 100
        
        await self.bot.edit_message_text(
            chat_id=self.chat_id,
            message_id=self.message_id,
            text=self._format_status(percent, info),
            parse_mode="Markdown"
        )
        
    async def complete(self, result=""):
        elapsed = time.time() - self.start_time
        await self.bot.edit_message_text(
            chat_id=self.chat_id,
            message_id=self.message_id,
            text=f"✅ *{self.task_name} Complete*\n\n{result}\n⏱️ Time: {elapsed:.1f}s",
            parse_mode="Markdown"
        )
        # Optionally unpin after delay
        # await self.bot.unpin_chat_message(self.chat_id, self.message_id)
```

## Mock Example - Complete Walkthrough

### Scenario: File Processing Bot

User uploads 5 files, bot processes them one by one with pinned progress.

**Initial State:**
```
╔════════════════════════════════════╗
║ 📁 Processing Files                ║
║                                    ║
║ 0/5 files processed                ║
║                                    ║
║ ░░░░░░░░░░░░ 0%                   ║
║                                    ║
║ 🚧 Initializing...                 ║
╚════════════════════════════════════╝
                              📌 Pinned
```

**After 2 files:**
```
╔════════════════════════════════════╗
║ 📁 Processing Files                ║
║                                    ║
║ 2/5 files processed                ║
║                                    ║
║ ██░░░░░░░░░░ 40%                  ║
║                                    ║
║ ✅ file1.pdf                       ║
║ ✅ file2.jpg                       ║
║ ▸ processing file3.png...          ║
╚════════════════════════════════════╝
                              📌 Pinned
```

**Complete:**
```
╔════════════════════════════════════════╗
║ ✅ Processing Complete                 ║
║                                        ║
║ 5/5 files processed                    ║
║                                        ║
║ ████████████░░░░░░ 100%                ║
║                                        ║
║ Files:                                 ║
║ ✅ file1.pdf (2.1 MB)                  ║
║ ✅ file2.jpg (1.4 MB)                  ║
║ ✅ file3.png (3.2 MB)                  ║
║ ✅ file4.docx (890 KB)                 ║
║ ✅ file5.pdf (1.8 MB)                  ║
║                                        ║
║ ⏱️ Total time: 12.3s                   ║
╚════════════════════════════════════════╝
                              📌 Pinned
```

### JSON Example - Initial Message

```json
POST /bot<token>/sendMessage
{
  "chat_id": 123456789,
  "text": "📁 *Processing Files*\n\n0/5 files processed\n\n`░░░░░░░░░░░░` 0%\n\n🚧 Initializing...",
  "parse_mode": "Markdown",
  "reply_markup": {
    "inline_keyboard": [
      [{"text": "⏹️ Cancel", "callback_data": "cancel_processing"}]
    ]
  }
}
```

### JSON Example - Update Message

```json
POST /bot<token>/editMessageText
{
  "chat_id": 123456789,
  "message_id": 999,
  "text": "📁 *Processing Files*\n\n2/5 files processed\n\n`██░░░░░░░░░░` 40%\n\n✅ file1.pdf\n✅ file2.jpg\n▸ processing file3.png...",
  "parse_mode": "Markdown"
}
```

### JSON Example - Pin Message

```json
POST /bot<token>/pinChatMessage
{
  "chat_id": 123456789,
  "message_id": 999,
  "disable_notification": false
}
```

## Best Practices

1. **Update Frequency**: Don't spam - update every 1-5 seconds or on milestone events
2. **Message Length**: Keep under 4096 characters (Telegram limit)
3. **Parse Mode**: Use Markdown for formatting, but escape special chars
4. **Error Handling**: Handle `Message Not Modified` errors gracefully
5. **Cleanup**: Unpin or delete progress messages when done
6. **Keyboard**: Add cancel button for long-running tasks
7. **Notifications**: Consider `disable_notification` for pinned updates

## Related

- [[skill:clawdcontrol]] - Clawdbot messaging provider
- Telegram Bot API: https://core.telegram.org/bots/api
- python-telegram-bot library: https://python-telegram-bot.org/
- Telethon library: https://telethon.readthedocs.io/

## Session Log

- 2026-01-16T19:48: Created initial research note
- Researched Telegram Bot API methods for message editing and pinning
- Compiled real-world bot patterns and best practices
- Added mock example with visual progress states
