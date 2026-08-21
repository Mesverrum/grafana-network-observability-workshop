#!/usr/bin/env python3
"""Build workshop dashboards as Grafana JSON.

Mirrors the lab collection path (Device Summary → Device Details) at workshop
scale. No ticket copy that names the guilty device.

Table rule: Device, Interface, and other friendly identifiers are always the
leftmost columns (IDENTITY_FIRST + organize). Do not leave them wherever the
API JSON or Prom labels happen to land.
"""

from __future__ import annotations

import json
from pathlib import Path

OUT = Path(__file__).resolve().parent

PROM = {"type": "prometheus", "uid": "${datasource}"}
LOKI = {"type": "loki", "uid": "${loki}"}
INF = {"type": "yesoreyeram-infinity-datasource", "uid": "${infinity}"}
DETAIL_UID = "workshop-device-details"
SUMMARY_UID = "workshop-device-summary"
SEL = 'tags_snmp_group=~"$snmp_group", provider=~"$provider", device_name=~"$device_name"'
DEV = 'device_name=~"$device"'


def ds_var(name: str, query: str, current: str) -> dict:
    return {
        "name": name,
        "type": "datasource",
        "query": query,
        "current": {"text": current, "value": current},
        "hide": 0,
        "includeAll": False,
        "multi": False,
        "options": [],
        "refresh": 1,
    }


def query_var(
    name: str,
    label: str,
    qry: str,
    *,
    include_all: bool = True,
    multi: bool = True,
    hide: int = 0,
) -> dict:
    current = (
        {"text": "All", "value": "$__all", "selected": True}
        if include_all
        else {"text": "", "value": ""}
    )
    return {
        "name": name,
        "label": label,
        "type": "query",
        "datasource": PROM,
        "definition": qry,
        "query": qry,
        "refresh": 2,
        "includeAll": include_all,
        "multi": multi,
        "allValue": ".*",
        "current": current,
        "sort": 1,
        "hide": hide,
    }


def grid(x: int, y: int, w: int, h: int) -> dict:
    return {"h": h, "w": w, "x": x, "y": y}


def prom_target(expr: str, ref: str = "A", legend: str = "", *, instant: bool = False) -> dict:
    t = {
        "datasource": PROM,
        "editorMode": "code",
        "expr": expr,
        "refId": ref,
        "legendFormat": legend or "__auto",
        "range": not instant,
        "instant": instant,
    }
    return t


def loki_target(expr: str, ref: str = "A") -> dict:
    return {
        "datasource": LOKI,
        "editorMode": "code",
        "expr": expr,
        "queryType": "range",
        "refId": ref,
    }


def infinity_url(path: str, root: str, columns: list[dict], ref: str = "A") -> dict:
    return {
        "datasource": INF,
        "refId": ref,
        "type": "json",
        "source": "url",
        "url": path,
        "url_options": {"method": "GET", "data": "", "params": []},
        "format": "table",
        "parser": "backend",
        "root_selector": root,
        "columns": columns,
        "filters": [],
    }


def row(pid: int, title: str, y: int, collapsed: bool = False) -> dict:
    return {
        "id": pid,
        "type": "row",
        "title": title,
        "gridPos": grid(0, y, 24, 1),
        "collapsed": collapsed,
        "panels": [],
    }


def thresholds(*steps: tuple[float | None, str]) -> dict:
    return {
        "mode": "absolute",
        "steps": [{"color": color, "value": value} for value, color in steps],
    }


def stat(
    pid: int,
    title: str,
    expr: str,
    pos: dict,
    unit: str = "none",
    *,
    description: str = "",
    steps: tuple | None = None,
) -> dict:
    steps = steps or ((None, "green"), (1, "orange"), (5, "red"))
    panel = {
        "id": pid,
        "type": "stat",
        "title": title,
        "description": description,
        "gridPos": pos,
        "datasource": PROM,
        "targets": [prom_target(expr, instant=False)],
        "options": {
            "reduceOptions": {"calcs": ["lastNotNull"], "fields": "", "values": False},
            "colorMode": "value",
            "graphMode": "area",
            "justifyMode": "auto",
            "textMode": "auto",
        },
        "fieldConfig": {
            "defaults": {"unit": unit, "thresholds": thresholds(*steps)},
            "overrides": [],
        },
    }
    return panel


def timeseries(pid: int, title: str, targets: list[dict], pos: dict, unit: str = "short", *, description: str = "") -> dict:
    wide = pos.get("w", 12) >= 17
    return {
        "id": pid,
        "type": "timeseries",
        "title": title,
        "description": description,
        "gridPos": pos,
        "datasource": PROM,
        "targets": targets,
        "fieldConfig": {
            "defaults": {
                "unit": unit,
                "min": 0,
                "custom": {
                    "drawStyle": "line",
                    "lineWidth": 2 if wide else 1,
                    "fillOpacity": 10,
                    "spanNulls": 600000,
                    "stacking": {"mode": "none"},
                },
            },
            "overrides": [],
        },
        "options": {
            "legend": {
                "displayMode": "table" if wide else "list",
                "placement": "right" if wide else "bottom",
                "calcs": ["min", "mean", "max"] if wide else [],
            },
            "tooltip": {"mode": "multi" if wide else "single"},
        },
    }


def bargauge(pid: int, title: str, expr: str, pos: dict, unit: str = "percent", *, description: str = "") -> dict:
    return {
        "id": pid,
        "type": "bargauge",
        "title": title,
        "description": description,
        "gridPos": pos,
        "datasource": PROM,
        "targets": [prom_target(expr, "A", "{{device_name}}", instant=True)],
        "options": {
            "reduceOptions": {"calcs": ["lastNotNull"], "fields": "", "values": False},
            "orientation": "horizontal",
            "displayMode": "gradient",
            "showUnfilled": True,
        },
        "fieldConfig": {
            "defaults": {
                "unit": unit,
                "min": 0,
                "max": 100 if unit == "percent" else None,
                "thresholds": thresholds((None, "green"), (70, "orange"), (85, "red")),
            },
            "overrides": [],
        },
    }


def table(pid: int, title: str, datasource: dict, targets: list[dict], pos: dict, *, transformations: list | None = None, description: str = "", overrides: list | None = None) -> dict:
    if transformations is None:
        transformations = identity_first_from_targets(targets)
    return {
        "id": pid,
        "type": "table",
        "title": title,
        "description": description,
        "gridPos": pos,
        "datasource": datasource,
        "targets": targets,
        "transformations": transformations,
        "options": {"showHeader": True, "cellHeight": "sm", "footer": {"show": False}},
        "fieldConfig": {"defaults": {}, "overrides": overrides or []},
    }


def logs(pid: int, title: str, expr: str, pos: dict, *, description: str = "") -> dict:
    return {
        "id": pid,
        "type": "logs",
        "title": title,
        "description": description,
        "gridPos": pos,
        "datasource": LOKI,
        "targets": [loki_target(expr)],
        "options": {"showTime": True, "showLabels": True, "wrapLogMessage": True},
    }


def alertlist(pid: int, title: str, pos: dict) -> dict:
    return {
        "id": pid,
        "type": "alertlist",
        "title": title,
        "description": "Firing and pending instances from Workshop / campus.",
        "gridPos": pos,
        "options": {
            "viewMode": "list",
            "groupMode": "default",
            "groupBy": [],
            "maxItems": 20,
            "sortOrder": 3,
            "dashboardAlerts": False,
            "alertName": "",
            "folderUID": "workshop-network",
            "alertInstanceLabelFilter": '{source="workshop"}',
            "stateFilter": {
                "firing": True,
                "pending": True,
                "noData": False,
                "normal": False,
                "error": False,
            },
        },
    }


# Friendly identifiers stay leftmost. Unindexed leftover fields otherwise jump to col 0.
IDENTITY_FIRST = (
    "Device",
    "Interface",
    "Sensor",
    "Src device",
    "Dst device",
    "Src",
    "Dst",
    "Building",
    "Site",
)


def column_index(*names: str) -> dict[str, int]:
    seen: list[str] = []
    for ident in IDENTITY_FIRST:
        if ident in names and ident not in seen:
            seen.append(ident)
    for name in names:
        if name not in seen:
            seen.append(name)
    return {name: i for i, name in enumerate(seen)}


def organize(rename: dict[str, str], exclude: list[str]) -> dict:
    return {
        "id": "organize",
        "options": {
            "excludeByName": {k: True for k in exclude},
            "renameByName": rename,
            "indexByName": column_index(*rename.values()),
        },
    }


def identity_first_from_targets(targets: list[dict]) -> list[dict]:
    """Pin Infinity columns in the order we declared (device / interface first)."""
    titles: list[str] = []
    raw: list[str] = []
    for target in targets:
        for col in target.get("columns") or []:
            title = col.get("text") or ""
            selector = col.get("selector") or ""
            if title:
                titles.append(title)
            if selector and selector != title:
                raw.append(selector)
    if not titles:
        return []
    leftovers = ["id", "type", "platform"]
    exclude = [name for name in leftovers + raw if name not in titles]
    return [
        {
            "id": "organize",
            "options": {
                "excludeByName": {name: True for name in exclude},
                "renameByName": {},
                "indexByName": column_index(*titles),
            },
        }
    ]


def series_table_transforms(rename: dict[str, str], extra_exclude: list[str] | None = None) -> list:
    hide = [
        "Time",
        "Index",
        "__name__",
        "job",
        "deployment_host",
        "service_name",
        "src_addr",
        "tags_container_service",
        "instrumentation_name",
        "tags_snmp_group",
    ] + (extra_exclude or [])
    return [
        {"id": "labelsToFields", "options": {"mode": "columns"}},
        {"id": "merge", "options": {}},
        organize(rename, hide),
    ]


def device_link_override() -> dict:
    return {
        "matcher": {"id": "byName", "options": "Device"},
        "properties": [
            {
                "id": "links",
                "value": [
                    {
                        "title": "Device details",
                        "url": (
                            f"/d/{DETAIL_UID}"
                            "?var-device=${__data.fields.Device}"
                            "&var-datasource=${datasource}"
                            "&var-loki=${loki}"
                            "&from=${__from}&to=${__to}"
                        ),
                    }
                ],
            }
        ],
    }


def summary_templating() -> dict:
    return {
        "list": [
            ds_var("datasource", "prometheus", "grafanacloud-prom"),
            ds_var("loki", "loki", "grafanacloud-logs"),
            ds_var("infinity", "yesoreyeram-infinity-datasource", "workshop-network-apis"),
            query_var(
                "snmp_group",
                "SNMP group",
                'label_values(kentik_snmp_PollingHealth{service_name="ktranslate-snmp-workshop"}, tags_snmp_group)',
            ),
            query_var(
                "provider",
                "Provider",
                f'label_values(kentik_snmp_PollingHealth{{{SEL}}}, provider)',
            ),
            query_var(
                "device_name",
                "Device",
                f'label_values(kentik_snmp_PollingHealth{{{SEL}}}, device_name)',
            ),
        ]
    }


def details_templating() -> dict:
    return {
        "list": [
            ds_var("datasource", "prometheus", "grafanacloud-prom"),
            ds_var("loki", "loki", "grafanacloud-logs"),
            query_var(
                "device",
                "Device",
                'label_values(kentik_snmp_PollingHealth{service_name="ktranslate-snmp-workshop"}, device_name)',
                include_all=False,
                multi=False,
            ),
            query_var(
                "interface",
                "Interface",
                f'label_values(kentik_snmp_if_OperStatus{{{DEV}}}, if_interface_name)',
                include_all=True,
                multi=True,
            ),
        ]
    }


def summary() -> dict:
    hide_meta = ["Time", "__name__", "tags_snmp_group"]
    device_table_rename = {
        "device_name": "Device",
        "provider": "Provider",
        "tags_kentik_model": "Model",
        "Value #A": "CPU %",
        "Value #B": "Memory %",
        "Value #C": "Poll",
        "Value #D": "Errors/s",
        "Value #E": "bps",
    }
    err_rename = {
        "device_name": "Device",
        "if_interface_name": "Interface",
        "if_Alias": "Alias",
        "Value": "Errors/s",
    }
    util_rename = {
        "device_name": "Device",
        "if_interface_name": "Interface",
        "if_Alias": "Alias",
        "Value": "bps",
    }
    cols_prtg = [
        {"selector": "device", "text": "Device", "type": "string"},
        {"selector": "name", "text": "Sensor", "type": "string"},
        {"selector": "status", "text": "Status", "type": "string"},
        {"selector": "last_message", "text": "Message", "type": "string"},
        {"selector": "vendor", "text": "Vendor", "type": "string"},
    ]
    panels = [
        row(1, "Fleet Alerts", 0),
        alertlist(2, "Active Network Alerts", grid(0, 1, 24, 7)),
        row(3, "Fleet Overview", 8),
        stat(
            4,
            "Total Devices",
            f'count(count by(device_name) (kentik_snmp_PollingHealth{{{SEL}}})) or vector(0)',
            grid(0, 9, 6, 4),
            description="Unique devices reporting SNMP polling health",
            steps=((None, "red"), (1, "green")),
        ),
        stat(
            5,
            "Interfaces Down",
            f'count(kentik_snmp_if_OperStatus{{{SEL}}} == 2) or vector(0)',
            grid(6, 9, 6, 4),
            description="Oper-down interfaces across the filtered fleet",
            steps=((None, "green"), (1, "orange"), (5, "red")),
        ),
        stat(
            6,
            "Avg Fleet CPU",
            f'avg(max by(device_name) (kentik_snmp_CPU{{{SEL}}}))',
            grid(12, 9, 6, 4),
            "percent",
            description="Average of each device's CPU",
            steps=((None, "green"), (70, "orange"), (85, "red")),
        ),
        stat(
            7,
            "Total Fleet Traffic",
            f'sum((kentik_snmp_ifHCInOctets{{{SEL}}} + kentik_snmp_ifHCOutOctets{{{SEL}}}) * 8 / 60)',
            grid(18, 9, 6, 4),
            "bps",
            description="Sum of in+out bits/sec (ktranslate 60s delta gauges)",
            steps=((None, "green"),),
        ),
        row(8, "Device Status", 13),
        table(
            9,
            "Device Status",
            PROM,
            [
                prom_target(
                    f"max by(device_name, provider, tags_kentik_model) (kentik_snmp_CPU{{{SEL}}})",
                    "A",
                    instant=True,
                ),
                prom_target(
                    f"max by(device_name) (kentik_snmp_MemoryUtilization{{{SEL}}})",
                    "B",
                    instant=True,
                ),
                prom_target(
                    f"max by(device_name) (kentik_snmp_PollingHealth{{{SEL}}})",
                    "C",
                    instant=True,
                ),
                prom_target(
                    f"sum by(device_name) (kentik_snmp_ifInErrors{{{SEL}}} / 60)",
                    "D",
                    instant=True,
                ),
                prom_target(
                    f"sum by(device_name) ((kentik_snmp_ifHCInOctets{{{SEL}}} + kentik_snmp_ifHCOutOctets{{{SEL}}}) * 8 / 60)",
                    "E",
                    instant=True,
                ),
            ],
            grid(0, 14, 24, 10),
            description="Click Device to open the detail view.",
            transformations=series_table_transforms(device_table_rename, hide_meta),
            overrides=[device_link_override()],
        ),
        row(10, "Resources", 24),
        bargauge(
            11,
            "Current CPU by Device",
            f"max by(device_name) (kentik_snmp_CPU{{{SEL}}})",
            grid(0, 25, 7, 8),
        ),
        timeseries(
            12,
            "CPU Utilization Over Time",
            [prom_target(f"max by(device_name) (kentik_snmp_CPU{{{SEL}}})", "A", "{{device_name}}")],
            grid(7, 25, 17, 8),
            "percent",
        ),
        bargauge(
            13,
            "Memory by Device",
            f"max by(device_name) (kentik_snmp_MemoryUtilization{{{SEL}}})",
            grid(0, 33, 7, 8),
        ),
        timeseries(
            14,
            "Memory Utilization Over Time",
            [prom_target(f"max by(device_name) (kentik_snmp_MemoryUtilization{{{SEL}}})", "A", "{{device_name}}")],
            grid(7, 33, 17, 8),
            "percent",
        ),
        row(15, "Interfaces", 41),
        table(
            16,
            "Top Interface Errors",
            PROM,
            [
                prom_target(
                    f"topk(10, sum by(device_name, if_interface_name, if_Alias) (kentik_snmp_ifInErrors{{{SEL}}} / 60))",
                    "A",
                    instant=True,
                )
            ],
            grid(0, 42, 12, 8),
            description="In errors/s (ktranslate 60s delta). Click Device for details.",
            transformations=series_table_transforms(err_rename, hide_meta),
            overrides=[device_link_override()],
        ),
        table(
            17,
            "Top Interface Utilization",
            PROM,
            [
                prom_target(
                    f"topk(10, sum by(device_name, if_interface_name, if_Alias) ((kentik_snmp_ifHCInOctets{{{SEL}}} + kentik_snmp_ifHCOutOctets{{{SEL}}}) * 8 / 60))",
                    "A",
                    instant=True,
                )
            ],
            grid(12, 42, 12, 8),
            description="Combined in+out bps. Click Device for details.",
            transformations=series_table_transforms(util_rename, hide_meta),
            overrides=[device_link_override()],
        ),
        row(18, "Events", 50),
        {
            **timeseries(
                19,
                "Syslog Volume by Device",
                [
                    {
                        **loki_target(
                            'sum by(device_name) (count_over_time({service_name="ktranslate-syslog-workshop"} | json | device_name=~"$device_name" [$__interval]))'
                        ),
                        "legendFormat": "{{device_name}}",
                    }
                ],
                grid(0, 51, 12, 8),
                "ops",
                description="Device syslog rate from the workshop collector.",
            ),
            "datasource": LOKI,
        },
        logs(
            20,
            "Recent Device Syslog",
            '{service_name="ktranslate-syslog-workshop"} | json | device_name=~"$device_name"',
            grid(12, 51, 12, 8),
        ),
        row(21, "Controller APIs (Infinity)", 59),
        table(
            22,
            "PRTG sensors",
            INF,
            [infinity_url("/prtg/api/v2/sensors", "sensors", cols_prtg)],
            grid(0, 60, 8, 8),
            description="Mock PRTG. Open Workshop PRTG Summary for the full page.",
            overrides=[device_link_override()],
        ),
        table(
            23,
            "Check Point gateways",
            INF,
            [infinity_url("/checkpoint/gateways", "gateways", [
                {"selector": "name", "text": "Device", "type": "string"},
                {"selector": "hardware", "text": "Model", "type": "string"},
                {"selector": "status", "text": "Status", "type": "string"},
                {"selector": "cpu", "text": "CPU", "type": "number"},
            ])],
            grid(8, 60, 8, 8),
            overrides=[device_link_override()],
        ),
        table(
            24,
            "Aruba EdgeConnect",
            INF,
            [infinity_url("/edgeconnect/appliances", "appliances", [
                {"selector": "hostName", "text": "Device", "type": "string"},
                {"selector": "site", "text": "Site", "type": "string"},
                {"selector": "state", "text": "State", "type": "string"},
                {"selector": "role", "text": "Role", "type": "string"},
            ])],
            grid(16, 60, 8, 8),
            overrides=[device_link_override()],
        ),
    ]
    return {
        "uid": SUMMARY_UID,
        "title": "Workshop Device Summary",
        "description": (
            "Fleet overview of the workshop campus (ktranslate-shaped SNMP). "
            "Start at alerts, then click a device to open Device Details."
        ),
        "tags": ["workshop", "network-o11y", "ktranslate"],
        "timezone": "browser",
        "schemaVersion": 39,
        "version": 1,
        "refresh": "30s",
        "editable": True,
        "graphTooltip": 1,
        "time": {"from": "now-1h", "to": "now"},
        "templating": summary_templating(),
        "panels": panels,
        "annotations": {"list": []},
        "links": [
            {
                "title": "Device Details",
                "type": "link",
                "url": f"/d/{DETAIL_UID}",
                "asDropdown": False,
                "icon": "dashboard",
            },
            {
                "title": "PRTG",
                "type": "link",
                "url": "/d/workshop-prtg-summary",
                "asDropdown": False,
                "icon": "cloud",
            },
            {
                "title": "Check Point",
                "type": "link",
                "url": "/d/workshop-checkpoint-summary",
                "asDropdown": False,
                "icon": "cloud",
            },
            {
                "title": "Aruba",
                "type": "link",
                "url": "/d/workshop-aruba-summary",
                "asDropdown": False,
                "icon": "cloud",
            },
        ],
        "fiscalYearStartMonth": 0,
    }


def details() -> dict:
    iface = f'{DEV}, if_interface_name=~"$interface"'
    iface_rename = {
        "if_interface_name": "Interface",
        "if_Alias": "Alias",
        "Value #A": "Oper",
        "Value #B": "Errors/s",
        "Value #C": "In bps",
        "Value #D": "Out bps",
    }
    panels = [
        row(1, "Overview", 0),
        stat(
            2,
            "Polling Health",
            f"max by(device_name) (kentik_snmp_PollingHealth{{{DEV}}})",
            grid(0, 1, 6, 4),
            description="1 = healthy",
            steps=((None, "red"), (1, "green")),
        ),
        stat(
            3,
            "CPU",
            f"max by(device_name) (kentik_snmp_CPU{{{DEV}}})",
            grid(6, 1, 6, 4),
            "percent",
            steps=((None, "green"), (70, "orange"), (85, "red")),
        ),
        stat(
            4,
            "Memory",
            f"max by(device_name) (kentik_snmp_MemoryUtilization{{{DEV}}})",
            grid(12, 1, 6, 4),
            "percent",
            steps=((None, "green"), (80, "orange"), (90, "red")),
        ),
        stat(
            5,
            "Interface Errors",
            f"sum(kentik_snmp_ifInErrors{{{DEV}}} / 60)",
            grid(18, 1, 6, 4),
            "eps",
            description="Device-wide in errors/s",
            steps=((None, "green"), (1, "orange"), (5, "red")),
        ),
        timeseries(
            6,
            "CPU Over Time",
            [prom_target(f"max by(device_name) (kentik_snmp_CPU{{{DEV}}})", "A", "{{device_name}}")],
            grid(0, 5, 12, 8),
            "percent",
        ),
        timeseries(
            7,
            "Memory Over Time",
            [prom_target(f"max by(device_name) (kentik_snmp_MemoryUtilization{{{DEV}}})", "A", "{{device_name}}")],
            grid(12, 5, 12, 8),
            "percent",
        ),
        row(8, "Interfaces", 13),
        table(
            9,
            "Interface Status",
            PROM,
            [
                prom_target(
                    f"max by(if_interface_name, if_Alias) (kentik_snmp_if_OperStatus{{{iface}}})",
                    "A",
                    instant=True,
                ),
                prom_target(
                    f"sum by(if_interface_name) (kentik_snmp_ifInErrors{{{iface}}} / 60)",
                    "B",
                    instant=True,
                ),
                prom_target(
                    f"sum by(if_interface_name) ((kentik_snmp_ifHCInOctets{{{iface}}}) * 8 / 60)",
                    "C",
                    instant=True,
                ),
                prom_target(
                    f"sum by(if_interface_name) ((kentik_snmp_ifHCOutOctets{{{iface}}}) * 8 / 60)",
                    "D",
                    instant=True,
                ),
            ],
            grid(0, 14, 24, 8),
            description="Oper 1 = up. Sort Errors/s or bps to find the outlier.",
            transformations=series_table_transforms(iface_rename, ["Time", "device_name"]),
        ),
        timeseries(
            10,
            "Interface Traffic In",
            [
                prom_target(
                    f"sum by(if_interface_name) ((kentik_snmp_ifHCInOctets{{{iface}}}) * 8 / 60)",
                    "A",
                    "{{if_interface_name}}",
                )
            ],
            grid(0, 22, 12, 8),
            "bps",
        ),
        timeseries(
            11,
            "Interface Traffic Out",
            [
                prom_target(
                    f"sum by(if_interface_name) ((kentik_snmp_ifHCOutOctets{{{iface}}}) * 8 / 60)",
                    "B",
                    "{{if_interface_name}}",
                )
            ],
            grid(12, 22, 12, 8),
            "bps",
        ),
        timeseries(
            12,
            "Interface Errors In",
            [
                prom_target(
                    f"sum by(if_interface_name) (kentik_snmp_ifInErrors{{{iface}}} / 60)",
                    "A",
                    "{{if_interface_name}}",
                )
            ],
            grid(0, 30, 12, 8),
            "eps",
        ),
        timeseries(
            13,
            "Interface Errors Out",
            [
                prom_target(
                    f"sum by(if_interface_name) (kentik_snmp_ifOutErrors{{{iface}}} / 60)",
                    "B",
                    "{{if_interface_name}}",
                )
            ],
            grid(12, 30, 12, 8),
            "eps",
        ),
        row(14, "Events", 38),
        logs(
            15,
            "Device Syslog",
            '{service_name="ktranslate-syslog-workshop"} | json | device_name=~"$device"',
            grid(0, 39, 24, 10),
            description="Forwarded syslog for the selected device.",
        ),
    ]
    return {
        "uid": DETAIL_UID,
        "title": "Workshop Device Details",
        "description": (
            "Single-device health for the workshop campus. "
            "Opened from Device Summary via the Device column."
        ),
        "tags": ["workshop", "network-o11y", "ktranslate"],
        "timezone": "browser",
        "schemaVersion": 39,
        "version": 1,
        "refresh": "30s",
        "editable": True,
        "graphTooltip": 1,
        "time": {"from": "now-1h", "to": "now"},
        "templating": details_templating(),
        "panels": panels,
        "annotations": {"list": []},
        "links": [
            {
                "title": "Device Summary",
                "type": "link",
                "url": f"/d/{SUMMARY_UID}",
                "asDropdown": False,
                "icon": "dashboard",
            },
            {
                "title": "PRTG",
                "type": "link",
                "url": "/d/workshop-prtg-summary",
                "asDropdown": False,
                "icon": "cloud",
            },
            {
                "title": "Check Point",
                "type": "link",
                "url": "/d/workshop-checkpoint-summary",
                "asDropdown": False,
                "icon": "cloud",
            },
            {
                "title": "Aruba",
                "type": "link",
                "url": "/d/workshop-aruba-summary",
                "asDropdown": False,
                "icon": "cloud",
            },
        ],
        "fiscalYearStartMonth": 0,
    }


def skeleton() -> dict:
    hint = (
        "This board is yours. Add panels after you have used Summary → Details.\n\n"
        "Ideas: an alert list, a device table with a drill-down, or Infinity "
        "`/meraki/devices` next to `kentik_snmp_CPU`."
    )
    return {
        "uid": "workshop-my-noc",
        "title": "My NOC view",
        "tags": ["workshop", "network-o11y", "lab4"],
        "timezone": "browser",
        "schemaVersion": 39,
        "version": 1,
        "refresh": "10s",
        "editable": True,
        "graphTooltip": 1,
        "time": {"from": "now-30m", "to": "now"},
        "templating": {
            "list": [
                ds_var("datasource", "prometheus", "grafanacloud-prom"),
                ds_var("loki", "loki", "grafanacloud-logs"),
                ds_var("infinity", "yesoreyeram-infinity-datasource", "workshop-network-apis"),
            ]
        },
        "panels": [
            {
                "id": 1,
                "type": "text",
                "title": "Build this",
                "gridPos": grid(0, 0, 24, 5),
                "options": {"mode": "markdown", "content": hint},
            }
        ],
        "annotations": {"list": []},
        "links": [],
        "fiscalYearStartMonth": 0,
    }


def main() -> None:
    import integrations
    import facilitator

    for name, builder in (
        ("device-summary.json", summary),
        ("device-details.json", details),
        ("my-noc-view.json", skeleton),
        ("prtg-summary.json", integrations.prtg_summary),
        ("checkpoint-summary.json", integrations.checkpoint_summary),
        ("aruba-summary.json", integrations.aruba_summary),
        ("facilitator-control.json", facilitator.facilitator_control),
    ):
        path = OUT / name
        path.write_text(json.dumps(builder(), indent=2) + "\n", encoding="utf-8")
        print(f"wrote {path}")


if __name__ == "__main__":
    main()
