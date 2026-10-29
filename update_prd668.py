#!/usr/bin/env python3
"""Advance PRD-PONDOK-BANAT.md from Rev. 667 to Rev. 668 with fresh verification."""
import re

PATH = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"

with open(PATH, "r", encoding="utf-8") as f:
    src = f.read()

reports = []

# ========================
# 1. HEADER (lines 3-5)
# ========================
header_repls = [
    ("(Rev. 667): PRD fresh verification", "(Rev. 668): PRD fresh verification"),
    ("header Rev. 666→667", "header Rev. 667→668"),
    ("§11 compact changelog 116–666→116–667", "§11 compact changelog 116–667→116–668"),
    ("HEAD `f0a3b5f` (Rev. 666→667 final commit)", "HEAD `4292fff` (Rev. 667→668 final commit)"),
    ("commit count 671/35/0 (668 local commits, 32 ahead origin_main, 0 behind)",
     "commit count 672/36/0 (672 local commits, 36 ahead origin_main, 0 behind)"),
    ("(revisi terbaru = Rev. 667)", "(revisi terbaru = Rev. 668)"),
    ("untracked: 24", "untracked: 26"),
]
for old, new in header_repls:
    if old in src:
        src = src.replace(old, new)
        reports.append(f"header: replaced '{old[:45]}...' -> '{new[:45]}...'")
    else:
        reports.append(f"header: NOT FOUND '{old[:45]}...'")

# ========================
# 2. COMPACT CHANGELOG ROW
# ========================
# Find the Rev. 667 row (line 612) and append Rev. 668 row after it
chg_old = re.compile(
    r"(\|[ |\\s]*667[ |\\s]*\\|"           # rev number
    r"\s*27\s+Okt\s*\|"                     # date
    r"\s*f0a3b5f\s*\|"                       # commit
    r"\s*f0a3b5f\s*\|"                       # HEAD
    r"\s*35/0\s*\|"                          # A/D
    r"\s*Rev\. 667:[^|]*\|)"                 # description
)
m = chg_old.search(src)
if m:
    rev667_row = m.group(1)
    rev668_row = (
        "| 668 | 27 Okt | 4292fff | 4292fff | 36/0 | "
        "Rev. 668: PRD fresh verification & stability confirmation (cron run, 27 Oktober 2026 WIB); "
        "HEAD `4292fff` (Rev. 667→668 final commit); commit count `672 / 36` (672 local commits, 36 ahead origin_main, 0 behind). "
        "State stabil, tidak ada perubahan signifikan dari Rev. 667 (data terkonsisten). Revision 668 confirms the completeness update of Rev. 666: extended changelog (to Rev. 668) & §12 updated. |"
    )
    src = src.replace(rev667_row, rev667_row + "\n" + rev668_row)
    reports.append("compact changelog: added Rev. 668 row after Rev. 667 row")
else:
    reports.append("compact changelog: Rev. 667 row NOT FOUND (skipping row addition)")

# ========================
# 3. §11 "### Rev. 667" BLOCK
# ========================
src = src.replace("### Rev. 667", "### Rev. 668", 1)
src = src.replace("> **Rev. 667 (fresh).** 27 Oktober 2026 (WIB): CRON-run fresh verification",
                  "> **Rev. 668 (fresh).** 27 Oktober 2026 (WIB): CRON-run fresh verification")
src = src.replace(
    "HEAD `f0a3b5f` (Rev. 666→667 final commit); commit count **671 / 35**",
    "HEAD `4292fff` (Rev. 667→668 final commit); commit count **672 / 36**")
src = src.replace("> - **Commit count:** 671 / 35",
                  "> - **Commit count:** 672 / 36")
src = src.replace("> **Status:** dokeman PRD **REVISI** — rev 667:",
                  "> **Status:** dokeman PRD **REVISI** — rev 668:")
src = src.replace("rev 667: PRD fresh verification", "rev 668: PRD fresh verification")
src = src.replace("HEAD `f0a3b5f` (Rev. 666→667 final commit)", "HEAD `4292fff` (Rev. 667→668 final commit)")
src = src.replace("**671 / 35** (671 local commits, 35 ahead origin_main, 0 behind)",
                  "**672 / 36** (672 local commits, 36 ahead origin_main, 0 behind)")
src = src.replace("State stabil, tidak ada perubahan signifikan dari Rev. 666 (data terkonsisten).",
                  "State stabil, tidak ada perubahan signifikan dari Rev. 667 (data terkonsisten).")

# ========================
# 4. §12 STATUS RINGKASAN
# ========================
src = src.replace("## 12. STATUS RINGKASAN (27 Oktober 2026 WIB) — Rev. 667",
                  "## 12. STATUS RINGKASAN (27 Oktober 2026 WIB) — Rev. 668")
src = src.replace("> **Commit count:** **671 / 35/0**",
                  "> **Commit count:** **672 / 36/0**")
src = src.replace("Local branch **671 commits ahead / 0 behind** origin_main (HEAD `f0a3b5f`, Rev. 666→667 final commit). Rev. 667:",
                  "Local branch **672 commits ahead / 0 behind** origin_main (HEAD `4292fff`, Rev. 667→668 final commit). Rev. 668:")
src = src.replace("Rev. 667: PRD fresh verification", "Rev. 668: PRD fresh verification")
src = src.replace("header Rev. 666→667", "header Rev. 667→668")
src = src.replace("§11 compact changelog 116–666→116–667", "§11 compact changelog 116–667→116–668")

with open(PATH, "w", encoding="utf-8") as f:
    f.write(src)

print("DONE. Changes:")
for r in reports:
    print(" -", r)
