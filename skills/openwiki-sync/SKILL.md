---
name: openwiki-sync
description: Sync OpenWiki personal wiki (~/.openwiki/wiki) into S2 Slow hl300 verbalizable
  memory
triggers:
- openwiki
- wiki
- personal brain
- sync wiki
- ~/.openwiki
j_space_target: S2
half_life: 300
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
- family-brain-wiki
- jspace-inspector
requires:
- memory-router
- safety-scanner
complementary:
- family-brain-wiki
---

# OpenWiki Sync
Bridges langchain-ai/openwiki personal brain into Ava S2.

- Reads ~/.openwiki/wiki markdown
- Embeds into S2 Slow slots via reportability loss CE(verbalizer(ws.mean), target_concept)
- Uses connectors: git-repo reads compact manifests, google uses Gmail API OAuth, notion via hosted MCP, x via OAuth user-context, web-search via Tavily, hackernews no creds
- Secrets stored in ~/.openwiki/.env, referenced by env var name, never raw in config
- Auth: openwiki auth gmail -> saves tokens, creates config, then ingest directly


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
