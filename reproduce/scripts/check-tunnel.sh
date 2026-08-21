#!/usr/bin/env bash
set -u
echo "docker:"
docker ps --filter name=mocks --format '{{.Names}} {{.Status}} {{.Ports}}'
echo "cloudflared_pid_file=$(cat /tmp/workshop-cloudflared.pid 2>/dev/null || echo none)"
pgrep -a cloudflared || echo "no cloudflared process"
echo "localhost:"
curl -fsS -m 3 http://127.0.0.1:8088/health || echo "localhost mock down"
echo
tail -n 30 /tmp/workshop-cloudflared.log 2>/dev/null || echo "no tunnel log"
