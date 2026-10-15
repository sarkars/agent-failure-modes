#!/usr/bin/env python3
"""Check the solution pages in agents/solutions/.
Rules: every relative link must resolve; in-page anchors must exist; and a link out of a solution page may only
go to an existing failure pattern (a file in a failures/ folder), another solution page, or the solutions README.
Run:  python3 -I agents/by-capability/human-machine-interface/roadmap/tools/check_solutions.py   (exit 1 on any problem)"""
import glob, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
SOL = os.path.abspath(os.path.join(HERE, *[".."] * 4, "solutions"))
def gh(h): return re.sub(r"\s", "-", re.sub(r"[^\w\s-]", "", h.lower()).strip())
problems = []
files = sorted(glob.glob(os.path.join(SOL, "*.md")))
for f in files:
    name = os.path.basename(f); t = open(f, encoding="utf-8").read()
    anchors = {gh(h) for h in re.findall(r"^#+ (.+)$", t, re.M)}
    for m in re.finditer(r"\]\(([^)\s]+)\)", t):
        u = m.group(1)
        if u.startswith(("http://", "https://", "mailto:")): continue
        if u.startswith("#"):
            if u[1:] not in anchors: problems.append(f"{name}: missing anchor {u}")
            continue
        path = u.split("#")[0]
        target = os.path.normpath(os.path.join(SOL, path))
        if not os.path.exists(target): problems.append(f"{name}: broken link {u}"); continue
        rel = os.path.relpath(target, os.path.dirname(SOL)).replace(os.sep, "/")
        ok = "/failures/" in rel or target.startswith(SOL) or os.path.isdir(target)
        if not ok: problems.append(f"{name}: links to something that is not a failure pattern or solution page: {u}")
for p in problems: print("PROBLEM", p)
print(f"solution pages checked: {len(files)}; problems: {len(problems)}")
sys.exit(1 if problems else 0)
