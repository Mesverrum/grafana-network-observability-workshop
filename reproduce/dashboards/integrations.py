"""Infinity summary boards for the mock PRTG, Check Point, and Aruba APIs."""

from __future__ import annotations

import build as b

PRTG_UID = "workshop-prtg-summary"
CP_UID = "workshop-checkpoint-summary"
ARUBA_UID = "workshop-aruba-summary"


def inf_templating() -> dict:
    return {
        "list": [
            b.ds_var("infinity", "yesoreyeram-infinity-datasource", "workshop-network-apis"),
            b.ds_var("datasource", "prometheus", "grafanacloud-prom"),
            b.ds_var("loki", "loki", "grafanacloud-logs"),
        ]
    }


def workshop_links() -> list[dict]:
    return [
        {
            "title": "Device Summary",
            "type": "link",
            "url": f"/d/{b.SUMMARY_UID}",
            "asDropdown": False,
            "icon": "dashboard",
        },
        {
            "title": "Device Details",
            "type": "link",
            "url": f"/d/{b.DETAIL_UID}",
            "asDropdown": False,
            "icon": "dashboard",
        },
        {
            "title": "PRTG",
            "type": "link",
            "url": f"/d/{PRTG_UID}",
            "asDropdown": False,
            "icon": "cloud",
        },
        {
            "title": "Check Point",
            "type": "link",
            "url": f"/d/{CP_UID}",
            "asDropdown": False,
            "icon": "cloud",
        },
        {
            "title": "Aruba",
            "type": "link",
            "url": f"/d/{ARUBA_UID}",
            "asDropdown": False,
            "icon": "cloud",
        },
    ]


def markdown(pid: int, title: str, content: str, pos: dict) -> dict:
    return {
        "id": pid,
        "type": "text",
        "title": title,
        "gridPos": pos,
        "options": {"mode": "markdown", "content": content},
    }


def inf_stat(
    pid: int,
    title: str,
    path: str,
    field: str,
    pos: dict,
    *,
    description: str = "",
    unit: str = "none",
    steps: tuple | None = None,
) -> dict:
    steps = steps or ((None, "text"),)
    return {
        "id": pid,
        "type": "stat",
        "title": title,
        "description": description,
        "gridPos": pos,
        "datasource": b.INF,
        "targets": [
            b.infinity_url(
                path,
                "",
                [{"selector": field, "text": title, "type": "number"}],
            )
        ],
        "options": {
            "reduceOptions": {"calcs": ["lastNotNull"], "fields": "", "values": False},
            "colorMode": "value",
            "graphMode": "none",
            "justifyMode": "auto",
            "textMode": "auto",
        },
        "fieldConfig": {
            "defaults": {"unit": unit, "thresholds": b.thresholds(*steps)},
            "overrides": [],
        },
    }


def snmp_join(pid: int, title: str, provider: str, pos: dict) -> dict:
    return b.table(
        pid,
        title,
        b.PROM,
        [
            b.prom_target(
                f'max by(device_name) (kentik_snmp_CPU{{provider="{provider}"}})',
                instant=True,
            )
        ],
        pos,
        description="Same device names on the ktranslate-shaped SNMP path. Click Device for details.",
        transformations=b.series_table_transforms(
            {"device_name": "Device", "Value": "CPU %"}
        ),
        overrides=[b.device_link_override()],
    )


def _shell(uid: str, title: str, description: str, panels: list[dict]) -> dict:
    return {
        "uid": uid,
        "title": title,
        "description": description,
        "tags": ["workshop", "network-o11y", "infinity"],
        "timezone": "browser",
        "schemaVersion": 39,
        "version": 1,
        "refresh": "30s",
        "editable": True,
        "graphTooltip": 1,
        "time": {"from": "now-1h", "to": "now"},
        "templating": inf_templating(),
        "panels": panels,
        "annotations": {"list": []},
        "links": workshop_links(),
        "fiscalYearStartMonth": 0,
    }


def prtg_summary() -> dict:
    cols = [
        {"selector": "device", "text": "Device", "type": "string"},
        {"selector": "name", "text": "Sensor", "type": "string"},
        {"selector": "building", "text": "Building", "type": "string"},
        {"selector": "type", "text": "Type", "type": "string"},
        {"selector": "status", "text": "Status", "type": "string"},
        {"selector": "last_message", "text": "Last message", "type": "string"},
        {"selector": "vendor", "text": "Vendor", "type": "string"},
        {"selector": "model", "text": "Model", "type": "string"},
    ]
    panels = [
        b.row(1, "Overview", 0),
        markdown(
            2,
            "What this is",
            (
                "Infinity against the workshop **PRTG** mock (`/prtg/api/v2/sensors`).\n\n"
                "Same skill as their NMS API — JSON in, table out. Click a device to "
                "open the SNMP Device Details board."
            ),
            b.grid(0, 1, 8, 5),
        ),
        inf_stat(
            3,
            "Sensors",
            "/prtg/api/v2/sensors",
            "count",
            b.grid(8, 1, 5, 5),
            description="`count` on GET /prtg/api/v2/sensors",
        ),
        inf_stat(
            4,
            "Alarms",
            "/prtg/api/v2/sensors",
            "problems",
            b.grid(13, 1, 5, 5),
            description="Sensors not Up",
            steps=((None, "green"), (1, "orange"), (3, "red")),
        ),
        inf_stat(
            5,
            "Alarms (alarms path)",
            "/prtg/api/v2/sensors/alarms",
            "count",
            b.grid(18, 1, 6, 5),
            description="GET /prtg/api/v2/sensors/alarms — PRTG v2-shaped",
            steps=((None, "green"), (1, "orange"), (3, "red")),
        ),
        b.row(6, "Sensors", 6),
        b.table(
            7,
            "All sensors",
            b.INF,
            [b.infinity_url("/prtg/api/v2/sensors", "sensors", cols)],
            b.grid(0, 7, 24, 10),
            description="GET /prtg/api/v2/sensors → sensors[]",
            overrides=[b.device_link_override()],
        ),
        b.table(
            8,
            "Alarms only",
            b.INF,
            [b.infinity_url("/prtg/api/v2/sensors/alarms", "sensors", cols)],
            b.grid(0, 17, 24, 8),
            description="GET /prtg/api/v2/sensors/alarms",
            overrides=[b.device_link_override()],
        ),
        b.row(9, "Same names over SNMP", 25),
        snmp_join(10, "Cisco (and others PRTG also polls)", "cisco", b.grid(0, 26, 24, 7)),
    ]
    return _shell(
        PRTG_UID,
        "Workshop PRTG Summary",
        "Mock PRTG sensor inventory via Infinity. Explore the NMS API, then join a name to SNMP.",
        panels,
    )


def checkpoint_summary() -> dict:
    gw_cols = [
        {"selector": "name", "text": "Device", "type": "string"},
        {"selector": "building", "text": "Building", "type": "string"},
        {"selector": "hardware", "text": "Model", "type": "string"},
        {"selector": "ipv4-address", "text": "IPv4", "type": "string"},
        {"selector": "status", "text": "Status", "type": "string"},
        {"selector": "cpu", "text": "CPU", "type": "number"},
        {"selector": "sessions", "text": "Sessions", "type": "number"},
        {"selector": "policy", "text": "Policy", "type": "string"},
        {"selector": "sic-status", "text": "SIC", "type": "string"},
    ]
    panels = [
        b.row(1, "Overview", 0),
        markdown(
            2,
            "What this is",
            (
                "Infinity against the workshop **Check Point** mock.\n\n"
                "`/checkpoint/gateways` is a convenience GET. "
                "`/checkpoint/web_api/show-gateways-and-servers` is the Management-shaped POST. "
                "Skyline on this mock is a status JSON — production Skyline is OTel, not REST."
            ),
            b.grid(0, 1, 8, 5),
        ),
        inf_stat(
            3,
            "Gateways",
            "/checkpoint/gateways",
            "count",
            b.grid(8, 1, 5, 5),
            description="GET /checkpoint/gateways",
        ),
        inf_stat(
            4,
            "Attention",
            "/checkpoint/gateways",
            "attention",
            b.grid(13, 1, 5, 5),
            description="status != OK",
            steps=((None, "green"), (1, "orange")),
        ),
        inf_stat(
            5,
            "Skyline objects",
            "/checkpoint/skyline/status",
            "gateways",
            b.grid(18, 1, 6, 5),
            description="GET /checkpoint/skyline/status → gateways",
        ),
        b.row(6, "Management inventory", 6),
        b.table(
            7,
            "Gateways",
            b.INF,
            [b.infinity_url("/checkpoint/gateways", "gateways", gw_cols)],
            b.grid(0, 7, 24, 9),
            description="GET /checkpoint/gateways → gateways[]",
            overrides=[b.device_link_override()],
        ),
        b.row(8, "Skyline status", 16),
        b.table(
            9,
            "Skyline objects",
            b.INF,
            [b.infinity_url("/checkpoint/skyline/status", "objects", gw_cols)],
            b.grid(0, 17, 16, 8),
            description="Same four gateways on the Skyline status document.",
            overrides=[b.device_link_override()],
        ),
        b.table(
            10,
            "FortiGate path alias",
            b.INF,
            [
                b.infinity_url(
                    "/fortigate/status",
                    "results",
                    [
                        {"selector": "hostname", "text": "Device", "type": "string"},
                        {"selector": "vendor", "text": "Vendor", "type": "string"},
                        {"selector": "version", "text": "Version", "type": "string"},
                        {"selector": "cpu", "text": "CPU", "type": "number"},
                        {"selector": "sessions", "text": "Sessions", "type": "number"},
                    ],
                )
            ],
            b.grid(16, 17, 8, 8),
            description="Leftover path — same box as bld4-fw-01.",
            overrides=[b.device_link_override()],
        ),
        b.row(11, "Same names over SNMP", 25),
        snmp_join(12, "Check Point over SNMP", "checkpoint", b.grid(0, 26, 24, 7)),
    ]
    return _shell(
        CP_UID,
        "Workshop Check Point Summary",
        "Mock Check Point gateways and Skyline status via Infinity.",
        panels,
    )


def aruba_summary() -> dict:
    ap_cols = [
        {"selector": "hostName", "text": "Device", "type": "string"},
        {"selector": "site", "text": "Site", "type": "string"},
        {"selector": "model", "text": "Model", "type": "string"},
        {"selector": "role", "text": "Role", "type": "string"},
        {"selector": "state", "text": "State", "type": "string"},
        {"selector": "ip", "text": "IP", "type": "string"},
        {"selector": "nePk", "text": "Network element ID", "type": "string"},
    ]
    tun_cols = [
        {"selector": "src", "text": "Src device", "type": "string"},
        {"selector": "dst", "text": "Dst device", "type": "string"},
        {"selector": "overlay", "text": "Overlay", "type": "string"},
        {"selector": "id", "text": "Tunnel", "type": "string"},
        {"selector": "state", "text": "State", "type": "string"},
        {"selector": "loss_pct", "text": "Loss %", "type": "number"},
        {"selector": "latency_ms", "text": "Latency ms", "type": "number"},
        {"selector": "note", "text": "Note", "type": "string"},
    ]
    central_cols = [
        {"selector": "name", "text": "Device", "type": "string"},
        {"selector": "building", "text": "Building", "type": "string"},
        {"selector": "serial", "text": "Serial", "type": "string"},
        {"selector": "model", "text": "Model", "type": "string"},
        {"selector": "status", "text": "Status", "type": "string"},
        {"selector": "client_count", "text": "Clients", "type": "number"},
    ]
    panels = [
        b.row(1, "Overview", 0),
        markdown(
            2,
            "What this is",
            (
                "Infinity against the workshop **Aruba EdgeConnect** mock "
                "(`/edgeconnect/gms/rest/appliance`).\n\n"
                "Central APs are a second Aruba API on the same datasource "
                "(`/aruba/monitoring/v2/aps`)."
            ),
            b.grid(0, 1, 8, 5),
        ),
        inf_stat(
            3,
            "Appliances",
            "/edgeconnect/appliances",
            "count",
            b.grid(8, 1, 4, 5),
        ),
        inf_stat(
            4,
            "Degraded",
            "/edgeconnect/appliances",
            "degraded",
            b.grid(12, 1, 4, 5),
            steps=((None, "green"), (1, "orange")),
        ),
        inf_stat(
            5,
            "Tunnels",
            "/edgeconnect/tunnels",
            "count",
            b.grid(16, 1, 4, 5),
        ),
        inf_stat(
            6,
            "Tunnel issues",
            "/edgeconnect/tunnels",
            "degraded",
            b.grid(20, 1, 4, 5),
            steps=((None, "green"), (1, "orange")),
        ),
        b.row(7, "Orchestrator", 6),
        b.table(
            8,
            "Appliances",
            b.INF,
            [b.infinity_url("/edgeconnect/appliances", "appliances", ap_cols)],
            b.grid(0, 7, 24, 8),
            description="GET /edgeconnect/appliances (alias of /gms/rest/appliance)",
            overrides=[b.device_link_override()],
        ),
        b.table(
            9,
            "Tunnels",
            b.INF,
            [b.infinity_url("/edgeconnect/tunnels", "tunnels", tun_cols)],
            b.grid(0, 15, 24, 7),
            description="GET /edgeconnect/tunnels",
        ),
        b.row(10, "Aruba Central", 22),
        inf_stat(
            11,
            "APs",
            "/aruba/aps",
            "count",
            b.grid(0, 23, 6, 4),
        ),
        inf_stat(
            12,
            "APs down",
            "/aruba/aps",
            "down",
            b.grid(6, 23, 6, 4),
            steps=((None, "green"), (1, "orange")),
        ),
        b.table(
            13,
            "Access points",
            b.INF,
            [b.infinity_url("/aruba/aps", "aps", central_cols)],
            b.grid(12, 23, 12, 8),
            description="GET /aruba/monitoring/v2/aps",
            overrides=[b.device_link_override()],
        ),
        b.row(14, "Same names over SNMP", 31),
        snmp_join(15, "Aruba over SNMP", "aruba", b.grid(0, 32, 24, 7)),
    ]
    return _shell(
        ARUBA_UID,
        "Workshop Aruba Summary",
        "Mock EdgeConnect appliances/tunnels and Central APs via Infinity.",
        panels,
    )
