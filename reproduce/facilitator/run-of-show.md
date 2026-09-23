# Run of show (about 2.5 hours)

Webinar. They do not deploy ktranslate. They do not need Linux. Delivery notes: [webinar.md](webinar.md).

**One shared stack.** Setup first (datasources, folder, dashboards, SM checks, Infinity). Hunt after they have seen healthy boards. You inject the Clos fault; they troubleshoot without being told the box.

| Clock | Module | You | Them |
|---|---|---|---|
| 0:00–0:12 | Cloud vs OSS | You ingest. Grafana owns Mimir/Loki/Tempo and upgrades. | Join webinar + shared Grafana. Mute. [00-login](../../labs/00-login.md) |
| 0:12–0:25 | ktranslate architecture | Slide or shared diagram: devices → ktranslate (SNMP, traps, flows, syslog) → Alloy → Cloud. Support honesty. | Stay in Grafana. |
| 0:25–0:50 | Explore (healthy) | Walk Summary → Details. They copy into a named folder if they want to chop. | [01-explore](../../labs/01-explore.md) |
| 0:50–1:10 | Synthetics | Show **workshop-tcp** / **workshop-tr**. They may clone with unique job names. | [02-synthetics](../../labs/02-synthetics.md) |
| 1:10–1:20 | Break | Confirm Clos SNMP (`spine1` / `leaf-br1`). Confirm SM checks still green. Stay on the call. | Stretch; keep the webinar open. |
| 1:20–1:50 | Inject + hunt | [inject-fault.md](inject-fault.md): disable leaf1 `ethernet-1/1`, wait ~90s, paste Lab 3. Do **not** name the box. | [03-troubleshoot](../../labs/03-troubleshoot.md) |
| 1:50–2:20 | Infinity + Assistant | Canned PRTG / Check Point / Aruba boards first. Paste the Lab 4 prompt. Ask them to name Assistant boards uniquely. | [04-infinity-assistant](../../labs/04-infinity-assistant.md) |
| 2:20–2:30 | Close | Clear the Clos fault. What is supported. Take-home [KtransToGrafana](https://github.com/Mesverrum/KtransToGrafana) for *their* team, not for today. | Screenshot / export the Assistant dashboard. |

Singapore second vantage is **optional stretch** ([stretch-second-vantage](../../labs/stretch-second-vantage.md)). They add Singapore on **their** checks. Skip if the hunt is running long.

## Pre-webinar setup

- **One** stack up. Overlay **includes** dashboards. Infinity plugin + `workshop-network-apis` at the mock origin (Allowed hosts = that URL). Attendees do not install plugins.
- Dual-ship Clos SNMP into this stack’s Prometheus. Expect `srl-hq` (`spine1`, `leaf1`, `leaf2`), `srl-branch1` (`leaf-br1`), `srl-branch2` (`leaf-br2`).
- Clos already discovered **before join**: `make discover GROUP=srl-hq` (then branch groups). Confirm `kentik_snmp_PollingHealth` on Explore. Restore collectors: `python3 local/scripts/ssm-alloy-ktranslate-parallel.py` from network-o11y-demo. Notes: [watch-discovery.md](watch-discovery.md). Campus Forti/Arista/Cisco is optional extra (`tags_snmp_group=campus`); do not default the hunt there.
- Synthetic Monitoring initialized. Checks **workshop-tr** and **workshop-tcp** exist. VIP `15.197.194.37:80` answers. Do not require Singapore or the hairpin toggle for the student path.
- **Stop `events-loop`** before Lab 1 so background flaps do not look like the incident. Infinity mocks have Building 4 degraded (Lab 4). Do not expect mock names (`bld4-*`, `wan-edge-01`) on Device Summary.
- Chat macros ready: labs URL, **shared Grafana URL** (no datasource tokens), Lab 3 incident paste, Assistant prompts.
- Fault command ready: `python3 local/scripts/ssm-workshop-inject-fault.py start` — [inject-fault.md](inject-fault.md).

## If things break

| Symptom | Fix |
|---|---|
| They want to "just SSH" | No. Their work is Cloud. |
| They offer production SNMP | Decline. Sandbox + lab appliances. |
| Empty hunt dashboards | Wait one 60s poll. Confirm `kentik_snmp_PollingHealth` (`spine1`, `leaf1`, `leaf-br1`). SNMP group All or `srl-*`. |
| SM has no probes / no checks | Initialize SM. Create canonical **workshop-tcp** / **workshop-tr** so they have a target to copy. |
| Someone names a check `workshop-tcp` | Tell them to use `workshop-tcp-<handle>`. Unique job names only. |
| Import JSON / UID exists | They must **Save as** into their folder, not re-import GitHub JSON. |
| Infinity missing | You install it. Do not send the room to Plugins. |
| Infinity allowlist / host refused | Allowed hosts must equal the mock origin (include `http://` and port). Edit the existing source. |
| Assistant will not use Infinity | Paste the follow-up from [assistant-prompts.md](assistant-prompts.md) into chat. |
| Duplicate Assistant dashboards | Folder `Network Observability — <name>`, title includes their name. |
| SM check quota / “limit reached” | Plan check cap. Have remaining people use the shared `workshop-tcp` only. |
| Someone is lost in UI | One volunteer screenshares, or they drop a screenshot in chat. Do not freeze the agenda. |
| Lab 3 hunt finds nothing | Confirm `workshop-fault-status` on colocated. Wait another poll. Do not name `leaf1`. |

## Do not

- Make them install Docker or ktranslate.
- Call ktranslate official Grafana Support.
- Run live SNMP discovery on the call.
- Paste Prom/Loki `glc_` tokens in chat.
- Point Infinity at a customer's production PRTG / Check Point / Orchestrator.
- Tell them which interface you disabled.
- Assume they have paper, a second person in the room, or can see anything you did not paste or share.
