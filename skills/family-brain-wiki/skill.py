# Solo personal project, no connection to employer, built with public/free-tier only
"""family-brain-wiki: Bridge to Family Brain OS WikiTab export wikiPages -> S2"""
from __future__ import annotations
from typing import Any, Dict, List
import os, pathlib, json, re, datetime

def describe():
    return {"name":"family-brain-wiki","description":"Bridge to Family Brain OS WikiTab export wikiPages -> S2","j_space_target":"S2","half_life":300,"triggers":["family","wiki","family-brain","davis"]}

def _scan_family_wiki() -> List[Dict[str,Any]]:
    # scan for family-brain-os storage key in local files or wiki folder
    candidates=[]
    # check src/components/WikiTab.tsx exists?
    fb_root = pathlib.Path.home() / "workspace" / "family-brain-os"
    if (fb_root / "src" / "components" / "WikiTab.tsx").exists():
        candidates.append({"source":"WikiTab.tsx","exists":True})
    # check localStorage export json?
    for name in ["your_files","family-brain-os"]:
        p = pathlib.Path.home() / "workspace" / name
        if p.exists():
            candidates.extend([{"source": str(f), "type":"md"} for f in p.rglob("*wiki*.md")][:5])
    return candidates

def _gen_pages_from_state(state: Dict[str,Any] | None) -> List[Dict[str,str]]:
    # mock generation from family brain state
    pages=[]
    if not state:
        pages=[
            {"title":"Family Policies","body":"# Policies\n- Roth $7000\n- Emergency 6mo\n- Vacation fund"},
            {"title":"Bills","body":"# Bills\n- Due dates calendar\n- Auto-pay status"},
        ]
    else:
        # state has accounts etc
        pages.append({"title":"Finances","body":f"# Finances\nAccounts: {len(state.get('accounts',[]))}\nEF: {state.get('burn',0)*6}"})
    return pages

def run(model: Any = None, tokenizer: Any = None, mode: str = "mock", **kw):
    import random
    if mode != "mock":
        # Simulated mass must never be labeled real (previous code passed mode through,
        # so mode="real" returned a random number presented as a live measurement).
        return {"skill":"family-brain-wiki","mode":"real","measured":None,"pass":False,
                "bar":"mass>=0.06",
                "error":"real mode not implemented: S2 injection mass needs a live model readout"}
    random.seed(kw.get("seed",7))
    wiki_info = _scan_family_wiki()
    pages = _gen_pages_from_state(kw.get("state"))
    # simulate S2 injection mass (mock only)
    mass = 0.06 + random.uniform(0,0.08) + 1e-5*len(pages)
    measured={"n_wiki_sources": len(wiki_info), "n_pages_generated": len(pages), "reportability_mass": mass, "pages": [p["title"] for p in pages], "sources": wiki_info[:3], "storage_key":"family-brain-wiki-pages:v1"}
    return {"skill":"family-brain-wiki","mode":"mock","measured":measured,"pass": mass>=0.06,"bar":"mass>=0.06","wiki_pages": pages}
