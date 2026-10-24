#!/usr/bin/env python3
# -*- coding: utf-8 -*-
with open("/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md", encoding="utf-8") as f:
    lines = f.read().splitlines()
l = lines[475]  # line 476
print("line 476 len:", len(l))
# Find the hash between backticks after "HEAD "
import re
m = re.search(r'`(7[0-9a-f]{20})`', l)
if m:
    print("hash found:", m.group(1), "len:", len(m.group(1)))
    print("full context:", repr(l[m.start()-10:m.end()+10]))
# Also print line 4 hash
l4 = lines[3]
m4 = re.search(r'`(7[0-9a-f]{20})`', l4)
if m4:
    print("line 4 hash:", m4.group(1))
# git HEAD~1
import subprocess
out = subprocess.run(["git", "rev-parse", "HEAD~1"], capture_output=True, text=True, cwd="/opt/data/home/workspace/dev/pondok-banat")
print("git HEAD~1:", out.stdout.strip())
