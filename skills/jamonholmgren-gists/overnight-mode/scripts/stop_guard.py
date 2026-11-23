"""Encourage an unattended agent to resolve decisions before ending its turn."""

import hashlib
import json
import re
import sys
from pathlib import Path

QUESTION = re.compile(
    r"\?|\b(?:should i|shall i|want me to|do you want|would you like|"
    r"let me know (?:if|whether|which|how)|your call)\b",
    re.IGNORECASE,
)
FENCED_CODE = re.compile(r"```.*?```", re.DOTALL)
MAX_BLOCKS = 2
REASON = (
    "Overnight mode is active. Continue with the best reversible step within scope "
    "and record debatable choices for the morning. If human action is required, "
    "state it as a NEEDS INPUT item without asking a question."
)


def main():
    marker = Path.home() / ".agents" / "OVERNIGHT"
    if not marker.exists():
        return

    try:
        event = json.load(sys.stdin)
    except ValueError:
        return
    if not isinstance(event, dict):
        return

    session = event.get("session_id")
    if not isinstance(session, str) or not session:
        return

    message = event.get("last_assistant_message")
    tail = FENCED_CODE.sub("", message).strip()[-500:] if isinstance(message, str) else ""
    state_dir = marker.parent / "overnight-stop-state"
    counter = state_dir / hashlib.sha256(session.encode()).hexdigest()

    try:
        if not QUESTION.search(tail):
            counter.unlink(missing_ok=True)
            return

        count = 0
        if event.get("stop_hook_active") and counter.exists():
            count = int(counter.read_text(encoding="utf-8"))
        if count >= MAX_BLOCKS:
            counter.unlink(missing_ok=True)
            return

        state_dir.mkdir(mode=0o700, exist_ok=True)
        counter.write_text(str(count + 1), encoding="utf-8")
    except (OSError, ValueError):
        # Allow the agent to finish if the retry count cannot be maintained.
        return

    print(json.dumps({"decision": "block", "reason": REASON}))


if __name__ == "__main__":
    main()
