"""
loader.py — dynamic skill loader, J-Space routed, half-life aware.

Solo personal project, no connection to employer, built with public/free-tier only
"""
from __future__ import annotations
from typing import Dict, Any, List
import os, pathlib, re, sys, json, math, importlib.util

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)

def _parse_frontmatter(text: str) -> tuple[Dict[str,Any], str]:
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}, text
    fm_raw = m.group(1)
    body = text[m.end():]
    try:
        import yaml
        fm = yaml.safe_load(fm_raw) or {}
    except Exception:
        fm = {}
        for line in fm_raw.splitlines():
            if ":" in line:
                k,v = line.split(":",1)
                fm[k.strip()] = v.strip().strip('"').strip("'")
    return fm, body

class Skill:
    def __init__(self, name: str, path: pathlib.Path, meta: Dict[str,Any], body: str):
        self.name = name
        self.path = path
        self.meta = meta
        self.body = body
        self.j_target = meta.get("j_space_target", "Router")
        self.hl = int(meta.get("half_life", meta.get("half-life", 80)))
        self.triggers = meta.get("triggers", [])
        self.deps = meta.get("dependencies", [])
        self._module = None

    def load_module(self):
        skill_py = self.path / "skill.py"
        if not skill_py.exists():
            return None
        spec = importlib.util.spec_from_file_location(f"skills.{self.name}.skill", skill_py)
        if spec and spec.loader:
            mod = importlib.util.module_from_spec(spec)
            sys.modules[spec.name] = mod
            spec.loader.exec_module(mod)  # type: ignore
            self._module = mod
            return mod
        return None

    def run(self, **kwargs) -> Dict[str,Any]:
        mod = self._module or self.load_module()
        if mod is None:
            return {"skill": self.name, "error": "no skill.py"}
        if hasattr(mod, "Skill"):
            inst = mod.Skill()
            if hasattr(inst, "run"):
                return inst.run(**kwargs)
        if hasattr(mod, "run"):
            return mod.run(**kwargs)
        return {"skill": self.name, "error": "no run()"}

    def decay(self, steps: int) -> float:
        return math.exp(-steps / max(1, self.hl))

class SkillLoader:
    def __init__(self, skills_dir: str | pathlib.Path | None = None):
        if skills_dir is None:
            here = pathlib.Path(__file__).parent
            skills_dir = here
        self.skills_dir = pathlib.Path(skills_dir)
        self.skills: Dict[str, Skill] = {}
        self.scan()

    def scan(self):
        self.skills.clear()
        if not self.skills_dir.exists():
            return
        for sub in self.skills_dir.iterdir():
            if not sub.is_dir():
                continue
            if sub.name == "__pycache__":
                continue
            md = sub / "SKILL.md"
            if not md.exists():
                continue
            text = md.read_text(encoding="utf-8", errors="ignore")
            meta, body = _parse_frontmatter(text)
            name = meta.get("name", sub.name)
            self.skills[name] = Skill(name=name, path=sub, meta=meta, body=body)

    def list(self) -> List[Dict[str,Any]]:
        return [{"name": s.name, "target": s.j_target, "hl": s.hl, "triggers": s.triggers, "desc": s.meta.get("description","")} for s in self.skills.values()]

    def load_all(self):
        for s in self.skills.values():
            s.load_module()

    def run(self, name: str, **kwargs) -> Dict[str,Any]:
        if name not in self.skills:
            raise KeyError(f"skill {name!r} not found, available {list(self.skills.keys())}")
        return self.skills[name].run(**kwargs)

def main():
    import argparse
    ap = argparse.ArgumentParser(description="ava-skills loader")
    ap.add_argument("cmd", nargs="?", default="list", help="list|run|test")
    ap.add_argument("skill", nargs="?", help="skill name")
    ap.add_argument("--mode", default="mock")
    ap.add_argument("--wiki-path", default=None)
    ap.add_argument("--ckpt", default=None)
    args = ap.parse_args()

    loader = SkillLoader()
    if args.cmd == "list":
        print(json.dumps(loader.list(), indent=2))
    elif args.cmd == "run":
        if not args.skill:
            print("Need skill name")
            sys.exit(1)
        res = loader.run(args.skill, mode=args.mode, wiki_path=args.wiki_path, ckpt=args.ckpt)
        print(json.dumps(res, indent=2))
    elif args.cmd == "test":
        loader.load_all()
        for name, skill in loader.skills.items():
            if args.skill and args.skill!=name:
                continue
            try:
                res = skill.run(mode="mock")
                print(f"{name}: PASS {str(res)[:200]}")
            except Exception as e:
                print(f"{name}: FAIL {e}")
    else:
        print("unknown cmd")

if __name__ == "__main__":
    main()
