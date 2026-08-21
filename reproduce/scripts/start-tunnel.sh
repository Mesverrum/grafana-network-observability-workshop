#!/usr/bin/env bash
# Quick tunnel for the mock API. Prints the trycloudflare.com URL.
set -euo pipefail
export PATH="$HOME/.local/bin:$PATH"
LOG="${TMPDIR:-/tmp}/workshop-cloudflared.log"
: > "$LOG"
cloudflared tunnel --url http://127.0.0.1:8088 --no-autoupdate >"$LOG" 2>&1 &
echo $! > "${TMPDIR:-/tmp}/workshop-cloudflared.pid"
for i in $(seq 1 40); do
  url="$(grep -oE 'https://[a-z0-9-]+\.trycloudflare\.com' "$LOG" | head -1 || true)"
  if [ -n "${url:-}" ]; then
    echo "$url"
    echo "$url" > "${TMPDIR:-/tmp}/workshop-mock-url.txt"
    exit 0
  fi
  sleep 1
done
echo "tunnel URL not ready; log follows" >&2
cat "$LOG" >&2
exit 1
