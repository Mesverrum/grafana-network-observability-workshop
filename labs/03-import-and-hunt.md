# Lab 3 — Import dashboards, then hunt

Import JSON from this repo, then work the boards like a NOC: table first, then a device, then the interface.

You need [00-datasources.md](00-datasources.md) done (`workshop-ktranslate` and `workshop-ktranslate-logs`).

## A. Download the JSON

Open [labs/dashboards](dashboards/).

Download these five files (GitHub: open the file → **Download raw file**). Do not paste JSON into chat; it will truncate.

| File | Dashboard title after import |
|---|---|
| `device-summary.json` | Workshop Device Summary |
| `device-details.json` | Workshop Device Details |
| `prtg-summary.json` | Workshop PRTG Summary |
| `checkpoint-summary.json` | Workshop Check Point Summary |
| `aruba-summary.json` | Workshop Aruba Summary |

Import **Summary before Details**. The Summary “click a device” link expects Details to exist.

## B. Create the folder

1. Left menu: **Dashboards**.
2. **New** → **New folder**.
3. Name: `Network Observability`.
4. Create.

If the folder already exists, use it.

## C. Import one file (repeat for all five)

1. **Dashboards** → **New** → **Import**.
2. **Upload dashboard JSON file** and pick the file.
3. **Name** should fill in. Leave it.
4. **Folder:** **Network Observability**.
5. **Data sources:**
   - Prometheus → **workshop-ktranslate**
   - Loki → **workshop-ktranslate-logs**
   - Infinity → **workshop-network-apis** if you already have it. If not, leave it; those panels wait until Lab 5.
6. **Import**.

Repeat for the other four files.

If import says the UID already exists, open the existing dashboard instead of duplicating.

## D. Open Device Summary

Top search (or **Dashboards** → folder **Network Observability**). Type `Workshop Device Summary`. Searching only `Network Observability` finds the folder, not the board.

At the top: **datasource**, **loki**, maybe **infinity**.

1. **datasource** = `workshop-ktranslate`
2. **loki** = `workshop-ktranslate-logs`
3. Time range: **Last 1 hour** (or Last 30 minutes).
4. If Device Status is empty, change the datasource dropdown and refresh.

## E. Fleet hunt

On **Workshop Device Summary**:

1. **Active Network Alerts** (top) may be empty. Use the table.
2. **Device Status** table. Sort **Errors/s** or **CPU %**. Look for `bld4-fw-01` (CPU) and/or `bld4-asw-01` (errors). Either is a valid hunt.
3. Click the **Device** name. That should open **Workshop Device Details** with that device selected.

If Details opens but CPU / interfaces are empty, use the **Device** dropdown at the top and pick `bld4-asw-01`.

## F. Device hunt

On Device Details:

1. Overview: is CPU or Memory the story, or are they fine?
2. **Interface Status**: sort by Errors/s or by bps. Which interface is the outlier? (On the switch story you want **Gi1/0/24**.)
3. Confirm on the In / Out timeseries.
4. **Device Syslog**: one line should agree (CRC / collisions / TOOBIG). If syslog is empty, check the Loki dropdown.

## You are done when

You can put in chat one sentence: which device you picked, why (table), and which interface or resource is sick.

## Stretch

Change the Device picker to a healthy box (`dc-core-01` or `bld1-asw-01`). The error charts should go quiet.
