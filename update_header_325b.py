#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Update Rev. 325 header summary with current verification state (targeted)."""
import os
REPO = "/opt/data/home/workspace/dev/pondok-banat"
PRD = os.path.join(REPO, "PRD-PONDOK-BANAT.md")

with open(PRD, encoding="utf-8") as f:
    c = f.read()

# 1) HEAD local (header)
old_head = "Git HEAD (local): `dbf2fe0bf557a9eca66c6849987ef4597cca8e23` (Rev. 323, commit dbf2fe0) (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `dbf2fe0bf557a9eca66c6849987ef4597cca8e23`)"
new_head = "Git HEAD (local): `4b246510265ea3b38962d400cba6426a68105458` (Rev. 324, commit 4b24651) (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `4b246510265ea3b38962d400cba6426a68105458`)"
print("old_head:", c.count(old_head))
assert c.count(old_head) == 1, "header HEAD not found"
c = c.replace(old_head, new_head)

# 2) header's two "17 commits ahead" occurrences (with surrounding context)
old_ah1 = "Git HEAD (origin/main): `74b54cfde74daeb356595d0abacee173537f7992` (Rev. 309) \u2014 17 commits ahead, 0 commit behind origin.main."
new_ah1 = "Git HEAD (origin/main): `74b54cfde74daeb356595d0abacee173537f7992` (Rev. 309) \u2014 18 commits ahead, 0 commit behind origin.main."
print("old_ah1:", c.count(old_ah1))
assert c.count(old_ah1) == 1, "header ahead1 not found"
c = c.replace(old_ah1, new_ah1)

old_ah2 = "**17 commits ahead**, **0 commit behind** origin.main."
new_ah2 = "**18 commits ahead**, **0 commit behind** origin.main."
print("old_ah2:", c.count(old_ah2))
assert c.count(old_ah2) == 2, "header ahead2 not found"
c = c.replace(old_ah2, new_ah2, 1)

# 3) latest revision note
old_latest = "revisi terbaru = Rev. 324, belum dicomit); hanya file .py tambahan yang tidak ter-track."
new_latest = "revisi terbaru = Rev. 325, belum dicomit"
print("old_latest:", c.count(old_latest))
assert c.count(old_latest) == 1, "latest revision note not found"
c = c.replace(old_latest, new_latest)

with open(PRD, "w", encoding="utf-8") as f:
    f.write(c)
print("Done. Header line:")
print(c.splitlines()[3])
