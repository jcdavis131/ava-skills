# Skill Spec — How to author skills for Ava

> Solo personal project, no connection to employer, built with public/free-tier only

## Anatomy

- `skills/<skill-id>/SKILL.md` — frontmatter + markdown, required
- `skills/<skill-id>/skill.py` — python module with `run()` and `describe()`
- `skills/<skill-id>/tests/test_*.py` — optional

Frontmatter fields:

```yaml
name: openwiki-sync
description: Sync OpenWiki personal wiki into S2 Slow hl300
triggers: ["openwiki", "wiki", "personal brain", "sync wiki"]
j_space_target: S2
half_life: 300
broadcast_target: 0.22
reportability_target: 0.065
dependencies: ["torch"] # pip names, optional
connectors: ["git-repo", "google", "notion", "web-search", "hackernews"] # for openwiki personal mode
provider: openai # openai, anthropic, openai-compatible, openai-chatgpt, etc
```

## J-Space mapping

- S1 Fast 32 hl8 w0.6 broadcast 0.18 — automatic, sensory no RoPE
- S2 Slow 64 hl300 w0.8 broadcast 0.22 verbalizable 0.065 — deliberate, our main long-term memory for openwiki
- Critic 16 hl30 w1.0 safety_concepts 1.0 — safety scanner skill
- Planner 32 hl150 w0.7 — temporal, jspace inspector

Bias vector example from factory branching:
- Code branch bias [0.25,0.45,0.05,0.25] freeze [system1]
- Math branch bias [0.10,0.65,0.20,0.05]
- Chat branch bias [0.15,0.25,0.35,0.25]

Skills expose `suggested_bias` override.

## OpenWiki integration fields

- `connectors`: list of OpenWiki connectors this skill needs (same names as CLI: git-repo reads configured local repository paths and writes compact manifests, x uses X API directly with OAuth user-context, notion targets hosted Notion MCP server via OAuth, google uses Gmail API directly with OAuth, web-search uses Tavily requires key, hackernews public feed no creds)
- Connector secrets stored in `~/.openwiki/.env`, referenced by env var name, never raw in config
- Auth flow: `openwiki auth gmail` saves tokens into `.env`, creates connector config when possible, after that Gmail connector can ingest directly

## Writing a skill

1. Create folder `skills/my-skill/`
2. SKILL.md with frontmatter
3. skill.py:

```python
# skill.py
# Solo personal project, no connection to employer, built with public/free-tier only

def describe():
return {"name":"my-skill","targets":["S2"]}

def run(model=None, tokenizer=None, mode="mock", query=None, **kw):
# lazy imports
try:
import torch
except:
torch = None
if mode=="mock":
return {"pass":True,"measured":{"score":0.9},"wiki_pages_synced":2}
# real: model.forward with hooks
return {"pass":True}
```

## Testing

```bash
pytest skills/jspace-inspector/tests
python -m skills.loader run jspace-inspector --mode mock --verbose
```

## Harness gating

Every skill run should emit metrics compatible with `ava-open-harness/harness/runner.py`:
- `measured` dict with floats from live forward
- `pass` bool
- `bar` string threshold

Runner will check anti-mock: no hardcoded 0.82 etc.

## CI

Workflow `.github/workflows/openwiki-update.yml` runs `openwiki code --update --print` on schedule.

Also runs harness gate: if harness PASS, merge auto.

