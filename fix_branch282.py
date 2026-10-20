#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fix Branch-ahead count=1 -> count=2 in Section 59/60 (label already 2, count stale)."""
PATH = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"
OLD = ("- **Branch-ahead:** 2 commit (sesuai `git rev-list --count origin/main..HEAD` = 1; "
       "`git rev-list --count HEAD..origin/main` = 0).")
NEW = ("- **Branch-ahead:** 2 commit (sesuai `git rev-list --count origin/main..HEAD` = 2; "
       "`git rev-list --count HEAD..origin/main` = 0).")

with open(PATH, "r", encoding="utf-8") as f:
    c = f.read()

cnt = c.count(OLD)
c = c.replace(OLD, NEW)

with open(PATH, "w", encoding="utf-8") as f:
    f.write(c)

print("replaced:", cnt)
print("remaining old pattern:", c.count(OLD))
print("new pattern count:", c.count(NEW))
