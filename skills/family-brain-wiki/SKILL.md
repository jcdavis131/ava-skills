---
name: family-brain-wiki
description: Bridge to Family Brain OS WikiTab export wikiPages -> S2
triggers: ['family', 'wiki', 'family-brain', 'davis']
j_space_target: S2
half_life: 300
broadcast_target: 0.22
reportability_target: 0.065
dependencies: ["numpy"]
connectors: ["git-repo", "google", "notion", "web-search"]
provider: openai
---

# Family Brain Wiki Bridge
Reads localStorage family-brain-wiki-pages:v1

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
