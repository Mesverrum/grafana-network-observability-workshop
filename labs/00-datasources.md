# Add the shared lab data sources

← Previous: [Start here](00-login.md)

A Grafana **data source** is a connection to a backend. **Prometheus** is metrics. **Loki** is logs.

SNMP and syslog for this workshop live on the facilitator’s Grafana Cloud. You add two data sources that point there, using values from **webinar chat**.

Grafana already created a Prometheus on **your** stack. Lab 2 synthetics write there. Leave **Default** off on the new sources so that built-in one stays the default.

If you cannot see **Add new data source**, post in chat. Your login needs permission to add sources.

Wait until chat has a block like this (values will differ):

```
Prometheus name: workshop-ktranslate
Prometheus URL: https://prometheus-....grafana.net/api/prom
Prometheus user: 1234567
Prometheus password: glc_...

Loki name: workshop-ktranslate-logs
Loki URL: https://logs-....grafana.net
Loki user: 1234567
Loki password: glc_...
```

Copy-paste from chat. The user field is digits only, not a URL.

## Connections

Left menu: **Connections**.

- **Add new connection** creates a source.
- **Data sources** is the list of what you already have.

## A. Prometheus (SNMP metrics)

1. **Add new connection**.
2. Search `Prometheus`. Click **Prometheus**.
3. **Add new data source** (upper right).
4. **Name:** `workshop-ktranslate`.
5. Leave **Default** off.
6. **Prometheus server URL:** the Prometheus URL from chat. It must end with `/api/prom` (Grafana Cloud’s metrics API path).
7. **Authentication:** **Basic authentication**.
8. **User:** Prometheus user from chat (digits only).
9. **Password:** Prometheus password from chat (starts with `glc_`).
10. If you see **Prometheus type**, set **Mimir** (Grafana Cloud’s Prometheus-compatible metrics). If you see **HTTP method**, set **POST**.
11. Scroll to the bottom. **Save & test**. You want a green success.

If Save & test fails, check for a swapped user/password, a missing `/api/prom`, or a trailing space. Try once more, then screenshot the error into chat.

## B. Loki (device syslog)

1. **Connections** → **Add new connection**.
2. Search `Loki`. Click **Loki**.
3. **Create a Loki data source** (or **Add new data source**).
4. **Name:** `workshop-ktranslate-logs`.
5. Leave **Default** off.
6. **URL:** the Loki URL from chat.
7. **Authentication:** **Basic authentication**.
8. **User** and **Password** from the Loki lines in chat.
9. **Save & test**. Green success.

## C. Prove the SNMP source

1. Left menu: **Explore** (compass icon). This is Grafana’s ad-hoc query page.
2. Top datasource picker: **workshop-ktranslate**. There may be several Prometheus entries. Pick the one you named, not the `grafanacloud-…-prom` Grafana already created.
3. Paste this query. `kentik_snmp_PollingHealth` is the collector’s “this device answered SNMP” metric (Lab 1 covers the naming):

```promql
count by (device_name) (kentik_snmp_PollingHealth)
```

4. Click **Run query**. You should see device names. If you want the sites too, run `count by (device_name, tags_snmp_group) (kentik_snmp_PollingHealth)`.

Empty here means the shared lab is not sending yet, or you are on the wrong datasource. Post in chat.

## You are done when

Explore against **workshop-ktranslate** shows device names (or chat confirmed the lab is still filling).

Then: [watch discovery](01-watch-discovery.md) when they say Lab 1. You need these sources before [import](03-import-and-hunt.md).

Next: [Lab 1 — Watch discovery](01-watch-discovery.md) →
