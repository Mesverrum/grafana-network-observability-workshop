# Lab 3 — Import dashboards

← Previous: [Lab 2 — Synthetics](02-synthetics.md)

Import dashboard files from this repo into a folder. You will hunt in the next lab. For now, get the boards onto your stack and confirm Device Summary loads.

You need [Lab 1](01-datasources.md) done (`workshop-ktranslate` and `workshop-ktranslate-logs`).

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
   - Infinity → leave as-is if you do not have that source yet. Lab 6 adds it. Those vendor panels stay empty until then.
6. **Import**.

Repeat for the other four files.

If Grafana says the dashboard already exists, open that dashboard instead of importing again.

## D. Confirm Device Summary loads

Search box at the **top of Grafana** (or **Dashboards** → folder **Network Observability**). Type `Workshop Device Summary`. Searching only `Network Observability` finds the folder, not the board.

Dropdowns at the top of the dashboard: **datasource**, **loki**, maybe **infinity**. Time range is the clock control at the **upper right**.

1. **datasource** = `workshop-ktranslate`
2. **loki** = `workshop-ktranslate-logs`
3. **SNMP group** = All (or pick `srl-hq`, then a branch, to see the three sites).
4. Time range: **Last 1 hour** (or Last 30 minutes).
5. If Device Status is empty, change the datasource dropdown and refresh (circular arrow).

You should see HQ (`spine1`, `leaf1`, `leaf2`) and the two branches (`leaf-br1`, `leaf-br2`). That is enough for this lab.

## You are done when

Workshop Device Summary is open, datasource dropdowns are set, and the Device Status table has rows.

Next: [Lab 4 — Explore](04-explore.md) →
