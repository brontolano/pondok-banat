#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Update Rev. 325 header summary with current verification state."""
import os
REPO = "/opt/data/home/workspace/dev/pondok-banat"
PRD = os.path.join(REPO, "PRD-PONDOK-BANAT.md")

with open(PRD, encoding="utf-8") as f:
    c = f.read()

# 1) HEAD local
old_head = "Git HEAD (local): `dbf2fe0bf557a9eca66c6849987ef4597cca8e23` (Rev. 323, commit dbf2fe0) (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `dbf2fe0bf557a9eca66c6849987ef4597cca8e23`)"
new_head = "Git HEAD (local): `4b246510265ea3b38962d400cba6426a68105458` (Rev. 324, commit 4b24651) (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `4b246510265ea3b38962d400cba6426a68105458`)"
print("old_head count:", c.count(old_head))
assert c.count(old_head) == 1
c = c.replace(old_head, new_head)

# 2) ahead count (2 occurrences)
print("old_ahead count:", c.count("17 commits ahead"))
assert c.count("17 commits ahead") == 2
c = c.replace("17 commits ahead", "18 commits ahead")

# 3) latest revision note
old_latest = "revisi terbaru = Rev. 324, belum dicomit"
new_latest = "revisi terbaru = Rev. 325, belum dicomit"
print("old_latest count:", c.count(old_latest))
assert c.count(old_latest) == 1
c = c.replace(old_latest, new_latest)

with open(PRD, "w", encoding="utf-8") as f:
    f.write(c)
print("Done. Header now:")
print(c.splitlines()[3])
