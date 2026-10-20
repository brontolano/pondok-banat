#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fix remaining messy HEAD references (line 7307, 7321, 7324)."""
import os
REPO = "/opt/data/home/workspace/dev/pondok-banat"
PRD = os.path.join(REPO, "PRD-PONDOK-BANAT.md")

with open(PRD, encoding="utf-8") as f:
    c = f.read()

# 1) Line 7307: "commit 4b24651 (branch" -> "commit 4b24651), branch"
old1 = "commit 4b24651 (branch `main`, remote"
new1 = "commit 4b24651), branch `main` (remote"
print("old1 count:", c.count(old1))
assert c.count(old1) == 1
c = c.replace(old1, new1)

# 2) Line 7321 backtick-wrapped HEAD
old2 = "`4b24651 Rev. 324: PRD fresh verification & stability confirmation (20 Oct 2026 WIB); updated header to Rev. 324 + added section 109`"
new2 = "`4b24651`"
print("old2 count:", c.count(old2))
assert c.count(old2) == 2
c = c.replace(old2, new2)

# 3) Line 7324 backtick-wrapped HEAD
old3 = "`4b24651 Rev. 324: PRD fresh verification & stability confirmation (20 Oct 2026 WIB); updated header to Rev. 324 + added section 109`"
new3 = "`4b24651`"
print("old3 count:", c.count(old3))
assert c.count(old3) == 1
c = c.replace(old3, new3)

with open(PRD, "w", encoding="utf-8") as f:
    f.write(c)
print("Done. Showing final relevant lines:")
for i, line in enumerate(c.splitlines(), 1):
    if i >= 7305 and i <= 7325:
        print(i, "|", line)
