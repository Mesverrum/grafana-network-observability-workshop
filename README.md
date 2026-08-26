# Grafana Network Observability Workshop

Hands-on **webinar** on Grafana Cloud: SNMP, synthetics, and controller APIs.

You work in your own Grafana Cloud stack while the facilitator shares theirs. Keep the webinar and Grafana side by side.

ktranslate is community / partner. It is **not** a Grafana Support product.

## Students

Start in [`labs/`](labs/README.md). You need a browser, the webinar join link, and the Grafana Cloud URL (email or chat). Log in, add the shared data sources from chat, create synthetics, then import the dashboard JSON. Explore first. The facilitator injects a failure after that.

| Lab | What you do |
|---|---|
| [00](labs/00-login.md) | Log in |
| [01](labs/01-datasources.md) | Add `workshop-ktranslate` Prometheus + Loki from chat |
| [02](labs/02-synthetics.md) | Traceroute + TCP to the shared public IP (public probe) |
| [03](labs/03-import-dashboards.md) | Import JSON into **Network Observability** |
| [04](labs/04-explore.md) | Learn Device Summary → Details while the fleet is healthy |
| [05](labs/05-troubleshoot.md) | Hunt after the facilitator injects a fault |
| [06](labs/06-infinity-assistant.md) | Infinity + Assistant across mock APIs |

Dashboard JSON: [`labs/dashboards/`](labs/dashboards/).

Controller API cheat sheet: [`labs/api-paths.md`](labs/api-paths.md).

## Facilitators

Webinar delivery and the kit to run this again: [`reproduce/`](reproduce/README.md).
