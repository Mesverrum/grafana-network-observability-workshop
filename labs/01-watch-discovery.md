# Lab 1 — Watch discovery

← Previous: [Add the shared lab data sources](00-datasources.md)

The facilitator is discovering the lab on their collector and sharing that screen. Follow the picture.

If you have not added **workshop-ktranslate** yet, you can still watch. Add the data sources from [00-datasources.md](00-datasources.md) before Lab 3.

## What to look for on the shared screen

**ktranslate** is the SNMP collector on the facilitator’s lab (community / partner, not Grafana Support). **Alloy** is Grafana’s agent that forwards that data into Cloud.

1. **Credential group** — one pile of candidate SNMP secrets per site (`srl-hq`, `srl-branch1`, `srl-branch2`), not a community string taped to each IP.
2. **Target range** — a CIDR in that group’s env (`TARGETS`). Discovery tries credentials against devices and keeps what authenticated.
3. **What shows up after** — a `devices-*.yaml` per group, then polling. Metrics are named `kentik_snmp_*` (the same family you queried in [00-datasources.md](00-datasources.md)). The label **`tags_snmp_group`** is the site.

## Note for yourself

- What protocols did they mention besides SNMP?
- Where does the data go after ktranslate?
- Is ktranslate official Grafana Support?

## Optional: see the same names on your stack

Only if [00-datasources.md](00-datasources.md) already succeeded.

**Explore** (compass) → top picker **workshop-ktranslate**. Click **Run query**:

```promql
count by (device_name, tags_snmp_group) (kentik_snmp_PollingHealth)
```

You should get a row per device with a site label. Empty means wait, or you are on the wrong datasource.

## You are done when

You can explain devices → ktranslate → Alloy → Cloud without staring at the shared diagram.

Next: [Lab 2 — Synthetics](02-synthetics.md) →
