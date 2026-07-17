# Solo personal project, no connection to employer, built with public/free-tier only
"""eval-harness-runner: Run ava-open-harness, gate stable checkpoint"""
from __future__ import annotations
from typing import Any, Dict
import os, sys, pathlib

def describe():
    return {"name":"eval-harness-runner","description":"Run ava-open-harness, gate stable checkpoint","j_space_target":"Router","half_life":80,"triggers":["harness","eval","gate"]}

def run(model: Any = None, tokenizer: Any = None, mode: str = "mock", **kw):
    # try to import harness
    try:
        # add ava-open-harness to path
        here = pathlib.Path(__file__).resolve().parents[2]
        harness_path = here.parent / "ava-open-harness"
        if harness_path.exists() and str(harness_path) not in sys.path:
            sys.path.insert(0, str(harness_path))
        from harness.runner import run_harness
        res = run_harness(eval_names=kw.get("eval","jspace_all,frontier_rubric"), mode=mode, ckpt=kw.get("ckpt"), preset=kw.get("preset","nano"), verbose=False)
        passed = res["meta"]["passed"]
        total = res["meta"]["total"]
        return {"skill":"eval-harness-runner","mode":mode,"measured":{"passed":passed,"total":total,"wall_s":res["meta"].get("wall_s",0),"results":res["evals"]},"pass": passed>=3,"bar":">=3 evals PASS"}
    except Exception as e:
        # Honest failure — NEVER fabricate a pass count. Previously this returned
        # random.randint(3,5) (always >=3 => guaranteed pass), which turned the
        # upstream anti-fabrication RuntimeError into a fake real-mode PASS: exactly
        # the antipattern the harness exists to prevent.
        return {"skill":"eval-harness-runner","mode":mode,"measured":None,"pass":False,
                "bar":">=3 evals PASS",
                "error":f"harness could not run in mode={mode}: {str(e)[:200]}"}
