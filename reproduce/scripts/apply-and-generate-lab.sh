#!/usr/bin/env bash
# Overlay dashboards + Infinity, send one OTLP batch, start the generator.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
export PATH="$HOME/.local/bin:$PATH"
MOCK_URL="${1:-}"
if [ -z "$MOCK_URL" ]; then
  if [ -f "${TMPDIR:-/tmp}/workshop-mock-url.txt" ]; then
    MOCK_URL="$(cat "${TMPDIR:-/tmp}/workshop-mock-url.txt")"
  fi
fi
if [ -z "$MOCK_URL" ]; then
  echo "usage: apply-and-generate-lab.sh https://PUBLIC_MOCK_URL" >&2
  exit 1
fi
echo "mock_url=$MOCK_URL"
python3 overlay/apply.py --manifest stacks.csv --mock-url "$MOCK_URL" --inspect
python3 generator/generate.py --manifest stacks.csv --once --fault
echo "one OTLP batch sent; starting generator"
nohup python3 generator/generate.py --manifest stacks.csv --interval 15 --fault \
  > "${TMPDIR:-/tmp}/workshop-generator.log" 2>&1 &
echo $! > "${TMPDIR:-/tmp}/workshop-generator.pid"
echo "generator_pid=$(cat "${TMPDIR:-/tmp}/workshop-generator.pid")"
