# Lab 1 — Watch discovery (you do not deploy this)

The facilitator is discovering the lab on **their** collector. Your job is to understand the picture, not to copy commands.

## What to look for on the shared screen

1. **Credential group** — a pile of candidate SNMP secrets, not one community string taped to each IP.
2. **Target range** — a CIDR or inventory list. Discovery tries credentials against devices and keeps what authenticated.
3. **What shows up after** — device names, then interface series. The metric family looks like `kentik_snmp_*` because that is ktranslate's schema.

## Write down (30 seconds)

- What protocols did they mention besides SNMP? (traps, flows, syslog)
- Where does the data go after ktranslate? (Alloy, then Cloud)
- Is ktranslate official Grafana Support? (No. Community / partner.)

## On your stack (optional, if they already seeded data)

**Explore** → Prometheus. Run:

```promql
count by (device_name) (kentik_snmp_PollingHealth)
```

Empty is fine during this lab. Data may land after the break.

## You are done when

You can sketch devices → ktranslate → Alloy → Cloud on a notepad without looking at the whiteboard.
