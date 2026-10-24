# -*- coding: utf-8 -*-
import io
PATH = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"
with io.open(PATH, "r", encoding="utf-8") as f:
    lines = f.read().split("\n")
for i, l in enumerate(lines, 1):
    if "> - **Status:**" in l and "rev 486" in l:
        print(i, repr(l))
