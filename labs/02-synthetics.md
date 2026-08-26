# Lab 2 — Synthetics: traceroute and a port check

← Previous: [Lab 1 — Add the shared lab data sources](01-datasources.md)

SNMP is what the box thinks. **Synthetics** are checks Grafana runs from the internet toward a target you choose.

This lab uses **your** stack’s Synthetic Monitoring (not the facilitator’s `workshop-ktranslate` source). Results land in the Prometheus Grafana already created on your stack. The facilitator will paste a **public IP** and `IP:port` in chat. Copy both. Every stack uses the same target.

Docs if you want them: [traceroute](https://grafana.com/docs/grafana-cloud/testing/synthetic-monitoring/create-checks/checks/traceroute/), [TCP](https://grafana.com/docs/grafana-cloud/testing/synthetic-monitoring/create-checks/checks/tcp/), [public probes](https://grafana.com/docs/grafana-cloud/testing/synthetic-monitoring/create-checks/public-probes/).

## Find Synthetics

1. Left menu: **Testing & synthetics**.
2. Click **Synthetics** (not **Performance Testing** / **k6**, which is a different load-testing product).
3. If the page asks you to **Initialize the plugin**, click it and wait for a Checks list. If you already have a Checks list, skip this.

## A. Traceroute check

1. **Add new check** (sometimes **Create check** or **Create new check**).
2. Choose the **Traceroute** card.
3. **Job name:** `workshop-tr`. This is the label Grafana stores on the check (`job` in metrics).
4. **Target:** the IP from chat (example `15.197.194.37`). No `https://`, no port.
5. **Probe locations:** a **probe** is the city Grafana runs the check from. Choose **one** public probe, **Oregon** or **North Virginia**. Uncheck anything else.
6. **Frequency:** `120` seconds, or **2 minutes** if the control is in minutes.
7. Scroll to the bottom. **Submit** / **Save**.
8. If the UI offers **Test**, click it once.

## B. TCP check

1. **Add new check** again.
2. Choose **TCP**. If you only see HTTP / Ping / DNS, scroll. It is not under “API Endpoint.”
3. **Job name:** `workshop-tcp`.
4. **Target:** IP **and port** from chat (example `15.197.194.37:80`).
5. **Probes:** the same single public probe as traceroute.
6. **Frequency:** `60` seconds is fine.
7. **Save**.

## C. Prove it on the check page

1. Open **workshop-tcp** from the Checks list.
2. Wait until at least one run is green. First TCP run is usually under a minute. If it stays red, the target or port is wrong; paste a screenshot in chat.
3. Confirm the check is green. Duration here is often only a few milliseconds.
4. Open **workshop-tr**. Traceroute can take up to two minutes for the first result.
5. Confirm you can see a hop list or traceroute map.

## You are done when

Both checks have a result and you know which public probe you used. Leave the target alone for the rest of the session.

## Stretch

Optional later: add public **Singapore** on the same checks — [a second vantage](stretch-second-vantage.md). Do that only if chat says to. Do not add Singapore during this lab unless they ask.

Next: [Lab 3 — Import dashboards](03-import-dashboards.md) →
