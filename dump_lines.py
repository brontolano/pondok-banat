# -*- coding: utf-8 -*-
import io
PATH = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"
with io.open(PATH, "r", encoding="utf-8") as f:
    lines = f.read().split("\n")
for i in range(420, 440):
    if i <= 0 or i > len(lines):
        continue
    print("%d|%r" % (i, lines[i-1]))
