# Guided discovery (facilitator share)

This is **not** a student lab. They log in, add data sources, and create synthetics while you share discovery. Student notes used to live in `labs/01-watch-discovery.md` (now a pointer).

Live discover on the colocated collector. Narrate while it runs. They do not SSH.

**ktranslate** is the SNMP collector (community / partner, not Grafana Support). **Alloy** is Grafana’s agent that forwards that data into Cloud.

## What to point at

1. **Credential group** — one pile of candidate SNMP secrets per site (`srl-hq`, `srl-branch1`, `srl-branch2`), not a community string taped to each IP.
2. **Target range** — a CIDR in that group’s env (`TARGETS`). Discovery tries credentials against devices and keeps what authenticated.
3. **What shows up after** — a `devices-*.yaml` per group, then polling. Metrics are named `kentik_snmp_*`. The label **`tags_snmp_group`** is the site.

Share `local/groups/srl-hq.env` (CIDR + community), then the matching `state/devices-srl-hq.yaml` on the colocated host (`/opt/network-o11y-demo/local/…`). Repeat the idea for the two branch groups.

Commands:

```text
make discover GROUP=srl-hq
make discover GROUP=srl-branch1
make discover GROUP=srl-branch2
```

Restore collectors if needed: `python3 local/scripts/ssm-alloy-ktranslate-parallel.py`.

Point at `kentik_snmp_PollingHealth` when it lands. Names: HQ `spine1` / `leaf1` / `leaf2`, branches `leaf-br1` / `leaf-br2`. Building 4 / Check Point / EdgeConnect names are the **Infinity mocks** in Lab 6, not this SNMP walk.

If they already finished Lab 1 Save & test, they can run the same query on `workshop-ktranslate`:

```promql
count by (device_name, tags_snmp_group) (kentik_snmp_PollingHealth)
```
