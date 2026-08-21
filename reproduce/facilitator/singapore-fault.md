# Singapore latency fault

Goal: they see a **path or latency change**, then write an alert. Prefer A (same public VIP, you shuffle AWS backends). DNS is not the lever. Announce the switch on **mic and chat**.

Wiring and the Grafana button: **[hairpin.md](hairpin.md)**.

## A. Hairpin (public VIP + dashboard action)

Do this on **your** path. Attendees only watch SM metrics on **their** stacks.

1. Before the webinar: GA VIP is healthy in the US. `hairpin-agent.py` is polling. Facilitator board `workshop-facilitator-control` is on **your** stack only. Lab 2 chat paste is the VIP and `:80`.
2. They create traceroute + TCP toward that IP and pick a **public** home probe (Oregon or North Virginia).
3. At Lab 4 start, open the facilitator board and click **Enable Singapore path**. That POSTs `/admin/hairpin`. The agent sets Singapore endpoint weight 100 / US 0. Destination IP does not change.
4. Wait one or two SM intervals. Duration should rise. Traceroute hops may move (anycast / region) or stay similar — duration is the finding either way.
5. Say: "Path changed. Lab 4 — find it." Paste Lab 4 in chat.
6. When you are done talking, click **Restore direct US**.

## B. Fallback: add the Singapore public probe

If the VIP shuffle is dead during the call:

1. Have them **edit** the Lab 2 TCP check. Paste those clicks in chat.
2. Add probe **Singapore** (APAC, AWS). Keep the home probe.
3. Save. Wait two intervals.

They will see Singapore duration higher than Oregon. That is a second vantage, not the VIP landing in APAC. Say that. The alert skill is identical: duration by `probe`.

## Alert they should create

They stay on the **workshop-tcp** check → **Alerts** / **Alerting**. Duration threshold = **2x Lab 2**, or **400ms**. You write PromQL only if you are debugging on your stack:

```promql
probe_duration_seconds{job="workshop-tcp"}
```

Path change is the traceroute **hop list on the check**, not Explore. If you need a hash series on your share:

```promql
changes(probe_traceroute_route_hash{job="workshop-tr"}[15m])
```

## Your checklist

- [ ] VIP answers from a public laptop (`curl http://15.197.194.37/`)
- [ ] Attendees told the **same IP** in chat; public Oregon or N. Virginia
- [ ] `hairpin-agent.py` running; Grafana button tested once (enable + restore)
- [ ] You know the pre-fault duration (and hop count if traceroute moved)
- [ ] Fallback B tested once on a sandbox stack before the webinar
- [ ] Chat text for “path changed” / “add Singapore probe” is ready to paste
