# Lab 3 — Import dashboards, then hunt

← Previous: [Lab 2 — Synthetics](02-synthetics.md)

Import dashboard files from this repo, then work them like a NOC: table first, then a device, then the interface.

You need [00-datasources.md](00-datasources.md) done (`workshop-ktranslate` and `workshop-ktranslate-logs`).

## A. Download the files

Open [labs/dashboards](dashboards/).

Download these five `.json` files (GitHub: open the file → **Download raw file**). Paste into chat and it will truncate.

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
5. **Data sources** (map each row to a source you already created):
   - Prometheus → **workshop-ktranslate**
   - Loki → **workshop-ktranslate-logs**
   - Infinity → leave as-is if you do not have that source yet. Lab 5 adds it. Those vendor panels stay empty until then.
6. **Import**.

Repeat for the other four files.

If Grafana says the dashboard already exists, open that dashboard instead of importing again.

## D. Open Device Summary

Search box at the **top of Grafana** (or **Dashboards** → folder **Network Observability**). Type `Workshop Device Summary`. Searching only `Network Observability` finds the folder, not the board.

Dropdowns at the top of the dashboard: **datasource**, **loki**, maybe **infinity**. Time range is the clock control at the **upper right**.

1. **datasource** = `workshop-ktranslate`
2. **loki** = `workshop-ktranslate-logs`
3. **SNMP group** = All (or pick `srl-hq`, then a branch, to see the three sites).
4. Time range: **Last 1 hour** (or Last 30 minutes).
5. If Device Status is empty, change the datasource dropdown and refresh (circular arrow).

## E. Fleet hunt

On **Workshop Device Summary**:

1. **Active Network Alerts** (top) may be empty. Use the table.
2. **Device Status** table. Click a column header to sort **Errors/s** or **CPU %**. Pick a box that stands out. Use **SNMP group** to flip HQ vs a branch.
3. Click the **Device** name. That should open **Workshop Device Details** with that device selected.

If Details opens but CPU / interfaces are empty, use the **Device** dropdown at the top of Details and pick another live name.

## F. Device hunt

On Device Details:

1. Overview: is CPU or Memory the story, or are they fine?
2. **Interface Status**: sort by Errors/s or by bps. Which interface is the outlier?
3. Confirm on the In / Out timeseries.
4. **Device Syslog**: may be empty. If it has lines, they should agree with the interface you picked. If syslog is empty, stay on the SNMP table — that is enough.

## You are done when

You can put in chat one sentence: which device you picked, why (table), and which interface or resource is sick.

## Stretch

Change the Device picker to a box on another site. Compare CPU, errors, and interfaces to the one you hunted.

Next: [Lab 4 — A second vantage](04-latency-fault.md) →
