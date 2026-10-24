#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Check exact content of line 773."""
import io

path = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"
with io.open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()

line = lines[772]
print("Line 773 (repr):")
print(repr(line[:300]))
print("---")
print("test '0 commit' in line:", "0 commit" in line)
idx = line.find("0 commit")
if idx != -1:
    print("Context:", repr(line[idx-20:idx+80]))
