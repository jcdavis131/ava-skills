---
name: memory-router
description: Route between S1/S2/Planner bias control
triggers: ['router', 'arbitration', 'bias', 'memory']
j_space_target: Router
half_life: 30
broadcast_target: 0.22
reportability_target: 0.065
dependencies: ["numpy"]
connectors: ["git-repo", "google", "notion", "web-search"]
provider: openai
---

# Memory Router
Bias [0.25,0.45,0.05,0.25] etc

## Install

```bash
openwiki code --init # for repo docs in openwiki/ 
openwiki personal --init # for personal brain ~/.openwiki/wiki from git, gmail, notion etc
openwiki auth gmail # saves to ~/.openwiki/.env, then ingest directly with no MCP
openwiki ingest all # reads ~/.openwiki/connectors/<connector>/raw/ then synthesizes wiki
```

CI keeps docs fresh: copy openwiki-update.yml into .github/workflows/openwiki-update.yml and use openwiki code --update --print in CI without init.

Secrets are referenced by env var name and stored in ~/.openwiki/.env; config files never contain raw secret values.

Solo personal project, no connection to employer, built with public/free-tier only.
