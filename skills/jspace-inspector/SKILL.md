---
name: jspace-inspector
description: Inspect J-space slots, run 5 canonical tests live
triggers:
- inspect
- jspace
- france china
- spider ant
- soccer rugby
- safety
j_space_target: Planner
half_life: 150
broadcast_target: 0.22
reportability_target: 0.065
dependencies:
- numpy
connectors:
- git-repo
- google
- notion
- web-search
provider: openai
version: 2.1.0
precedes:
- eval-harness-runner
requires:
- memory-router
- safety-scanner
- openwiki-sync
complementary:
- family-brain-wiki
---

# JSpace Inspector
Inspect S1 Fast hl8, S2 Slow hl300, Critic hl30, Planner hl150

- Runs ava-open-harness jspace_all
- Dumps top_concepts mass, broadcast 20% check
- Early warning offset for Critic

Maps:
- S2 -> openwiki personal wiki recall
- Planner -> France->China generalization


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
