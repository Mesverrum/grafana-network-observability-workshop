"""Shared campus inventory for mocks, generator, and dashboard copy.

Building 4 is the workshop fault. Flip `fault_active` in the mock admin API
or pass --fault on the generator; both should tell the same story.

Estate flavor: PRTG over Cisco, Check Point firewalls, Aruba EdgeConnect SD-WAN.
Meraki is the Infinity Lab 5 controller. FortiGate paths stay as aliases.
"""

from __future__ import annotations

TICKET = "Users in Building 4 are slow."
SNMP_GROUP = "campus"
SERVICE_NAME = "ktranslate-snmp-workshop"
SYSLOG_SERVICE = "ktranslate-syslog-workshop"

DEVICES = [
    {
        "name": "dc-core-01",
        "ip": "10.0.0.1",
        "role": "core",
        "building": "dc",
        "provider": "cisco",
        "model": "Nexus 93180YC-EX",
        "cpu": 18.0,
        "mem": 34.0,
        "healthy": True,
    },
    {
        "name": "wan-edge-01",
        "ip": "10.0.1.1",
        "role": "sdwan",
        "building": "dc",
        "provider": "aruba",
        "model": "EdgeConnect EC-M-H",
        "cpu": 22.0,
        "mem": 41.0,
        "healthy": True,
    },
    {
        "name": "bld1-asw-01",
        "ip": "10.1.0.10",
        "role": "access",
        "building": "bld1",
        "provider": "cisco",
        "model": "Catalyst 9300-48P",
        "cpu": 12.0,
        "mem": 28.0,
        "healthy": True,
    },
    {
        "name": "bld2-asw-01",
        "ip": "10.2.0.10",
        "role": "access",
        "building": "bld2",
        "provider": "cisco",
        "model": "Catalyst 9300-48P",
        "cpu": 14.0,
        "mem": 30.0,
        "healthy": True,
    },
    {
        "name": "bld3-asw-01",
        "ip": "10.3.0.10",
        "role": "access",
        "building": "bld3",
        "provider": "cisco",
        "model": "Catalyst 9300-48P",
        "cpu": 11.0,
        "mem": 27.0,
        "healthy": True,
    },
    {
        "name": "bld4-asw-01",
        "ip": "10.4.0.10",
        "role": "access",
        "building": "bld4",
        "provider": "cisco",
        "model": "Catalyst 9300-48P",
        "cpu": 19.0,
        "mem": 33.0,
        "healthy": True,
        "fault": "crc_uplink",
    },
    {
        "name": "bld4-fw-01",
        "ip": "10.4.0.1",
        "role": "firewall",
        "building": "bld4",
        "provider": "checkpoint",
        "model": "Quantum 6200",
        "cpu": 24.0,
        "mem": 38.0,
        "healthy": True,
        "fault": "cpu_sessions",
    },
    {
        "name": "bld4-wlc-01",
        "ip": "10.4.0.5",
        "role": "wlc",
        "building": "bld4",
        "provider": "cisco",
        "model": "C9800-L",
        "cpu": 16.0,
        "mem": 29.0,
        "healthy": True,
    },
]

# Interfaces used by the generator and Path A dashboards.
INTERFACES = {
    "dc-core-01": [
        ("Eth1/1", "Uplink-WAN", "up", "normal"),
        ("Eth1/48", "To-Bld4", "up", "normal"),
    ],
    "wan-edge-01": [
        ("wan0", "Underlay-ISP-A", "up", "normal"),
        ("lan0", "Campus", "up", "normal"),
        ("tun0", "Overlay-Bld4", "up", "overlay"),
    ],
    "bld1-asw-01": [
        ("Gi1/0/1", "Access", "up", "normal"),
        ("Gi1/0/48", "Uplink", "up", "normal"),
    ],
    "bld2-asw-01": [
        ("Gi1/0/1", "Access", "up", "normal"),
        ("Gi1/0/48", "Uplink", "up", "normal"),
    ],
    "bld3-asw-01": [
        ("Gi1/0/1", "Access", "up", "normal"),
        ("Gi1/0/48", "Uplink", "up", "normal"),
    ],
    "bld4-asw-01": [
        ("Gi1/0/1", "Access-closet", "up", "normal"),
        ("Gi1/0/24", "Access-IDF-B4", "up", "crc"),
        ("Gi1/0/48", "Uplink-to-core", "up", "saturated"),
    ],
    "bld4-fw-01": [
        ("eth1", "External", "up", "normal"),
        ("eth2", "Bld4-LAN", "up", "normal"),
    ],
    "bld4-wlc-01": [
        ("Gi0/0/1", "To-asw", "up", "normal"),
    ],
}

MERAKI_APS = [
    {"serial": "Q2XX-1A2B-0001", "name": "bld1-ap-01", "building": "bld1", "status": "online", "clients": 18},
    {"serial": "Q2XX-1A2B-0002", "name": "bld2-ap-04", "building": "bld2", "status": "online", "clients": 22},
    {"serial": "Q2XX-1A2B-0003", "name": "bld3-ap-02", "building": "bld3", "status": "online", "clients": 14},
    {"serial": "Q2XX-1A2B-0412", "name": "bld4-ap-12", "building": "bld4", "status": "online", "clients": 27, "fault": "offline"},
    {"serial": "Q2XX-1A2B-0413", "name": "bld4-ap-13", "building": "bld4", "status": "online", "clients": 9},
]

ARUBA_APS = [
    {"serial": "CN1234001", "name": "bld1-iap-01", "building": "bld1", "status": "Up", "clients": 11},
    {"serial": "CN1234042", "name": "bld4-iap-02", "building": "bld4", "status": "Up", "clients": 16, "fault": "Down"},
]

# Controller-only. Four gateways matches the Skyline story they already run.
CHECKPOINT_GATEWAYS = [
    {"name": "dc-fw-01", "ip": "10.0.0.2", "model": "Quantum 16200", "building": "dc", "cpu": 19.0, "sessions": 8420, "policy": "Standard"},
    {"name": "bld1-fw-01", "ip": "10.1.0.1", "model": "Quantum 6200", "building": "bld1", "cpu": 14.0, "sessions": 2100, "policy": "Standard"},
    {"name": "bld4-fw-01", "ip": "10.4.0.1", "model": "Quantum 6200", "building": "bld4", "cpu": 24.0, "sessions": 1840, "policy": "Standard", "fault": "cpu_sessions"},
    {"name": "wan-fw-01", "ip": "10.0.1.2", "model": "Quantum 6400", "building": "dc", "cpu": 21.0, "sessions": 4310, "policy": "VPN-Hub"},
]

# Orchestrator inventory. wan-edge-01 is also in SNMP; spokes are Infinity-only.
EDGECONNECT_APPLIANCES = [
    {
        "nePk": "0.NE.1",
        "name": "wan-edge-01",
        "model": "EC-M-H",
        "site": "dc",
        "role": "hub",
        "state": "normal",
        "ip": "10.0.1.1",
    },
    {
        "nePk": "4.NE.1",
        "name": "bld4-ec-01",
        "model": "EC-US-SMALL",
        "site": "bld4",
        "role": "spoke",
        "state": "normal",
        "ip": "10.4.1.1",
        "fault": "overlay_degraded",
    },
    {
        "nePk": "1.NE.1",
        "name": "bld1-ec-01",
        "model": "EC-US-SMALL",
        "site": "bld1",
        "role": "spoke",
        "state": "normal",
        "ip": "10.1.1.1",
    },
]


def device(name: str) -> dict:
    for d in DEVICES:
        if d["name"] == name:
            return d
    raise KeyError(name)
