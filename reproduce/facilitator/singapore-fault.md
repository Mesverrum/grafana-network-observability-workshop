# Singapore latency fault

Goal: they see a **path or latency change**, then write an alert. Two ways to get there. Prefer A.

## A. Hairpin (you own the routing)

Do this on **your** lab path, not on their laptops.

1. Before the room: they already created traceroute + TCP toward a hostname you control (Lab 2). Home probe is Oregon or North Virginia.
2. At Lab 4 start, change routing so that prefix hairpins through Singapore (or any APAC hop that was not on the baseline). Keep the destination IP the same so their check target does not change.
3. On a spare screen, run a traceroute from a US VPS or from the same public hostname so you can narrate hops if SM is slow.
4. Tell the room: "Path changed. Find it."

What they should see within a few SM intervals:

- `probe_duration_seconds` up on the home probe
- Traceroute: more hops and/or `probe_traceroute_route_hash` changed
- `probe_traceroute_total_hops` up

Traceroute frequency in Cloud is 120s minimum. Budget 4 minutes before you panic.

## B. Fallback: add the Singapore public probe

If you cannot touch routing in the room:

1. Have them **edit** the Lab 2 TCP (or HTTP) check.
2. Add probe **Singapore** (APAC, AWS). Keep Oregon.
3. Save. Wait two intervals.

They will see Singapore duration higher than Oregon. That is geo latency, not a hairpin. Say that. The alert skill is identical: duration by `probe`.

## Alert they should create

PromQL (Synthetic Monitoring metrics land on `grafanacloud-prom`):

```promql
max by (probe, instance, job) (probe_duration_seconds{job=~".*workshop.*"})
```

Or if they named the job `workshop-tcp`:

```promql
probe_duration_seconds{job="workshop-tcp"}
```

Threshold: above **2x their pre-fault p50**, or a fixed 0.4s if you do not want them doing math.

For path change:

```promql
changes(probe_traceroute_route_hash{job="workshop-tr"}[15m])
```

Above 0 means the path moved.

## Your checklist

- [ ] Board hostname is reachable from public probes (firewall allow-list if needed: Cloud SM public probe IPs)
- [ ] You know the pre-fault hop count
- [ ] You can revert the hairpin in one command
- [ ] Fallback B tested once on a Brokkr stack before the event
