#!/usr/bin/env python3
"""Fix trailing pipes in M01/M04 table rows."""
base = "/opt/data/home/workspace/dev/pondok-banat"
prd = base + "/PRD-PONDOK-BANAT.md"
with open(prd, encoding="utf-8") as f:
    lines = f.read().split("\n")

fixed = 0
for i, l in enumerate(lines):
    if "| M01 |" in l and "Catatan statis" not in l:
        if l.endswith(" | |"):
            lines[i] = l.rstrip(" |") + "|"
            fixed += 1
    if "| M04 |" in l and "Catatan Prisma" not in l:
        if l.endswith(" | |"):
            lines[i] = l.rstrip(" |") + "|"
            fixed += 1

with open(prd, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print("Fixed rows:", fixed)
