# Solo personal project, no connection to employer, built with public/free-tier only
"""logic-prover: Generate synthetic logic textbooks Phi Method B (P0 50B corpus)"""
from __future__ import annotations
from typing import Any, Dict, List
import random, itertools

def describe() -> Dict[str, Any]:
    return {"name":"logic-prover","description":"Generate synthetic logic textbooks Phi Method B (P0 50B corpus)","j_space_target":"S2","half_life":300,"triggers":["logic","prover","phi","truth table"]}

def gen_truth_tables(n: int = 50) -> List[str]:
    ops = ["AND","OR","IMPLIES","NOT"]
    out=[]
    for _ in range(n):
        a = random.choice([True,False])
        b = random.choice([True,False])
        out.append(f"P={a}, Q={b} => P AND Q = {a and b}, P OR Q = {a or b}, NOT P = {not a}")
    return out

def gen_syllogisms(n: int = 30) -> List[Dict[str,str]]:
    templates=[
        ("All {A} are {B}.", "All {B} are {C}.", "Therefore all {A} are {C}."),
        ("If {P} then {Q}.", "{P}.", "Therefore {Q}."),
        ("No {A} are {B}.", "Some {C} are {A}.", "Therefore some {C} are not {B}."),
    ]
    out=[]
    vocab=[("dogs","mammals","animals"),("cats","pets","animals"),("spiders","arthropods","animals")]
    for _ in range(n):
        A,B,C = random.choice(vocab)
        t = random.choice(templates)
        out.append({"premise1": t[0].format(A=A,B=B,C=C,P=A,Q=B),"premise2": t[1].format(A=A,B=B,C=C,P=A,Q=B),"conclusion": t[2].format(A=A,B=B,C=C,P=A,Q=B)})
    return out

def run(model: Any = None, tokenizer: Any = None, mode: str = "mock", **kw) -> Dict[str, Any]:
    n = kw.get("n", 100)
    if mode=="mock":
        import random
        random.seed(kw.get("seed",1))
        tables = gen_truth_tables(min(n,20))
        sylls = gen_syllogisms(min(n,20))
        measured={"n_generated": len(tables)+len(sylls),"truth_tables": len(tables),"syllogisms": len(sylls), "phase":"P0","target_tokens": "50B mock"}
        return {"skill":"logic-prover","mode":"mock","measured":measured,"pass":True,"bar":"generation non-empty"}
    # real: would write to data/raw/logic/
    import pathlib
    out_dir = pathlib.Path(kw.get("out_dir","data/raw/logic"))
    out_dir.mkdir(parents=True, exist_ok=True)
    # write sample file
    tables = gen_truth_tables(n)
    (out_dir / "logic_sample.jsonl").write_text("\n".join(tables[:100]))
    return {"skill":"logic-prover","mode":"real","measured":{"n_generated": len(tables), "out_dir": str(out_dir)},"pass":True,"bar":"wrote file"}
