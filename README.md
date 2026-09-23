# Grafana Network Observability Workshop

Hands-on **webinar** on Grafana Cloud: SNMP, synthetics, and controller APIs.

Everyone works in **one shared Grafana Cloud stack**. The facilitator provisions datasources, the clean **Network Observability** folder, and canonical `workshop-tcp` / `workshop-tr` **before join**. You do not add remote Prometheus/Loki, and you do not import JSON (those UIDs already exist). You **do** make a named folder and may create uniquely named synthetic checks.

Keep the webinar and Grafana side by side.

ktranslate is community / partner. It is **not** a Grafana Support product.

## Students

Start in [`labs/`](labs/README.md). You need a browser, the webinar join link, and the shared Grafana Cloud URL (email or chat). Log in, make a folder with your name, copy boards if you want to chop, then explore a healthy fleet. The facilitator injects a failure after that.

| Lab | What you do |
|---|---|
| [00](labs/00-login.md) | Log into the **shared** stack; create `Network Observability — Your Name` |
| [01](labs/01-explore.md) | Learn Device Summary → Details; Save as into your folder |
| [02](labs/02-synthetics.md) | Shared `workshop-tcp` / `workshop-tr`, or your own uniquely named checks |
| [03](labs/03-troubleshoot.md) | Hunt after the facilitator injects a fault |
| [04](labs/04-infinity-assistant.md) | Infinity + Assistant; save into your folder |

Controller API cheat sheet: [`labs/api-paths.md`](labs/api-paths.md).

Dashboard JSON in [`labs/dashboards/`](labs/dashboards/) is for the **facilitator** to import before the call, not for you.

## Facilitators

Webinar delivery and the kit to run this again: [`reproduce/`](reproduce/README.md).

Provision one stack. Dual-ship or poll live SNMP into **that** stack. Import dashboards, create `workshop-tcp` / `workshop-tr`, add Infinity + the mock URL. Chat the Grafana URL. They never paste `glc_` tokens.
