# Chat paste (facilitator)

Paste these as separate messages when that lab starts. Fill the blanks from your lab Cloud stack (Connections → the built-in Prom/Loki, or Grafana.com stack details). Do not paste a token that can write or see unrelated stacks. Prefer a Cloud Access Policy with `metrics:read` / `logs:read` only, scoped if you can.

## Join

```
Labs: https://github.com/Mesverrum/grafana-network-observability-workshop/tree/main/labs
Work in the Grafana URL from your invite email. Keep this webinar visible.
Your stack starts empty. When I paste data source credentials, do lab 00-datasources next.
Chat a screenshot if Save & test fails.
```

## After login (data sources)

```
Add these two data sources (lab 00-datasources). Leave Default off.

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
Probe: Oregon or North Virginia (public). Do not add Singapore yet.
Testing & synthetics → Synthetics (not k6 / Performance Testing).
```

## Lab 3 (import)

```
Import JSON from labs/dashboards into a folder named Network Observability.
Map Prometheus → workshop-ktranslate, Loki → workshop-ktranslate-logs.
Start with device-summary.json then device-details.json.
```

## Lab 4 (second vantage)

```
Same IP as Lab 2. Do not change the target.
Edit workshop-tcp → add public probe Singapore (keep Oregon or North Virginia) → Save.
Edit workshop-tr → add Singapore the same way.
Wait two TCP runs (~2 min). Compare duration by probe, and traceroute hops/map by probe.
Then Lab 4 alert (workshop-tcp duration, threshold in seconds — not 400).
```

## Lab 5 (Infinity)

```
Infinity data source name: workshop-network-apis
Mock URL: http://18.217.39.189:8088
If Infinity is missing from Add new connection:
  Administration → Plugins and data → Plugins → search Infinity → Install
  Then Connections → Add new connection → Infinity → Add new data source.
URL = the mock origin (no path). Allowed hosts = that same URL (include http:// and :8088).
Auth: No Auth. Save & test, then Explore: JSON, path /meraki/devices, Root empty.
```
