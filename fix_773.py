#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Apply final fix — §12 line 773 — Rev. 467 update."""
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

# Fix: §12 line 773 — 0 commit → 4 commits
replace_once(
    "4 / 0 (0 commit ahead origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 466 (data terkonsisten). Build gate: NOT RE-RUNABLE",
    "4 / 0 (4 commits ahead origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 466 (data terkonsisten). Build gate: NOT RE-RUNABLE",
    "2.LINE773",
)

print("Changes:", changes)
print("Total:", len(changes))
print("All OK:", all('OK' in c for c in changes))

with io.open(path, "w", encoding="utf-8") as f:
    f.write(content)
print("Total lines:", content.count(chr(10)) + 1)
