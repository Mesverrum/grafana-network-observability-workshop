#!/usr/bin/env bash
set -u
echo "cloudflared=$(command -v cloudflared || echo missing)"
echo "flyctl=$(command -v flyctl || echo missing)"
echo "ngrok=$(command -v ngrok || echo missing)"
echo "gcloud=$(command -v gcloud || echo missing)"
if command -v gcloud >/dev/null; then
  gcloud config get-value project 2>/dev/null || true
  gcloud auth list --filter=status:ACTIVE --format='value(account)' 2>/dev/null | head -3 || true
fi
docker ps --format '{{.Names}}' 2>/dev/null | head -20 || true
