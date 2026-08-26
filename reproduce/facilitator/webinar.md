# Webinar delivery

This workshop is a **webinar**, not a classroom. Attendees are remote, on mute, with Grafana in another window. They will not have a whiteboard, a printed workbook, or a person to wave at.

## How you run it

- **You share** architecture slides (or a simple diagram), then your collector / Grafana. They **drive their own** stack for labs 1–6.
- **Chat is the board.** Paste from [chat-paste.md](chat-paste.md): labs URL, **datasource credentials**, public VIP + `:80`, mock/Infinity URL, Assistant prompts, “start Lab N”.
- **Do not wait** for everyone to finish. Give a timebox, ask for a thumbs-up or a one-line chat readout from volunteers, then move.
- **UI, not Explore.** They live in Synthetics check pages and **Network Observability** dashboards. You show Explore once on the share in Lab 1 (Save & test prove-out).
- **Help:** they raise hand or chat. Unmute one person at a time. Screenshare *their* Grafana only if they can; otherwise they screenshot into chat.
- **Break:** they stay in the webinar. You use it to confirm Clos SNMP on the shared Prom + SM checks, not to walk the room.

## Paste this at join

See the full blocks in [chat-paste.md](chat-paste.md). Join message:

```
Labs: https://github.com/Mesverrum/grafana-network-observability-workshop/tree/main/labs
Work in the Grafana URL from your invite email. Keep this webinar visible.
Your stack starts empty. Log in first. When I paste data source credentials, do Lab 1 (01-datasources).
Chat a screenshot if Save & test fails.
```

After login, paste the **workshop-ktranslate** Prometheus + Loki block. They cannot import until that Save & test is green.

Order they drive: login → data sources → synthetics → import → explore → **you inject a fault** → they hunt → Infinity.

At Lab 2, paste this so they can copy it:

```
Target: 15.197.194.37
TCP: 15.197.194.37:80
Probe: Oregon or North Virginia (public). Do not add Singapore unless I say so.
```

Do not tell them to install or select a private probe. Their stacks cannot see yours. Singapore is optional stretch, not the incident. Clos fault: [inject-fault.md](inject-fault.md).

At Lab 6, paste the Infinity block from [chat-paste.md](chat-paste.md). They install Infinity from **Plugins** if the catalog is empty, then add `workshop-network-apis` (URL + Allowed hosts = mock origin, No Auth). Prove with Explore `/meraki/devices`.

## What not to say

- “Write it on the board / your notepad / the whiteboard.”
- “Wave if you are stuck.”
- “I will come around.”
- The device or interface you disabled.
- Anything that assumes they are in the same room.
