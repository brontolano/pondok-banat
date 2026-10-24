#!/usr/bin/env python3
# Fix: Rev. 489 entry should be AFTER Rev. 488 (table sorted ascending)
path = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"
with open(path, "r", encoding="utf-8") as f:
    c = f.read()

# Find the Rev. 489 entry line (our new entry) and the Rev. 488 entry line
# We'll swap them so Rev. 488 comes before Rev. 489 in the §12 table
import re

# Strategy: split into lines, find the two lines, and reorder them
lines = c.split("\n")

rev489_idx = None
rev488_idx = None
for i, line in enumerate(lines):
    if "Rev. 489 (final): PRD fresh verification & stability confirmation" in line and "24 Oktober 2026 (WIB)" in line:
        rev489_idx = i
    if "Rev. 488 (final): PRD fresh verification & stability confirmation" in line and "24 Oktober 2026 (WIB)" in line:
        rev488_idx = i

print("Rev.489 idx:", rev489_idx, "Rev.488 idx:", rev488_idx)

if rev489_idx is not None and rev488_idx is not None:
    # Swap: ensure Rev. 488 comes before Rev. 489
    # Currently: line[rev489_idx] = Rev.489, line[rev488_idx] = Rev.488
    # We want: Rev.488 at the lower index, Rev.489 at the higher index
    if rev489_idx < rev488_idx:
        # swap
        lines[rev489_idx], lines[rev488_idx] = lines[rev488_idx], lines[rev489_idx]
        print("Swapped (Rev.488 now before Rev.489)")

c = "\n".join(lines)
with open(path, "w", encoding="utf-8") as f:
    f.write(c)
print("WRITTEN")
