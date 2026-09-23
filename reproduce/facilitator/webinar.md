# Webinar delivery

This workshop is a **webinar**, not a classroom. Attendees are remote, on mute, with Grafana in another window. They will not have a whiteboard, a printed workbook, or a person to wave at.

Everyone is on **one shared Grafana Cloud stack**. You provision datasources and the clean folder. They log in, make a named folder, and may clone synthetics with unique job names.

## How you run it

- **You share** architecture slides (or a simple diagram), then Grafana on the **shared** stack. They **drive the same** stack for labs 1–4.
- **Chat is the board.** Paste from [chat-paste.md](chat-paste.md): labs URL, **Grafana URL** (no tokens), “start Lab N”, Assistant prompts.
- **Do not wait** for everyone to finish. Give a timebox, ask for a thumbs-up or a one-line chat readout from volunteers, then move.
- **UI, not Explore.** They live in dashboards (shared folder or their copy) and Synthetics. You show Explore once on the share if SNMP looks empty.
- **Help:** they raise hand or chat. Unmute one person at a time. Screenshare *their* Grafana only if they can; otherwise they screenshot into chat.
- **Break:** they stay in the webinar. You use it to confirm Clos SNMP + SM checks, not to walk the room.

## Paste this at join

See the full blocks in [chat-paste.md](chat-paste.md). Join message:

```
Labs: https://github.com/Mesverrum/grafana-network-observability-workshop/tree/main/labs
Grafana: REPLACE_SHARED_STACK_URL
Log in first. Do not add Prom/Loki. Do not import GitHub JSON.
Make a folder: Network Observability — Your Name
```

Order they drive: login → named folder + explore → synthetics (shared and/or unique jobs) → **you inject a fault** → they hunt → Infinity.

Do not tell them to install or select a private probe. Singapore is optional stretch on **their** checks. Clos fault: [inject-fault.md](inject-fault.md).

At Lab 4, paste the Infinity block from [chat-paste.md](chat-paste.md). The source `workshop-network-apis` already exists. Prove with Explore `/meraki/devices` if someone is stuck.

## What not to say

- “Write it on the board / your notepad / the whiteboard.”
- “Wave if you are stuck.”
- “I will come around.”
- The device or interface you disabled.
- “Paste this glc_ token into Connections.”
- Anything that assumes they are in the same room.
