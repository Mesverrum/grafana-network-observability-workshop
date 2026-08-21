"""Mock NMS and controller APIs for the network workshop.

Faithful-enough JSON so Infinity queries transfer to real PRTG v2, Check Point
Management / Skyline-ish status, Aruba EdgeConnect Orchestrator, plus the
existing SolarWinds / Zabbix / Meraki / FortiGate / Aruba Central shapes.
Building 4 degrades when fault_active is true (default).
"""

from __future__ import annotations

import sys
from pathlib import Path

from fastapi import FastAPI, Header, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from inventory import (  # noqa: E402
    ARUBA_APS,
    CHECKPOINT_GATEWAYS,
    DEVICES,
    EDGECONNECT_APPLIANCES,
    MERAKI_APS,
    TICKET,
)

app = FastAPI(title="Network workshop mocks", version="1.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

STATE = {"fault_active": True}


def fault() -> bool:
    return bool(STATE["fault_active"])


def tenant_of(x_workshop_tenant: str | None) -> str:
    return x_workshop_tenant or "default"


@app.get("/health")
def health() -> dict:
    return {"ok": True, "fault_active": fault(), "ticket": TICKET}


class FaultBody(BaseModel):
    active: bool


@app.post("/admin/fault")
def set_fault(body: FaultBody) -> dict:
    STATE["fault_active"] = body.active
    return {"fault_active": fault()}


@app.get("/admin/fault")
def get_fault() -> dict:
    return {"fault_active": fault()}


def _node_status(device: dict) -> str:
    if fault() and device.get("fault"):
        return "Warning" if device["fault"] == "crc_uplink" else "Critical"
    return "Up"


# --- SolarWinds SWIS-ish -------------------------------------------------


@app.get("/solarwinds/Query")
@app.get("/solarwinds/nodes")
def solarwinds_nodes(x_workshop_tenant: str | None = Header(default=None)) -> dict:
    results = []
    for d in DEVICES:
        status = _node_status(d)
        cpu = d["cpu"]
        if fault() and d.get("fault") == "cpu_sessions":
            cpu = 87.0
        results.append(
            {
                "Caption": d["name"],
                "IPAddress": d["ip"],
                "StatusDescription": status,
                "Vendor": d["provider"].title(),
                "MachineType": d["model"],
                "CPULoad": cpu,
                "MemoryUsed": d["mem"],
                "Building": d["building"],
                "Role": d["role"],
                "Tenant": tenant_of(x_workshop_tenant),
            }
        )
    return {"results": results}


@app.get("/solarwinds/alerts")
def solarwinds_alerts() -> dict:
    if not fault():
        return {"results": []}
    return {
        "results": [
            {
                "AlertName": "High interface errors",
                "EntityCaption": "bld4-asw-01 - Gi1/0/24",
                "Severity": "Warning",
                "Message": "CRC / ifInErrors rising on Access-IDF-B4",
                "Building": "bld4",
            },
            {
                "AlertName": "Uplink saturation",
                "EntityCaption": "bld4-asw-01 - Gi1/0/48",
                "Severity": "Warning",
                "Message": "Uplink-to-core above 90% for 12 minutes",
                "Building": "bld4",
            },
        ]
    }


# --- PRTG API v2-ish (primary NMS: Cisco campus) -------------------------


def _prtg_status(device: dict) -> tuple[str, str]:
    if fault() and device.get("fault") == "crc_uplink":
        return "Warning", "Errors on Gi1/0/24"
    if fault() and device.get("fault") == "cpu_sessions":
        return "Down", "CPU 87%"
    return "Up", "OK"


def _prtg_sensor(
    device: str,
    name: str,
    status: str,
    last_message: str,
    building: str,
    stype: str,
    vendor: str,
    model: str,
    *,
    sid: int | None = None,
) -> dict:
    return {
        "device": device,
        "name": name,
        "building": building,
        "status": status,
        "last_message": last_message,
        "type": stype,
        "vendor": vendor,
        "model": model,
        "id": sid if sid is not None else abs(hash(name)) % 100000,
    }


@app.get("/prtg/api/v2/sensors")
@app.get("/prtg/api/v2/objects")
@app.get("/prtg/sensors")
def prtg_sensors() -> dict:
    sensors = []
    for d in DEVICES:
        status, last = _prtg_status(d)
        sensors.append(
            _prtg_sensor(
                d["name"],
                f"{d['name']} ping",
                status,
                last,
                d["building"],
                "ping",
                d["provider"],
                d["model"],
            )
        )
        if d["provider"] == "cisco":
            sensors.append(
                _prtg_sensor(
                    d["name"],
                    f"{d['name']} SNMP CPU",
                    "Up",
                    f"{d['cpu']:.0f} %",
                    d["building"],
                    "snmpcpu",
                    "cisco",
                    d["model"],
                )
            )
    if fault():
        sensors.extend(
            [
                _prtg_sensor(
                    "bld4-asw-01",
                    "bld4-asw-01 Gi1/0/24 errors",
                    "Warning",
                    "CRC incrementing",
                    "bld4",
                    "snmptraffic",
                    "cisco",
                    "Catalyst 9300-48P",
                    sid=4124,
                ),
                _prtg_sensor(
                    "bld4-fw-01",
                    "bld4-fw-01 Check Point CPU",
                    "Down",
                    "CPU 87% — ticket would open in HEAT",
                    "bld4",
                    "snmpcustom",
                    "checkpoint",
                    "Quantum 6200",
                    sid=4125,
                ),
                _prtg_sensor(
                    "bld4-ec-01",
                    "bld4-ec-01 overlay tunnel",
                    "Warning",
                    "Overlay-Bld4 rekeys elevated",
                    "bld4",
                    "ping",
                    "aruba",
                    "EC-US-SMALL",
                    sid=4126,
                ),
            ]
        )
    problems = [s for s in sensors if s["status"] != "Up"]
    return {"sensors": sensors, "count": len(sensors), "problems": len(problems)}


@app.get("/prtg/api/v2/sensors/alarms")
@app.get("/prtg/alarms")
def prtg_alarms() -> dict:
    body = prtg_sensors()
    alarms = [s for s in body["sensors"] if s["status"] != "Up"]
    return {"sensors": alarms, "count": len(alarms)}


# --- Zabbix JSON-RPC -----------------------------------------------------


@app.post("/zabbix/api_jsonrpc.php")
async def zabbix_rpc(request: Request) -> dict:
    body = await request.json()
    method = body.get("method")
    req_id = body.get("id", 1)
    if method == "user.login":
        return {"jsonrpc": "2.0", "result": "workshop-fake-auth", "id": req_id}
    if method in ("host.get", "host.get"):
        hosts = []
        for d in DEVICES:
            hosts.append(
                {
                    "hostid": str(abs(hash(d["name"])) % 10000),
                    "host": d["name"],
                    "name": d["name"],
                    "status": "0",
                    "inventory": {"location": d["building"], "os": d["model"]},
                }
            )
        return {"jsonrpc": "2.0", "result": hosts, "id": req_id}
    if method == "trigger.get":
        triggers = []
        if fault():
            triggers = [
                {
                    "triggerid": "9001",
                    "description": "High CRC on {HOST.NAME} Gi1/0/24",
                    "priority": "3",
                    "value": "1",
                    "hosts": [{"host": "bld4-asw-01"}],
                },
                {
                    "triggerid": "9002",
                    "description": "Check Point CPU high on {HOST.NAME}",
                    "priority": "4",
                    "value": "1",
                    "hosts": [{"host": "bld4-fw-01"}],
                },
            ]
        return {"jsonrpc": "2.0", "result": triggers, "id": req_id}
    return {"jsonrpc": "2.0", "error": {"code": -32601, "message": f"unknown {method}"}, "id": req_id}


# --- Meraki --------------------------------------------------------------


@app.get("/meraki/api/v1/organizations/org-workshop/devices")
@app.get("/meraki/devices")
def meraki_devices() -> list:
    out = []
    for ap in MERAKI_APS:
        status = ap["status"]
        clients = ap["clients"]
        if fault() and ap.get("fault") == "offline":
            status, clients = "offline", 0
        out.append(
            {
                "serial": ap["serial"],
                "name": ap["name"],
                "model": "MR46",
                "status": status,
                "lanIp": "10.4.12.20" if "bld4" in ap["name"] else "10.1.12.20",
                "building": ap["building"],
                "clients": clients,
            }
        )
    return out


@app.get("/meraki/api/v1/organizations/org-workshop/devices/statuses")
def meraki_statuses() -> list:
    return meraki_devices()


# --- Check Point (Management-ish + Skyline status) -----------------------


def _checkpoint_gateways() -> list[dict]:
    out = []
    for gw in CHECKPOINT_GATEWAYS:
        cpu = gw["cpu"]
        sessions = gw["sessions"]
        status = "OK"
        if fault() and gw.get("fault") == "cpu_sessions":
            cpu, sessions, status = 87.0, 14220, "Attention"
        out.append(
            {
                "name": gw["name"],
                "building": gw["building"],
                "hardware": gw["model"],
                "ipv4-address": gw["ip"],
                "status": status,
                "cpu": cpu,
                "sessions": sessions,
                "policy": gw["policy"],
                "sic-status": "communicating",
                "type": "gateway",
            }
        )
    return out


@app.get("/checkpoint/gateways")
def checkpoint_gateways() -> dict:
    rows = _checkpoint_gateways()
    attention = [g for g in rows if g["status"] != "OK"]
    return {"gateways": rows, "count": len(rows), "attention": len(attention)}


@app.get("/checkpoint/skyline/status")
def checkpoint_skyline() -> dict:
    return {
        "exporter": "skyline",
        "otlp": True,
        "gateways": 4,
        "note": "Same four gateways they already send to Grafana. Cloud just ingests.",
        "objects": _checkpoint_gateways(),
    }


@app.post("/checkpoint/web_api/login")
def checkpoint_login() -> dict:
    return {"sid": "workshop-fake-sid", "api-server-version": "1.9"}


@app.post("/checkpoint/web_api/show-gateways-and-servers")
def checkpoint_show_gateways() -> dict:
    return {"objects": _checkpoint_gateways()}


# FortiGate paths stay as aliases so the Aug 18 dry-run board does not 404.
@app.get("/fortigate/api/v2/monitor/system/status")
@app.get("/fortigate/status")
def fortigate_status_alias() -> dict:
    gw = next(g for g in _checkpoint_gateways() if g["name"] == "bld4-fw-01")
    return {
        "results": {
            "hostname": gw["name"],
            "version": "R81.20",
            "cpu": gw["cpu"],
            "memory": 38,
            "sessions": gw["sessions"],
            "uptime": 1844221,
            "vendor": "checkpoint",
        }
    }


@app.get("/fortigate/api/v2/monitor/vpn/ipsec")
@app.get("/fortigate/vpn")
def fortigate_vpn_alias() -> dict:
    up = not fault()
    return {
        "results": [
            {
                "name": "bld4-to-dc",
                "status": "up" if up else "degraded",
                "incoming_bytes": 9_400_000_000,
                "outgoing_bytes": 8_100_000_000,
                "note": "rekeys elevated" if fault() else "stable",
                "vendor": "checkpoint",
            }
        ]
    }


# --- Aruba EdgeConnect Orchestrator --------------------------------------


def _ec_state(appliance: dict) -> str:
    if fault() and appliance.get("fault") == "overlay_degraded":
        return "degraded"
    return appliance["state"]


@app.get("/edgeconnect/appliances")
@app.get("/edgeconnect/gms/rest/appliance")
@app.get("/aruba/orchestrator/appliances")
def edgeconnect_appliances() -> dict:
    rows = []
    for a in EDGECONNECT_APPLIANCES:
        rows.append(
            {
                "hostName": a["name"],
                "site": a["site"],
                "role": a["role"],
                "model": a["model"],
                "ip": a["ip"],
                "state": _ec_state(a),
                "platform": "EdgeConnect",
                "nePk": a["nePk"],
            }
        )
    degraded = [r for r in rows if r["state"] != "normal"]
    return {"appliances": rows, "count": len(rows), "degraded": len(degraded)}


@app.get("/edgeconnect/tunnels")
@app.get("/edgeconnect/gms/rest/tunnels")
def edgeconnect_tunnels() -> dict:
    degraded = fault()
    tunnels = [
        {
            "src": "wan-edge-01",
            "dst": "bld1-ec-01",
            "overlay": "Overlay-Campus",
            "id": "dc-to-bld1",
            "state": "up",
            "loss_pct": 0.0,
            "latency_ms": 4,
        },
        {
            "src": "wan-edge-01",
            "dst": "bld4-ec-01",
            "overlay": "Overlay-Bld4",
            "id": "dc-to-bld4",
            "state": "degraded" if degraded else "up",
            "loss_pct": 2.4 if degraded else 0.1,
            "latency_ms": 48 if degraded else 6,
            "note": "rekeys elevated" if degraded else "stable",
        },
    ]
    bad = [t for t in tunnels if t["state"] != "up"]
    return {"tunnels": tunnels, "count": len(tunnels), "degraded": len(bad)}


# --- Aruba Central APs ---------------------------------------------------


@app.get("/aruba/monitoring/v2/aps")
@app.get("/aruba/aps")
def aruba_aps() -> dict:
    aps = []
    for ap in ARUBA_APS:
        status = ap["status"]
        clients = ap["clients"]
        if fault() and ap.get("fault") == "Down":
            status, clients = "Down", 0
        aps.append(
            {
                "name": ap["name"],
                "building": ap["building"],
                "serial": ap["serial"],
                "model": "AP-635",
                "status": status,
                "client_count": clients,
            }
        )
    down = [a for a in aps if a["status"] != "Up"]
    return {"aps": aps, "count": len(aps), "down": len(down)}


@app.get("/")
def index() -> dict:
    return {
        "ticket": TICKET,
        "fault_active": fault(),
        "paths": {
            "prtg": "/prtg/api/v2/sensors",
            "checkpoint": "/checkpoint/gateways",
            "skyline": "/checkpoint/skyline/status",
            "edgeconnect": "/edgeconnect/appliances",
            "edgeconnect_tunnels": "/edgeconnect/tunnels",
            "meraki": "/meraki/devices",
            "solarwinds": "/solarwinds/nodes",
            "zabbix": "POST /zabbix/api_jsonrpc.php",
            "fortigate_alias": "/fortigate/status",
            "aruba_aps": "/aruba/aps",
            "fault": "POST /admin/fault {\"active\": true|false}",
        },
    }
