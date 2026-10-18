#!/usr/bin/env python3
"""Check that written HMI patterns can be imported by the published Astro site.
The site's importer (scripts/import_patterns.py in the site repo) expects:
  - the file at agents/by-capability/human-machine-interface/goals/<family>/failures/<name>.md
  - line 1 is the H1 (it drops the first line of the file)
  - a line '**Frequency**: Very Common|Common|Occasional|Rare'
  - a line '## Issue: <one sentence>'
  - a README.md in goals/<family>/ (used as the goal page)
Run:  python3 -I agents/by-capability/human-machine-interface/roadmap/tools/check_site_compat.py   (exit 1 on any problem)"""
import glob, os, re, sys
AREA = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
problems = []
files = sorted(glob.glob(os.path.join(AREA, "**", "failures", "*.md"), recursive=True))
for f in files:
    rel = os.path.relpath(f, AREA); parts = rel.split(os.sep)
    if not (len(parts) == 4 and parts[0] == "goals" and parts[2] == "failures"):
        problems.append(f"{rel}: not at goals/<family>/failures/<name>.md"); continue
    text = open(f, encoding="utf-8").read()
    if not text.startswith("# "):
        problems.append(f"{rel}: line 1 must be the H1 (the importer drops line 1)")
    if not re.search(r"^\*\*Frequency\*\*: (Very Common|Common|Occasional|Rare)\s*$", text, re.M):
        problems.append(f"{rel}: missing '**Frequency**: Very Common|Common|Occasional|Rare'")
    if not re.search(r"^## Issue: .{20,}", text, re.M):
        problems.append(f"{rel}: missing '## Issue: <one sentence>'")
    if "<!-- SEO" in text.split("\n", 1)[0]:
        problems.append(f"{rel}: SEO comment on line 1")
    if not os.path.exists(os.path.join(AREA, "goals", parts[1], "README.md")):
        problems.append(f"{rel}: goals/{parts[1]}/README.md is missing")
for p in problems: print("PROBLEM", p)
print(f"patterns checked: {len(files)}; problems: {len(problems)}")
sys.exit(1 if problems else 0)
