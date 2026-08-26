# Lab 5 — Troubleshoot

← Previous: [Lab 4 — Explore](04-explore.md)

Chat will say the lab changed. The facilitator will **not** tell you which box. Use the boards you already have. Do not change the synthetic target.

This is your workflow, not a scripted click-path. Stay on **your** stack.

## What you already have

- **Workshop Device Summary** / **Workshop Device Details** → shared SNMP + syslog (`workshop-ktranslate` / `workshop-ktranslate-logs`)
- **workshop-tcp** / **workshop-tr** → **your** stack’s Synthetic Monitoring (the public VIP)

## Hunt

1. Open **Workshop Device Summary**. Time range **Last 15 minutes** or **Last 30 minutes**. Refresh.
2. Sort the Device Status table. What moved vs Lab 4 (errors, oper status, CPU)?
3. Click into **Workshop Device Details**. Interface table first, then timeseries, then **Device Syslog**.
4. Check **workshop-tcp**. Did the user path from the internet change, or only something on the Clos?

If syslog is empty, stay on the SNMP table — that is enough.

## You are done when

You can put in chat **one sentence**: site (HQ / branch), device, what changed, and which signal proved it (table, interface, syslog, or synthetics).

## Stretch

Ask Assistant (datasource `workshop-ktranslate`):

```
In the last 20 minutes, which device_name and interface look unhealthy?
Use kentik_snmp_ifOperStatus, (kentik_snmp_ifInErrors)/60, and Loki syslog if present.
Do not invent Building 4 or Meraki — that is a later lab.
```

Next: [Lab 6 — Infinity + Assistant](06-infinity-assistant.md) →
