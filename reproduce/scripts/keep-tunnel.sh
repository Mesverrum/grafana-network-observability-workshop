#!/usr/bin/env bash
set -euo pipefail
export PATH="$HOME/.local/bin:$PATH"
echo "starting cloudflared against http://127.0.0.1:8088"
exec cloudflared tunnel --url http://127.0.0.1:8088 --no-autoupdate
