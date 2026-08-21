#!/usr/bin/env python3
"""Poll the workshop hairpin API and apply local routing commands.

Run this on the private Synthetic Monitoring probe host (or a sidecar next to
it). Grafana never talks to this process. Grafana POSTs desired state to the
public mock; this agent GETs that flag and runs HAIRPIN_ON_CMD / HAIRPIN_OFF_CMD.

No DNS changes. Destination IP stays the same.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request

API = os.environ.get("HAIRPIN_API_URL", "http://127.0.0.1:8088").rstrip("/")
TOKEN = os.environ.get("HAIRPIN_ADMIN_TOKEN", os.environ.get("WORKSHOP_ADMIN_TOKEN", "")).strip()
ON_CMD = os.environ.get("HAIRPIN_ON_CMD", "").strip()
OFF_CMD = os.environ.get("HAIRPIN_OFF_CMD", "").strip()
POLL = float(os.environ.get("HAIRPIN_POLL_SECS", "2"))


def _req(method: str, path: str, body: dict | None = None) -> dict:
    data = None if body is None else json.dumps(body).encode()
    headers = {"Accept": "application/json", "Content-Type": "application/json"}
    if TOKEN:
        headers["X-Workshop-Admin"] = TOKEN
    req = urllib.request.Request(API + path, data=data, method=method, headers=headers)
    with urllib.request.urlopen(req, timeout=10) as resp:
        raw = resp.read().decode()
        return json.loads(raw) if raw else {}


def _run(cmd: str, label: str) -> None:
    if not cmd:
        print(f"hairpin: {label} (noop — set HAIRPIN_ON_CMD / HAIRPIN_OFF_CMD)", flush=True)
        return
    print(f"hairpin: {label}: {cmd}", flush=True)
    subprocess.run(cmd, shell=True, check=True)


def main() -> int:
    current: bool | None = None
    print(f"hairpin: polling {API}/admin/hairpin every {POLL}s", flush=True)
    while True:
        try:
            state = _req("GET", "/admin/hairpin")
            desired = bool(state.get("active"))
            if current is None or desired != current:
                _run(ON_CMD if desired else OFF_CMD, "singapore" if desired else "direct")
                _req("POST", "/admin/hairpin/applied", {"active": desired})
                current = desired
                print(f"hairpin: applied desired={desired} path={state.get('path')}", flush=True)
        except urllib.error.HTTPError as e:
            print(f"hairpin: HTTP {e.code} {e.read()[:200]!r}", file=sys.stderr, flush=True)
        except Exception as e:  # noqa: BLE001 — keep the loop alive on the probe
            print(f"hairpin: {type(e).__name__}: {e}", file=sys.stderr, flush=True)
        time.sleep(POLL)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        raise SystemExit(0)
