# Chat paste (facilitator)

Paste these as separate messages when that lab starts. **Do not paste Prometheus/Loki tokens.** The shared stack already has datasources.

## Join

```
Labs: https://github.com/Mesverrum/grafana-network-observability-workshop/tree/main/labs
Grafana: REPLACE_SHARED_STACK_URL  (same stack for everyone)
Log in first (labs/00-login.md). Do not add Prom/Loki. Do not import the GitHub JSON (UIDs already exist).
Folder Network Observability is the clean copy.
Make your own folder: Network Observability — Your Name
Then Save as / copy Device Summary + Details into that folder so you can chop.
Chat a screenshot if you cannot see Workshop Device Summary.
```

## Lab 1 (explore)

```
Open Workshop Device Summary. SNMP group All. Click a device into Details.
Learn the table → device → interface path while the fleet is quiet.
Copy those two boards into your named folder if you want to edit panels.
```

## Lab 2 (synthetics)

```
Testing & synthetics → Synthetics (not k6 / Performance Testing).
Open workshop-tcp and workshop-tr first (do not Edit those).
Optional: create your own TCP + traceroute. Job names MUST be unique:
  workshop-tcp-YOURHANDLE
  workshop-tr-YOURHANDLE
Same target: 15.197.194.37  and  15.197.194.37:80
Probe: Oregon or North Virginia (public).
```

## Lab 3 (incident)

```
Something changed on the shared lab. Do not change the synthetic target.
Use Device Summary → Details (shared or your copy), syslog if present, and TCP (workshop-tcp or yours).
Chat one sentence: site, device, what changed, how you know.
```

## Lab 4 (Infinity)

```
Infinity data source workshop-network-apis is already on this stack. Do not create a second Infinity.
Explore: JSON, path /meraki/devices, Root empty.
Then Network Observability → Workshop PRTG / Check Point / Aruba Summary.
Save Assistant boards into YOUR folder. Title: Workshop campus — Your Name.
```

## Optional stretch (Singapore)

```
Same IP as Lab 2. Do not change the target.
Add public probe Singapore on YOUR checks (workshop-tcp-YOURHANDLE). Leave the shared workshop-tcp alone unless I say so.
Wait two TCP runs (~2 min). Compare duration by probe, and traceroute hops/map by probe.
```
