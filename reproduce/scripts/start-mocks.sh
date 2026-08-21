#!/usr/bin/env bash
# Build and run the workshop mock API on :8088.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
docker compose -f mocks/docker-compose.yaml up -d --build
sleep 2
curl -fsS http://127.0.0.1:8088/health
echo
curl -fsS http://127.0.0.1:8088/ | python3 -m json.tool
