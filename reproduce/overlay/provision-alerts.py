#!/usr/bin/env python3
"""Provision Workshop / campus alert rules on attendee Grafana Cloud stacks.

Same Reduce + Threshold shape as the lab collection. Scoped to
tags_snmp_group=campus so they do not collide with Network Lab / ktranslate.
`for` is 1m so instances fire during a half-day room.
"""

from __future__ import annotations

import argparse
import csv
import json
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FOLDER_UID = "workshop-network"
RULE_GROUP = "Workshop / campus"
PROM_DS = "grafanacloud-prom"
SUMMARY_UID = "workshop-device-summary"
DETAIL_UID = "workshop-device-details"


def _ctx() -> ssl.SSLContext:
    return ssl.create_default_context()


def api(base: str, token: str, path: str, *, method: str = "GET", body: dict | None = None) -> tuple[int, object]:
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
            "X-Disable-Provenance": "true",
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


def prom_query(expr: str) -> dict:
    return {
        "refId": "A",
        "queryType": "",
        "relativeTimeRange": {"from": 600, "to": 0},
        "datasourceUid": PROM_DS,
        "model": {
            "datasource": {"type": "prometheus", "uid": PROM_DS},
            "expr": expr,
            "instant": True,
            "intervalMs": 1000,
            "legendFormat": "__auto",
            "maxDataPoints": 43200,
            "refId": "A",
        },
    }


def reduce_b() -> dict:
    return {
        "refId": "B",
        "queryType": "",
        "relativeTimeRange": {"from": 0, "to": 0},
        "datasourceUid": "__expr__",
        "model": {
            "datasource": {"type": "__expr__", "uid": "__expr__"},
            "expression": "A",
            "intervalMs": 1000,
            "maxDataPoints": 43200,
            "reducer": "last",
            "refId": "B",
            "settings": {"mode": "dropNN"},
            "type": "reduce",
        },
    }


def threshold_c() -> dict:
    return {
        "refId": "C",
        "queryType": "",
        "relativeTimeRange": {"from": 0, "to": 0},
        "datasourceUid": "__expr__",
        "model": {
            "conditions": [
                {
                    "evaluator": {"params": [0], "type": "gt"},
                    "operator": {"type": "and"},
                    "query": {"params": ["C"]},
                    "reducer": {"params": [], "type": "last"},
                    "type": "query",
                }
            ],
            "datasource": {"type": "__expr__", "uid": "__expr__"},
            "expression": "B",
            "intervalMs": 1000,
            "maxDataPoints": 43200,
            "refId": "C",
            "type": "threshold",
        },
    }


def rule(uid: str, title: str, expr: str, summary: str, description: str, severity: str, grafana: str) -> dict:
    return {
        "uid": uid,
        "title": title,
        "condition": "C",
        "data": [prom_query(expr), reduce_b(), threshold_c()],
        "noDataState": "OK",
        "execErrState": "Error",
        "for": "1m",
        "annotations": {
            "summary": summary,
            "description": description,
            "runbook_url": f"{grafana}/d/{DETAIL_UID}?var-device={{{{ $labels.device_name }}}}",
        },
        "labels": {
            "category": "network",
            "source": "workshop",
            "severity": severity,
            "dashboard_uid": SUMMARY_UID,
        },
        "isPaused": False,
    }


def rules(grafana: str) -> list[dict]:
    campus = 'tags_snmp_group="campus"'
    return [
        rule(
            "ws-high-device-cpu",
            "High device CPU",
            f"max by(device_name) (kentik_snmp_CPU{{{campus}}}) > 80",
            "CPU above 80% on {{ $labels.device_name }}",
            "Workshop campus CPU has been above 80% for 1 minute.",
            "warning",
            grafana,
        ),
        rule(
            "ws-high-interface-errors",
            "High interface error rate",
            (
                "sum by(device_name, if_interface_name) ("
                f"kentik_snmp_ifInErrors{{{campus}}} / 60) > 5"
            ),
            "High errors on {{ $labels.device_name }} {{ $labels.if_interface_name }}",
            "In errors exceed 5/s (ktranslate 60s delta gauge).",
            "warning",
            grafana,
        ),
        rule(
            "ws-snmp-polling-unhealthy",
            "SNMP polling unhealthy",
            f"max by(device_name) (kentik_snmp_PollingHealth{{{campus}}}) < 1",
            "SNMP polling unhealthy on {{ $labels.device_name }}",
            "PollingHealth is below 1 for 1 minute.",
            "critical",
            grafana,
        ),
    ]


def provision(base: str, token: str, dry: bool) -> None:
    payload = {"title": RULE_GROUP, "interval": 60, "rules": rules(base)}
    path = (
        f"/api/v1/provisioning/folder/{FOLDER_UID}/rule-groups/"
        + urllib.parse.quote(RULE_GROUP, safe="")
    )
    if dry:
        print(f"  DRY PUT {path} ({len(payload['rules'])} rules)")
        for r in payload["rules"]:
            print(f"    - {r['uid']}: {r['title']}")
        return
    code, body = api(base, token, path, method="PUT", body=payload)
    if 200 <= code < 300:
        print(f"  alerts ok {RULE_GROUP} ({len(payload['rules'])})")
        return
    print(f"  alerts FAILED HTTP {code} {body}", file=sys.stderr)
    raise SystemExit(6)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--manifest", type=Path, required=True)
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()
    rows = load_manifest(args.manifest)
    if not rows:
        raise SystemExit(f"No rows in {args.manifest}")
    for row in rows:
        print(f"== {row['url']}")
        provision(row["url"], row["token"], args.dry_run)
    print("done")


if __name__ == "__main__":
    main()
