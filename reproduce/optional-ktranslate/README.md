# Facilitator / take-home collector

Attendees do **not** run this during the webinar. You use it (or [KtransToGrafana](https://github.com/Mesverrum/KtransToGrafana)) for the guided discovery you screen-share. They can clone it later if their team wants a collector.

ktranslate is community / partner. It is not Grafana Support.

## Preferred: KtransToGrafana

The maintained path is Marc's repo:

https://github.com/Mesverrum/KtransToGrafana

1. Clone it on a Linux host or WSL with Docker.
2. Copy `.env.sample` → `.env`.
3. From your Brokkr stack: **Add new connection → OpenTelemetry (OTLP)**. Paste:

   - `GC_OTLP_URL` = endpoint
   - `GC_OTLP_ACCOUNT` = instance id (username)
   - `GC_OTLP_KEY` = `glc_...` token

4. If you have real gear, set `groups/onboarding.env` `TARGETS` to a lab subnet.
5. If you do **not** have gear, start the simulator in this folder, then point `TARGETS` at it:

```
docker compose up -d snmpsim
```

Use the published SNMP address from `docker compose port snmpsim 161/udp` (or `127.0.0.1` if you used `network_mode: host`). Community `public`.

6. `make generate && make up && make discover GROUP=onboarding`
7. Explore: `count by (device_name) (kentik_snmp_PollingHealth)`

Import the 00–10 dashboards from that repo. Do not stop at Device Details.

## This folder

| File | Purpose |
|---|---|
| `docker-compose.yaml` | `snmpsim` (always) + optional `alloy` forwarder |
| `.env.sample` | Brokkr OTLP names |
| `config.alloy.sample` | Alloy → Grafana Cloud OTLP if you already have a local OTLP producer |
| `ktranslate-snmp.yaml` | Example ktranslate device file targeting snmpsim |

`ktranslate` itself is intentionally **not** pinned here. Image flags change. Use KtransToGrafana's compose for the collector, and this snmpsim when you have no routers to share.
