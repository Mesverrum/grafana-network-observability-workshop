#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
echo "starting workshop generator against stacks.csv"
exec python3 generator/generate.py --manifest stacks.csv --interval 15 --fault
