# Lab 5 — Infinity + Assistant

Grafana Cloud does not ship first-class PRTG / Check Point / Aruba EdgeConnect / Meraki integrations that replace those controllers. **Infinity** is how you pull an arbitrary HTTPS API into the same Cloud stack.

Today the API is a **mock** the facilitator hosted. Canned summaries live next to Device Summary:

- Workshop PRTG Summary
- Workshop Check Point Summary
- Workshop Aruba Summary

Paths: [api-paths.md](api-paths.md). The same datasource also has `/meraki/devices`. On a real estate those URLs become the live controller.

## A. Confirm the datasource

1. **Connections** → datasources. Open `workshop-network-apis` (Infinity).
2. If it is missing, tell a facilitator. Do not create a second one unless they ask.
3. **Explore** → that datasource.
4. Type JSON, source URL, URL `/meraki/devices`, parser backend, format table. Run.

You should see APs. One in Building 4 may be offline.

## B. Assistant builds the board

Open **Assistant** in this stack. Paste:

```
Using datasource workshop-network-apis, query GET /meraki/devices as JSON.
Build a dashboard titled Workshop campus that has:
1. A table of Meraki APs with name, status, clients, building.
2. A timeseries of kentik_snmp_CPU by device_name.
3. A timeseries of rate(kentik_snmp_ifInErrors[5m]) for bld4-asw-01.
4. A timeseries of probe_duration_seconds by probe for job workshop-tcp.
Put a text panel at the top that says users in Building 4 are slow.
```

If it ignores Infinity, send the follow-up in the facilitator prompt sheet.

## C. You edit, it does not have to be pretty

- Move Building 4 to the top of the AP table if you can sort or filter.
- Check that SNMP and synthetics actually have data (time range last 30–60 minutes).

## You are done when

You have one dashboard that a network person and an app person could stand in front of: controller API + device errors + probe latency.

Export it (Share → Export) if you want a take-home.

## Stretch

Ask Assistant:

```
Which Meraki AP is offline, and is that in the same building as the switch with the highest ifInErrors?
```
