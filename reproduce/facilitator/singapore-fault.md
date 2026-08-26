# Lab 4 — two public probes (facilitator)

Student lab: [`labs/04-latency-fault.md`](../../labs/04-latency-fault.md). They add the public **Singapore** probe on the **same VIP**. You do not need the hairpin board for this exercise.

Goal: **vantage**. Same target, two cities, two paths. Then an alert on the TCP check.

## What you say

> Probe is where Grafana runs the check. Target is the IP. Lab 2 was one US city. Add Singapore. Keep the first probe.

> TCP duration on this VIP may stay small on both (Global Accelerator handshake is to a nearby edge). Traceroute hop list / map by probe is still two different paths. If Singapore TCP is slower, that is extra.

Paste the Lab 4 block from [chat-paste.md](chat-paste.md).

## Hairpin board (optional aside)

[`hairpin.md`](hairpin.md) still moves which nginx **origin** answers (`curl` body Ohio vs Singapore). Public SM TCP/traceroute to the anycast VIP does **not** follow that origin. Do not make students wait on it.

## Alert they should create

`workshop-tcp` check UI, or Grafana-managed:

```promql
probe_duration_seconds{job="workshop-tcp"}
```

Threshold in **seconds** (example `0.05`). Do not use `400`. Group by `probe` if the UI allows.

## Checklist

- [ ] Lab 2 paste said **do not add Singapore yet**
- [ ] Lab 4 paste: add Singapore on tcp + traceroute, same IP
- [ ] You are not blocked on `applied_num` / GA weights
- [ ] If Singapore is missing from the probe list, they refresh **Testing & synthetics → Probes**
