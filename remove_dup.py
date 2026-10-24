#!/usr/bin/env python3
"""Remove duplicate Rev. 523 line 450."""

path = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"
with open(path) as f:
    lines = f.read().split("\n")

# Find duplicate consecutive Rev. 523 lines (starting with "    ||- **Rev. 523 (final).**")
seen = []
removed = 0
for i, line in enumerate(lines):
    if line.startswith("    ||- **Rev. 523 (final).**") and line in seen:
        lines.pop(i)
        removed += 1
        print(f"Removed duplicate at line {i+1}")
    else:
        seen.append(line)

with open(path, "w") as f:
    f.write("\n".join(lines))

print(f"Total removed: {removed}")
