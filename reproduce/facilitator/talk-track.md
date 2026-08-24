# Talk track

Short sentences. Honest limits. No Linux homework. You are on a **webinar**: share slides or a diagram; paste the public IP and prompts in chat. See [webinar.md](webinar.md).

## Cloud vs the OSS scar (first 10 minutes)

This is the objection they will bring before architecture.

> Grafana OSS upgrades are your problem: Linux deps, Prometheus / DB schema, dashboards gone. Check Point Skyline still pointed at OSS Grafana is a common version of that scar.

> Cloud is the opposite: you ingest. Grafana runs Mimir, Loki, Tempo, and the upgrades. Skyline already speaks OTel. The same export can land here without you owning the backend.

> We are not asking for SNMP into production today. This session is Cloud sandboxes and lab appliances. PRTG, Check Point, and Aruba EdgeConnect look familiar because the mocks are shaped like those APIs. Overlay, not rip-and-replace.

Give them one sentence to steal for leadership:

> We already export OTel. Cloud is where it stops being our upgrade problem.

## ktranslate architecture (10–12 min)

Share this left to right (slide or draw on the shared screen):

```
campus gear  →  ktranslate  →  Alloy  →  Grafana Cloud
 SNMP / traps / flows / syslog     OTLP      Mimir Loki Tempo
```

Say:

> ktranslate is a collector. It speaks the protocols network teams already have: SNMP polling, traps, NetFlow/sFlow/IPFIX, syslog. It turns that into OpenTelemetry. Alloy is Grafana's shipper. Cloud is where you look.

> Grafana's *supported* SNMP path is Alloy `prometheus.exporter.snmp`. It works. It is more YAML and MIB pain. We use ktranslate in the field because discovery and vendor profiles are faster. It is **not** a Grafana Support product. If your leadership asks, say community/partner.

> You are not installing this today. I will discover the lab on my screen. You will live in Cloud.

## Guided discovery (while it runs)

> Credential group, not a spreadsheet of community strings per IP. Discovery tries candidates against a range and keeps what authenticated. After this, polling is boring, which is what you want.

Point at the first `kentik_snmp_PollingHealth` series when it lands. Names they should recognize: Cisco access (`bld4-asw-01`), Check Point (`bld4-fw-01`), EdgeConnect (`wan-edge-01`).

## Cloud backends + Assistant (8–10 min)

> Three backends you will touch today. **Mimir** is metrics: SNMP counters, synthetic probe latency. **Loki** is logs: syslog and traps. **Tempo** is traces if the sandbox has an app — not the switch.

> Value-add is not another poller. It is one place to ask questions. **Assistant** inherits Grafana RBAC and your datasources. It is a consumption layer. It will not replace a network engineer.

Paste this in chat (also in [assistant-prompts.md](assistant-prompts.md)). They should ask **Assistant**, not type PromQL in Explore:

> In the last 30 minutes, which `device_name` has the highest `kentik_snmp_CPU`?

## Synthetics primer (5 min, then they drive)

> SNMP tells you what the box thinks. Synthetics tell you what a user path looks like. Same public IP for everyone. You pick a **public** home probe — Oregon or North Virginia. I will shuffle where that IP lands in AWS. I do not touch your stack, and I do not flip DNS.

> Create two checks: a **traceroute** and a **TCP port** check. Same probe. Stay on the check page for duration and hops. I will show **Explore once** on my share so they see the series; that is not the rest of the day.

Paste this as its own chat message:

```
Target: 15.197.194.37
TCP: 15.197.194.37:80
Probe: Oregon or North Virginia (public). Do not add Singapore yet.
```

## Import + hunt (2 min)

> Open Device Summary. Alerts on the fleet, a device table, click through to one box. I will share the shape once; you click on your stack.

## Fault (2 min)

> I am changing where that IP lands. Same address you already typed. Open the checks you already have — duration and hops are on those pages. Lab 4 is in chat.

Click **Enable Singapore path**, wait ~30 seconds plus one check interval, then send them to Lab 4.

If duration does not move: "Edit the TCP check and add the public Singapore probe. Same alert skill." Repeat it in chat.

## Infinity + Assistant (4 min)

> PRTG is your NMS. Check Point and EdgeConnect have their own controllers. We do not have native Cloud integrations that replace those. **Infinity** is the generic API datasource. Open the canned PRTG / Check Point / Aruba boards first. Then ask Assistant to build one board that puts Meraki next to SNMP errors and the TCP check they already watch in Synthetics.

> After the webinar that URL becomes the real controller plus an API key. The skill is the same.

Paste the Lab 5 Assistant block into chat.

## Close (8 min)

> Today you consumed Cloud. You did not become a ktranslate admin. Your team can take [KtransToGrafana](https://github.com/Mesverrum/KtransToGrafana) home if you want the collector. Synthetics and Infinity you can use this week without Linux. Cloud upgrades stay Grafana's problem.

Stop talking. Drop the GitHub link in chat again.
