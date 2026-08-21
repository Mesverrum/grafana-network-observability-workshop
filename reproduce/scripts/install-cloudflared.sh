#!/usr/bin/env bash
set -euo pipefail
if command -v cloudflared >/dev/null; then
  cloudflared --version
  exit 0
fi
ARCH="$(uname -m)"
case "$ARCH" in
  x86_64) DEB_ARCH=amd64 ;;
  aarch64) DEB_ARCH=arm64 ;;
  *) echo "unsupported arch $ARCH" >&2; exit 1 ;;
esac
TMP="$(mktemp -d)"
curl -fsSL "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-${DEB_ARCH}" -o "$TMP/cloudflared"
chmod +x "$TMP/cloudflared"
mkdir -p "$HOME/.local/bin"
mv "$TMP/cloudflared" "$HOME/.local/bin/cloudflared"
export PATH="$HOME/.local/bin:$PATH"
cloudflared --version
