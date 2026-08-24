# Lab 4 — The path got worse

The facilitator is sending the **same public IP** from Lab 2 to a farther backend. Leave the check **target** as that IP. Keep the same public probe.

## Investigate

1. **Testing & synthetics** → **Synthetics** → open **workshop-tcp**. Look at the **duration / latency** chart. You want a step up from Lab 2 on this same graph.
2. Open **workshop-tr**. Look at hops over time (list or map). Did the path change after the step in latency?

If hops moved, that is a path change. If hops did not move but duration stepped up, that is still the finding.

If chat says to use the **Singapore** probe: on **workshop-tcp**, click **Edit** (top of the check). In **Probe locations**, add public probe **Singapore**. Save. Wait two runs. Singapore will be slower than Oregon because it is farther away.

## Alert

On the **workshop-tcp** check page, look for **Alerts** or **Alerting** (tab or section on that same page).

- Threshold on **duration / latency**: about **2x the flat part** of the chart before the step, or **400ms** if you want a default.
- Save so the check UI creates the Grafana alert.

If that control is missing, create the rule yourself:

1. Left menu: **Alerting** (bell) → **Alert rules** → **New alert rule**. Choose **Grafana-managed** (Grafana evaluates the rule on a timer).
2. Query A: datasource = the Prometheus Grafana created on **your** stack (name like `grafanacloud-…-prom`). That is where Lab 2 checks write. Not `workshop-ktranslate` (that is SNMP).
3. Metric `probe_duration_seconds` (TCP check duration, in seconds). Filter `job` = `workshop-tcp`.
4. Keep **Reduce** (Last) and **Threshold**. Threshold **Is above `0.4`**. The query value is **seconds** (`400` will never fire).
5. Folder: **Network Observability** (the folder from Lab 3).
6. **Evaluation group** is how often Grafana re-checks the rule. **New**, name `workshop`, every **1m**, pending **2m** (must stay broken for two minutes before it fires).
7. Save. You can skip notification / Slack.

## You are done when

You can say whether this was a **path change** (hops moved) or **just slower** (duration up, hops unchanged).
