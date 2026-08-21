#!/usr/bin/env python3
"""Post-provision overlay for Brokkr Observability Workshop stacks.

Creates folder, optional Infinity datasource, and imports dashboards.
Does not install plugins unless --install-plugin is set (needs admin).
"""

from __future__ import annotations

import argparse
import csv
import json
import ssl
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DASH_DIR = ROOT / "dashboards"
FOLDER_UID = "workshop-network"
FOLDER_TITLE = "Network Observability"
DS_UID = "workshop-network-apis"
DS_NAME = "workshop-network-apis"
PLUGIN_ID = "yesoreyeram-infinity-datasource"
TENANT_HEADER = "X-Workshop-Tenant"

DASHBOARDS = [
    "device-summary.json",
    "device-details.json",
    "my-noc-view.json",
    "prtg-summary.json",
    "checkpoint-summary.json",
    "aruba-summary.json",
]


def _ctx() -> ssl.SSLContext:
    return ssl.create_default_context()


def api(
    base: str,
    token: str,
    path: str,
    *,
    method: str = "GET",
    body: dict | None = None,
) -> tuple[int, object]:
    url = base.rstrip("/") + path
    data = None if body is None else json.dumps(body).encode()
    req = urllib.request.Request(
        url,
        data=data,
        method=method,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, context=_ctx(), timeout=60) as resp:
            raw = resp.read().decode()
            return resp.status, json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        raw = e.read().decode()
        try:
            parsed: object = json.loads(raw) if raw else {"error": raw}
        except json.JSONDecodeError:
            parsed = {"error": raw[:800]}
        return e.code, parsed


def load_manifest(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as f:
        return [row for row in csv.DictReader(f) if row.get("url")]


def ensure_folder(base: str, token: str, dry: bool) -> None:
    code, _ = api(base, token, f"/api/folders/{FOLDER_UID}")
    if code == 200:
        print(f"  folder exists {FOLDER_UID}")
        return
    payload = {"uid": FOLDER_UID, "title": FOLDER_TITLE}
    if dry:
        print(f"  DRY folder {payload}")
        return
    code, body = api(base, token, "/api/folders", method="POST", body=payload)
    if code in (200, 201):
        print(f"  folder created {FOLDER_UID}")
        return
    print(f"  folder FAILED HTTP {code} {body}", file=sys.stderr)
    raise SystemExit(2)


def plugin_present(base: str, token: str) -> bool:
    code, body = api(base, token, f"/api/plugins/{PLUGIN_ID}/settings")
    return code == 200 and bool(body)


def ensure_infinity_ds(base: str, token: str, mock_url: str, tenant: str, dry: bool) -> None:
    payload = {
        "name": DS_NAME,
        "uid": DS_UID,
        "type": PLUGIN_ID,
        "access": "proxy",
        "url": mock_url.rstrip("/"),
        "isDefault": False,
        "jsonData": {
            "auth_method": "none",
            "allowedHosts": [mock_url.rstrip("/")],
            "httpHeaderName1": TENANT_HEADER,
        },
        "secureJsonData": {
            "httpHeaderValue1": tenant or "default",
        },
    }
    code, existing = api(base, token, f"/api/datasources/uid/{DS_UID}")
    if dry:
        print(f"  DRY datasource {'update' if code == 200 else 'create'} {DS_UID} -> {mock_url}")
        return
    if code == 200 and isinstance(existing, dict):
        payload["id"] = existing.get("id")
        code, body = api(
            base,
            token,
            f"/api/datasources/{existing.get('id')}",
            method="PUT",
            body=payload,
        )
    else:
        code, body = api(base, token, "/api/datasources", method="POST", body=payload)
    if code in (200, 201):
        print(f"  datasource ok {DS_UID}")
        return
    print(f"  datasource FAILED HTTP {code} {body}", file=sys.stderr)
    print("  hint: Editor tokens cannot create datasources. Re-run with --skip-datasource or use admin.", file=sys.stderr)
    raise SystemExit(3)


def import_dashboards(base: str, token: str, dry: bool) -> None:
    for name in DASHBOARDS:
        path = DASH_DIR / name
        dash = json.loads(path.read_text(encoding="utf-8"))
        uid = dash.get("uid")
        payload = {
            "dashboard": dash,
            "folderUid": FOLDER_UID,
            "overwrite": True,
            "message": "network-o11y-workshop overlay",
        }
        if dry:
            print(f"  DRY dashboard {uid} ({name})")
            continue
        code, body = api(base, token, "/api/dashboards/db", method="POST", body=payload)
        if code in (200, 201):
            print(f"  dashboard ok {uid}")
        else:
            print(f"  dashboard FAILED {uid} HTTP {code} {body}", file=sys.stderr)
            raise SystemExit(4)


def inspect_stack(base: str, token: str) -> None:
    print("  inspect:")
    code, ds = api(base, token, "/api/datasources")
    if code != 200 or not isinstance(ds, list):
        print(f"    datasources FAILED HTTP {code}")
        return
    for row in ds:
        if row.get("uid") in (
            "grafanacloud-prom",
            "grafanacloud-logs",
            "grafanacloud-traces",
            "grafanacloud-infinity",
            DS_UID,
        ) or "infinity" in str(row.get("type", "")):
            print(f"    ds {row.get('type')} uid={row.get('uid')} name={row.get('name')}")
    print(f"    infinity plugin: {plugin_present(base, token)}")


def apply_row(row: dict[str, str], args: argparse.Namespace) -> None:
    base = row["url"].rstrip("/")
    token = row["token"]
    tenant = row.get("tenant") or "default"
    print(f"== {base} tenant={tenant}")
    if args.inspect and not args.dry_run:
        inspect_stack(base, token)
    ensure_folder(base, token, args.dry_run)
    if not args.skip_datasource:
        if not args.dry_run and not plugin_present(base, token):
            print("  Infinity plugin not found. Install yesoreyeram-infinity-datasource, then re-run.", file=sys.stderr)
            if not args.allow_missing_plugin:
                raise SystemExit(5)
        ensure_infinity_ds(base, token, args.mock_url, tenant, args.dry_run)
    if not args.skip_dashboards:
        import_dashboards(base, token, args.dry_run)


def main() -> None:
    p = argparse.ArgumentParser(description="Overlay network workshop assets onto Brokkr stacks")
    p.add_argument("--manifest", type=Path, required=True)
    p.add_argument("--mock-url", required=True, help="Public base URL for mocks (Grafana Cloud must reach it)")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--skip-datasource", action="store_true")
    p.add_argument(
        "--skip-dashboards",
        action="store_true",
        help="Folder + Infinity only. Attendees import dashboards themselves in Lab 3.",
    )
    p.add_argument("--allow-missing-plugin", action="store_true")
    p.add_argument("--inspect", action="store_true", help="Print Cloud UIDs before applying")
    args = p.parse_args()

    rows = load_manifest(args.manifest)
    if not rows:
        raise SystemExit(f"No rows in {args.manifest}")
    for row in rows:
        apply_row(row, args)
    print("done")


if __name__ == "__main__":
    main()
