# Start here

← Previous: [Labs](README.md)

1. Join the webinar. Stay on mute unless you are asking a question.
2. Log into the **shared** Grafana Cloud URL from the **invite email** or webinar chat. Use the password from that same message. If Grafana.com asks you to pick an org, pick the one that matches the URL they sent (`something.grafana.net`).
3. Confirm Grafana opens. You should already see a **Network Observability** folder (or the folder name in chat). If the left menu is only icons, click **☰**. Later labs use **Dashboards**, top search, and **Testing & synthetics**. Keep Grafana next to the webinar.

Do **not** add Prometheus/Loki from a token, and do **not** import the GitHub JSON. Those objects already exist. A second import with the same dashboard UID overwrites everyone.

## Your sandbox folder

You **should** make a folder to chop boards in:

1. **Dashboards** → **New** → **New folder**.
2. Name: `Network Observability — ` plus your name (example `Network Observability — Jane Doe`).
3. Create.

Leave the shared **Network Observability** folder alone as the clean copy. After Lab 1 you will **Save as** / copy dashboards into your folder (Grafana assigns new UIDs). Hunt in Lab 3 still works on your copy — same PromQL, same fleet.

Next: [Lab 1 — Explore the fleet](01-explore.md) →
