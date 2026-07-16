import os
import re

root = "agents"
mit_re = re.compile(r"## Mitigation Strategies\n(.*?)(?=\n## |\Z)", re.S)
placeholder_re = re.compile(r"\[Add|\[TODO|\[TBD|\[insert", re.I)

missing = []
placeholder = []
bold_only = []

for dirpath, dirnames, filenames in os.walk(root):
    if not dirpath.endswith(os.sep + "failures") and not dirpath.endswith("failures"):
        continue
    for fn in filenames:
        if not fn.endswith(".md"):
            continue
        path = os.path.join(dirpath, fn)
        with open(path, encoding="utf-8") as f:
            content = f.read()
        m = mit_re.search(content)
        if not m:
            if "**Mitigation Strategies**" in content:
                bold_only.append(path)
            else:
                missing.append(path)
        else:
            body = m.group(1)
            if placeholder_re.search(body) or len(body.strip()) < 50:
                placeholder.append(path)

print("MISSING ## Mitigation Strategies heading entirely (no bold fallback either):", len(missing))
for p in missing:
    print("  ", p)

print()
print("OLD BOLD-PAIR FORMAT (no ## heading):", len(bold_only))
for p in bold_only:
    print("  ", p)

print()
print("PLACEHOLDER/EMPTY body under ## heading:", len(placeholder))
for p in placeholder:
    print("  ", p)

print()
print("TOTAL GAPS:", len(missing) + len(bold_only) + len(placeholder))
