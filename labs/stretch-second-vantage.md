# Stretch — A second vantage

← Previous: [Lab 1 — Explore](01-explore.md) or [Lab 2 — Synthetics](02-synthetics.md)

Optional. Skip unless chat says to. This is **not** the Lab 3 incident.

Same public IP as Lab 2. You are not changing the target. You add a **second public probe** so Grafana measures that IP from **Singapore** as well as from Oregon or North Virginia.

Prefer **your** checks (`workshop-tcp-<handle>`). Do not Edit the shared `workshop-tcp` / `workshop-tr` unless the facilitator says the whole room should.

A **probe** is where Grafana runs the check. Two probes = two vantages, two paths across the internet.

## Investigate

1. **Testing & synthetics** → **Synthetics** → open **your** TCP check (or `workshop-tcp` if you did not create one).
2. **Edit** (top of the check).
3. **Probe locations:** keep the US probe. Add public probe **Singapore**. Save.
4. Wait two runs (~1–2 minutes).
5. On the **duration** chart, there should be **two series**. Compare Singapore to your US probe.

Do the same on your traceroute check. Wait one traceroute interval (~2 minutes). Open the **hop list** / **map** and switch between probes. The hops should not match — different city, different path.

On this VIP, TCP duration can stay a few milliseconds on **both** probes (Global Accelerator finishes the handshake at a nearby AWS edge). If both look fast, the **traceroute maps** are still the finding.

## Alert (on your check)

On **your** TCP check page, look for **Alerts** / **Alerting**. Threshold on **duration** for the Singapore series if it is the slow one.

If that control is missing:

1. Left menu: **Alerting** → **Alert rules** → **New alert rule**. Grafana-managed.
2. Query A: this stack’s Prometheus (`grafanacloud-…-prom`).
3. Metric `probe_duration_seconds`. Filter `job` = your job name (`workshop-tcp-jdoe`).
4. **Reduce** (Last) and **Threshold**. Value is **seconds**. Try **Is above `0.05`**. Do **not** type `400`.
5. Folder: **your** folder. Evaluation group `workshop-<handle>`, every **1m**, pending **2m**.
6. Save. Skip Slack if you want.

## You are done when

You can say, in one sentence, how **Oregon/N. Virginia** differed from **Singapore** (duration and/or hops).

Back: [Lab 1 — Explore](01-explore.md) · Next if the room is ready: [Lab 3 — Troubleshoot](03-troubleshoot.md) →
