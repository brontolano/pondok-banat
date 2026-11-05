#!/usr/bin/env python3
with open("/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md", "r", encoding="utf-8") as f:
    lines = f.read().split("\n")
print(repr(lines[4203]))
print()
print("Line 4204 content:")
print(lines[4203])
