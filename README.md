# Grafana Network Observability Workshop

Hands-on lab for Grafana Cloud: consume ktranslate-shaped SNMP, synthetics, and controller APIs — without installing collectors in the room.

ktranslate is community / partner. It is **not** a Grafana Support product.

## Students

Start in [`labs/`](labs/README.md). You only need a browser and the Grafana Cloud URL from the facilitator.

| Lab | What you do |
|---|---|
| [00](labs/00-login.md) | Log in |
| [01](labs/01-watch-discovery.md) | Watch discovery (you do not deploy) |
| [02](labs/02-synthetics.md) | Traceroute + TCP checks |
| [03](labs/03-import-and-hunt.md) | Device Summary → Device Details |
| [04](labs/04-latency-fault.md) | Path / latency change + an alert |
| [05](labs/05-infinity-assistant.md) | Infinity + Assistant across mock APIs |

Importable dashboards (if the facilitator asks you to import): [`labs/dashboards/`](labs/dashboards/).

Controller API cheat sheet: [`labs/api-paths.md`](labs/api-paths.md).

## Facilitators

Everything needed to run this again lives in [`reproduce/`](reproduce/README.md): mocks, telemetry generator, Grafana overlay, run-of-show, and an optional collector path ([KtransToGrafana](https://github.com/Mesverrum/KtransToGrafana)).

## What this is not

- Production SNMP into a customer estate
- Each attendee deploying ktranslate
- Official Grafana Support for ktranslate
