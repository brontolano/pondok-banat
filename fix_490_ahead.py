#!/usr/bin/env python3
# -*- coding: utf-8 -*-
PATH = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"
with open(PATH, encoding="utf-8") as f:
    src = f.read()

# Align the Rev.490 compact entry's ahead-count with the verified current count (20).
old = "HEAD `94d19e3175718470e7214641aee6e0cb46f34177` (Rev. 490 commit), 19 / 0 (19 commits ahead origin_main). Fresh verification seluruh kondisi repository"
new = "HEAD `94d19e3175718470e7214641aee6e0cb46f34177` (Rev. 490 commit), 20 / 0 (20 commits ahead origin_main). Fresh verification seluruh kondisi repository"

cnt = src.count(old)
print("occurrences:", cnt)
assert cnt == 1, cnt
src = src.replace(old, new)

with open(PATH, "w", encoding="utf-8") as f:
    f.write(src)
print("done")
