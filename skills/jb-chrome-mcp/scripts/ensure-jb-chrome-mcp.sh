#!/usr/bin/env bash
set -euo pipefail

NAME="jb-chrome-mcp"
HOST="127.0.0.1"
PORT="9222"
VERSION="${CHROME_DEVTOOLS_MCP_VERSION:-1.2.0}"
USER_DATA_DIR="${CHROME_DEVTOOLS_MCP_USER_DATA_DIR:-${HOME}/Library/Application Support/Google/Chrome}"
DESCRIPTION="Chrome DevTools MCP via local Chrome remote debugging"

if ! command -v mcporter >/dev/null 2>&1; then
  echo "mcporter is required but not installed." >&2
  exit 1
fi

if ! command -v lsof >/dev/null 2>&1; then
  echo "lsof is required to verify Chrome remote debugging on ${HOST}:${PORT}." >&2
  exit 1
fi

if ! lsof -nP -iTCP:"${PORT}" -sTCP:LISTEN 2>/dev/null | grep -q "${HOST}:${PORT}"; then
  cat >&2 <<EOF
Chrome remote debugging is not listening on ${HOST}:${PORT}.

Prerequisite:
- open chrome://inspect/#remote-debugging
- turn remote debugging on
- confirm Chrome shows: Server running at: ${HOST}:${PORT}
EOF
  exit 2
fi

mcporter config add "${NAME}" \
  --stdio npx \
  --arg -y \
  --arg "chrome-devtools-mcp@${VERSION}" \
  --arg --auto-connect \
  --arg --userDataDir \
  --arg "${USER_DATA_DIR}" \
  --arg --no-usage-statistics \
  --description "${DESCRIPTION}" \
  --scope home >/dev/null

echo "Configured mcporter server '${NAME}' using chrome-devtools-mcp@${VERSION}."
echo "Using Chrome user data dir: ${USER_DATA_DIR}"
echo "Verify with: mcporter list ${NAME} --schema"
echo "If the first live mcporter call hangs, check Chrome for a permission prompt and click Allow."
