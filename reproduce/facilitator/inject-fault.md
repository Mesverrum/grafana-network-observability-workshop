# Inject Clos fault (Lab 5)

Student lab: [`labs/05-troubleshoot.md`](../../labs/05-troubleshoot.md). They already imported dashboards and explored a **healthy** fleet. You change the lab. They hunt. Do **not** name the device or interface in chat.

## What you inject

Sustained admin-disable of **HQ `leaf1` `ethernet-1/1`** (client-facing). SNMP Device Summary / Details and traps/syslog move. **Public-VIP synthetics stay green** — that is the teaching point (box vs user path).

Do not use `make emit-events` here. A 5s flap is gone before a 60s poll.

From **network-o11y-demo** (Windows host → SSM):

```text
python3 local/scripts/ssm-workshop-inject-fault.py start
```

On the colocated host:

```text
make -C local workshop-fault
```

Wait ~90s. On **your** Device Details for `leaf1`, confirm `ethernet-1/1` is down. Then paste the Lab 5 block from [chat-paste.md](chat-paste.md).

## What you say

> Something changed. Use the boards you already have. I am not going to tell you which box.

> Device Summary first. Then Details. Then syslog. Then your TCP check — does the internet path still look fine?

Timebox ~20 minutes. Volunteer one-line readouts in chat. Do not freeze for stragglers.

## Clear before Infinity (or at close)

```text
python3 local/scripts/ssm-workshop-inject-fault.py stop
```

or `make -C local workshop-fault-stop`.

Status: `python3 local/scripts/ssm-workshop-inject-fault.py status`

The start command also stops `events-loop` so background flaps do not compete with the hunt.

## Do not

- Announce `leaf1` or `ethernet-1/1`
- Shuffle Global Accelerator / hairpin for this lab
- Point them at Building 4 / Meraki (that is Lab 6)

## Checklist

- [ ] Lab 4 explore happened while the interface was still up
- [ ] `events-loop` stopped
- [ ] Fault start succeeded; your Details shows the port down
- [ ] Lab 5 chat paste does not name the box
- [ ] Fault cleared before close (or before Lab 6 if you want a clean SNMP picture on the Assistant board)
