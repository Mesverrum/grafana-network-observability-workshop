"""Facilitator-only board: Infinity visualization actions toggle the hairpin API."""

from __future__ import annotations

import build as b
import integrations as inf

UID = "workshop-facilitator-control"


def _action(title: str, active: bool, *, confirm: str, color: str) -> dict:
    return {
        "type": "infinity",
        "title": title,
        "confirmation": confirm,
        "oneClick": True,
        "style": {"backgroundColor": color},
        "infinity": {
            "method": "POST",
            "url": "/admin/hairpin",
            "body": '{"active": ' + ("true" if active else "false") + "}",
            "headers": [["Content-Type", "application/json"]],
            "queryParams": [],
            "datasourceUid": "workshop-hairpin-control",
        },
    }


def _hairpin_table(pid: int, title: str, pos: dict, actions: list[dict], description: str) -> dict:
    panel = b.table(
        pid,
        title,
        b.INF,
        [
            b.infinity_url(
                "/admin/hairpin",
                "",
                [
                    {"selector": "label", "text": "State", "type": "string"},
                    {"selector": "path", "text": "Path", "type": "string"},
                    {"selector": "in_sync", "text": "In sync", "type": "boolean"},
                ],
            )
        ],
        pos,
        description=description,
        transformations=[],
    )
    panel["fieldConfig"] = {"defaults": {"actions": actions}, "overrides": []}
    panel["options"]["cellHeight"] = "md"
    return panel


def facilitator_control() -> dict:
    enable = _action(
        "Enable Singapore path",
        True,
        confirm="Route the public VIP via Singapore? Destination IP stays the same.",
        color="semi-dark-red",
    )
    disable = _action(
        "Restore direct US",
        False,
        confirm="Remove the Singapore hairpin and restore the direct path?",
        color="semi-dark-green",
    )
    tcp_stat = {
        "id": 4,
        "type": "stat",
        "title": "TCP duration (workshop-tcp)",
        "description": "Public-probe TCP handshake to the GA edge — stays low after hairpin. Use traceroute hops for Lab 4.",
        "gridPos": b.grid(12, 6, 12, 6),
        "datasource": b.PROM,
        "targets": [
            b.prom_target(
                'max(probe_duration_seconds{job="workshop-tcp"})',
                instant=True,
            )
        ],
        "options": {
            "reduceOptions": {"calcs": ["lastNotNull"], "fields": "", "values": False},
            "colorMode": "value",
            "graphMode": "area",
            "justifyMode": "auto",
            "textMode": "auto",
        },
        "fieldConfig": {
            "defaults": {
                "unit": "s",
                "thresholds": b.thresholds((None, "green"), (0.25, "orange"), (0.4, "red")),
            },
            "overrides": [],
        },
    }
    panels = [
        inf.markdown(
            1,
            "Facilitator only",
            (
                "This board is **not** for attendees. Click a control table to POST "
                "`/admin/hairpin` through Infinity (`workshop-hairpin-control`). "
                "The hairpin agent on the control host polls that flag and runs "
                "**your** on/off commands — no DNS flip.\n\n"
                "Need **Editor** (Viewers cannot run visualization actions). "
                "If the click does nothing, edit the panel → Data links and actions → "
                "Connection = the Infinity datasource `workshop-hairpin-control`.\n\n"
                "Setup notes live in `reproduce/facilitator/hairpin.md`."
            ),
            b.grid(0, 0, 24, 6),
        ),
        inf.inf_stat(
            2,
            "Desired path",
            "/admin/hairpin",
            "active_num",
            b.grid(0, 6, 6, 6),
            description="0 = direct US. 1 = Singapore hairpin requested.",
            steps=((None, "green"), (1, "red")),
        ),
        inf.inf_stat(
            3,
            "Applied on probe",
            "/admin/hairpin",
            "applied_num",
            b.grid(6, 6, 6, 6),
            description="What the probe agent last reported. Stale if the agent is down.",
            steps=((None, "green"), (1, "red")),
        ),
        tcp_stat,
        _hairpin_table(
            5,
            "Enable Singapore path — click this table",
            b.grid(0, 12, 12, 8),
            [enable],
            'One-click Infinity POST {"active": true}. Confirm, then watch Desired path go red.',
        ),
        _hairpin_table(
            6,
            "Restore direct US — click this table",
            b.grid(12, 12, 12, 8),
            [disable],
            'One-click Infinity POST {"active": false}.',
        ),
        b.timeseries(
            7,
            "Synthetic TCP duration",
            [
                b.prom_target(
                    'probe_duration_seconds{job="workshop-tcp"}',
                    "A",
                    "{{probe}}",
                )
            ],
            b.grid(0, 20, 24, 8),
            "s",
        ),
        b.timeseries(
            8,
            "Traceroute hops",
            [
                b.prom_target(
                    'probe_traceroute_total_hops{job="workshop-tr"}',
                    "A",
                    "{{probe}}",
                )
            ],
            b.grid(0, 28, 12, 8),
            "short",
        ),
        b.timeseries(
            9,
            "Route hash changes",
            [
                b.prom_target(
                    'changes(probe_traceroute_route_hash{job="workshop-tr"}[15m])',
                    "A",
                    "{{probe}}",
                )
            ],
            b.grid(12, 28, 12, 8),
            "short",
        ),
    ]
    dash = inf._shell(
        UID,
        "Workshop Facilitator — path control",
        (
            "Toggle the Singapore hairpin from Grafana. Infinity actions POST "
            "/admin/hairpin; the control-host agent applies GA weights. Do not import "
            "onto attendee stacks."
        ),
        panels,
    )
    dash["tags"] = ["workshop", "network-o11y", "facilitator"]
    dash["refresh"] = "5s"
    dash["templating"]["list"].insert(
        1,
        b.ds_var("hairpin", "yesoreyeram-infinity-datasource", "workshop-hairpin-control"),
    )
    return dash
