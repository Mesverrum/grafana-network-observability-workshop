# Optional stretch — two public probes (facilitator)

Student page: [`labs/stretch-second-vantage.md`](../../labs/stretch-second-vantage.md). They add the public **Singapore** probe on the **same VIP**. This is **not** Lab 5. The incident is the Clos interface you disable ([inject-fault.md](inject-fault.md)).

Skip this stretch if the hunt is running long. You do not need the hairpin board.

## What you say (only if you run it)

> Probe is where Grafana runs the check. Target is the IP. Lab 2 was one US city. Add Singapore. Keep the first probe.

> TCP duration on this VIP may stay small on both (Global Accelerator handshake is to a nearby edge). Traceroute hop list / map by probe is still two different paths. If Singapore TCP is slower, that is extra.

Paste the optional Singapore block from [chat-paste.md](chat-paste.md).

## Hairpin board (optional aside)

[`hairpin.md`](hairpin.md) still moves which nginx **origin** answers (`curl` body Ohio vs Singapore). Public SM TCP/traceroute to the anycast VIP does **not** follow that origin. Do not make students wait on it.

## Alert they should create

`workshop-tcp` check UI, or Grafana-managed:

```promql
probe_duration_seconds{job="workshop-tcp"}
```

Threshold in **seconds** (example `0.05`). Do not use `400`. Group by `probe` if the UI allows.

## Checklist

- [ ] Lab 2 paste said **do not add Singapore unless I say so**
- [ ] Stretch paste: add Singapore on tcp + traceroute, same IP
- [ ] You are not blocked on `applied_num` / GA weights
- [ ] If Singapore is missing from the probe list, they refresh **Testing & synthetics → Probes**
