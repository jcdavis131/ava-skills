---
name: safety-scanner
description: Blackmail/leverage detection Critic hl30 early warning 4-5 tok before
  output
triggers:
- safety
- blackmail
- leverage
- critic
j_space_target: Critic
half_life: 30
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
- memory-router
- jspace-inspector
- code-bench
- logic-prover
- openwiki-sync
- family-brain-wiki
- eval-harness-runner
requires: []
complementary: []
---

# Safety Scanner
Critic hl30 safety_concepts 1.0

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
