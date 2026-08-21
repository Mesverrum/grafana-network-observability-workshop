# Assistant prompts (webinar chat + Lab 5)

Paste these into webinar chat. Adjust datasource names if the sandbox differs.

## After Cloud talk (optional, 1 minute)

```
In the last 30 minutes, which device_name has the highest kentik_snmp_CPU?
```

```
Show me interface error rates for device_name bld4-asw-01.
```

## Lab 5: connect then build

After Infinity `workshop-network-apis` is working (they tested `/meraki/devices` in Explore):

```
Using datasource workshop-network-apis, query GET /meraki/devices as JSON.
Build a dashboard titled Workshop campus that has:
1. A table of Meraki APs with name, status, clients, building.
2. A timeseries of kentik_snmp_CPU by device_name.
3. A timeseries of rate(kentik_snmp_ifInErrors[5m]) for bld4-asw-01.
4. A timeseries of probe_duration_seconds by probe for job workshop-tcp.
Put a text panel at the top that says users in Building 4 are slow.
```

If Assistant ignores Infinity:

```
The Infinity datasource uid is workshop-network-apis.
The mock API base is already configured on that datasource.
GET /meraki/devices returns a JSON array with fields name, status, clients, building, serial.
Do not invent SNMP. Use grafanacloud-prom for kentik_snmp_* and probe_*.
```

## Stretch

```
Which Meraki AP is offline, and is that in the same building as the switch with the highest ifInErrors?
```

```
Using datasource workshop-network-apis, query GET /prtg/api/v2/sensors (root sensors) and GET /checkpoint/gateways (root gateways).
Which Building 4 sensors are not Up, and which Check Point gateway is in Attention?
```
