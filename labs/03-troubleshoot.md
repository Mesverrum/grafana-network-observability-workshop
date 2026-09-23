# Lab 3 — Troubleshoot

← Previous: [Lab 2 — Synthetics](02-synthetics.md)

Chat will say the lab changed. The facilitator will **not** tell you which box. Use the boards you already have. Do not change the synthetic **target**. You may watch **workshop-tcp** or your own `workshop-tcp-<handle>`.

This is your workflow, not a scripted click-path. Stay on the **shared** stack.

## What you already have

- **Workshop Device Summary** / **Workshop Device Details** (or **03.** / **04.** Network Device …) → SNMP + syslog already on this stack
- **workshop-tcp** / **workshop-tr** → Synthetic Monitoring on this same stack (the public VIP)

## Hunt

1. Open **Workshop Device Summary**. Time range **Last 15 minutes** or **Last 30 minutes**. Refresh.
2. Sort the Device Status table. What moved vs Lab 1 (errors, oper status, CPU)?
3. Click into **Workshop Device Details**. Interface table first, then timeseries, then **Device Syslog**.
4. Check **workshop-tcp**. Did the user path from the internet change, or only something on the Clos?

If syslog is empty, stay on the SNMP table — that is enough.

## You are done when

You can put in chat **one sentence**: site (HQ / branch), device, what changed, and which signal proved it (table, interface, syslog, or synthetics).

## Stretch

Ask Assistant (this stack’s Prometheus):

```
In the last 20 minutes, which device_name and interface look unhealthy?
Use kentik_snmp_ifOperStatus, (kentik_snmp_ifInErrors)/60, and Loki syslog if present.
Do not invent Building 4 or Meraki — that is a later lab.
```

Next: [Lab 4 — Infinity + Assistant](04-infinity-assistant.md) →
