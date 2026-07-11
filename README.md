# ava-skills

> **Solo personal project, no connection to employer, built with public/free-tier only**

Skill system for Ava AGI Factory v6.4 — dynamic loading, J-Space routed (S1 Fast hl=8, S2 Slow hl=300, Critic hl=30, Planner hl=150, Router), half-life aware, openwiki-synced.

Inspired by `cursor-agent-skills` (42 skills) but purpose-built for Ava's Global Workspace architecture. Each skill is a markdown contract `SKILL.md` + typed Python module `skill.py` + tests.

## Quickstart

```bash
pip install -e .
python -m skills.loader --list
python -m skills.loader --load openwiki-sync --target S2
python skills/openwiki-sync/skill.py --wiki-path ~/.openwiki/wiki
```

## Skill Format

Frontmatter in SKILL.md:

```yaml
---
name: openwiki-sync
description: Sync openwiki personal wiki into S2 Slow slots
triggers: ["wiki", "openwiki", "personal brain"]
j_space_target: S2
half_life: 300
dependencies: []
version: 0.1.0
---
```

## 8 Starter Skills

| Skill | J-Target | hl | Purpose |
|---|---|---|---|
| jspace-inspector | Router | 50 | Inspect S1/S2/Critic/Planner slots, top_concepts, broadcast 20% |
| openwiki-sync | S2 | 300 | Sync ~/.openwiki/wiki into S2 verbalizable concepts |
| logic-prover | S2 | 300 | Synthetic logic textbook generation (Phase0 Phi Method B) |
| code-bench | Planner | 150 | Exec-verified Python generation |
| safety-scanner | Critic | 30 | Blackmail/leverage detection, AUC 0.91→0.94 early 4-5 tok |
| memory-router | Router | 80 | Route S1/S2/Planner with KL w0.4 + inter-MI cos 0.45 |
| eval-harness-runner | Router | 80 | Run ava-open-harness evals |
| family-brain-wiki | S2 | 300 | Bridge to family-brain-os WikiTab |

## Architecture

- `skills/loader.py` — scans SKILL.md, parses frontmatter, loads skill.py Skill class with run(**kwargs)->dict, routes by j_space_target, respects half-life exp(-steps/hl), topo sort deps.
- `docs/SKILL_SPEC.md` — authoring guide

## Integration

```python
from skills.loader import SkillLoader
loader = SkillLoader(skills_dir="path/to/ava-skills/skills")
loader.load_all()
result = loader.run("openwiki-sync", wiki_path="~/.openwiki/wiki")
```

Family Brain: skill reads/writes encrypted wiki pages same format as WikiTab.

## Free-tier only

Public pip only, torch lazy, MIT. Solo personal project, no connection to employer, built with public/free-tier only.
