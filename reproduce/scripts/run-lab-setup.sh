#!/usr/bin/env bash
# Start mocks and install cloudflared if needed.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
sed -i 's/\r$//' "$ROOT"/scripts/*.sh || true
bash "$ROOT/scripts/install-cloudflared.sh"
bash "$ROOT/scripts/start-mocks.sh"
echo "mocks ready; copy stacks.example.csv to stacks.csv and fill tokens"
