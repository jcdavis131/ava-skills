# Solo personal project, no connection to employer, built with public/free-tier only
"""memory-router: Route between S1/S2/Planner bias control"""
from __future__ import annotations
from typing import Any, Dict, List

def describe():
    return {"name":"memory-router","description":"Route between S1/S2/Planner bias control","j_space_target":"Router","half_life":30,"triggers":["router","arbitration","bias","memory"]}

BRANCH_BIASES = {
    "code": [0.25,0.45,0.05,0.25],
    "math": [0.10,0.65,0.20,0.05],
    "chat": [0.15,0.25,0.35,0.25],
    "base": [0.20,0.40,0.15,0.25],
}

def route_score(instruction: str) -> Dict[str,float]:
    # heuristic routing: look for keywords
    instr = instruction.lower()
    scores = {"S1":0.2,"S2":0.2,"Critic":0.1,"Planner":0.2,"Router":0.3}
    if any(k in instr for k in ["code","python","function"]):
        scores = {"S1":0.25,"S2":0.45,"Critic":0.05,"Planner":0.25,"Router":0.0}
    elif any(k in instr for k in ["math","prove","logic"]):
        scores = {"S1":0.10,"S2":0.65,"Critic":0.20,"Planner":0.05,"Router":0.0}
    elif any(k in instr for k in ["safety","blackmail","threat"]):
        scores = {"S1":0.05,"S2":0.20,"Critic":0.60,"Planner":0.15,"Router":0.0}
    elif any(k in instr for k in ["plan","temporal","deadline"]):
        scores = {"S1":0.15,"S2":0.25,"Critic":0.10,"Planner":0.50,"Router":0.0}
    return scores

def run(model: Any = None, tokenizer: Any = None, mode: str = "mock", instruction: str = "", branch: str = "base", **kw):
    bias = BRANCH_BIASES.get(branch, BRANCH_BIASES["base"])
    routed = route_score(instruction or kw.get("query",""))
    # compute KL vs bias target
    import math
    # routed as list order S1,S2,Critic,Planner
    routed_list = [routed["S1"], routed["S2"], routed["Critic"], routed["Planner"]]
    kl= sum(r*math.log((r+1e-9)/(b+1e-9)) for r,b in zip(routed_list,bias) if r>0)
    measured={"routed": routed, "bias": bias, "branch": branch, "kl": kl, "target_kl_w":0.4, "inter_mi_target":0.45}
    passed = kl < 1.0
    return {"skill":"memory-router","mode":mode,"measured":measured,"pass":passed,"bar":"kl<1.0"}
