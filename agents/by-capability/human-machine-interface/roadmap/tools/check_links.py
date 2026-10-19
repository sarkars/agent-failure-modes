#!/usr/bin/env python3
"""Check internal links, heading anchors, row structure, and ID uniqueness in the HMI area.
Run:  python3 -I agents/by-capability/human-machine-interface/roadmap/tools/check_links.py   (exit code 1 on any problem)"""
import re, glob, os, sys
AREA = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.chdir(AREA)
SKIP_TABLE = {"README.md", "index.md", "execution-plan.md", "content-program.md", "merge-proposals.md", "gap-analysis.md", "learning-agent.md"}
def slug(h): return re.sub(r"[^a-z0-9 -]", "", h.lower()).strip().replace(" ", "-")
bad = tot = 0
for f in sorted(glob.glob("**/*.md", recursive=True)):
    if f.startswith("_templates"):
        continue
    t = open(f).read()
    for m in re.finditer(r"\]\((?!http)([^)\s]+)\)", t):
        l = m.group(1)
        if f.startswith("incidents/") and l.startswith("/"):
            continue  # incident drafts use the site's own routes (/pattern-slug/)
        tot += 1
        p, _, a = l.partition("#")
        tp = os.path.normpath(os.path.join(os.path.dirname(f), p)) if p else f
        ok = os.path.exists(tp)
        if ok and a and tp.endswith(".md"):
            ok = a in {slug(h) for h in re.findall(r"^#+\s+(.*)$", open(tp).read(), re.M)}
        if not ok:
            bad += 1; print("BROKEN LINK", f, "->", l[:120])
ids = []
for f in sorted(glob.glob("roadmap/*.md")):
    if os.path.basename(f) in SKIP_TABLE:
        continue
    for l in open(f).read().split("\n"):
        if re.match(r"^\| [A-Z]{2}-[A-Z]?\d+ \|", l):
            c = [x.strip() for x in l.strip().strip("|").split("|")]
            ids.append(c[0])
            if len(c) != 9:
                bad += 1; print("BAD ROW COLUMNS", f, c[0], len(c))
dups = {i for i in ids if ids.count(i) > 1}
if dups:
    bad += len(dups); print("DUPLICATE IDS", sorted(dups))
print(f"links checked: {tot}; catalog rows: {len(ids)}; problems: {bad}")
sys.exit(1 if bad else 0)
