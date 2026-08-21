# Lab 4 — The path got worse

The facilitator is sending the **same public IP** from Lab 2 to a farther backend. Do not edit the check target. Keep the same public probe.

## Investigate

1. **Testing & synthetics** → **Synthetics** → **workshop-tcp**. Look at the **duration / latency** chart. You want a step up from Lab 2 on this same graph.
2. Open **workshop-tr**. Look at hops over time (list or map). Did the path change after the step in latency?

If hops moved, that is a path change. If hops did not move but duration stepped up, that is still the finding.

If chat says to use the **Singapore** probe: edit **workshop-tcp**, add public probe **Singapore**, save, wait two runs. Singapore will be slower than Oregon because it is farther away.

## Alert

On the **workshop-tcp** check, open **Alerts** / **Alerting**.

- Threshold on **duration / latency**: about **2x the flat part** of the chart before the step, or **400ms** if you want a default.
- Let the check UI create the Grafana alert.

If that control is missing:

1. **Alerting** → **Alert rules** → **New alert rule** (Grafana-managed).
2. Query A: datasource = your stack Prometheus (`grafanacloud-…-prom`, not `workshop-ktranslate`). Metric `probe_duration_seconds`. Filter `job` = `workshop-tcp`.
3. Keep **Reduce** (Last) and **Threshold**. Threshold **Is above `0.4`**. That value is **seconds** (`400` will never fire).
4. Folder: **Network Observability**.
5. Evaluation group: **New**, name `workshop`, every **1m**, pending **2m**.
6. Save. You do not need Slack.

## You are done when

You can say whether this was a **path change** (hops moved) or **just slower** (duration up, hops unchanged).
