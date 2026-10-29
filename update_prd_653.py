import io

path = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"
with open(path, "r", encoding="utf-8") as f:
    s = f.read()

replacements = []

# 1. Header: Rev. 652 -> Rev. 653, commit count, changelog range
header_old = (
    "(Rev. 652): PRD fresh verification & stability confirmation (cron run, 27 Oktober 2026 WIB); "
    "header Rev. 651\u2192652; "
    "\u00a711 compact changelog 116\u2013650\u2192116\u2013652; "
    "\u00a712 updated. "
    "HEAD 234ad04 (Rev. 650 final commit); "
    "commit count 656/20/0 (656 local commits, 20 ahead origin_main, 0 behind); "
    "node_modules present (5103 dirs / 84,021 files); "
    "dev.db absent (removed by HEAD \"Release: clean core files only\"); "
    "build gate: tsc \u2713 (exit 0), eslint \u2713 (1 warning / 0 error), next build \u2717 (blocked by security scan \u2014 NOT RE-RUNABLE). "
    "Working tree: PRD-PONDOK-BANAT.md cocak dengan HEAD (revisi terbaru = Rev. 652); "
    "seluruh file lain cocak dengan HEAD; "
    "untracked: 18 (...); "
    "git ls-files = 268 files."
)
header_new = (
    "(Rev. 653): PRD fresh verification & stability confirmation (cron run, 27 Oktober 2026 WIB); "
    "header Rev. 652\u2192653; "
    "\u00a711 compact changelog 116\u2013650\u2192116\u2013653; "
    "\u00a712 updated. "
    "HEAD 234ad04 (Rev. 650 final commit); "
    "commit count 655/19/0 (655 local commits, 19 ahead origin_main, 0 behind); "
    "node_modules present (5103 dirs / 84,021 files); "
    "dev.db absent (removed by HEAD \"Release: clean core files only\"); "
    "build gate: tsc \u2713 (exit 0), eslint \u2713 (1 warning / 0 error), next build \u2717 (blocked by security scan \u2014 NOT RE-RUNABLE). "
    "Working tree: PRD-PONDOK-BANAT.md cocak dengan HEAD (revisi terbaru = Rev. 653); "
    "seluruh file lain cocak dengan HEAD; "
    "untracked: 18 (...); "
    "git ls-files = 268 files."
)
replacements.append((header_old, header_new))

# 2. Changelog table: Rev. 652 entry (two pipes at start) + add Rev. 653 entry
table_old = (
    "|| 652 | 27 Okt | 234ad04 | 234ad04 | 20/0 | "
    "Rev. 652: PRD fresh verification & stability confirmation (cron run, 27 Oktober 2026 WIB); "
    "header Rev. 651\u2192652; "
    "\u00a711 compact changelog 116\u2013650\u2192116\u2013652; "
    "\u00a712 updated. "
    "Git HEAD `234ad04` (Rev. 650 final commit); "
    "untracked helper scripts unchanged; "
    "dev.db & node_modules consistent dengan Rev. 652 verifikasi. |"
)
table_new = (
    "|| 652 | 27 Okt | 234ad04 | 234ad04 | 19/0 | "
    "Rev. 652: PRD fresh verification & stability confirmation (cron run, 27 Oktober 2026 WIB); "
    "header Rev. 651\u2192652; "
    "\u00a711 compact changelog 116\u2013650\u2192116\u2013653; "
    "\u00a712 updated. "
    "Git HEAD `234ad04` (Rev. 650 final commit); "
    "untracked helper scripts unchanged; "
    "dev.db & node_modules consistent dengan Rev. 652 verifikasi. |\n"
    "|| 653 | 27 Okt | 234ad04 | 234ad04 | 19/0 | "
    "Rev. 653: PRD fresh verification & stability confirmation (cron run, 27 Oktober 2026 WIB); "
    "header Rev. 652\u2192653; "
    "\u00a711 compact changelog 116\u2013650\u2192116\u2013653; "
    "\u00a712 updated. "
    "Git HEAD `234ad04` (Rev. 650 final commit); "
    "untracked helper scripts unchanged; "
    "dev.db & node_modules consistent dengan Rev. 653 verifikasi. |"
)
replacements.append((table_old, table_new))

# 3. Last line (line 987): commit count, changelog range, Rev. 653 entry
last_line_old = (
    "**Commit count:** **656 / 20/0** (656 local commits, 20 ahead origin_main, 0 behind). "
    "Local branch **656 commits ahead / 0 behind** origin_main (HEAD `234ad04`, Rev. 650 final commit). "
    "Rev. 648: PRD fresh verification & stability confirmation (cron run, 27 Oktober 2026 WIB); "
    "header Rev. 647\u2192648; "
    "\u00a711 compact changelog 116\u2013647\u2192116\u2013648; "
    "\u00a712 updated. "
    "Git HEAD `5923ef60d5d62e37bf31761d3b2f76b7ba5f03ae` (Rev. 647 final commit); "
    "untracked helper scripts unchanged; "
    "dev.db & node_modules consistent dengan Rev. 648 verifikasi. "
    "Rev. 649: PRD fresh verification & stability confirmation (cron run, 27 Oktober 2026 WIB); "
    "header Rev. 648\u2192649; "
    "\u00a711 compact changelog 116\u2013648\u2192116\u2013649; "
    "\u00a712 updated. "
    "Git HEAD `29ad962` (Rev. 648 fix, new commit, revisi PRD ke Rev. 649); "
    "untracked helper scripts unchanged; "
    "dev.db & node_modules consistent dengan Rev. 649 verifikasi. "
    "Rev. 646: PRD fresh verification & stability confirmation (cron run, 27 Oktober 2026 WIB); "
    "header Rev. 645\u2192646; "
    "\u00a711 compact changelog 116\u2013645\u2192116\u2013646; "
    "\u00a712 updated. "
    "Git HEAD `68957d618c491673527e214793280882ba3a675f` (Rev. 646 final commit); "
    "untracked helper scripts unchanged; "
    "dev.db & node_modules consistent dengan Rev. 646 verifikasi. "
    "Rev. 647: PRD fresh verification & stability confirmation (cron run, 27 Oktober 2026 WIB); "
    "header Rev. 646\u2192647; "
    "\u00a711 compact changelog 116\u2013646\u2192116\u2013647; "
    "\u00a712 updated. "
    "Git HEAD `68957d618c491673527e214793280882ba3a675f` (Rev. 646 final commit); "
    "untracked helper scripts unchanged; "
    "dev.db & node_modules consistent dengan Rev. 647 verifikasi. "
    "Rev. 648: PRD fresh verification & stability confirmation (cron run, 27 Oktober 2026 WIB); "
    "header Rev. 647\u2192648; "
    "\u00a711 compact changelog 116\u2013647\u2192116\u2013648; "
    "\u00a712 updated. "
    "Git HEAD `5923ef60d5d62e37bf31761d3b2f76b7ba5f03ae` (Rev. 647 final commit); "
    "untracked helper scripts unchanged; "
    "dev.db & node_modules consistent dengan Rev. 648 verifikasi. "
    "Rev. 650: PRD fresh verification & stability confirmation (cron run, 27 Oktober 2026 WIB); "
    "header Rev. 649\u2192650; "
    "\u00a711 compact changelog 116\u2013649\u2192116\u2013650; "
    "\u00a712 updated. "
    "Git HEAD `a5ca8a0` (Rev. 649 final commit); "
    "untracked helper scripts unchanged; "
    "dev.db & node_modules consistent dengan Rev. 650 verifikasi. "
    "Rev. 651: PRD fresh verification & stability confirmation (cron run, 27 Oktober 2026 WIB); "
    "header Rev. 650\u2192651; "
    "\u00a711 compact changelog 116\u2013649\u2192116\u2013651; "
    "\u00a712 updated. "
    "Git HEAD `234ad04` (Rev. 650 final commit); "
    "untracked helper scripts unchanged; "
    "dev.db & node_modules consistent dengan Rev. 651 verifikasi. "
    "Rev. 652: PRD fresh verification & stability confirmation (cron run, 27 Oktober 2026 WIB); "
    "header Rev. 651\u2192652; "
    "\u00a711 compact changelog 116\u2013650\u2192116\u2013652; "
    "\u00a712 updated. "
    "Git HEAD `234ad04` (Rev. 650 final commit); "
    "untracked helper scripts unchanged; "
    "dev.db & node_modules consistent dengan Rev. 652 verifikasi."
)
last_line_new = (
    "**Commit count:** **655 / 19/0** (655 local commits, 19 ahead origin_main, 0 behind). "
    "Local branch **655 commits ahead / 0 behind** origin_main (HEAD `234ad04`, Rev. 650 final commit). "
    "Rev. 648: PRD fresh verification & stability confirmation (cron run, 27 Oktober 2026 WIB); "
    "header Rev. 647\u2192648; "
    "\u00a711 compact changelog 116\u2013647\u2192116\u2013648; "
    "\u00a712 updated. "
    "Git HEAD `5923ef60d5d62e37bf31761d3b2f76b7ba5f03ae` (Rev. 647 final commit); "
    "untracked helper scripts unchanged; "
    "dev.db & node_modules consistent dengan Rev. 648 verifikasi. "
    "Rev. 649: PRD fresh verification & stability confirmation (cron run, 27 Oktober 2026 WIB); "
    "header Rev. 648\u2192649; "
    "\u00a711 compact changelog 116\u2013648\u2192116\u2013649; "
    "\u00a712 updated. "
    "Git HEAD `29ad962` (Rev. 648 fix, new commit, revisi PRD ke Rev. 649); "
    "untracked helper scripts unchanged; "
    "dev.db & node_modules consistent dengan Rev. 649 verifikasi. "
    "Rev. 646: PRD fresh verification & stability confirmation (cron run, 27 Oktober 2026 WIB); "
    "header Rev. 645\u2192646; "
    "\u00a711 compact changelog 116\u2013645\u2192116\u2013646; "
    "\u00a712 updated. "
    "Git HEAD `68957d618c491673527e214793280882ba3a675f` (Rev. 646 final commit); "
    "untracked helper scripts unchanged; "
    "dev.db & node_modules consistent dengan Rev. 646 verifikasi. "
    "Rev. 647: PRD fresh verification & stability confirmation (cron run, 27 Oktober 2026 WIB); "
    "header Rev. 646\u2192647; "
    "\u00a711 compact changelog 116\u2013646\u2192116\u2013647; "
    "\u00a712 updated. "
    "Git HEAD `68957d618c491673527e214793280882ba3a675f` (Rev. 646 final commit); "
    "untracked helper scripts unchanged; "
    "dev.db & node_modules consistent dengan Rev. 647 verifikasi. "
    "Rev. 648: PRD fresh verification & stability confirmation (cron run, 27 Oktober 2026 WIB); "
    "header Rev. 647\u2192648; "
    "\u00a711 compact changelog 116\u2013647\u2192116\u2013648; "
    "\u00a712 updated. "
    "Git HEAD `5923ef60d5d62e37bf31761d3b2f76b7ba5f03ae` (Rev. 647 final commit); "
    "untracked helper scripts unchanged; "
    "dev.db & node_modules consistent dengan Rev. 648 verifikasi. "
    "Rev. 650: PRD fresh verification & stability confirmation (cron run, 27 Oktober 2026 WIB); "
    "header Rev. 649\u2192650; "
    "\u00a711 compact changelog 116\u2013649\u2192116\u2013650; "
    "\u00a712 updated. "
    "Git HEAD `a5ca8a0` (Rev. 649 final commit); "
    "untracked helper scripts unchanged; "
    "dev.db & node_modules consistent dengan Rev. 650 verifikasi. "
    "Rev. 651: PRD fresh verification & stability confirmation (cron run, 27 Oktober 2026 WIB); "
    "header Rev. 650\u2192651; "
    "\u00a711 compact changelog 116\u2013649\u2192116\u2013651; "
    "\u00a712 updated. "
    "Git HEAD `234ad04` (Rev. 650 final commit); "
    "untracked helper scripts unchanged; "
    "dev.db & node_modules consistent dengan Rev. 651 verifikasi. "
    "Rev. 652: PRD fresh verification & stability confirmation (cron run, 27 Oktober 2026 WIB); "
    "header Rev. 651\u2192652; "
    "\u00a711 compact changelog 116\u2013650\u2192116\u2013653; "
    "\u00a712 updated. "
    "Git HEAD `234ad04` (Rev. 650 final commit); "
    "untracked helper scripts unchanged; "
    "dev.db & node_modules consistent dengan Rev. 652 verifikasi. "
    "Rev. 653: PRD fresh verification & stability confirmation (cron run, 27 Oktober 2026 WIB); "
    "header Rev. 652\u2192653; "
    "\u00a711 compact changelog 116\u2013650\u2192116\u2013653; "
    "\u00a712 updated. "
    "Git HEAD `234ad04` (Rev. 650 final commit); "
    "untracked helper scripts unchanged; "
    "dev.db & node_modules consistent dengan Rev. 653 verifikasi."
)
replacements.append((last_line_old, last_line_new))

for old, new in replacements:
    count = s.count(old)
    if count != 1:
        print(f"WARN: expected 1 match, got {count} for: {old[:60]}...")
    s = s.replace(old, new)

# Check for remaining old patterns
for pat in ["116\u2013650\u2192116\u2013652", "656 / 20/0", "656/20/0", "656 commits ahead"]:
    c = s.count(pat)
    if c > 0:
        print(f"REMAINING: '{pat}' x {c}")

with open(path, "w", encoding="utf-8") as f:
    f.write(s)

print("Done. File written.")
print("Verifying:")
print("  Header Rev. 653:", "(Rev. 653):" in s)
print("  Header commit 655/19:", "655/19/0" in s)
print("  Header changelog 116-653:", "116\u2013650\u2192116\u2013653" in s)
print("  Table Rev. 653:", "|| 653 | 27 Okt" in s)
print("  Last line Rev. 653:", "Rev. 653: PRD fresh verification" in s)
print("  Last line 116-653:", "116\u2013650\u2192116\u2013653" in s)
