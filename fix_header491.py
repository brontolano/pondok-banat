#!/usr/bin/env python3
# -*- coding: utf-8 -*-
PATH = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"
with open(PATH, encoding="utf-8") as f:
    src = f.read()

old = "header Rev. 489, §11 kompakt changelog 116–488, §12 updated; HEAD 8ee6d40"
new = "header Rev. 491, §11 kompakt changelog 116–490, §12 updated; HEAD 8ee6d40"

cnt = src.count(old)
print("occurrences:", cnt)
assert cnt == 1, cnt
src = src.replace(old, new)

with open(PATH, "w", encoding="utf-8") as f:
    f.write(src)
print("done")
