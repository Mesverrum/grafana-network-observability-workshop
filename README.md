# Grafana Network Observability Workshop

Hands-on **webinar** on Grafana Cloud: SNMP, synthetics, and controller APIs.

You work in your own Grafana Cloud stack while the facilitator shares theirs. Keep the webinar and Grafana side by side.

ktranslate is community / partner. It is **not** a Grafana Support product.

## Students

Start in [`labs/`](labs/README.md). You need a browser, the webinar join link, and the Grafana Cloud URL (email or chat). Add the shared data sources from chat, then import the dashboard JSON.

| Lab | What you do |
|---|---|
| [00](labs/00-login.md) | Log in |
| [00b](labs/00-datasources.md) | Add `workshop-ktranslate` Prometheus + Loki from chat |
| [01](labs/01-watch-discovery.md) | Watch discovery on the shared screen |
| [02](labs/02-synthetics.md) | Traceroute + TCP to the shared public IP (public probe) |
| [03](labs/03-import-and-hunt.md) | Import JSON into **Network Observability**, then hunt |
| [04](labs/04-latency-fault.md) | Same IP, slower path on the check + an alert |
| [05](labs/05-infinity-assistant.md) | Infinity + Assistant across mock APIs (extra credit: Tempo / APM) |

Dashboard JSON: [`labs/dashboards/`](labs/dashboards/).

Controller API cheat sheet: [`labs/api-paths.md`](labs/api-paths.md).

## Facilitators

Webinar delivery and the kit to run this again: [`reproduce/`](reproduce/README.md).
