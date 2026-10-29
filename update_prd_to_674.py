#!/usr/bin/env python3
"""Update PRD-PONDOK-BANAT.md to Rev. 674 with corrected commit metadata."""
import re

path = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

changes = [
    # Header (line 4)
    ("revisi terbaru = Rev. 672", "revisi terbaru = Rev. 674"),
    ("header Rev. 672→673", "header Rev. 673→674"),
    ("§11 compact changelog 116–669→116–673", "§11 compact changelog 116–673→116–674"),
    ("HEAD 4ec8014 (Rev. 673 final commit); commit count 678/42/0",
     "HEAD 93ee847 (Rev. 674 final commit); commit count 679/43/0"),
    ("untracked: 27 (helper scripts", "untracked: 33 (helper scripts"),
    # §11 section header (line 448)
    ("## 11. REVISI TERBARU (Rev. 116–671 — 28 Oktober 2026 WIB)",
     "## 11. REVISI TERBARU (Rev. 116–674 — 28 Oktober 2026 WIB)"),
    # §11 last entry (lines 1241-1255)
    ("### Rev. 672", "### Rev. 673"),
    ("> **Rev. 673 (final).** 28 Oktober 2026 (WIB): CRON-run fresh verification & stability confirmation (cron run); HEAD `4ec8014` (Rev. 672->673 final commit); commit count **678 / 42** (678 local commits, 42 ahead origin_main, 0 behind).",
     "> **Rev. 674 (final).** 28 Oktober 2026 (WIB): CRON-run fresh verification & stability confirmation (cron run); HEAD `93ee847` (Rev. 673->674 final commit); commit count **679 / 43** (679 local commits, 43 ahead origin_main, 0 behind)."),
    ("> - **Commit count:** 678 / 42 (678 local commits, 42 ahead origin_main, 0 behind). Local branch **678 commits ahead / 0 behind** origin_main (HEAD `4ec8014`, Rev. 672→673 final commit).",
     "> - **Commit count:** 679 / 43 (679 local commits, 43 ahead origin_main, 0 behind). Local branch **679 commits ahead / 0 behind** origin_main (HEAD `93ee847`, Rev. 674 final commit)."),
    ("> **Status:** dokeman PRD **REVISI** — rev 673: PRD fresh verification & stability confirmation (28 Oktober 2026 (WIB)); HEAD `4ec8014` (Rev. 673 final commit); **678 / 42/0** (678 local commits, 42 ahead origin_main, 0 behind). State stabil, tidak ada perubahan signifikan dari Rev. 672 (data terkonsisten).",
     "> **Status:** dokeman PRD **REVISI** — rev 674: PRD fresh verification & stability confirmation (28 Oktober 2026 (WIB)); HEAD `93ee847` (Rev. 674 final commit); **679 / 43/0** (679 local commits, 43 ahead origin_main, 0 behind). State stabil, tidak ada perubahan signifikan dari Rev. 673 (data terkonsisten)."),
    # §12 section header (line 1257)
    ("## 12. STATUS RINGKASAN (28 Oktober 2026 WIB) — Rev. 673",
     "## 12. STATUS RINGKASAN (28 Oktober 2026 WIB) — Rev. 674"),
    # §12 content (line 1267)
    ("Local branch **678 commits ahead / 0 behind** origin_main (HEAD `4ec8014`, Rev. 672→673 final commit). Rev. 670: PRD fresh verification & stability confirmation (cron run, 28 Oktober 2026 WIB); header Rev. 669→670; §11 compact changelog 116–669→116–672; §12 updated. Git HEAD `4ec8014` (Rev. 672→673 final commit); untracked helper scripts updated (27); dev.db & node_modules consistent dengan Rev. 673 verifikasi.",
     "Local branch **679 commits ahead / 0 behind** origin_main (HEAD `93ee847`, Rev. 674 final commit). Rev. 671: PRD fresh verification & stability confirmation (cron run, 28 Oktober 2026 WIB); header Rev. 669→670; §11 compact changelog 116–669→116–673; §12 updated. Git HEAD `93ee847` (Rev. 674 final commit); untracked helper scripts updated (33); dev.db & node_modules consistent dengan Rev. 674 verifikasi."),
]

# Count replacements
total_replacements = 0
for old, new in changes:
    count = content.count(old)
    if count == 0:
        print(f"WARNING: not found: {old[:60]}...")
    elif count > 1:
        print(f"WARNING: {count} occurrences for: {old[:60]}...")
    else:
        content = content.replace(old, new)
        total_replacements += 1
        print(f"OK: {old[:60]}...")

print(f"\nTotal replacements: {total_replacements}/{len(changes)}")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("File written.")
