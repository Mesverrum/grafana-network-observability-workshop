# Lab 1 — Watch discovery

The facilitator is discovering the lab on their collector and sharing that screen. Follow the picture.

If you have not added **workshop-ktranslate** yet, you can still watch. Add the data sources from [00-datasources.md](00-datasources.md) before Lab 3.

## What to look for on the shared screen

1. **Credential group** — a pile of candidate SNMP secrets, not one community string taped to each IP.
2. **Target range** — a CIDR or inventory list. Discovery tries credentials against devices and keeps what authenticated.
3. **What shows up after** — device names, then interface series. The metric family looks like `kentik_snmp_*` because that is ktranslate’s schema.

## Note for yourself

- What protocols did they mention besides SNMP? (traps, flows, syslog)
- Where does the data go after ktranslate? (Alloy, then Cloud)
- Is ktranslate official Grafana Support? (No. Community / partner.)

## Optional: see the same names on your stack

Only if [00-datasources.md](00-datasources.md) already succeeded.

**Explore** → top picker **workshop-ktranslate**. Click **Run query**:

```promql
count by (device_name) (kentik_snmp_PollingHealth)
```

You want names like `bld4-asw-01` and `dc-core-01`. Empty means wait, or you are on the wrong datasource.

## You are done when

You can explain devices → ktranslate → Alloy → Cloud without staring at the shared diagram.
