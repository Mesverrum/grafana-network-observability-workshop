# Lab 3 — Summary, then drill in

You already have a fleet. Work it the way a NOC would: alerts, then a device, then the interface.

**Workshop Device Summary** and **Workshop Device Details** should already be in the **Network Observability** folder. If that folder is empty, post in chat and keep watching the shared screen until the facilitator unblocks you.

## A. Fleet

Open **Workshop Device Summary**.

1. Look at **Active Network Alerts**. Note which devices (and interfaces, if shown) are firing.
2. Look at **Device Status**. Sort or scan CPU % and Errors/s. Do the same names show up?
3. Click a Device name. That should open **Workshop Device Details** with that device selected.

Do not start in Explore. The dashboards are the path.

## B. Device

On Device Details:

1. Overview: is CPU or Memory the story, or are they fine?
2. **Interface Status**: sort by Errors/s or by bps. Which interface is the outlier?
3. Confirm on the In / Out timeseries. One chart should make the same interface obvious.
4. Open **Device Syslog** for that device. One line should agree with the interface story.

## You are done when

You can put in chat (or say on unmute) one sentence: which device you picked, why (alert or table), and which interface or resource is sick — without a PromQL cheat sheet.

## Stretch

Change the Device picker to a healthy box (`dc-core-01` or `bld1-asw-01`). The error charts should go quiet. That is the control.
