# Lab 4 — Infinity + Assistant

← Previous: [Lab 3 — Troubleshoot](03-troubleshoot.md)

Grafana Cloud does not ship native PRTG / Check Point / Aruba EdgeConnect / Meraki integrations. **Infinity** is a Grafana data source that pulls an HTTP API into the same stack (JSON in, table on a dashboard).

Today that API is a **mock** the facilitator is hosting. The Infinity source `workshop-network-apis` should **already exist** on this shared stack. If it is missing, post in chat — do not create a second copy.

This is a **different** story from Lab 3. Building 4 / Meraki names are **not** in SNMP.

## A. Confirm the mock

1. **Explore** (compass) → datasource picker `workshop-network-apis`.
2. Query settings on that page:
   - **Type:** **JSON**
   - **Source:** **URL** (fetch from the mock, not inline text)
   - **Parser:** **backend**
   - **Format:** **table**
3. **URL** field: `/meraki/devices` (path only; the data source already has the host).
4. **Root:** which JSON key holds the rows. Meraki returns a bare list, so leave Root **empty**.
5. **Run query**. You should see APs. Note which building looks unhealthy.

If this errors, the mock URL is down or Allowed hosts does not match. Post in chat.

## B. Open the vendor dashboards

**Dashboards** → folder **Network Observability**:

- Workshop PRTG Summary
- Workshop Check Point Summary
- Workshop Aruba Summary

At the top, set the **infinity** dropdown to `workshop-network-apis` if it is blank. Building 4 should look unhealthy.

## C. Assistant builds a combined board

Left menu: **AI**. That is **Grafana Assistant** in this stack.

Paste:

```
Using datasource workshop-network-apis, query GET /meraki/devices as JSON.
Build a dashboard titled Workshop campus that has:
1. A table of Meraki APs with name, status, clients, building.
2. A timeseries of kentik_snmp_CPU by device_name from this stack's Prometheus.
3. A timeseries of (kentik_snmp_ifInErrors{device_name="leaf1"}) / 60 — ktranslate 60s gauges, not rate().
4. A timeseries of probe_duration_seconds by probe for job=~"workshop-tcp.*" from grafanacloud-prom (or the stack Prometheus).
Put a text panel at the top that says users in Building 4 are slow.
```

If it ignores Infinity, paste this follow-up:

```
The Infinity datasource uid is workshop-network-apis.
GET /meraki/devices returns a JSON array with fields name, status, clients, building, serial.
Do not invent SNMP. Use this stack's Prometheus for kentik_snmp_*. Use grafanacloud-prom for probe_*.
```

Save the board into **your** folder (`Network Observability — <your name>`). Title can be `Workshop campus — <your name>`.

## D. Tidy the board

- Sort or filter so Building 4 is easy to see.
- Time range (upper right clock): last 30–60 minutes.

## You are done when

You have a dashboard with the controller API, SNMP errors, and TCP latency on one page.

To take it home: on the dashboard, **Share** → **Export**.

## Stretch

Ask Assistant:

```
Which Meraki AP is offline? Building 4 is the mock-API story. Do not look for those AP names in SNMP.
```

Next: [API paths (reference)](api-paths.md) →
