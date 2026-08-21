# Reproduce this workshop

This folder is the facilitator kit. Attendees stay in [`../labs/`](../labs/).

## Before the room

1. Provision Grafana Cloud stacks (Brokkr **Observability Workshop**, or your own).
2. Copy `stacks.example.csv` → `stacks.csv` (gitignored). One row per stack: Grafana URL, API token, OTLP endpoint / instance / token.
3. Host the mock API where Cloud can GET it:

```bash
bash scripts/start-mocks.sh          # :8088
bash scripts/start-tunnel.sh         # prints a trycloudflare URL
# prefer a named Cloudflare tunnel or Cloud Run for a stable URL
```

4. Overlay folder + Infinity. Skip dashboards so they import in Lab 3 (or import them yourself):

```bash
python3 overlay/apply.py --manifest stacks.csv --mock-url https://YOUR_MOCK_HOST --skip-dashboards
python3 overlay/provision-alerts.py --manifest stacks.csv
```

5. Start ktranslate-shaped telemetry into their OTLP:

```bash
python3 generator/generate.py --manifest stacks.csv --interval 15 --fault
```

6. Your collector stays on **your** machine. Screen-share discovery. Do not have them SSH. Optional path: [KtransToGrafana](https://github.com/Mesverrum/KtransToGrafana) or [`optional-ktranslate/`](optional-ktranslate/).

## Day-of

Follow [`facilitator/run-of-show.md`](facilitator/run-of-show.md). Talk track: [`facilitator/talk-track.md`](facilitator/talk-track.md). Latency fault: [`facilitator/singapore-fault.md`](facilitator/singapore-fault.md). Assistant paste: [`facilitator/assistant-prompts.md`](facilitator/assistant-prompts.md).

Rebuild dashboard JSON after edits:

```bash
python3 dashboards/build.py
```

Copy the JSON into `../labs/dashboards/` if students import from git.

## Layout

| Path | Role |
|---|---|
| `inventory.py` | Shared campus names (Cisco / Check Point / EdgeConnect) |
| `mocks/` | FastAPI controller mocks (PRTG, Check Point, EdgeConnect, Meraki, …) |
| `generator/` | OTLP exporter of ktranslate-shaped `kentik_snmp_*` |
| `overlay/` | Folder, Infinity datasource, dashboard import, alerts |
| `dashboards/` | Dashboard builders + JSON |
| `scripts/` | Mocks, tunnel, generator helpers |
| `optional-ktranslate/` | SNMP simulator + notes; not for attendees in the room |

## Plugins

Infinity (`yesoreyeram-infinity-datasource`) must be on the stack. Sankey (`netsage-sankey-panel`) is optional for flow diagrams. Cloud plugin install needs a grafana.com access policy with `stack-plugins:write`.

## Secrets

Never commit `stacks.csv`, `.env`, or live tokens. `stacks.example.csv` is the template.
