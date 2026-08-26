# Labs

Keep the webinar and Grafana Cloud in two windows. Use **chat** if you get stuck.

Your sandbox starts empty. **Log in**, add two data sources from chat (Prometheus for metrics, Loki for logs), create synthetics, then import dashboards. After that you explore a healthy fleet. The facilitator will inject a failure for you to hunt.

Synthetic checks you create stay on **your** stack.

The facilitator will paste datasource credentials, the synthetic target IP, and when to start each lab.

1. [Login](00-login.md)
2. [Add shared data sources](01-datasources.md) (when chat has the credentials)
3. [Synthetics](02-synthetics.md)
4. [Import dashboards](03-import-dashboards.md)
5. [Explore](04-explore.md)
6. [Troubleshoot](05-troubleshoot.md) (wait for chat — something will change)
7. [Infinity + Assistant](06-infinity-assistant.md)

Optional stretch: [a second vantage](stretch-second-vantage.md) (Singapore public probe). Skip unless chat says to.

Dashboard JSON: [dashboards/](dashboards/). Mock API paths (Lab 6): [api-paths.md](api-paths.md).
