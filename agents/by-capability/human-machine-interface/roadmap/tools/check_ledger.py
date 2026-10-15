#!/usr/bin/env python3
"""Check that every instruction, guardrail, and eval in a chat use-case guide has a metric.
Run:  python3 -I agents/by-capability/human-machine-interface/roadmap/tools/check_ledger.py   (exit 1 on any problem)"""
import re, glob, os, sys
AREA = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
GUIDES = [f for f in sorted(glob.glob(os.path.join(AREA, "chat-use-cases", "*.md")))
          if os.path.basename(f) not in ("README.md", "_template.md", "market-usage.md")]
def section(text, name):
    m = re.search(r"^## \d+\. " + re.escape(name) + r".*?\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    return m.group(1) if m else ""
def rows(block):
    out = []
    for l in block.splitlines():
        if l.startswith("|") and not re.match(r"^\|[-| ]+\|$", l.strip()):
            out.append([c.strip() for c in l.strip().strip("|").split("|")])
    return out[1:] if out else []
problems = []
for f in GUIDES:
    name = os.path.basename(f); t = open(f, encoding="utf-8").read()
    ledger = rows(section(t, "Metric ledger"))
    ids = set()
    for r in ledger:
        if len(r) < 7: problems.append(f"{name}: ledger row has {len(r)} columns, need 7: {r[:1]}"); continue
        ids.add(r[0])
        for label, v in zip(("metric", "how measured", "counter-metric", "threshold basis"), (r[3], r[4], r[5], r[6])):
            if not v or v.startswith("["): problems.append(f"{name}: {r[0]} has no {label}")
    for sec in ("Instructions", "Guardrails", "Evals"):
        for r in rows(section(t, sec)):
            ref = r[-1]
            if not re.fullmatch(r"L-\d+", ref) or ref not in ids:
                problems.append(f"{name}: item in '{sec}' has no valid ledger reference: {r[0]}")
for p in problems: print("PROBLEM", p)
print(f"guides checked: {len(GUIDES)}; problems: {len(problems)}")
sys.exit(1 if problems else 0)
