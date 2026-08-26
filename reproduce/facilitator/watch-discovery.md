# Pre-session discovery (facilitator)

Finish this **before** attendees join. Do not run discovery on the call. They never watch it.

Student notes used to live in `labs/01-watch-discovery.md` (now a pointer off this path).

**ktranslate** is the SNMP collector (community / partner, not Grafana Support). **Alloy** is Grafana’s agent that forwards that data into Cloud.

## Before the webinar

On the colocated host, discover all three groups so polling is already live:

```text
make discover GROUP=srl-hq
make discover GROUP=srl-branch1
make discover GROUP=srl-branch2
```

Restore collectors if needed: `python3 local/scripts/ssm-alloy-ktranslate-parallel.py`.

Confirm on **your** Explore before you start:

```promql
count by (device_name, tags_snmp_group) (kentik_snmp_PollingHealth)
```

Expect HQ `spine1` / `leaf1` / `leaf2`, branches `leaf-br1` / `leaf-br2`. Building 4 / Check Point / EdgeConnect names are the **Infinity mocks** in Lab 6, not this SNMP walk.

## How it worked (architecture talk only)

If you explain discovery on a slide, keep it past tense. They are not watching a run.

1. **Credential group** — one pile of candidate SNMP secrets per site (`srl-hq`, `srl-branch1`, `srl-branch2`), not a community string taped to each IP.
2. **Target range** — a CIDR in that group’s env (`TARGETS`). Discovery tried credentials against devices and kept what authenticated.
3. **What is polling now** — a `devices-*.yaml` per group. Metrics are named `kentik_snmp_*`. The label **`tags_snmp_group`** is the site.

Group files live at `local/groups/srl-hq.env` (and the two branch files). Device lists: `state/devices-srl-*.yaml` on the colocated host (`/opt/network-o11y-demo/local/…`).
