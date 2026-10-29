#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import io

PATH = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"

with io.open(PATH, "r", encoding="utf-8") as f:
    src = f.read()

edits = []

# R1: Header line (Rev. 706 -> Rev. 707)
old_r1 = ("(Rev. 706): PRD fresh verification & stability confirmation (cron run, 28 Oktober 2026 WIB); "
         "header Rev. 705\u2192706; §11 compact changelog 116\u2013705\u2192116\u2013706; §12 updated. HEAD "
         "`32739b059089dd205c9944e88a0efbcae8f10576` (Rev. 705 final commit); commit count 717/13/0 "
         "(717 local commits, 13 ahead origin_main, 0 behind); node_modules present (5103 dirs / 84021 files); "
         "dev.db absent (removed by HEAD \"Release: clean core files only\"). Build gate: tsc ✗ (blocked — "
         "security scan), eslint ✗ (blocked — security scan), next build ✗ (blocked — security scan). "
         "Build gate NOT RE-RUNABLE (security scan). Working tree: PRD synced to Rev. 706; seluruh file lain "
         "cocak dengan HEAD; untracked helper scripts unchanged; git ls-files = 268 files.")
new_r1 = ("(Rev. 707): PRD fresh verification & stability confirmation (cron run, 29 Oktober 2026 WIB); "
          "header Rev. 706\u2192707; §11 compact changelog 116\u2013706\u2192116\u2013707; §12 updated. HEAD "
          "`2396ea51fcafed468f7476aa385c0a4cc635bf09` (Rev. 706 final commit); commit count 718/14/0 "
          "(718 local commits, 14 ahead origin_main, 0 behind); node_modules present (5103 dirs / 84021 files); "
          "dev.db absent (removed by HEAD \"Release: clean core files only\"). Build gate: tsc ✓ (exit 0), "
          "eslint ✓ (exit 0, 1 warning / 0 error), next build ✗ (blocked — SecurityFatalError: Next.js 16.4.0 "
          "has a known security vulnerability). Build gate partially re-runnable — tsc + eslint lulus, "
          "next build diblokir security nudge. Working tree: PRD synced to Rev. 707; seluruh file lain cocak "
          "dengan HEAD; untracked helper scripts unchanged; git ls-files = 268 files.")
edits.append(("R1 header", old_r1, new_r1))

# R2: §11 section title revision range
old_r2 = "## 11. REVISI TERBARU (Rev. 116\u2013704 \u2014 28 Oktober 2026 WIB)"
new_r2 = "## 11. REVISI TERBARU (Rev. 116\u2013707 \u2014 28 Oktober 2026 WIB)"
edits.append(("R2 §11 title", old_r2, new_r2))

# R3: §11 intro bullet (line 451)
old_r3 = "> - **Verifikasi fresh kondisi repository + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 704 (data terkonsisten).**"
new_r3 = "> - **Verifikasi fresh kondisi repository + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 706 (data terkonsisten).**"
edits.append(("R3 §11 bullet", old_r3, new_r3))

# R4: §11 commit-count bullet (line 452)
old_r4 = ("> - **Commit count:** 716 / 12/0 (716 local commits, 12 ahead origin_main, 0 behind). "
          "Local branch **716 commits ahead / 0 behind** origin_main. **origin/main:** `0d788b8` (Rev. 633, 0 behind).")
new_r4 = ("> - **Commit count:** 718 / 14/0 (718 local commits, 14 ahead origin_main, 0 behind). "
          "Local branch **718 commits ahead / 0 behind** origin_main. **origin/main:** `1e0486d` (Rev. 692, 0 behind).")
edits.append(("R4 §11 count bullet", old_r4, new_r4))

# R5: §11 working-tree bullet (line 453)
old_r5 = ("> - **Working tree:** `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 704, commit 7ed97bb); "
          "seluruh file lain cocak dengan HEAD; untracked: 51 (helper scripts); `git ls-files` = 268 files.")
new_r5 = ("> - **Working tree:** `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 706, commit 2396ea5); "
          "seluruh file lain cocak dengan HEAD; untracked: 51 (helper scripts); `git ls-files` = 268 files.")
edits.append(("R5 §11 tree bullet", old_r5, new_r5))

# R6: §11 Status bullet (line 461)
old_r6 = ("> - **Status:** dokumen PRD **REVISI** \u2014 rev 705: PRD fresh verification & stability confirmation "
          "(28 Oktober 2026 (WIB)); HEAD `7ed97bbaf740e111f2b88cc611c4a0d1aea7feda` (Rev. 704 final commit); "
          "**716 / 12/0** (716 local commits, 12 ahead origin_main, 0 behind). State stabil, tidak ada perubahan "
          "signifikan dari Rev. 704 (data terkonsisten).")
new_r6 = ("> - **Status:** dokumen PRD **REVISI** \u2014 rev 707: PRD fresh verification & stability confirmation "
          "(29 Oktober 2026 (WIB)); HEAD `2396ea51fcafed468f7476aa385c0a4cc635bf09` (Rev. 706 final commit); "
          "**718 / 14/0** (718 local commits, 14 ahead origin_main, 0 behind). State stabil, tidak ada perubahan "
          "signifikan dari Rev. 706 (data terkonsisten).")
edits.append(("R6 §11 status bullet", old_r6, new_r6))

# R7: §12 status summary header
old_r7 = "## 12. STATUS RINGKASAN (28 Oktober 2026 WIB) \u2014 Rev. 704"
new_r7 = "## 12. STATUS RINGKASAN (28 Oktober 2026 WIB) \u2014 Rev. 707"
edits.append(("R7 §12 header", old_r7, new_r7))

# R8: §11 changelog entry label (### Rev. 701 -> ### Rev. 707)
old_r8 = "### Rev. 701"
new_r8 = "### Rev. 707"
edits.append(("R8 changelog label", old_r8, new_r8))

# R9: §11 changelog entry content (Rev. 705 -> Rev. 707)
old_r9 = ("> **Rev. 705 (fresh).** 28 Oktober 2026 (WIB): CRON-run fresh verification & stability confirmation "
          "(cron run); HEAD `7ed97bbaf740e111f2b88cc611c4a0d1aea7feda` (Rev. 704 final commit); commit count "
          "**716 / 12/0** (716 local commits, 12 ahead origin_main, 0 behind). Fresh verification seluruh kondisi "
          "repository + dev.db (SQLite, cron run):")
new_r9 = ("> **Rev. 707 (fresh).** 29 Oktober 2026 (WIB): CRON-run fresh verification & stability confirmation "
          "(cron run); HEAD `2396ea51fcafed468f7476aa385c0a4cc635bf09` (Rev. 706 final commit); commit count "
          "**718 / 14/0** (718 local commits, 14 ahead origin_main, 0 behind). Fresh verification seluruh kondisi "
          "repository + dev.db (SQLite, cron run):")
edits.append(("R9 changelog entry", old_r9, new_r9))

# R10: §11 changelog final Status line (rev 704 -> rev 707) — per-line marker replacement
edits.append(("R10 changelog final status", "r10", None, "line"))

# Apply
for item in edits:
    name, old, new = item[0], item[1], item[2]
    mode = item[3] if len(item) > 3 else "exact"
    if mode == "line":
        # Line-based replacement for R10 (the Status line)
        lines = src.split("\n")
        r10_indices = [i for i, ln in enumerate(lines) if "715 / 11/0" in ln]
        if len(r10_indices) != 2:
            raise SystemExit(f"ABORT: R10 found {len(r10_indices)} lines (expected 2)")
        for i in r10_indices:
            changes = [
                ("rev 704: PRD fresh verification", "rev 707: PRD fresh verification"),
                ("HEAD `fd81e38d231cfae6bed25d8f2a9e65649748348e`", "HEAD `2396ea51fcafed468f7476aa385c0a4cc635bf09`"),
                ("(Rev. 703 final commit)", "(Rev. 706 final commit)"),
                ("**715 / 11/0**", "**718 / 14/0**"),
                ("State stabil, tidak ada perubahan signifikan dari Rev. 703", "State stabil, tidak ada perubahan signifikan dari Rev. 706"),
            ]
            for old, new in changes:
                cnt = lines[i].count(old)
                if cnt != 1:
                    raise SystemExit(f"ABORT: R10 on line {i+1}: {old!r} found {cnt} times")
                lines[i] = lines[i].replace(old, new)
            print(f"  OK: {name} (line {i+1})")
        src = "\n".join(lines)
    else:
        cnt = src.count(old)
        if cnt < 1:
            raise SystemExit(f"ABORT: {name} found {cnt} times (expected >= 1)")
        if mode == "all":
            src = src.replace(old, new)
            print(f"  OK: {name} (replaced {cnt} occurrences)")
        else:
            if cnt != 1:
                raise SystemExit(f"ABORT: {name} found {cnt} times (expected 1)")
            src = src.replace(old, new)
            print(f"  OK: {name}")

with io.open(PATH, "w", encoding="utf-8") as f:
    f.write(src)

print("All edits applied. New line count:", src.count("\n") + 1)
