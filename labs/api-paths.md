# Mock controller APIs (Infinity)

The facilitator hosts a mock API and points the Infinity datasource `workshop-network-apis` at it. Explore with **type JSON**, **source URL**, parser **backend**, format **table**.

These paths are workshop-shaped. Auth and schemas on live controllers will differ.

| Integration | Path | Root | Identity fields |
|---|---|---|---|
| PRTG | `/prtg/api/v2/sensors` | `sensors` | `device`, `name` |
| PRTG alarms | `/prtg/api/v2/sensors/alarms` | `sensors` | `device`, `name` |
| Check Point | `/checkpoint/gateways` | `gateways` | `name` |
| Check Point Skyline status | `/checkpoint/skyline/status` | `objects` | `name` |
| Aruba EdgeConnect | `/edgeconnect/appliances` | `appliances` | `hostName` |
| EdgeConnect tunnels | `/edgeconnect/tunnels` | `tunnels` | `src`, `dst` |
| Aruba Central APs | `/aruba/aps` | `aps` | `name` |
| Meraki | `/meraki/devices` | _(array)_ | `name` |

Canned summary boards (if imported):

- Workshop PRTG Summary (`workshop-prtg-summary`)
- Workshop Check Point Summary (`workshop-checkpoint-summary`)
- Workshop Aruba Summary (`workshop-aruba-summary`)

After the webinar, the same Infinity skill points at the real API plus a token.
