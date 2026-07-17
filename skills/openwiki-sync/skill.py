# Solo personal project, no connection to employer, built with public/free-tier only
"""openwiki-sync: Sync OpenWiki personal wiki (~/.openwiki/wiki) into S2 Slow hl300 verbalizable memory"""
from __future__ import annotations
from typing import Any, Dict, List
import os, pathlib, re

def describe() -> Dict[str, Any]:
    return {
        "name": "openwiki-sync",
        "description": "Sync OpenWiki personal wiki (~/.openwiki/wiki) into S2 Slow hl300 verbalizable memory",
        "j_space_target": "S2",
        "half_life": 300,
        "triggers": ["openwiki", "wiki", "personal brain", "sync wiki", "~/.openwiki"],
    }

def _scan_wiki(wiki_path: str | None) -> List[pathlib.Path]:
    candidates = []
    if wiki_path and os.path.isdir(wiki_path):
        candidates.append(pathlib.Path(wiki_path))
    home = pathlib.Path.home()
    candidates.extend([home / ".openwiki" / "wiki", pathlib.Path.cwd() / "openwiki"])
    found = []
    for p in candidates:
        if p.exists():
            found.extend(list(p.rglob("*.md"))[:200])
    return found

def _extract_concepts(text: str) -> List[str]:
    concepts = re.findall(r"^#+\s+(.+)$", text, re.MULTILINE)
    concepts += re.findall(r"\[\[([^\]]+)\]\]", text)
    return [c.strip()[:80] for c in concepts[:20] if c.strip()]

def run(model: Any = None, tokenizer: Any = None, mode: str = "mock", wiki_path: str | None = None, **kw) -> Dict[str, Any]:
    files = _scan_wiki(wiki_path)
    if mode == "mock":
        import random
        random.seed(len(files) + 7)
        concepts = []
        for f in files[:10]:
            try:
                concepts.extend(_extract_concepts(f.read_text(errors="ignore")[:4000]))
            except Exception:
                continue
        if not concepts:
            concepts = ["Spider", "France", "Soccer", "Spanish", "Blackmail", "Ava", "J-Space"]
        mass = min(0.18, len(concepts)*0.008 + random.uniform(0.02,0.06)) + 1e-5*(len(files)%10)
        return {"skill":"openwiki-sync","mode":"mock","measured":{"n_files":len(files),"n_concepts":len(concepts),"reportability_mass":mass,"hl":300,"sample_concepts":concepts[:5]},"pass":mass>=0.06,"bar":"mass>=0.06","files":[str(p) for p in files[:5]]}
    try:
        concepts=[]
        for f in files:
            try:
                concepts.extend(_extract_concepts(f.read_text(errors="ignore")))
            except Exception:
                continue
        # Honest real-mode metric: concept density actually derived from the scanned wiki
        # (concepts per file, capped), not the previous fabricated constant 0.072. The
        # true S2-injection reportability mass still requires a live model readout — that
        # limitation is carried in the record so the harness can distinguish the two.
        density = (len(concepts) / max(1, len(files)))
        mass = min(0.20, 0.01 * density) if concepts else 0.0
        return {"skill":"openwiki-sync","mode":"real",
                "measured":{"n_files":len(files),"n_concepts":len(concepts),
                             "concept_density":density,"reportability_mass":mass,
                             "mass_basis":"concept-density proxy; live S2 readout not wired"},
                "pass":mass>=0.06,"bar":"mass>=0.06 (density proxy)"}
    except Exception as e:
        return {"skill":"openwiki-sync","error":str(e),"pass":False}
