# Run of show (about 3 hours)

They do not deploy ktranslate. They do not need Linux.

| Clock | Module | You | Them |
|---|---|---|---|
| 0:00–0:12 | Cloud vs OSS | You ingest. Grafana owns Mimir/Loki/Tempo and upgrades. | Listen. Open their Cloud stack. |
| 0:12–0:28 | ktranslate architecture | Whiteboard: devices → ktranslate (SNMP, traps, flows, syslog) → Alloy → Cloud. Support honesty. | Stay in the stack. |
| 0:28–0:42 | Guided discovery | Live discover the lab on **your** collector. Talk while it runs. | [01-watch-discovery](../../labs/01-watch-discovery.md) |
| 0:42–0:55 | Cloud backends + Assistant | Mimir / Loki / Tempo, why OTLP, Assistant as consumption not a second NMS. | Try one Assistant question. |
| 0:55–1:30 | Synthetics | 5 min primer. Walk the first click, then get off the screen. | [02-synthetics](../../labs/02-synthetics.md) |
| 1:30–1:40 | Break | Confirm generator is filling their stacks. Confirm SM checks exist. | |
| 1:40–2:10 | Summary → details | Point at Device Summary. Alerts first, then click a device. | [03-import-and-hunt](../../labs/03-import-and-hunt.md) |
| 2:10–2:30 | Fault | Hairpin or Singapore probe. See [singapore-fault.md](singapore-fault.md). | [04-latency-fault](../../labs/04-latency-fault.md) |
| 2:30–3:00 | Infinity + Assistant | No OOTB PRTG / Check Point / EdgeConnect. Infinity is the glue. Lab 5 uses Meraki. | [05-infinity-assistant](../../labs/05-infinity-assistant.md) |
| 3:00–3:10 | Close | What is supported. Take-home [KtransToGrafana](https://github.com/Mesverrum/KtransToGrafana) for *their* team, not for today. | Screenshot the Assistant dashboard. |

## Room setup

- Stacks up. Overlay ran with `--skip-dashboards` (or dashboards already imported). Infinity `workshop-network-apis` points at the **public** mock URL.
- Generator running against `stacks.csv`. On a volunteer stack: `count by (device_name) (kentik_snmp_PollingHealth)` is 8.
- Your ktranslate lab is polling something you can discover again.
- Synthetic Monitoring is enabled. Public probes include Oregon and Singapore.
- SNMP / PRTG / Check Point / EdgeConnect **fault on** so hunts have a finding. Path fault **off** until Lab 4.

## If things break

| Symptom | Fix |
|---|---|
| They want to "just SSH" | No. Watch your discovery. Their work is Cloud. |
| They offer production SNMP | Decline. Sandbox + lab appliances. |
| Empty hunt dashboards | Generator / OTLP. Wait 60s. Check `kentik_snmp_PollingHealth`. |
| SM has no probes | Testing & synthetics → Synthetics → Probes. Refresh. |
| Infinity allowlist | Re-apply with the public mock URL. |
| Assistant will not use Infinity | Prompt must name `workshop-network-apis` and `/meraki/devices`. |
| Hairpin did not change the path | Singapore-probe fallback in [singapore-fault.md](singapore-fault.md). |

## Do not

- Make them install Docker or ktranslate.
- Call ktranslate official Grafana Support.
- Point Infinity at a customer's production PRTG / Check Point / Orchestrator.
