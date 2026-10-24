#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Apply final fixes to the PRD — Rev. 467 update."""
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

# Fix 1: §11 Rev. 462 entry — restore to 0 / 0 (historical entry)
replace_once(
    "||- **Rev. 462.** 23 Oktober 2026 (WIB): PRD fresh verification & stability confirmation (23 Oct 2026 WIB); HEAD `360cfb1f5864524570e622ed4d94a61c6e5950ef` (Rev. 462: PRD fresh verification & stability confirmation (23 Oct 2026 WIB); header Rev. 467, §11 kompakt changelog 116–466, §12 updated), 4 / 0",
    "||- **Rev. 462.** 23 Oktober 2026 (WIB): PRD fresh verification & stability confirmation (23 Oct 2026 WIB); HEAD `360cfb1f5864524570e622ed4d94a61c6e5950ef` (Rev. 462: PRD fresh verification & stability confirmation (23 Oct 2026 WIB); header Rev. 467, §11 kompakt changelog 116–466, §12 updated), 0 / 0",
    "1.§11REV462",
)

# Fix 2: §12 line 773 — 0 commit → 4 commits
replace_once(
    "4 / 0 (0 commit ahead origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 466 (data terkonsisten). Build gate: NOT RE-RUNABLE",
    "4 / 0 (4 commits ahead origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 466 (data terkonsisten). Build gate: NOT RE-RUNABLE",
    "2.LINE773",
)

# Fix 3: §13 Rev. 467 entry — 0 commit → 4 commits
replace_once(
    "4 / 0 (0 commit ahead origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 462 (data terkonsisten). Build gate: NOT RE-RUNABLE",
    "4 / 0 (4 commits ahead origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 462 (data terkonsisten). Build gate: NOT RE-RUNABLE",
    "3.§13467",
)

print("Changes:", changes)
print("Total:", len(changes))
print("All OK:", all('OK' in c for c in changes))

with io.open(path, "w", encoding="utf-8") as f:
    f.write(content)
print("Total lines:", content.count(chr(10)) + 1)
