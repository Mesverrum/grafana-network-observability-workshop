# Lab 2 — Synthetics: traceroute and a port check

SNMP is what the box thinks. Synthetics are what a path from the internet looks like.

The facilitator will **paste a target hostname in webinar chat** (and usually on a slide). Use that. Do not invent a customer production VIP.

Docs: [Traceroute checks](https://grafana.com/docs/grafana-cloud/testing/synthetic-monitoring/create-checks/checks/traceroute/), [TCP checks](https://grafana.com/docs/grafana-cloud/testing/synthetic-monitoring/create-checks/checks/tcp/), [public probes](https://grafana.com/docs/grafana-cloud/testing/synthetic-monitoring/create-checks/public-probes/).

## A. Traceroute

1. Left menu: **Testing & synthetics** → **Synthetics**.
2. **Create new check** (wording may be **Add new check**).
3. Choose **Traceroute**.
4. Job name: `workshop-tr`
5. Target: the hostname from chat.
6. Probe locations: pick **one** home probe, **Oregon** or **North Virginia**. Do not add Singapore yet.
7. Frequency: 120 seconds (minimum for traceroute).
8. **Save**. **Test** once if the UI offers it.

## B. TCP port

1. Create another check. Type **TCP** (sometimes under API Endpoint; set protocol to TCP).
2. Job name: `workshop-tcp`
3. Target: hostname **and port** from chat (example `lab.example.com:443`).
4. Same home probe as the traceroute.
5. Frequency: 60 seconds is fine.
6. Save.

## C. Prove it

1. Open the check → recent runs. You want at least one green.
2. **Explore** → Prometheus:

```promql
probe_duration_seconds{job="workshop-tcp"}
```

```promql
probe_traceroute_total_hops{job="workshop-tr"}
```

Save today's hop count and a ballpark duration (screenshot or a note). You will need that after the fault.

## You are done when

Both checks have a result, and you know which probe you used. If the UI is confusing, post a screenshot in chat rather than waiting.

## Stretch

Add a second home-region probe (Ohio or Montreal). Still no Singapore.
