#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fix remaining messy HEAD references in section 110."""
import os
REPO = "/opt/data/home/workspace/dev/pondok-banat"
PRD = os.path.join(REPO, "PRD-PONDOK-BANAT.md")

with open(PRD, encoding="utf-8") as f:
    c = f.read()

# 1) Line 7307: "4b24651 (branch" -> "4b24651), branch" (close the commit parens cleanly)
old1 = "4b24651 (branch `main`, remote"
new1 = "4b24651), branch `main` (remote"
print("old1 count:", c.count(old1))
assert c.count(old1) == 1
c = c.replace(old1, new1)

# 2) Both backtick-wrapped HEAD occurrences (lines 7321 and 7324)
old2 = "`4b24651 Rev. 324: PRD fresh verification & stability confirmation (20 Oct 2026 WIB); updated header to Rev. 324 + added section 109`"
new2 = "`4b24651`"
print("old2 count:", c.count(old2))
assert c.count(old2) == 2
c = c.replace(old2, new2)

with open(PRD, "w", encoding="utf-8") as f:
    f.write(c)
print("Done. Verifying:")
for i, line in enumerate(c.splitlines(), 1):
    if 7300 <= i <= 7325:
        print(i, "|", line)
