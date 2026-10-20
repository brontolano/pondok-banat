#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Restore the missing closing paren + 'hanya file .py tambahan' text in Rev.325 header."""
import os
REPO = "/opt/data/home/workspace/dev/pondok-banat"
PRD = os.path.join(REPO, "PRD-PONDOK-BANAT.md")

with open(PRD, encoding="utf-8") as f:
    c = f.read()

old = "revisi terbaru = Rev. 325, belum dicomit Local branch"
new = "revisi terbaru = Rev. 325, belum dicomit); hanya file .py tambahan yang tidak ter-track. Local branch"
print("old count:", c.count(old))
assert c.count(old) == 1, f"count={c.count(old)}"
c = c.replace(old, new)

with open(PRD, "w", encoding="utf-8") as f:
    f.write(c)
print("Fixed. Header line:")
print(c.splitlines()[3])
