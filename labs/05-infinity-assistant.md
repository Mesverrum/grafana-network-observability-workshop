# Lab 5 — Infinity + Assistant

Grafana Cloud does not ship native PRTG / Check Point / Aruba EdgeConnect / Meraki integrations. **Infinity** is a Grafana data source that pulls an HTTP API into the same stack (JSON in, table on a dashboard).

Today that API is a **mock** the facilitator is hosting. Chat will have a **mock URL**. Add one Infinity data source, then open the vendor dashboards from Lab 3 (or build one with Assistant).

## A. Add Infinity

If **Connections** → **Data sources** already lists `workshop-network-apis`, skip to B.

### Install the plugin if needed

A **plugin** is extra Grafana UI. Infinity is not always preinstalled.

1. **Connections** → **Add new connection**. Search `Infinity`.
2. If the **Infinity** card is there, go to **Create the data source**.
3. If it is missing: left menu **Administration** (gear) → **Plugins and data** → **Plugins**. Search `Infinity`. Open **Infinity**. Click **Install**. Wait until it says installed, then go back to **Add new connection**.
4. If **Install** is hidden or errors, post in chat.

### Create the data source

1. **Connections** → **Add new connection**.
2. Search `Infinity`. Click the **Infinity** card.
3. **Add new data source**.
4. **Name:** `workshop-network-apis`.
5. Leave **Default** off.
6. **URL:** the mock URL from chat (example `http://18.217.39.189:8088`). Host only. Paths like `/meraki/devices` go in Explore, not here.
7. **Allowed hosts:** add that same URL, including `http://` and the port. Infinity will only call hosts you list.
8. **Authentication:** **No Auth** (or **None**).
9. **Save & test**.

## B. Confirm the mock

1. **Explore** (compass) → datasource picker `workshop-network-apis`.
2. Query settings on that page:
   - **Type:** **JSON**
   - **Source:** **URL** (fetch from the mock, not inline text)
   - **Parser:** **backend**
   - **Format:** **table**
3. **URL** field: `/meraki/devices` (path only; the data source already has the host).
4. **Root:** which JSON key holds the rows. Meraki returns a bare list, so leave Root **empty**.
5. **Run query**. You should see APs. One in Building 4 may be offline (`bld4-ap-12`).

If this errors, the mock URL is down or Allowed hosts does not match. Post in chat.

## C. Open the vendor dashboards from Lab 3

**Dashboards** → folder **Network Observability**:

- Workshop PRTG Summary
- Workshop Check Point Summary
- Workshop Aruba Summary

At the top, set the **infinity** dropdown to `workshop-network-apis` if it is blank. Building 4 should look unhealthy.

Skip this if you did not import those three JSON files in Lab 3.

## D. Assistant builds a combined board

Left menu: **AI**. That is **Grafana Assistant** in this stack.

Paste:

```
Using datasource workshop-network-apis, query GET /meraki/devices as JSON.
Build a dashboard titled Workshop campus that has:
1. A table of Meraki APs with name, status, clients, building.
2. A timeseries of kentik_snmp_CPU by device_name from datasource workshop-ktranslate.
3. A timeseries of (kentik_snmp_ifInErrors{device_name="bld4-asw-01"}) / 60 from workshop-ktranslate — ktranslate 60s gauges, not rate().
4. A timeseries of probe_duration_seconds by probe for job workshop-tcp from the stack Prometheus (grafanacloud-prom), same TCP check as Lab 2.
Put a text panel at the top that says users in Building 4 are slow.
```

If it ignores Infinity, paste this follow-up:

```
The Infinity datasource uid is workshop-network-apis.
GET /meraki/devices returns a JSON array with fields name, status, clients, building, serial.
Do not invent SNMP. Use workshop-ktranslate for kentik_snmp_*. Use the stack Prometheus (grafanacloud-prom) for probe_*.
```

## E. Tidy the board

- Sort or filter so Building 4 is easy to see.
- Time range (upper right clock): last 30–60 minutes.

## You are done when

You have a dashboard with the controller API, SNMP errors, and TCP latency on one page.

To take it home: on the dashboard, **Share** → **Export**.

## Stretch

Ask Assistant:

```
Which Meraki AP is offline, and is that in the same building as the switch with the highest ifInErrors?
```
