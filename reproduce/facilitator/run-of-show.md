# Run of show (about 3 hours)

Webinar. They do not deploy ktranslate. They do not need Linux. Delivery notes: [webinar.md](webinar.md).

| Clock | Module | You | Them |
|---|---|---|---|
| 0:00–0:12 | Cloud vs OSS | You ingest. Grafana owns Mimir/Loki/Tempo and upgrades. | Join webinar + Grafana. Mute. |
| 0:12–0:28 | ktranslate architecture | Slide or shared diagram: devices → ktranslate (SNMP, traps, flows, syslog) → Alloy → Cloud. Support honesty. | Stay in Grafana; watch the share. |
| 0:28–0:42 | Guided discovery | Live discover on **your** collector. Narrate while it runs. | [01-watch-discovery](../../labs/01-watch-discovery.md) |
| 0:42–0:55 | Cloud backends + Assistant | Mimir / Loki / Tempo, why OTLP, Assistant as consumption not a second NMS. | Try one Assistant prompt from chat. |
| 0:55–1:30 | Synthetics | Share the first click. Paste the public VIP. They prove TCP is green and traceroute has a hop list. | [02-synthetics](../../labs/02-synthetics.md) |
| 1:30–1:40 | Break | Confirm Clos SNMP on the shared Prom (`spine1` / `leaf-br1`). Confirm SM checks exist. Stay on the call. | Stretch; keep the webinar open. |
| 1:40–2:10 | Summary → details | Point at Device Summary on **your** share. Alerts first, then click a device. They do the same on theirs. | [03-import-and-hunt](../../labs/03-import-and-hunt.md) |
| 2:10–2:30 | Two vantages | Paste Lab 4. They add public **Singapore** on `workshop-tcp` and `workshop-tr`. You talk probe vs target. Hairpin board is optional aside, not their lever. | [04-latency-fault](../../labs/04-latency-fault.md) |
| 2:30–3:00 | Infinity + Assistant | Canned PRTG / Check Point / Aruba boards first. Paste the Lab 5 prompt. No Infinity Explore unless they are stuck. | [05-infinity-assistant](../../labs/05-infinity-assistant.md) |
| 3:00–3:10 | Close | What is supported. Take-home [KtransToGrafana](https://github.com/Mesverrum/KtransToGrafana) for *their* team, not for today. | Screenshot / export the Assistant dashboard. |

## Pre-webinar setup

- Stacks up. Overlay skipped dashboards. Attendees add Infinity in Lab 5: **Administration → Plugins** if Infinity is missing, then **Connections → Add new connection → Infinity** named `workshop-network-apis` at the mock origin (Allowed hosts = that URL). Brokkr does not preinstall Infinity.
- Attendees query the **3-site Clos** via `workshop-ktranslate` (not the generator inventory). Expect `srl-hq` (`spine1`, `leaf1`, `leaf2`), `srl-branch1` (`leaf-br1`), `srl-branch2` (`leaf-br2`).
- Live discover on colocated: share `groups/srl-hq.env` (then the branch files) and `make discover GROUP=srl-hq`. Restore collectors: `python3 local/scripts/ssm-alloy-ktranslate-parallel.py` from network-o11y-demo. Campus Forti/Arista/Cisco is optional extra (`tags_snmp_group=campus`); do not default the hunt there.
- Synthetic Monitoring is enabled on attendee stacks (public probes only). VIP `15.197.194.37:80` answers. Lab 4 they add the public **Singapore** probe; do not require the hairpin toggle for the student exercise.
- Clos SNMP is live on the shared `workshop-ktranslate` source. Infinity mocks have Building 4 degraded (Lab 5). Do not expect mock names (`bld4-*`, `wan-edge-01`) on Device Summary.
- Chat macros ready: labs URL, Grafana URL reminder, Lab 2 VIP paste, Assistant prompts.

## If things break

| Symptom | Fix |
|---|---|
| They want to "just SSH" | No. Watch your discovery. Their work is Cloud. |
| They offer production SNMP | Decline. Sandbox + lab appliances. |
| Empty hunt dashboards | Wait one 60s poll. Confirm `kentik_snmp_PollingHealth` on **your** Explore (`spine1`, `leaf1`, `leaf-br1`). SNMP group All or `srl-*`. |
| SM has no probes | Testing & synthetics → Synthetics → Probes. Refresh. Paste the click-path in chat. |
| Infinity missing from catalog | Administration → Plugins and data → Plugins → Infinity → Install. Then add `workshop-network-apis`. |
| Infinity allowlist / host refused | Allowed hosts must equal the mock origin (include `http://` and port). Edit the existing source. |
| Assistant will not use Infinity | Paste the follow-up from [assistant-prompts.md](assistant-prompts.md) into chat. |
| Singapore probe missing / greyed out | Public probes list → Singapore. Refresh. They Edit the check and add it; they do not need your hairpin board. |
| Someone is lost in UI | One volunteer screenshares, or they drop a screenshot in chat. Do not freeze the agenda. |

## Do not

- Make them install Docker or ktranslate.
- Call ktranslate official Grafana Support.
- Point Infinity at a customer's production PRTG / Check Point / Orchestrator.
- Assume they have paper, a second person in the room, or can see anything you did not paste or share.
