#!/usr/bin/env python3
"""Rebuild the chat agent spec builder from the failure library and content.py.
Run:  python3 -I agents/by-capability/human-machine-interface/chat-use-cases/builder/build.py
Writes data.json and index.html (a standalone page). failures.json is an intermediate file."""
import json, pathlib, runpy, sys
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
runpy.run_path(str(HERE / "data_gen.py"))
import content as C
F = json.load(open(HERE / "failures.json"))
for gid, g in C.GOALS.items():
    assert all(f in F for f in g["failures"]) and all(r in C.RULES for r in g["rules"]), gid
for rid, r in C.RULES.items():
    assert all(f in F for f in r["prevents"]) and r["metric"] and r["counter"] and r["how"], rid
for kind in ("goals", "rules"):
    for vid, segs in C.VARIANTS[kind].items():
        base = (C.GOALS if kind == "goals" else C.RULES)[vid]
        for seg, f in segs.items():
            merged = {**base, **f}
            for k in ("metric", "counter") + (("how",) if kind == "rules" else ("measure",)):
                assert merged.get(k), (kind, vid, seg, k)
for u in C.USECASES:
    assert all(g in C.GOALS for g in u["goals"]), u["id"]
data = dict(goals=C.GOALS, rules=C.RULES, usecases=C.USECASES, failures=F, variants=C.VARIANTS,
            linkBase="https://github.com/sarkars/agent-failure-modes/blob/main/agents/")
(HERE / "data.json").write_text(json.dumps(data))
page = (HERE / "page.tpl").read_text().replace("__DATA__", json.dumps(data).replace("</", "<\\/"))
(HERE / "index.html").write_text('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head><body>' + page + "</body></html>")
(HERE / "failures.json").unlink(missing_ok=True)
print("built", len(C.GOALS), "goals,", len(C.RULES), "rules,", len(C.USECASES), "use cases")
