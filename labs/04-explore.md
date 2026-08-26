# Lab 4 — Explore the fleet

← Previous: [Lab 3 — Import dashboards](03-import-dashboards.md)

The lab is healthy. Learn the boards before anything breaks. Click around like a NOC that just came on shift: table first, then a device, then an interface. Leave synthetics as they are.

You need [Lab 3](03-import-dashboards.md) imported and [Lab 2](02-synthetics.md) checks green.

## A. Device Summary

On **Workshop Device Summary**:

1. **Active Network Alerts** (top) may be empty. That is fine while the fleet is quiet.
2. **Device Status** table. Sort by **CPU %** or **Errors/s**. Note the five names: `spine1`, `leaf1`, `leaf2`, `leaf-br1`, `leaf-br2`.
3. Use **SNMP group** to flip HQ (`srl-hq`) vs a branch. All three groups should have live boxes.
4. Click a **Device** name. That should open **Workshop Device Details** with that device selected.

If Details opens but CPU / interfaces are empty, use the **Device** dropdown at the top of Details and pick another live name.

## B. Device Details

On Device Details:

1. Overview: CPU and Memory should look boring. That is the baseline.
2. **Interface Status**: sort by bps. Which interfaces carry traffic vs sit idle?
3. Confirm on the In / Out timeseries.
4. **Device Syslog**: may be quiet. Know where the panel is. Lab 5 uses it.

## C. Synthetics are still yours

**Testing & synthetics** → **workshop-tcp**. It should still be green from Lab 2. You will use this later to decide whether a problem is “the box” or “the user path.”

## You are done when

You can say, without hunting a failure: how many sites, which device you opened, and where syslog lives on Details.

## Stretch

Optional second vantage (same public IP, add Singapore): [stretch — a second vantage](stretch-second-vantage.md). Skip unless chat says to.

Next: wait for chat. Then [Lab 5 — Troubleshoot](05-troubleshoot.md) →
