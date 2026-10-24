#!/usr/bin/env python3
"""Debug: find §12 Rev. 522 entry."""

path = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"
with open(path) as f:
    lines = f.read().split("\n")

print(f"Total lines: {len(lines)}")

# Show lines 550-556
for i in range(549, min(len(lines), 556)):
    line = lines[i]
    print(f"Line {i+1}: '{line[:50]}' ({len(line)} chars)")
