# Lab 4 — The path got worse

The facilitator is changing routing (or adding a Singapore probe). Your Lab 2 checks stay pointed at the same hostname.

## Investigate

1. Open your `workshop-tcp` check. Compare duration **now** vs the number you wrote in Lab 2.
2. Explore:

```promql
probe_duration_seconds{job="workshop-tcp"}
```

Legend by `probe`. Which location got slower?

3. Traceroute:

```promql
probe_traceroute_total_hops{job="workshop-tr"}
```

```promql
changes(probe_traceroute_route_hash{job="workshop-tr"}[20m])
```

If hops went up or the hash changed, the path moved. That is the hairpin story.

4. Open the traceroute check UI and look at the hop list if the UI shows one.

## Alert

**Alerting** → New alert rule.

- Name: `workshop tcp latency`
- Query: `probe_duration_seconds{job="workshop-tcp"}`
- Condition: above a number **you** choose (2x your Lab 2 baseline, or 400ms if you want a default)
- Evaluate every 1m, pending 2m

Save it. You do not need to page Slack.

## You are done when

You can say whether this was a **path change** (hops/hash) or **just a slower probe** (Singapore added, hops maybe unchanged).

If hops did not move, that is still a valid finding. Write it down.
