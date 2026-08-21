#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
python3 dashboards/build.py
python3 -c "import inventory; print('devices', len(inventory.DEVICES)); print('gateways', len(inventory.CHECKPOINT_GATEWAYS)); print('ec', len(inventory.EDGECONNECT_APPLIANCES))"
