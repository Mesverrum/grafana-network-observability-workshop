# Talk track

Short sentences. Honest limits. No Linux homework.

## Cloud vs the OSS scar (first 10 minutes)

This is the objection they will bring before architecture.

> Grafana OSS upgrades are your problem: Linux deps, Prometheus / DB schema, dashboards gone. Check Point Skyline still pointed at OSS Grafana is a common version of that scar.

> Cloud is the opposite: you ingest. Grafana runs Mimir, Loki, Tempo, and the upgrades. Skyline already speaks OTel. The same export can land here without you owning the backend.

> We are not asking for SNMP into production today. This room is Cloud sandboxes and lab appliances. PRTG, Check Point, and Aruba EdgeConnect look familiar because the mocks are shaped like those APIs. Overlay, not rip-and-replace.

Give them one sentence to steal for leadership:

> We already export OTel. Cloud is where it stops being our upgrade problem.

## ktranslate architecture (10–12 min)

Draw this left to right:

```
campus gear  →  ktranslate  →  Alloy  →  Grafana Cloud
 SNMP / traps / flows / syslog     OTLP      Mimir Loki Tempo
```

Say:

> ktranslate is a collector. It speaks the protocols network teams already have: SNMP polling, traps, NetFlow/sFlow/IPFIX, syslog. It turns that into OpenTelemetry. Alloy is Grafana's shipper. Cloud is where you look.

> Grafana's *supported* SNMP path is Alloy `prometheus.exporter.snmp`. It works. It is more YAML and MIB pain. We use ktranslate in the field because discovery and vendor profiles are faster. It is **not** a Grafana Support product. If your leadership asks, say community/partner.

> You are not installing this today. I will discover the lab. You will live in Cloud.

## Guided discovery (while it runs)

> Credential group, not a spreadsheet of community strings per IP. Discovery tries candidates against a range and keeps what authenticated. After this, polling is boring, which is what you want.

Point at the first `kentik_snmp_PollingHealth` series when it lands. Names they should recognize: Cisco access (`bld4-asw-01`), Check Point (`bld4-fw-01`), EdgeConnect (`wan-edge-01`).

## Cloud backends + Assistant (8–10 min)

> Three backends you will touch today. **Mimir** is metrics: SNMP counters, synthetic probe latency. **Loki** is logs: syslog and traps. **Tempo** is traces if the sandbox has an app — not the switch.

> Value-add is not another poller. It is one place to ask questions. **Assistant** inherits Grafana RBAC and your datasources. It is a consumption layer. It will not replace a network engineer.

Give them one prompt (also in [assistant-prompts.md](assistant-prompts.md)):

> In the last 30 minutes, which `device_name` has the highest `kentik_snmp_CPU`?

## Synthetics primer (5 min, then they drive)

> SNMP tells you what the box thinks. Synthetics tell you what a user path from the internet looks like. Grafana Cloud runs public probes in AMER, EMEA, APAC. Today you create two checks: a **traceroute** and a **TCP port** check.

> Pick Oregon or North Virginia as your "home" probe. We will mess with the path later.

Target: you publish one hostname (lab VIP or a stable public port you control). Write it on the board.

## Import + hunt (2 min)

> Open Device Summary. Alerts on the fleet, a device table, click through to one box. I will not click for you.

## Fault (2 min)

> I am changing the path. Your job is latency and traceroute, not my router.

If the hairpin fails: "Singapore probe is the fallback. Same alert skill."

## Infinity + Assistant (4 min)

> PRTG is your NMS. Check Point and EdgeConnect have their own controllers. We do not have first-class Cloud integrations that replace those. **Infinity** is the generic API datasource. You will point it at a mock that looks like those APIs (Lab 5 uses Meraki because the JSON is simple). Then you ask Assistant to build a board that puts controller status next to SNMP errors and the synthetic latency you already have.

> On Monday that URL becomes the real controller plus an API key. The skill is the same.

## Close (8 min)

> Today you consumed Cloud. You did not become a ktranslate admin. Your team can take [KtransToGrafana](https://github.com/Mesverrum/KtransToGrafana) home if you want the collector. Synthetics and Infinity you can use this week without Linux. Cloud upgrades stay Grafana's problem.

Stop talking.
