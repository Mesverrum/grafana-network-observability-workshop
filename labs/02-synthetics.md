# Lab 2 — Synthetics: traceroute and a port check

← Previous: [Lab 1 — Explore](01-explore.md)

SNMP is what the box thinks. **Synthetics** are checks Grafana runs from the internet toward a target the facilitator chose.

The stack already has **workshop-tr** and **workshop-tcp**. Open those first so you know the target and probe. You **may** create your own checks. Job names must be **yours** — a second `workshop-tcp` collides with the shared one.

Docs: [traceroute](https://grafana.com/docs/grafana-cloud/testing/synthetic-monitoring/create-checks/checks/traceroute/), [TCP](https://grafana.com/docs/grafana-cloud/testing/synthetic-monitoring/create-checks/checks/tcp/), [public probes](https://grafana.com/docs/grafana-cloud/testing/synthetic-monitoring/create-checks/public-probes/).

## Find Synthetics

1. Left menu: **Testing & synthetics**.
2. Click **Synthetics** (not **Performance Testing** / **k6**, which is a different load-testing product).
3. If the page asks to **Initialize the plugin**, stop and post in chat.

## A. Look at the shared checks

1. Open **workshop-tcp**. Confirm a green run. Note **target** (`IP:port`) and **probe** (Oregon or North Virginia).
2. Open **workshop-tr**. Confirm a hop list or map. Same IP, no port.

Do not **Edit** the shared checks (probes, target, or name). Leave them as the room’s known-good path.

## B. Optional: your own checks

Use the **same target** from chat / from the shared checks. **Job name** must include your name:

1. **Add new check** → **TCP**.
2. **Job name:** `workshop-tcp-` plus a short handle (`workshop-tcp-jdoe`). Letters, numbers, hyphen.
3. **Target:** the `IP:port` from chat (example `15.197.194.37:80`).
4. **Probes:** one public probe, Oregon or North Virginia.
5. **Frequency:** 60s is fine. **Save**.
6. Repeat for **Traceroute**, job `workshop-tr-jdoe`, target = IP only, frequency 120s.

If Save says the name exists, change the job name. Do not overwrite `workshop-tcp`.

## You are done when

You have seen a green TCP run (shared and/or yours) and know which probe you used. Leave the **target** alone for the rest of the session.

## Stretch

Singapore on **your** checks: [stretch — a second vantage](stretch-second-vantage.md). Skip unless chat says to. Do not add Singapore on the shared `workshop-tcp` unless the facilitator says so.

Next: wait for chat. Then [Lab 3 — Troubleshoot](03-troubleshoot.md) →
