# Optional stretch — two public probes (facilitator)

Student page: [`labs/stretch-second-vantage.md`](../../labs/stretch-second-vantage.md). They add public **Singapore** on **their** checks (`workshop-tcp-<handle>`). Leave canonical `workshop-tcp` alone unless you want the whole room on one object. This is **not** Lab 3.

Skip this stretch if the hunt is running long. You do not need the hairpin board.

## What you say (only if you run it)

> Probe is where Grafana runs the check. Target is the IP. Lab 2 was one US city. I will add Singapore on the shared checks. Keep the first probe. Do not Edit unless I name you.

> TCP duration on this VIP may stay small on both (Global Accelerator handshake is to a nearby edge). Traceroute hop list / map by probe is still two different paths. If Singapore TCP is slower, that is extra.

Paste the optional Singapore block from [chat-paste.md](chat-paste.md).

## Hairpin board (optional aside)

[`hairpin.md`](hairpin.md) still moves which nginx **origin** answers (`curl` body Ohio vs Singapore). Public SM TCP/traceroute to the anycast VIP does **not** follow that origin. Do not make students wait on it.

## Alert (optional, one volunteer)

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
