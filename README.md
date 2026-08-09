# ava-skills

> **Solo personal project, no connection to employer, built with public/free-tier only**

Skill system for the [Ava Factory v6.4](https://github.com/jcdavis131/ava-agi-factory-v6-4) research project. Skills are dynamically loaded and routed to the model's J-Space slot banks (S1 fast, S2 slow, critic, planner), each with a configured half-life. Each skill is a markdown contract (`SKILL.md`) plus a typed Python module (`skill.py`) plus tests.

Status: experimental; developed alongside the Ava Factory pilots.

## Quickstart

```bash
pip install -e .

python -m skills.loader list                # all skills in topological order, with metadata
python -m skills.loader graph               # Tool Graph (precedes/requires/complementary) + topo order
python -m skills.loader rerank "inspect jspace safety"   # wRRF-ranked skills for a query
python -m skills.loader run openwiki-sync --mode mock --wiki-path ~/.openwiki/wiki
python -m skills.loader run-graph --query "safety check then inspect jspace"
python -m skills.loader test                # smoke-run every skill in mock mode
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

## Starter skills (9)

Values below mirror each skill's `SKILL.md` frontmatter — the single source of truth
(`describe()` reads the manifest at runtime, so code and docs cannot drift).

| Skill | J-Target | hl | Purpose |
|---|---|---|---|
| jspace-inspector | Planner | 150 | Inspect S1/S2/Critic/Planner slots; real mode runs the 5 canonical J-tests via ava-open-harness |
| openwiki-sync | S2 | 300 | Sync ~/.openwiki/wiki into S2 verbalizable concepts |
| logic-prover | S2 | 300 | Synthetic logic corpus generation (truth tables + syllogisms, JSONL) |
| code-bench | S2 | 350 | Exec-verified Python generation |
| safety-scanner | Critic | 30 | Blackmail/leverage detection; AUC/AUPRC/FPR computed from each run's scores |
| memory-router | Router | 30 | ShardMemo Tier A/B/C scoping + S1/S2/Planner routing with real KL vs branch bias |
| memory-mint | Router | 30 | Trace-capture -> shard-mint ingestion pipeline feeding memory-router |
| eval-harness-runner | Planner | 150 | Run ava-open-harness evals, gate on all requested evals passing |
| family-brain-wiki | S2 | 300 | Bridge family-brain-os WikiTab pages (localStorage JSON export) into S2 |

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

## Ecosystem

Status as of 2026-08-09.

This repository is vendored into [dottie](https://github.com/jcdavis131/dottie) at `packages/ava-skills`. Per dottie's `docs/CONSOLIDATION.md`, the standalone repos are vendored mirrors, not sources of truth: development consolidates in dottie, changes originate there and are pushed outward, never the reverse.

In dottie's CI (`.github/workflows/ci.yml`):

- Ruff lint on `packages/ava-skills` is a hard gate held at zero findings (ruff 0.15.22, pinned; hard since 2026-08-01).
- The test suite runs as a hard gate (`uv run pytest packages/ava-skills`), with 89 tests passing at the 2026-08-01 measurement recorded in that workflow.

Sync state, measured 2026-08-09 by `diff -rq` against dottie's `packages/ava-skills`: this mirror lags the dottie copy. 22 files differ, and 5 paths exist only in dottie (the `jspace-context-engine` skill, `skills/state_store.py`, `skills/telemetry_export.py`, and two test files); nothing here is absent from dottie. For current code, use dottie.

## Free-tier only

Public pip only, torch lazy, MIT. Solo personal project, no connection to employer, built with public/free-tier only.
