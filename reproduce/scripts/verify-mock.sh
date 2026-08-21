#!/usr/bin/env bash
set -euo pipefail
URL="${1:?url}"
curl -fsS -A "workshop-verify" "$URL/health"
echo
curl -fsS -A "workshop-verify" "$URL/checkpoint/gateways" | python3 -c "import sys,json; d=json.load(sys.stdin); print('gateways', d['count'], [g['name'] for g in d['gateways']])"
curl -fsS -A "workshop-verify" "$URL/edgeconnect/appliances" | python3 -c "import sys,json; d=json.load(sys.stdin); print('ec', d['count'], [a['hostName'] for a in d['appliances']])"
curl -fsS -A "workshop-verify" "$URL/prtg/api/v2/sensors" | python3 -c "import sys,json; d=json.load(sys.stdin); print('prtg', d['count'])"
