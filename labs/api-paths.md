# Mock controller APIs (Infinity)

Paths on the workshop mock. Point Infinity `workshop-network-apis` at the mock URL from chat, then use these in Explore or Assistant.

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

Canned boards (if imported in Lab 3): Workshop PRTG Summary, Workshop Check Point Summary, Workshop Aruba Summary.
