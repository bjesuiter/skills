#!/usr/bin/env bash
set -euo pipefail

NAME="jb-pinchtab-mcp"
SERVER_URL="${PINCHTAB_SERVER:-http://127.0.0.1:9867}"
DESCRIPTION="PinchTab native MCP via a running PinchTab server"

if ! command -v mcporter >/dev/null 2>&1; then
  echo "mcporter is required but not installed." >&2
  exit 1
fi

if ! command -v pinchtab >/dev/null 2>&1; then
  echo "pinchtab is required but not installed." >&2
  exit 1
fi

if ! pinchtab --server "${SERVER_URL}" health --json >/dev/null 2>&1; then
  cat >&2 <<EOF
PinchTab server is not healthy or not reachable.

Expected a running PinchTab server that answers:
  pinchtab --server ${SERVER_URL} health --json

Useful next steps:
- start the dashboard/server: pinchtab
- or start the bridge-only runtime: pinchtab bridge --headless
- then retry this bootstrap script
EOF
  exit 2
fi

args=(mcp)
if [[ "${SERVER_URL}" != "http://127.0.0.1:9867" ]]; then
  args=(--server "${SERVER_URL}" mcp)
fi

cmd=(
  mcporter config add "${NAME}"
  --stdio pinchtab
  --description "${DESCRIPTION}"
  --scope home
)
for arg in "${args[@]}"; do
  cmd+=(--arg "$arg")
done

"${cmd[@]}" >/dev/null

echo "Configured mcporter server '${NAME}'."
echo "Verify with: mcporter --config ~/.mcporter/mcporter.json list ${NAME} --schema"
if [[ "${SERVER_URL}" != "http://127.0.0.1:9867" ]]; then
  echo "Using remote PinchTab server: ${SERVER_URL}"
  echo "If the remote server requires auth, export PINCHTAB_TOKEN in the shell before mcporter calls."
fi
