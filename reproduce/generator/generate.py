#!/usr/bin/env python3
"""Fan out ktranslate-shaped OTLP metrics and syslog to Brokkr stacks."""

from __future__ import annotations

import argparse
import base64
import csv
import json
import random
import ssl
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from inventory import DEVICES, INTERFACES, SERVICE_NAME, SNMP_GROUP, SYSLOG_SERVICE  # noqa: E402

# ktranslate ifHC* on Marc's dashboards is often treated as a 60s increment.
# Emit both a growing counter and a per-interval gauge-like increment via the
# same metric name as a cumulative counter (rate() still works).


def load_manifest(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as f:
        return [row for row in csv.DictReader(f) if row.get("otlp_endpoint")]


def now_ns() -> int:
    return time.time_ns()


def attr(key: str, value: str | int | float) -> dict:
    if isinstance(value, bool):
        return {"key": key, "value": {"boolValue": value}}
    if isinstance(value, int) and not isinstance(value, bool):
        return {"key": key, "value": {"intValue": str(value)}}
    if isinstance(value, float):
        return {"key": key, "value": {"doubleValue": value}}
    return {"key": key, "value": {"stringValue": str(value)}}


def gauge(name: str, value: float, labels: dict[str, str], t: int) -> dict:
    return {
        "name": name,
        "gauge": {
            "dataPoints": [
                {
                    "asDouble": float(value),
                    "timeUnixNano": str(t),
                    "attributes": [attr(k, v) for k, v in labels.items()],
                }
            ]
        },
    }


def counter(name: str, value: float, labels: dict[str, str], t: int) -> dict:
    return {
        "name": name,
        "sum": {
            "aggregationTemporality": 2,  # CUMULATIVE
            "isMonotonic": True,
            "dataPoints": [
                {
                    "asDouble": float(value),
                    "timeUnixNano": str(t),
                    "startTimeUnixNano": str(t - 60_000_000_000),
                    "attributes": [attr(k, v) for k, v in labels.items()],
                }
            ],
        },
    }


def device_labels(d: dict) -> dict[str, str]:
    return {
        "device_name": d["name"],
        "device_ip": d["ip"],
        "provider": d["provider"],
        "tags_snmp_group": SNMP_GROUP,
        "tags_kentik_model": d["model"],
        "building": d["building"],
        "role": d["role"],
    }


def iface_labels(d: dict, if_name: str, alias: str) -> dict[str, str]:
    labels = device_labels(d)
    labels.update(
        {
            "if_interface_name": if_name,
            "if_Alias": alias,
            "if_Description": alias,
            "if_AdminStatus": "up",
            "if_Type": "ethernetCsmacd",
        }
    )
    return labels


def build_metrics(fault: bool, tick: int, rng: random.Random) -> dict:
    t = now_ns()
    metrics: list[dict] = []
    for d in DEVICES:
        labels = device_labels(d)
        cpu = d["cpu"] + rng.uniform(-1.5, 1.5)
        mem = d["mem"] + rng.uniform(-1.0, 1.0)
        if fault and d.get("fault") == "cpu_sessions":
            cpu = 87.0 + rng.uniform(-2, 3)
        metrics.append(gauge("kentik_snmp_PollingHealth", 1, labels, t))
        metrics.append(gauge("kentik_snmp_CPU", max(1.0, cpu), labels, t))
        metrics.append(gauge("kentik_snmp_MemoryUtilization", max(1.0, mem), labels, t))
        metrics.append(gauge("kentik_snmp_Uptime", 1_800_000 + tick * 15, labels, t))
        metrics.append(gauge("kentik_snmp_MemoryUsed", mem * 40, labels, t))
        metrics.append(gauge("kentik_snmp_MemoryAvailable", (100 - mem) * 40, labels, t))

        for if_name, alias, _admin, kind in INTERFACES.get(d["name"], []):
            il = iface_labels(d, if_name, alias)
            oper = 1
            in_inc = 12_000_000 + rng.randint(0, 2_000_000)
            out_inc = 9_000_000 + rng.randint(0, 1_500_000)
            err_in = rng.randint(0, 1)
            err_out = 0
            if fault and kind == "crc":
                err_in = 420 + rng.randint(0, 80)
            if fault and kind == "saturated":
                in_inc = 140_000_000 + rng.randint(0, 10_000_000)
                out_inc = 135_000_000 + rng.randint(0, 8_000_000)
            metrics.append(gauge("kentik_snmp_if_OperStatus", oper, il, t))
            # Gauges, not OTLP sums. Cloud adds `_total` to monotonic sums, which
            # hides the ktranslate names the boards query.
            metrics.append(gauge("kentik_snmp_ifHCInOctets", in_inc, il, t))
            metrics.append(gauge("kentik_snmp_ifHCOutOctets", out_inc, il, t))
            metrics.append(gauge("kentik_snmp_ifInErrors", err_in, il, t))
            metrics.append(gauge("kentik_snmp_ifOutErrors", err_out, il, t))

    return {
        "resourceMetrics": [
            {
                "resource": {
                    "attributes": [
                        attr("service.name", SERVICE_NAME),
                        attr("workshop.kit", "network-o11y-workshop"),
                    ]
                },
                "scopeMetrics": [
                    {
                        "scope": {"name": "ktranslate", "version": "workshop"},
                        "metrics": metrics,
                    }
                ],
            }
        ]
    }


def build_logs(fault: bool) -> dict:
    t = now_ns()
    records = [
        {
            "device_name": "dc-core-01",
            "severity": "info",
            "body": "%LINEPROTO-5-UPDOWN: Line protocol on Interface Eth1/1, changed state to up",
        }
    ]
    if fault:
        records.extend(
            [
                {
                    "device_name": "bld4-asw-01",
                    "severity": "error",
                    "body": "%EXCESSCOLL: Gi1/0/24 excess collision / CRC rising (Access-IDF-B4)",
                },
                {
                    "device_name": "bld4-asw-01",
                    "severity": "warning",
                    "body": "%LINK-4-TOOBIG: Gi1/0/48 output drops, uplink toward dc-core-01 saturated",
                },
                {
                    "device_name": "bld4-fw-01",
                    "severity": "warning",
                    "body": "Check Point: CPU utilization exceeded threshold on bld4-fw-01 (87%) session table 14220",
                },
                {
                    "device_name": "wan-edge-01",
                    "severity": "warning",
                    "body": "EdgeConnect: tunnel dc-to-bld4 Overlay-Bld4 degraded, loss 2.4% latency 48ms",
                },
            ]
        )
    log_records = []
    for rec in records:
        log_records.append(
            {
                "timeUnixNano": str(t),
                "severityText": rec["severity"],
                "body": {"stringValue": rec["body"]},
                "attributes": [
                    attr("device_name", rec["device_name"]),
                    attr("instrumentation_name", "ktranslate-syslog"),
                    attr("severity", rec["severity"]),
                    attr("building", "bld4" if rec["device_name"].startswith("bld4") else "dc"),
                ],
            }
        )
    return {
        "resourceLogs": [
            {
                "resource": {
                    "attributes": [
                        attr("service.name", SYSLOG_SERVICE),
                    ]
                },
                "scopeLogs": [
                    {
                        "scope": {"name": "ktranslate-syslog"},
                        "logRecords": log_records,
                    }
                ],
            }
        ]
    }


def otlp_post(endpoint: str, instance: str, token: str, path: str, payload: dict, timeout: int) -> int:
    url = endpoint.rstrip("/") + path
    raw = json.dumps(payload).encode()
    auth = base64.b64encode(f"{instance}:{token}".encode()).decode()
    req = urllib.request.Request(
        url,
        data=raw,
        method="POST",
        headers={
            "Authorization": f"Basic {auth}",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, context=ssl.create_default_context(), timeout=timeout) as resp:
            resp.read()
            return resp.status
    except urllib.error.HTTPError as e:
        print(f"  OTLP {path} HTTP {e.code}: {e.read()[:300]!r}", file=sys.stderr)
        return e.code


def send_stack(row: dict[str, str], metrics: dict, logs: dict, timeout: int, dry: bool) -> None:
    name = row.get("url") or row.get("otlp_endpoint")
    if dry:
        n = len(metrics["resourceMetrics"][0]["scopeMetrics"][0]["metrics"])
        print(f"  DRY {name} metrics={n}")
        return
    ep = row["otlp_endpoint"]
    inst = row["otlp_instance"]
    tok = row["otlp_token"]
    m = otlp_post(ep, inst, tok, "/v1/metrics", metrics, timeout)
    l = otlp_post(ep, inst, tok, "/v1/logs", logs, timeout)
    print(f"  {name} metrics={m} logs={l}")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--manifest", type=Path, required=True)
    p.add_argument("--interval", type=int, default=15)
    p.add_argument("--once", action="store_true")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--fault", dest="fault", action="store_true", default=True)
    p.add_argument("--no-fault", dest="fault", action="store_false")
    p.add_argument("--timeout", type=int, default=20)
    args = p.parse_args()

    rows = load_manifest(args.manifest)
    if not rows:
        raise SystemExit(f"No OTLP rows in {args.manifest}")
    print(f"targets={len(rows)} interval={args.interval}s fault={args.fault}")
    rng = random.Random(4)
    tick = 1
    while True:
        metrics = build_metrics(args.fault, tick, rng)
        logs = build_logs(args.fault)
        for row in rows:
            send_stack(row, metrics, logs, args.timeout, args.dry_run)
        if args.once or args.dry_run:
            break
        tick += 1
        time.sleep(args.interval)


if __name__ == "__main__":
    main()
