#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Apply remaining fixes to the PRD — Rev. 467 update."""
import io

path = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

changes = []

def replace_once(old, new, label):
    global content
    if old in content:
        content = content.replace(old, new, 1)
        changes.append(f"[{label}] OK")
    else:
        changes.append(f"[{label}] FAIL (not found)")

# Fix 1: §12 line 760 — header Rev. 463 → Rev. 467
old1 = "header Rev. 463, §11 kompakt changelog 116–462, §12 updated). Local branch **4 commits ahead / 0 behind** origin_main."
new1 = "header Rev. 467, §11 kompakt changelog 116–466, §12 updated). Local branch **4 commits ahead / 0 behind** origin_main."
replace_once(old1, new1, "1.LINE760HDR")

# Fix 2: §12 line 773 — 0 commit → 4 commits
old2 = "4 / 0 (0 commit ahead origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 466 (data terkonsisten). Build gate: NOT RE-RUNABLE"
new2 = "4 / 0 (4 commits ahead origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 466 (data terkonsisten). Build gate: NOT RE-RUNABLE"
replace_once(old2, new2, "2.LINE773")

print("Changes:", changes)

with io.open(path, "w", encoding="utf-8") as f:
    f.write(content)
print("Total lines:", content.count(chr(10)) + 1)
