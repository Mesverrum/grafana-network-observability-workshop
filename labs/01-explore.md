# Lab 1 — Explore the fleet

← Previous: [Start here](00-login.md)

The lab is healthy. Learn the boards before anything breaks. Click around like a NOC that just came on shift: table first, then a device, then an interface.

You need to be logged into the **shared** stack. Start in folder **Network Observability** (or the name in chat).

Datasources are already mapped. If a dashboard has **datasource** / **loki** dropdowns, leave the values the facilitator set (often `grafanacloud-…-prom` / `grafanacloud-…-logs`, or aliases `workshop-ktranslate` / `workshop-ktranslate-logs`).

## A. Device Summary

On **Workshop Device Summary** (or **03. Network Device Summary** if that is what this stack imported):

1. **Active Network Alerts** (top) may be empty. That is fine while the fleet is quiet.
2. **Device Status** table. Sort by **CPU %** or **Errors/s**. Note the five names: `spine1`, `leaf1`, `leaf2`, `leaf-br1`, `leaf-br2`.
3. Use **SNMP group** to flip HQ (`srl-hq`) vs a branch. All three groups should have live boxes.
4. Click a **Device** name. That should open **Workshop Device Details** (or **04. Network Device Details**) with that device selected.

If Details opens but CPU / interfaces are empty, use the **Device** dropdown at the top of Details and pick another live name.

## B. Device Details

On Device Details:

1. Overview: CPU and Memory should look boring. That is the baseline.
2. **Interface Status**: sort by bps. Which interfaces carry traffic vs sit idle?
3. Confirm on the In / Out timeseries.
4. **Device Syslog**: may be quiet. Know where the panel is. Lab 3 uses it.

## C. Copy into your folder (so you can chop)

If you created `Network Observability — <your name>` in Lab 0:

1. Open **Workshop Device Summary**.
2. **Share** / dashboard settings → **Save as** (or **Copy** / **Copy to folder**, wording varies).
3. Folder: **your** folder. New title can stay or add your name. Grafana must give it a **new UID** — if it offers overwrite of the original, cancel.
4. Repeat for **Workshop Device Details**.

Chop only the copies. Do not delete panels on the shared originals.

## You are done when

You can say, without hunting a failure: how many sites, which device you opened, and where syslog lives on Details. You have copies in your folder if you want to edit.

## Stretch

Optional second vantage: [stretch — a second vantage](stretch-second-vantage.md). Skip unless chat says to.

Next: [Lab 2 — Synthetics](02-synthetics.md) →
