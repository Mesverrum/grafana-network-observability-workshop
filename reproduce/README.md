# Reproduce this workshop

This folder is the facilitator kit for a **webinar**. Attendees stay in [`../labs/`](../labs/). How to host the call: [`facilitator/webinar.md`](facilitator/webinar.md).

**Default delivery is one shared Grafana Cloud stack.** Attendees log in, make a named folder, and may create uniquely named synthetic checks. They do not add remote datasources and they do not import GitHub JSON (those dashboard UIDs already exist).

**Student SNMP story is the colocated 3-site Clos**, not the mock campus names and not the leftover OTLP generator. Infinity mocks (PRTG / Check Point / EdgeConnect / Meraki) are a **separate** Lab 4 API. Those hostnames are not in SNMP.

**Student order:** login → own folder + explore (healthy) → synthetics (shared and/or unique job names) → you inject a Clos fault → they hunt → Infinity. Finish SNMP discovery **before** the call ([`facilitator/watch-discovery.md`](facilitator/watch-discovery.md)). Synthetics: you create `workshop-tr` + `workshop-tcp` on the shared stack (one public VIP, Oregon or N. Virginia). Singapore is optional stretch — **you** add the probe; they watch. Hairpin / GA origin toggle is optional facilitator `curl` only — [`facilitator/inject-fault.md`](facilitator/inject-fault.md), [`facilitator/singapore-fault.md`](facilitator/singapore-fault.md), [`facilitator/hairpin.md`](facilitator/hairpin.md).

## Before the webinar

1. Provision **one** Grafana Cloud stack. Dual-ship or poll live Clos SNMP/syslog/traps/flows into **that** stack’s OTLP (same Prom/Loki they will query). Do not hand out `glc_` read tokens. Do not provision a Brokkr sandbox per attendee.
2. Copy `stacks.example.csv` → `stacks.csv` (gitignored) for **this** stack (Infinity overlay, hairpin board). Do **not** run `generator/` — Device Summary filters `tags_snmp_group=~"srl-.*"` and those campus names will not hunt.
3. Host the mock API where Cloud can GET it (Lab 4 Infinity only):

```bash
bash scripts/start-mocks.sh          # :8088
bash scripts/start-tunnel.sh         # prints a trycloudflare URL
# prefer a named Cloudflare tunnel or Cloud Run for a stable URL
```

4. Overlay folder + Infinity + **dashboards**. On the shared stack:

```bash
python3 overlay/apply.py --manifest stacks.csv --mock-url https://YOUR_MOCK_HOST
python3 overlay/apply.py --manifest stacks-facilitator.csv --mock-url https://YOUR_MOCK_HOST \
  --admin-token "$WORKSHOP_ADMIN_TOKEN" --facilitator
```

`overlay/provision-alerts.py` writes Clos SNMP rules (`tags_snmp_group=~"srl-.*"`) against `grafanacloud-prom` on the stack in the manifest. Run it on the shared stack that has live `kentik_snmp_*`.

Public VIP + dashboard toggle: [`facilitator/hairpin.md`](facilitator/hairpin.md).

5. Live SNMP / syslog / traps come from **network-o11y-demo** on the colocated host (ktranslate + Alloy, dual-ship to the **shared workshop stack**). Restore: `python3 local/scripts/ssm-alloy-ktranslate-parallel.py`. **Before the webinar:** `make discover GROUP=srl-hq` (then branch groups) so polling is already live. Optional campus vendors stay `tags_snmp_group=campus` and off the hunt boards.

6. On the shared stack, create Synthetic Monitoring checks **workshop-tr** (traceroute) and **workshop-tcp** (TCP) to the public VIP, one US public probe. Initialize the SM plugin if the stack is new.

7. They do not SSH and they do not watch discovery. Take-home collector notes: [KtransToGrafana](https://github.com/Mesverrum/KtransToGrafana) or [`optional-ktranslate/`](optional-ktranslate/) — not the webinar path.

## Day-of

Follow [`facilitator/run-of-show.md`](facilitator/run-of-show.md). Chat paste: [`facilitator/chat-paste.md`](facilitator/chat-paste.md). Talk track: [`facilitator/talk-track.md`](facilitator/talk-track.md). Clos incident: [`facilitator/inject-fault.md`](facilitator/inject-fault.md). Optional Singapore: [`facilitator/singapore-fault.md`](facilitator/singapore-fault.md). Assistant paste: [`facilitator/assistant-prompts.md`](facilitator/assistant-prompts.md).

Dashboard JSON is **pulled from live Grafana**, not generated here. `python3 dashboards/build.py` exits on purpose (it would wipe Assistant edits). Re-pull from network-o11y-demo (`local/scripts/_export-workshop-live.py`) and copy into `../labs/dashboards/` when you change the boards.

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
| `optional-ktranslate/` | Take-home snmpsim notes. Webinar SNMP is the colocated Clos (discovered before the call). |

## Plugins

Install Infinity (`yesoreyeram-infinity-datasource`) **once** on the shared stack. Create `workshop-network-apis` (URL + Allowed hosts = mock origin, No Auth). Do not have attendees install plugins.

Facilitator API fallback (needs grafana.com `stack-plugins:write` on a `glc_` policy): `POST https://grafana.com/api/instances/<stack-slug>/plugins` with `{"plugin":"yesoreyeram-infinity-datasource"}`. Sankey (`netsage-sankey-panel`) is optional for flow diagrams.

Do not mutate `grafanacloud-infinity` if Cloud provisioned one.

## Secrets

Never commit `stacks.csv`, `.env`, or live tokens. `stacks.example.csv` is the template. Never paste write tokens or Prom/Loki `glc_` passwords into webinar chat.
