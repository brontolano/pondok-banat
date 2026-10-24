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

# Fix 1: Header — Rev. 465 → Rev. 467 (in the Git HEAD (local) line)
replace_once(
    "header Rev. 465, §11 kompakt changelog 116–464, §12 updated). Branch",
    "header Rev. 467, §11 kompakt changelog 116–466, §12 updated). Branch",
    "1.HEADER2",
)

# Fix 2: Header — Rev. 465 → Rev. 467
replace_once(
    "> **Git HEAD (local):** `360cfb1f5864524570e622ed4d94a61c6e5950ef` (Rev. 465: PRD fresh verification",
    "> **Git HEAD (local):** `360cfb1f5864524570e622ed4d94a61c6e5950ef` (Rev. 467: PRD fresh verification",
    "2.HEADER3",
)

# Fix 3: §12 line 760 — 0/0 → 4/0, and branch status
replace_once(
    "updated), 0 / 0 (0 commit ahead origin_main). Local branch **4 commits ahead / 0 behind** origin_main. **origin/main:**",
    "updated), 4 / 0 (4 commits ahead origin_main). Local branch **4 commits ahead / 0 behind** origin_main. **origin/main:**",
    "3.LINE760C",
)

# Fix 4: §13 line 778 — header Rev. 463 → Rev. 467, changelog 116–462 → 466, 0/0 → 4/0
replace_once(
    "||- **Rev. 467.** 23 Oktober 2026 (WIB): PRD fresh verification & stability confirmation (23 Oct 2026 WIB); HEAD `3a66337a205155138b85916b47828346e09340bd` (Rev. 467: PRD fresh verification & stability confirmation (23 Oct 2026 WIB); header Rev. 463, §11 kompakt changelog 116–462, §12 updated), 0 / 0",
    "||- **Rev. 467.** 23 Oktober 2026 (WIB): PRD fresh verification & stability confirmation (23 Oct 2026 WIB); HEAD `3a66337a205155138b85916b47828346e09340bd` (Rev. 467: PRD fresh verification & stability confirmation (23 Oct 2026 WIB); header Rev. 467, §11 kompakt changelog 116–466, §12 updated), 4 / 0",
    "4.§13467ENTRY",
)

print("=== Changes applied ===")
for c in changes:
    print(c)
print(f"\nTotal: {len(changes)}")
print(f"All successful: {all('OK' in c for c in changes)}")

with io.open(path, "w", encoding="utf-8") as f:
    f.write(content)

print(f"Total lines: {content.count(chr(10)) + 1}")
