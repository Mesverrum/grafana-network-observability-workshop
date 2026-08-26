# Mock controller APIs (Infinity)

← Previous: [Lab 6 — Infinity + Assistant](06-infinity-assistant.md)

Use this in **Lab 6** after `workshop-network-apis` exists. In Explore, **Root** is the JSON key that holds the rows. Meraki has no key (the response is already a list).

| Integration | Path | Root | Identity fields |
|---|---|---|---|
| PRTG | `/prtg/api/v2/sensors` | `sensors` | `device`, `name` |
| PRTG alarms | `/prtg/api/v2/sensors/alarms` | `sensors` | `device`, `name` |
| Check Point | `/checkpoint/gateways` | `gateways` | `name` |
| Check Point Skyline status | `/checkpoint/skyline/status` | `objects` | `name` |
| Aruba EdgeConnect | `/edgeconnect/appliances` | `appliances` | `hostName` |
| EdgeConnect tunnels | `/edgeconnect/tunnels` | `tunnels` | `src`, `dst` |
| Aruba Central APs | `/aruba/aps` | `aps` | `name` |
| Meraki | `/meraki/devices` | leave empty (JSON array) | `name` |

Vendor dashboards from Lab 3: Workshop PRTG Summary, Workshop Check Point Summary, Workshop Aruba Summary.

Next: [Labs](README.md) →
