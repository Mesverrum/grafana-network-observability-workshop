# Reproduce this workshop

This folder is the facilitator kit for a **webinar**. Attendees stay in [`../labs/`](../labs/). How to host the call: [`facilitator/webinar.md`](facilitator/webinar.md).

**Synthetics workflow:** one public VIP for every stack. Attendees create traceroute + TCP from a public probe (Oregon or N. Virginia). You flip US vs Singapore behind that IP from the facilitator board. They never select a private probe. Details: [`facilitator/hairpin.md`](facilitator/hairpin.md).

## Before the webinar

1. Provision Grafana Cloud stacks (Brokkr **Observability Workshop**, or your own). Attendee stacks stay empty of network boards. They add **your** Prom/Loki from chat ([`facilitator/chat-paste.md`](facilitator/chat-paste.md)) and import JSON in Lab 3.
2. Copy `stacks.example.csv` → `stacks.csv` (gitignored) for **your** facilitator stack (Infinity overlay, hairpin board). You do not need generator OTLP into every attendee stack if they use `workshop-ktranslate`.
3. Host the mock API where Cloud can GET it:

```bash
bash scripts/start-mocks.sh          # :8088
bash scripts/start-tunnel.sh         # prints a trycloudflare URL
# prefer a named Cloudflare tunnel or Cloud Run for a stable URL
```

4. Overlay folder + Infinity. Skip student dashboards so they import in Lab 3. On **your** stack, also import the hairpin control board:

```bash
python3 overlay/apply.py --manifest stacks.csv --mock-url https://YOUR_MOCK_HOST --skip-dashboards
python3 overlay/apply.py --manifest stacks-facilitator.csv --mock-url https://YOUR_MOCK_HOST \
  --admin-token "$WORKSHOP_ADMIN_TOKEN" --facilitator --skip-dashboards
python3 overlay/provision-alerts.py --manifest stacks.csv
```

Public VIP + dashboard toggle (students use public probes; you shuffle AWS backends): [`facilitator/hairpin.md`](facilitator/hairpin.md).

5. ktranslate-shaped telemetry lives on **your** lab Mimir/Loki. Attendees query it via the shared data sources. Optional: still run the generator into stacks that should have a local copy:

```bash
python3 generator/generate.py --manifest stacks.csv --interval 15 --fault
```

6. Your collector stays on **your** machine. Screen-share discovery. They do not SSH. Optional path: [KtransToGrafana](https://github.com/Mesverrum/KtransToGrafana) or [`optional-ktranslate/`](optional-ktranslate/).

## Day-of

Follow [`facilitator/run-of-show.md`](facilitator/run-of-show.md). Chat paste: [`facilitator/chat-paste.md`](facilitator/chat-paste.md). Talk track: [`facilitator/talk-track.md`](facilitator/talk-track.md). Latency fault: [`facilitator/hairpin.md`](facilitator/hairpin.md) and [`facilitator/singapore-fault.md`](facilitator/singapore-fault.md). Assistant paste: [`facilitator/assistant-prompts.md`](facilitator/assistant-prompts.md).

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
| `facilitator/` | Webinar run-of-show, talk track, prompts |
| `optional-ktranslate/` | SNMP simulator + notes; attendees do not run this during the webinar |

## Plugins

Infinity (`yesoreyeram-infinity-datasource`) must be on **each** stack. Brokkr Observability Workshop orgs usually do **not** preinstall it. Attendees install and add the source in the GUI (Lab 5):

1. If **Connections** → **Add new connection** has no Infinity card: **Administration** → **Plugins and data** → **Plugins** → search **Infinity** → **Install**.
2. **Connections** → **Add new connection** → Infinity → **Add new data source**.
3. Name `workshop-network-apis`. URL = mock origin. **Allowed hosts** = that same origin. Auth **No Auth**. Default off. **Save & test**, then Explore `/meraki/devices`.

Do not mutate `grafanacloud-infinity` if Cloud provisioned one.

Facilitator API fallback (needs grafana.com `stack-plugins:write` on a `glc_` policy): `POST https://grafana.com/api/instances/<stack-slug>/plugins` with `{"plugin":"yesoreyeram-infinity-datasource"}`. Sankey (`netsage-sankey-panel`) is optional for flow diagrams.

## Secrets

Never commit `stacks.csv`, `.env`, or live tokens. `stacks.example.csv` is the template.
