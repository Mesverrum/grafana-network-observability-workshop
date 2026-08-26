# Public VIP + dashboard path toggle

Each attendee has their own Brokkr stack. They cannot pick a private probe you registered on yours. Give them **one public IP**. They hit it with a **public** Synthetic Monitoring probe. You shuffle **where that IP lands in AWS**.

```
Attendee stacks
  → public probe (Oregon / N. Virginia)
  → Global Accelerator anycast VIP :80
  → US nginx  (hairpin off)
  → Singapore nginx  (hairpin on)

Facilitator dashboard (Editor)
  → Infinity POST /admin/hairpin
  → hairpin-agent on the control host
  → aws globalaccelerator UpdateEndpointGroup  (US weight 100/0 vs SG 100/0)
```

Same destination IP all day. No DNS flip. No private probe on student stacks.

## What you stand up once

1. **AWS Global Accelerator** with a TCP :80 listener and two endpoint groups:
   - `us-east-2` — EIP of the US nginx target
   - `ap-southeast-1` — EIP of the Singapore nginx
2. Control API (`POST`/`GET` `/admin/hairpin`) on a public URL. Optional `WORKSHOP_ADMIN_TOKEN`.
3. `hairpin-agent.py` on the control host. `HAIRPIN_ON_CMD` / `HAIRPIN_OFF_CMD` call `aws globalaccelerator update-endpoint-group`.
4. Facilitator dashboard imported **only** on your stack.

GA anycast can move **traceroute hops** (different ingress PoP). It will **not** move public-probe TCP duration — GA finishes the handshake at the edge. Laptop `curl` to `:80` still shows origin RTT and the Singapore vs US body. Health-check + weight updates take ~15–30s, then wait one traceroute interval (~2 min).

## Agent

On the control host (Python 3 stdlib only):

```bash
export HAIRPIN_API_URL=http://127.0.0.1:8088
export HAIRPIN_ADMIN_TOKEN=...          # same as WORKSHOP_ADMIN_TOKEN
export HAIRPIN_ON_CMD='/usr/local/sbin/hairpin-on'
export HAIRPIN_OFF_CMD='/usr/local/sbin/hairpin-off'
python3 hairpin-agent.py
```

Those scripts set US weight 0 / SG 100 (on) and the reverse (off). Report loop POSTs `/admin/hairpin/applied` so the dashboard **Applied** stat matches desired.

## Currently running (2026-08-21)

Account `494614287886`. Tear down when the webinar is over.

| Thing | Value |
|---|---|
| Grafana stack (facilitator) | `marcnetterfield1` |
| Student target VIP | `15.197.194.37` (GA pair `3.33.195.105`) |
| TCP | `15.197.194.37:80` |
| Control API | `http://18.217.39.189:8088/admin/hairpin` |
| Facilitator board | UID `workshop-facilitator-control` |
| Direct (US Ohio) | ~150 ms from a US laptop; body `workshop-hairpin-target` |
| Singapore backend | ~390 ms from the same laptop; body `workshop-hairpin-singapore` |

Chat paste for Lab 2:

```
Target: 15.197.194.37
TCP: 15.197.194.37:80
Probe: Oregon or North Virginia (public)
```

Admin token is gitignored: `network-o11y-demo/local/state/workshop-hairpin-admin.token`.

AWS: accelerator `workshop-hairpin`, US target `i-0d1bd8765c3795a40`, Singapore `i-06adae86d134510e1`, control host `i-05a27ce9fcbcaf424`. The old WireGuard private-probe hairpin is unused.

## Grafana button

Board UID `workshop-facilitator-control`. Overlay on **your** stack:

```bash
python3 overlay/apply.py \
  --manifest stacks-facilitator.csv \
  --mock-url https://YOUR_CONTROL_HOST \
  --admin-token "$WORKSHOP_ADMIN_TOKEN" \
  --facilitator
```

Student overlay must **not** use `--facilitator`.

Click **Enable Singapore path**. Grafana 12.2+ visualization actions send the POST **through Infinity**. You need **Editor**.

## Revert

Click **Restore direct US**, or:

```bash
curl -sS -H "X-Workshop-Admin: $WORKSHOP_ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"active":false}' \
  https://YOUR_CONTROL_HOST/admin/hairpin
```

The agent should flip within `HAIRPIN_POLL_SECS` (default 2s). GA then needs ~15–30s.

## Optional Singapore stretch

Student stretch is adding a **public Singapore probe** on the same VIP ([`singapore-fault.md`](singapore-fault.md)). Lab 5 is the Clos interface you disable ([`inject-fault.md`](inject-fault.md)). This hairpin board is an optional origin demo (`curl` body). It is not their lever.
