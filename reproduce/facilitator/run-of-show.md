# Run of show (about 3 hours)

Webinar. They do not deploy ktranslate. They do not need Linux. Delivery notes: [webinar.md](webinar.md).

Setup first. Hunt after they have boards. You inject the Clos fault; they troubleshoot without being told the box.

| Clock | Module | You | Them |
|---|---|---|---|
| 0:00–0:12 | Cloud vs OSS | You ingest. Grafana owns Mimir/Loki/Tempo and upgrades. | Join webinar + Grafana. Mute. [00-login](../../labs/00-login.md) |
| 0:12–0:25 | ktranslate architecture | Slide or shared diagram: devices → ktranslate (SNMP, traps, flows, syslog) → Alloy → Cloud. Support honesty. | Stay in Grafana; finish login. |
| 0:25–0:40 | Data sources | Paste Prom/Loki. Clos SNMP is already polling — [pre-session discovery](watch-discovery.md). | [01-datasources](../../labs/01-datasources.md) |
| 0:40–1:10 | Synthetics | Share the first click. Paste the public VIP. They prove TCP is green and traceroute has a hop list. | [02-synthetics](../../labs/02-synthetics.md) |
| 1:10–1:20 | Break | Confirm Clos SNMP on the shared Prom (`spine1` / `leaf-br1`). Confirm SM checks exist. Stay on the call. | Stretch; keep the webinar open. |
| 1:20–1:40 | Import | Point at Device Summary on **your** share so they know the shape. They import JSON only. | [03-import-dashboards](../../labs/03-import-dashboards.md) |
| 1:40–1:55 | Explore (healthy) | Walk Summary → Details once. No incident yet. | [04-explore](../../labs/04-explore.md) |
| 1:55–2:25 | Inject + hunt | [inject-fault.md](inject-fault.md): disable leaf1 `ethernet-1/1`, wait ~90s, paste Lab 5. Do **not** name the box. | [05-troubleshoot](../../labs/05-troubleshoot.md) |
| 2:25–2:55 | Infinity + Assistant | Canned PRTG / Check Point / Aruba boards first. Paste the Lab 6 prompt. No Infinity Explore unless they are stuck. | [06-infinity-assistant](../../labs/06-infinity-assistant.md) |
| 2:55–3:05 | Close | Clear the Clos fault. What is supported. Take-home [KtransToGrafana](https://github.com/Mesverrum/KtransToGrafana) for *their* team, not for today. | Screenshot / export the Assistant dashboard. |

Singapore second vantage is **optional stretch** ([stretch-second-vantage](../../labs/stretch-second-vantage.md)). Skip if the hunt is running long. Hairpin board is optional aside, not their lever.

## Pre-webinar setup

- Stacks up. Overlay skipped dashboards. Attendees add Infinity in Lab 6: **Administration → Plugins** if Infinity is missing, then **Connections → Add new connection → Infinity** named `workshop-network-apis` at the mock origin (Allowed hosts = that URL). Brokkr does not preinstall Infinity.
- Attendees query the **3-site Clos** via `workshop-ktranslate` (not the generator inventory). Expect `srl-hq` (`spine1`, `leaf1`, `leaf2`), `srl-branch1` (`leaf-br1`), `srl-branch2` (`leaf-br2`).
- Clos already discovered **before join**: `make discover GROUP=srl-hq` (then branch groups). Confirm `kentik_snmp_PollingHealth` on your Explore. Restore collectors: `python3 local/scripts/ssm-alloy-ktranslate-parallel.py` from network-o11y-demo. Notes: [watch-discovery.md](watch-discovery.md). Campus Forti/Arista/Cisco is optional extra (`tags_snmp_group=campus`); do not default the hunt there.
- Synthetic Monitoring is enabled on attendee stacks (public probes only). VIP `15.197.194.37:80` answers. Do not require Singapore or the hairpin toggle for the student path.
- Clos SNMP is live on the shared `workshop-ktranslate` source. **Stop `events-loop`** before Lab 4 so background flaps do not look like the incident. Infinity mocks have Building 4 degraded (Lab 6). Do not expect mock names (`bld4-*`, `wan-edge-01`) on Device Summary.
- Chat macros ready: labs URL, Grafana URL reminder, Lab 2 VIP paste, Lab 5 incident paste, Assistant prompts.
- Fault command ready: `python3 local/scripts/ssm-workshop-inject-fault.py start` — [inject-fault.md](inject-fault.md).

## If things break

| Symptom | Fix |
|---|---|
| They want to "just SSH" | No. Their work is Cloud. |
| They offer production SNMP | Decline. Sandbox + lab appliances. |
| Empty hunt dashboards | Wait one 60s poll. Confirm `kentik_snmp_PollingHealth` on **your** Explore (`spine1`, `leaf1`, `leaf-br1`). SNMP group All or `srl-*`. |
| SM has no probes | Testing & synthetics → Synthetics → Probes. Refresh. Paste the click-path in chat. |
| Infinity missing from catalog | Administration → Plugins and data → Plugins → Infinity → Install. Then add `workshop-network-apis`. |
| Infinity allowlist / host refused | Allowed hosts must equal the mock origin (include `http://` and port). Edit the existing source. |
| Assistant will not use Infinity | Paste the follow-up from [assistant-prompts.md](assistant-prompts.md) into chat. |
| Singapore probe missing / greyed out | Optional stretch only. Public probes list → Singapore. Refresh. |
| Someone is lost in UI | One volunteer screenshares, or they drop a screenshot in chat. Do not freeze the agenda. |
| Lab 5 hunt finds nothing | Confirm `workshop-fault-status` on colocated. Wait another poll. Do not name `leaf1`. |

## Do not

- Make them install Docker or ktranslate.
- Call ktranslate official Grafana Support.
- Run live SNMP discovery on the call.
- Point Infinity at a customer's production PRTG / Check Point / Orchestrator.
- Tell them which interface you disabled.
- Assume they have paper, a second person in the room, or can see anything you did not paste or share.
