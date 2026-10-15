#!/usr/bin/env python3
"""Protect existing public URLs on the published site (Google has indexed them).
The site's importer builds a pattern URL (/<slug>/) from a file's name, and goal and category pages from folder
names. This check fails if a file behind an existing URL was moved, renamed, or deleted, or if a new file would
claim an existing slug. HMI pages are exempt (they may change).
Baseline: public-urls.tsv (frozen from the site on 2026-10-15). Run:
  python3 -I agents/by-capability/human-machine-interface/roadmap/tools/check_public_urls.py   (exit 1 on any problem)"""
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
AGENTS = os.path.abspath(os.path.join(HERE, *[".."] * 4))
def slugify(t):
    s = re.sub(r"[^\w\s-]", "", t.lower()); return re.sub(r"[-\s]+", "-", s).strip("-")
base = {"pattern": {}, "goal": set(), "category": set()}
for line in open(os.path.join(HERE, "public-urls.tsv"), encoding="utf-8"):
    if line.startswith("#") or not line.strip(): continue
    kind, slug, src = (line.rstrip("\n").split("\t") + ["", ""])[:3]
    if kind == "pattern": base["pattern"][slug] = src
    else: base[kind].add(slug)
problems = []
for slug, src in base["pattern"].items():
    if not os.path.exists(os.path.join(AGENTS, src)):
        problems.append(f"/{slug}/ would change or disappear: source file is gone: {src}")
known_src = set(base["pattern"].values())
known_slugs = set(base["pattern"])
for top in ("by-capability", "by-use-case", "cross-cutting"):
    for root, _, files in os.walk(os.path.join(AGENTS, top)):
        if "failures" not in root.split(os.sep): continue
        for f in files:
            if not f.endswith(".md") or f.lower() == "readme.md": continue
            rel = os.path.relpath(os.path.join(root, f), AGENTS).replace(os.sep, "/")
            if "human-machine-interface" in rel or rel in known_src: continue
            s = slugify(f[:-3])
            if s in known_slugs:
                problems.append(f"new file {rel} would claim the existing URL /{s}/")
for g in base["goal"]:
    if not any(os.path.isdir(os.path.join(AGENTS, t, c, "goals", g)) for t in ("by-capability", "by-use-case", "cross-cutting") for c in os.listdir(os.path.join(AGENTS, t)) if os.path.isdir(os.path.join(AGENTS, t, c))):
        problems.append(f"/goals/{g}/ has no source folder any more")
for c in base["category"]:
    if not any(os.path.isdir(os.path.join(AGENTS, t, c)) for t in ("by-capability", "by-use-case", "cross-cutting")):
        problems.append(f"/categories/{c}/ has no source folder any more")
for p in problems: print("PROBLEM", p)
print(f"public URLs checked: {len(base['pattern'])} patterns, {len(base['goal'])} goals, {len(base['category'])} categories; problems: {len(problems)}")
sys.exit(1 if problems else 0)
