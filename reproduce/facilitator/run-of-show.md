# Run of show (about 3 hours)

Webinar. They do not deploy ktranslate. They do not need Linux. Delivery notes: [webinar.md](webinar.md).

| Clock | Module | You | Them |
|---|---|---|---|
| 0:00–0:12 | Cloud vs OSS | You ingest. Grafana owns Mimir/Loki/Tempo and upgrades. | Join webinar + Grafana. Mute. |
| 0:12–0:28 | ktranslate architecture | Slide or shared diagram: devices → ktranslate (SNMP, traps, flows, syslog) → Alloy → Cloud. Support honesty. | Stay in Grafana; watch the share. |
| 0:28–0:42 | Guided discovery | Live discover on **your** collector. Narrate while it runs. | [01-watch-discovery](../../labs/01-watch-discovery.md) |
| 0:42–0:55 | Cloud backends + Assistant | Mimir / Loki / Tempo, why OTLP, Assistant as consumption not a second NMS. | Try one Assistant prompt from chat. |
| 0:55–1:30 | Synthetics | Share the first click. Paste the public VIP. **Explore once on your share** (TCP duration), then send them back to the check page. | [02-synthetics](../../labs/02-synthetics.md) |
| 1:30–1:40 | Break | Confirm generator is filling stacks. Confirm SM checks exist. Stay on the call. | Stretch; keep the webinar open. |
| 1:40–2:10 | Summary → details | Point at Device Summary on **your** share. Alerts first, then click a device. They do the same on theirs. | [03-import-and-hunt](../../labs/03-import-and-hunt.md) |
| 2:10–2:30 | Fault | Open **Workshop Facilitator — path control**, click Enable Singapore path. Wait ~30s + one SM interval. Tell them to reopen **their checks**, not Explore. See [hairpin.md](hairpin.md). | [04-latency-fault](../../labs/04-latency-fault.md) |
| 2:30–3:00 | Infinity + Assistant | Canned PRTG / Check Point / Aruba boards first. Paste the Lab 5 prompt. Extra credit if time: Tempo Search + the traces Assistant prompt. Sample traces are not the lab fault. | [05-infinity-assistant](../../labs/05-infinity-assistant.md) |
| 3:00–3:10 | Close | What is supported. Take-home [KtransToGrafana](https://github.com/Mesverrum/KtransToGrafana) for *their* team, not for today. | Screenshot / export the Assistant dashboard. |

## Pre-webinar setup

- Stacks up. Overlay skipped dashboards. Attendees add Infinity in Lab 5: **Administration → Plugins** if Infinity is missing, then **Connections → Add new connection → Infinity** named `workshop-network-apis` at the mock origin (Allowed hosts = that URL). Brokkr does not preinstall Infinity.
- Generator running against `stacks.csv`. On a volunteer stack: **Workshop Device Summary** shows ~8 devices (you may still use `kentik_snmp_PollingHealth` on your share).
- Your ktranslate lab is polling something you can discover again (and share).
- Synthetic Monitoring is enabled on attendee stacks (public probes only). VIP `15.197.194.37:80` answers. Path fault **off** until Lab 4. Public Singapore probe is the fallback only.
- Facilitator board imported with `overlay/apply.py --facilitator`. `hairpin-agent.py` running on the **control** host. Button tested once (enable → Singapore page, restore → US).
- SNMP / PRTG / Check Point / EdgeConnect **fault on** so hunts have a finding.
- Chat macros ready: labs URL, Grafana URL reminder, Lab 2 VIP paste, Assistant prompts.

## If things break

| Symptom | Fix |
|---|---|
| They want to "just SSH" | No. Watch your discovery. Their work is Cloud. |
| They offer production SNMP | Decline. Sandbox + lab appliances. |
| Empty hunt dashboards | Generator / OTLP. Wait 60s. Open Device Summary; you can confirm `kentik_snmp_PollingHealth` on **your** Explore. |
| SM has no probes | Testing & synthetics → Synthetics → Probes. Refresh. Paste the click-path in chat. |
| Infinity missing from catalog | Administration → Plugins and data → Plugins → Infinity → Install. Then add `workshop-network-apis`. |
| Infinity allowlist / host refused | Allowed hosts must equal the mock origin (include `http://` and port). Edit the existing source. |
| Assistant will not use Infinity | Paste the follow-up from [assistant-prompts.md](assistant-prompts.md) into chat. |
| Hairpin did not change the path | Confirm agent `applied_num=1` on the facilitator board, then Singapore-probe fallback in [singapore-fault.md](singapore-fault.md). Say it on mic. |
| Someone is lost in UI | One volunteer screenshares, or they drop a screenshot in chat. Do not freeze the agenda. |

## Do not

- Make them install Docker or ktranslate.
- Call ktranslate official Grafana Support.
- Point Infinity at a customer's production PRTG / Check Point / Orchestrator.
- Assume they have paper, a second person in the room, or can see anything you did not paste or share.
