# Dashboard JSON (facilitator)

Pulled from live Grafana on the facilitator lab (Assistant-edited). **Import these before the webinar**, into a folder named **Network Observability**. Students do **not** import.

Map Prometheus → this stack’s Prometheus (`grafanacloud-…-prom`, or an alias named `workshop-ktranslate`). Map Loki → this stack’s Loki (`grafanacloud-…-logs`, or `workshop-ktranslate-logs`). Map Infinity → `workshop-network-apis` after you create that source.

1. [device-summary.json](device-summary.json) → Workshop Device Summary
2. [device-details.json](device-details.json) → Workshop Device Details
3. [prtg-summary.json](prtg-summary.json) → Workshop PRTG Summary
4. [checkpoint-summary.json](checkpoint-summary.json) → Workshop Check Point Summary
5. [aruba-summary.json](aruba-summary.json) → Workshop Aruba Summary

On GitHub, open a file → **Download raw file**. Prefer `gcx dashboards create` / the v2 API for tabbed boards — do not flatten them with legacy `POST /api/dashboards/db` if the export is a v2 manifest.
