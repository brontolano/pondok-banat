#!/usr/bin/env python3
"""Debug: print exact line 260 and 300 from PRD."""

path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'

with open(path, 'r') as f:
    lines = f.readlines()

print("=== Line 260 (index 259) ===")
print(repr(lines[259][:200]))
print()
print("=== Line 300 (index 299) ===")
print(repr(lines[299][:300]))
print()
print("=== Line 300 (index 299) - full ===")
print(lines[299])
