# Reproduce this workshop

This folder is the facilitator kit for a **webinar**. Attendees stay in [`../labs/`](../labs/). How to host the call: [`facilitator/webinar.md`](facilitator/webinar.md).

**Student SNMP story is the colocated 3-site Clos**, not the mock campus names and not the leftover OTLP generator. Infinity mocks (PRTG / Check Point / EdgeConnect / Meraki) are a **separate** Lab 6 API. Those hostnames are not in SNMP.

**Student order:** login → data sources → synthetics → import dashboards → explore (healthy) → you inject a Clos fault → they hunt → Infinity. Discovery is **your** share during data sources, not a student lab. Synthetics: one public VIP, Oregon or N. Virginia. Singapore is optional stretch. Hairpin / GA origin toggle is optional facilitator `curl` only — [`facilitator/inject-fault.md`](facilitator/inject-fault.md), [`facilitator/singapore-fault.md`](facilitator/singapore-fault.md), [`facilitator/hairpin.md`](facilitator/hairpin.md).

## Before the webinar

1. Provision Grafana Cloud stacks (Brokkr **Observability Workshop**, or your own). Attendee stacks stay empty of network boards. They add **your** Prom/Loki from chat ([`facilitator/chat-paste.md`](facilitator/chat-paste.md)) and import JSON in Lab 3.
2. Copy `stacks.example.csv` → `stacks.csv` (gitignored) for **your** facilitator stack (Infinity overlay, hairpin board). Do **not** run `generator/` into attendee stacks — Device Summary filters `tags_snmp_group=~"srl-.*"` and those campus names will not hunt.
3. Host the mock API where Cloud can GET it (Lab 6 Infinity only):

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
```

`overlay/provision-alerts.py` writes Clos SNMP rules (`tags_snmp_group=~"srl-.*"`) against `grafanacloud-prom` on the stack in the manifest. Run it only on a stack that actually has live `kentik_snmp_*` (facilitator / workshop write dest). Attendee sandboxes do not — they query the shared `workshop-ktranslate` remote source from imported dashboards.

Public VIP + dashboard toggle: [`facilitator/hairpin.md`](facilitator/hairpin.md).

5. Live SNMP / syslog / traps come from **network-o11y-demo** on the colocated host (ktranslate + Alloy, dual-ship to the workshop stack). Restore: `python3 local/scripts/ssm-alloy-ktranslate-parallel.py`. Guided discovery is `make discover GROUP=srl-hq` (then branch groups). Optional campus vendors stay `tags_snmp_group=campus` and off the hunt boards.

6. You screen-share discovery. They do not SSH. Take-home collector notes: [KtransToGrafana](https://github.com/Mesverrum/KtransToGrafana) or [`optional-ktranslate/`](optional-ktranslate/) — not the webinar path.

## Day-of

Follow [`facilitator/run-of-show.md`](facilitator/run-of-show.md). Chat paste: [`facilitator/chat-paste.md`](facilitator/chat-paste.md). Talk track: [`facilitator/talk-track.md`](facilitator/talk-track.md). Clos incident: [`facilitator/inject-fault.md`](facilitator/inject-fault.md). Optional Singapore: [`facilitator/singapore-fault.md`](facilitator/singapore-fault.md). Assistant paste: [`facilitator/assistant-prompts.md`](facilitator/assistant-prompts.md).

Student dashboard JSON is **pulled from live Grafana**, not generated here. `python3 dashboards/build.py` exits on purpose (it would wipe Assistant edits). Re-pull from network-o11y-demo (`local/scripts/_export-workshop-live.py`) and copy into `../labs/dashboards/` if students import from git.

## Layout

| Path | Role |
|---|---|
| `inventory.py` | **Infinity mock** campus names (Building 4 fault). Not the SNMP hunt. |
| `mocks/` | FastAPI controller mocks (PRTG, Check Point, EdgeConnect, Meraki, …) |
| `generator/` | Leftover OTLP campus faker. Do not use for the webinar hunt. |
| `overlay/` | Folder, Infinity datasource, dashboard import, Clos alerts |
| `dashboards/` | Live-pulled JSON + helpers (do not regenerate) |
| `scripts/` | Mocks, tunnel, leftover generator helpers |
| `facilitator/` | Webinar run-of-show, talk track, Clos fault inject, prompts |
| `optional-ktranslate/` | Take-home snmpsim notes. Webinar discovery is the colocated Clos. |

## Plugins

Infinity (`yesoreyeram-infinity-datasource`) must be on **each** stack. Brokkr Observability Workshop orgs usually do **not** preinstall it. Attendees install and add the source in the GUI (Lab 6):

1. If **Connections** → **Add new connection** has no Infinity card: **Administration** → **Plugins and data** → **Plugins** → search **Infinity** → **Install**.
2. **Connections** → **Add new connection** → Infinity → **Add new data source**.
3. Name `workshop-network-apis`. URL = mock origin. **Allowed hosts** = that same origin. Auth **No Auth**. Default off. **Save & test**, then Explore `/meraki/devices`.

Do not mutate `grafanacloud-infinity` if Cloud provisioned one.

Facilitator API fallback (needs grafana.com `stack-plugins:write` on a `glc_` policy): `POST https://grafana.com/api/instances/<stack-slug>/plugins` with `{"plugin":"yesoreyeram-infinity-datasource"}`. Sankey (`netsage-sankey-panel`) is optional for flow diagrams.

## Secrets

Never commit `stacks.csv`, `.env`, or live tokens. `stacks.example.csv` is the template.
