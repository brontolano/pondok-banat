#!/usr/bin/env python3
"""Update PRD-PONDOK-BANAT.md from Rev. 666 to Rev. 667 with fresh verification."""
import re

PATH = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"

with open(PATH, "r", encoding="utf-8") as f:
    src = f.read()

reports = []

# --- 1. Header line (line 4) ---
repls = [
    ("(Rev. 666): PRD fresh verification", "(Rev. 667): PRD fresh verification"),
    ("header Rev. 665→666", "header Rev. 666→667"),
    ("§11 compact changelog 116–665→116–666", "§11 compact changelog 116–666→116–667"),
    ("HEAD `9d84b7e240bdf04796e3d37675912bada6f9de07` (Rev. 666 final commit)",
     "HEAD `f0a3b5f` (Rev. 666→667 final commit)"),
    ("commit count 668/32/0", "commit count 671/35/0"),
    ("(revisi terbaru = Rev. 666)", "(revisi terbaru = Rev. 667)"),
]
for old, new in repls:
    if old in src:
        src = src.replace(old, new)
        reports.append(f"header: replaced '{old[:40]}...' -> '{new[:40]}...'")
    else:
        reports.append(f"header: NOT FOUND '{old[:40]}...'")

# --- 2. Compact changelog: add Rev. 667 row after Rev. 666 row ---
# The changelog rows look like: | 666 | 27 Okt | 9d84b7e... | 9d84b7e... | 32/0 | Rev. 666: ... |
# Find the Rev. 666 row (any pipe-count prefix) and append Rev. 667 row after it.
chg_old = re.compile(
    r"(\|[ |\s]*666[ |\s]*\|\s*27\s*Okt\s*\|\s*9d84b7e240bdf04796e3d37675912bada6f9de07\s*\|\s*9d84b7e240bdf04796e3d37675912bada6f9de07\s*\|\s*32/0\s*\|\s*Rev\. 666:[^|]*\|)"
)
m = chg_old.search(src)
if m:
    rev666_row = m.group(1)
    rev667_row = (
        "| 667 | 27 Okt | f0a3b5f | f0a3b5f | 35/0 | Rev. 667: PRD fresh verification & stability confirmation "
        "(cron run, 27 Oktober 2026 WIB); HEAD `f0a3b5f` (Rev. 666→667 final commit); commit count `671 / 35` "
        "(671 local commits, 35 ahead origin_main, 0 behind). State stabil, tidak ada perubahan signifikan dari Rev. 666 "
        "(data terkonsisten). Revision 667 confirms the completeness update of Rev. 666: extended changelog (to Rev. 667) "
        "& §12 updated. |"
    )
    src = src.replace(rev666_row, rev666_row + "\n" + rev667_row)
    reports.append("compact changelog: added Rev. 667 row after Rev. 666 row")
else:
    reports.append("compact changelog: Rev. 666 row NOT FOUND (skipping row addition)")

# --- 3. §11 "### Rev. 666" block -> "### Rev. 667" ---
src = src.replace("### Rev. 666", "### Rev. 667", 1)
src = src.replace("> **Rev. 666 (fresh).** 27 Oktober 2026 (WIB): CRON-run fresh verification",
                  "> **Rev. 667 (fresh).** 27 Oktober 2026 (WIB): CRON-run fresh verification")
src = src.replace("HEAD `9d84b7e240bdf04796e3d37675912bada6f9de07` (Rev. 666 final commit); commit count **668 / 32** (668 local commits, 32 ahead origin_main, 0 behind).",
                  "HEAD `f0a3b5f` (Rev. 666→667 final commit); commit count **671 / 35** (671 local commits, 35 ahead origin_main, 0 behind).")
src = src.replace("> - **Commit count:** 668 / 32 (668 local commits, 32 ahead origin_main, 0 behind).",
                  "> - **Commit count:** 671 / 35 (671 local commits, 35 ahead origin_main, 0 behind).")
src = src.replace("> **Status:** dokumen PRD **REVISI** — rev 666: PRD fresh verification & stability confirmation (27 Oktober 2026 (WIB)); HEAD `9d84b7e240bdf04796e3d37675912bada6f9de07` (Rev. 666 final commit); **668 / 32**",
                  "> **Status:** dokumen PRD **REVISI** — rev 667: PRD fresh verification & stability confirmation (27 Oktober 2026 (WIB)); HEAD `f0a3b5f` (Rev. 666→667 final commit); **671 / 35**")

# --- 4. §12 STATUS RINGKASAN ---
src = src.replace("## 12. STATUS RINGKASAN (27 Oktober 2026 WIB) — Rev. 666",
                  "## 12. STATUS RINGKASAN (27 Oktober 2026 WIB) — Rev. 667")
src = src.replace("> **Commit count:** **668 / 32/0** (668 local commits, 32 ahead origin_main, 0 behind).",
                  "> **Commit count:** **671 / 35/0** (671 local commits, 35 ahead origin_main, 0 behind).")
src = src.replace("Local branch **668 commits ahead / 0 behind** origin_main (HEAD `9d84b7e240bdf04796e3d37675912bada6f9de07`, Rev. 666 final commit). Rev. 666:",
                  "Local branch **671 commits ahead / 0 behind** origin_main (HEAD `f0a3b5f`, Rev. 666→667 final commit). Rev. 667:")

with open(PATH, "w", encoding="utf-8") as f:
    f.write(src)

print("DONE. Changes:")
for r in reports:
    print(" -", r)
