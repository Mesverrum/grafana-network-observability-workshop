# Chat paste (facilitator)

Paste these as separate messages when that lab starts. Fill the blanks from your lab Cloud stack (Connections → the built-in Prom/Loki, or Grafana.com stack details). Do not paste a token that can write or see unrelated stacks. Prefer a Cloud Access Policy with `metrics:read` / `logs:read` only, scoped if you can.

## Join

```
Labs: https://github.com/Mesverrum/grafana-network-observability-workshop/tree/main/labs
Work in the Grafana URL from your invite email. Keep this webinar visible.
Your stack starts empty. Log in first (labs/00-login.md). When I paste data source credentials, do Lab 1 (01-datasources).
Chat a screenshot if Save & test fails.
```

## After login (data sources) — Lab 1

```
Add these two data sources (Lab 1 — 01-datasources). Leave Default off.

Prometheus name: workshop-ktranslate
Prometheus URL: https://prometheus-prod-67-prod-us-west-0.grafana.net/api/prom
Prometheus user: 3532656
Prometheus password: REPLACE_GLC_TOKEN

Loki name: workshop-ktranslate-logs
Loki URL: https://logs-prod-021.grafana.net
Loki user: 1762003
Loki password: REPLACE_GLC_TOKEN
```

## Lab 2 (synthetics)

```
Target: 15.197.194.37
TCP: 15.197.194.37:80
Probe: Oregon or North Virginia (public). Do not add Singapore unless I say so.
Testing & synthetics → Synthetics (not k6 / Performance Testing).
```

## Lab 3 (import)

```
Import JSON from labs/dashboards into a folder named Network Observability.
Map Prometheus → workshop-ktranslate, Loki → workshop-ktranslate-logs.
Start with device-summary.json then device-details.json.
Confirm Device Summary has rows. Do not hunt yet.
```

## Lab 4 (explore)

```
Open Workshop Device Summary. SNMP group All. Click a device into Details.
Learn the table → device → interface path while the fleet is quiet.
Leave workshop-tcp as it is.
```

## Lab 5 (incident)

```
Something changed on the shared lab. Do not change your synthetic target.
Use Workshop Device Summary → Details, syslog if present, and workshop-tcp.
Chat one sentence: site, device, what changed, how you know.
```

## Lab 6 (Infinity)

```
Infinity data source name: workshop-network-apis
Mock URL: http://18.217.39.189:8088
If Infinity is missing from Add new connection:
  Administration → Plugins and data → Plugins → search Infinity → Install
  Then Connections → Add new connection → Infinity → Add new data source.
URL = the mock origin (no path). Allowed hosts = that same URL (include http:// and :8088).
Auth: No Auth. Save & test, then Explore: JSON, path /meraki/devices, Root empty.
```

## Optional stretch (Singapore)

```
Same IP as Lab 2. Do not change the target.
Edit workshop-tcp → add public probe Singapore (keep Oregon or North Virginia) → Save.
Edit workshop-tr → add Singapore the same way.
Wait two TCP runs (~2 min). Compare duration by probe, and traceroute hops/map by probe.
```
