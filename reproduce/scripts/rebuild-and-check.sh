#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
# Dashboard JSON is live-pulled; build.py exits on purpose.
python3 -c "import inventory; print('mock devices', len(inventory.DEVICES)); print('gateways', len(inventory.CHECKPOINT_GATEWAYS)); print('ec', len(inventory.EDGECONNECT_APPLIANCES))"
