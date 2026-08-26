# Lab 4 — A second vantage

← Previous: [Lab 3 — Import dashboards, then hunt](03-import-and-hunt.md)

Same public IP as Lab 2. You are not changing the target. You add a **second public probe** so Grafana measures that IP from **Singapore** as well as from Oregon or North Virginia.

A **probe** is where Grafana runs the check. Two probes = two vantages, two paths across the internet. That is the concept: synthetics are “what does this look like from here,” not “what the box in AWS thinks.”

Leave the **target** (`15.197.194.37` / `:80`) alone.

## Investigate

1. **Testing & synthetics** → **Synthetics** → open **workshop-tcp**.
2. **Edit** (top of the check).
3. **Probe locations:** keep your Lab 2 probe. Add public probe **Singapore**. Save.
4. Wait two runs (~1–2 minutes).
5. On the **duration** chart, there should be **two series** (two probe names). Compare Singapore to your US probe.

Do the same add on **workshop-tr** (Edit → add **Singapore** → Save). Wait one traceroute interval (~2 minutes). Open the **hop list** / **map** and switch between probes (or two recent runs). The hops should not match — different city, different path.

On this VIP, TCP duration can stay a few milliseconds on **both** probes (Global Accelerator finishes the handshake at a nearby AWS edge). If both look fast, the **traceroute maps** are still the finding. If Singapore TCP is clearly slower, say that too.

## Alert

On the **workshop-tcp** check page, look for **Alerts** / **Alerting**. Threshold on **duration** for the Singapore series if it is the slow one.

If that control is missing, create the rule yourself:

1. Left menu: **Alerting** (bell) → **Alert rules** → **New alert rule**. Choose **Grafana-managed**.
2. Query A: datasource = the Prometheus Grafana created on **your** stack (`grafanacloud-…-prom`). Lab 2 checks write there. Not `workshop-ktranslate`.
3. Metric `probe_duration_seconds`. Filter `job` = `workshop-tcp`. Legend / group by `probe` if you can.
4. Keep **Reduce** (Last) and **Threshold**. The query value is **seconds**. Try **Is above `0.05`** (50 ms) if Singapore is slower; do **not** type `400`.
5. If both probes stay under 50 ms, still save the rule — that is the shape — and use traceroute as the picture of two paths.
6. Folder: **Network Observability**.
7. **Evaluation group**: **New**, name `workshop`, every **1m**, pending **2m**.
8. Save. You can skip notification / Slack.

## You are done when

You can say, in one sentence, how **Oregon/N. Virginia** differed from **Singapore** (duration and/or hops), and you have an alert rule aimed at that TCP check.

Next: [Lab 5 — Infinity + Assistant](05-infinity-assistant.md) →
