#!/usr/bin/env python3
"""Fix stale entries in §12 description (Rev. 468–518 section)."""

path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'

with open(path, 'r') as f:
    content = f.read()

# Fix 1: Replace stale "Status: rev 517" line (references Rev. 516 commit, no changes)
old1 = """> - **Status:** dokumen PRD **REVISI** — rev 517: PRD fresh verification & stability confirmation (24 Oct 2026 WIB); HEAD `3b3751b972c70052b930f91011e1b01f84771ff7` (Rev. 516 commit); 0 / 0 (0 commits ahead origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 516 (data terkonsisten)."""

new1 = """> - **Status:** dokumen PRD **REVISI** — rev 518: PRD fresh verification & stability confirmation (24 Oct 2026 WIB); HEAD `d36eb62911dc50d7d2e452ac1d37a801024dd3b6` (Rev. 517 commit); 0 / 0 (0 commits ahead origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 517 (data terkonsisten)."""

if old1 in content:
    content = content.replace(old1, new1)
    print("Fix 1: Replaced stale Status: rev 517 entry with Rev. 518 status.")
else:
    print("Fix 1: Stale Status: rev 517 entry NOT FOUND.")

# Fix 2: Remove duplicate "Verifikasi fresh kondisi" line (line 468)
# The first occurrence is at line 450, the second is at line 468
# We keep the first and remove the second
dup_pattern = """> - **Status:** dokumen PRD **REVISI** — rev 518: PRD fresh verification & stability confirmation (24 Oct 2026 WIB); HEAD `d36eb62911dc50d7d2e452ac1d37a801024dd3b6` (Rev. 517 commit); 0 / 0 (0 commits ahead origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 517 (data terkonsisten).
> **Verifikasi fresh kondisi repository + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 516 (data terkonsisten).**"""

# Wait, the second block is:
# > - **Status:** dokemen PRD **REVISI** — rev 517: ... (stale, at line 479)
# > **Verifikasi fresh kondisi repository + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 516 (data terkonsisten).** (line 468)

# Actually, looking at the output:
# Line 467: > - **Status:** dokumen PRD **REVISI** — rev 517: ... HEAD `3b3751b...` (Rev. 516 commit); 0 / 0 (0 commits ahead origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 516 (data terkonsisten).
# Line 468: > **Verifikasi fresh kondisi repository + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 516 (data terkonsisten).**
# Line 469: > - **Commit count:** 0 / 0 ... origin/main: d36eb629... (Rev. 517, in sync).

# So the duplicate is the "Verifikasi fresh kondisi" line at 468, followed by "Commit count" at 469.
# But line 467 is the stale "Status: rev 517" entry.

# Fix 2: Remove duplicate "Verifikasi fresh kondisi" line (line 468)
old2 = """> - **Status:** dokumen PRD **REVISI** — rev 518: PRD fresh verification & stability confirmation (24 Oct 2026 WIB); HEAD `d36eb62911dc50d7d2e452ac1d37a801024dd3b6` (Rev. 517 commit); 0 / 0 (0 commits ahead origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 517 (data terkonsisten).
> **Verifikasi fresh kondisi repository + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 516 (data terkonsisten).**"""

new2 = """> - **Status:** dokumen PRD **REVISI** — rev 518: PRD fresh verification & stability confirmation (24 Oct 2026 WIB); HEAD `d36eb62911dc50d7d2e452ac1d37a801024dd3b6` (Rev. 517 commit); 0 / 0 (0 commits ahead origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 517 (data terkonsisten).**"""

# Wait, that's not right. Let me re-read the output more carefully.

# The output shows:
# Line 449: > **Verifikasi fresh dilakukan:** ...
# Line 450: > **Verifikasi fresh kondisi repository + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 516 (data terkonsisten).**
# Line 451: > - **Commit count:** 0 / 0 (0 commits ahead origin_main). Local branch **0 commits ahead / 0 behind** origin_main. **origin/main:** `d36eb62911dc50d7d2e452ac1d37a801024dd3b6` (Rev. 517, in sync).
# ...
# Line 467: > - **Status:** dokumen PRD **REVISI** — rev 517: ... HEAD `3b3751b972c70052b930f91011e1b01f84771ff7` (Rev. 516 commit); 0 / 0 (0 commits ahead origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 516 (data terkonsisten).
# Line 468: > **Verifikasi fresh kondisi repository + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 516 (data terkonsisten).**
# Line 469: > - **Commit count:** 0 / 0 (0 commits ahead origin_main). Local branch **0 commits ahead / 0 behind** origin_main. **origin/main:** `d36eb62911dc50d7d2e452ac1d37a801024dd3b6` (Rev. 517, in sync).

# So the duplicate is:
# > - **Status:** dokumen PRD **REVISI** — rev 518: ... (line 467, but with stale content)
# > **Verifikasi fresh kondisi repository + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 516 (data terkconsisten).** (line 468)

# The fix should:
# 1. Replace the stale "Status: rev 517" entry with the correct "Status: rev 518" entry
# 2. Remove the duplicate "Verifikasi fresh kondisi" line

# Actually, looking at the output more carefully, the structure is:
# > **Verifikasi fresh dilakukan:** ... (line 449)
# > **Verifikasi fresh kondisi repository + dev.db:** ... (line 450)
# > - **Commit count:** 0 / 0 ... (line 451)
# > - **Working tree:** ... (line 452)
# > - **Database (dev.db):** ... (line 453)
# > - **Build quality gate:** ... (line 454)
# > - **Source files:** ... (line 455)
# > - **M02a (NFC):** ... (line 456)
# > - **Auth hardcode:** ... (line 457)
# > - **Beranda hardcode:** ... (line 458)
# > - **Prisma schema:** ... (line 459)
# > - **Status:** dokumen PRD **REVISI** — rev 517: ... (line 460) - STALE
# > - **Status:** dokumen PRD **REVISI** — rev 518: ... (line 461) - This is the correct one
# > **Verifikasi fresh kondisi repository + dev.db:** ... (line 462)
# > - **Commit count:** 0 / 0 ... (line 463)
# > - **Working tree:** ... (line 464)
# > - **Database (dev.db):** ... (line 465)
# > - **Build quality gate:** ... (line 466)
# > - **Source files:** ... (line 467)
# > - **M02a (NFC):** ... (line 468)
# > - **Auth hardcode:** ... (line 469)
# > - **Beranda hardcode:** ... (line 470)
# > - **Prisma schema:** ... (line 471)
# > - **Status:** dokumen PRD **REVISI** — rev 517: ... (line 472) - STALE
# > - **Status:** dokumen PRD **REVISI** — rev 518: ... (line 473)
# > - **Commit count:** 0 / 0 ... (line 474) - This is the second description
# > - **Working tree:** ... (line 475)
# > - **Database (dev.db):** ... (line 476)
# > - **Build quality gate:** ... (line 477)
# > - **Source files:** ... (line 478)
# > - **M02a (NFC):** ... (line 479)
# > - **Auth hardcode:** ... (line 480)
# > - **Beranda hardcode:** ... (line 481)
# > - **Prisma schema:** ... (line 482)
# > - **Status:** dokumen PRD **REVISI** — rev 517: ... (line 483) - STALE
# > - **Status:** dokumen PRD **REVISI** — rev 518: ... (line 484)

# Wait, this doesn't match what I see in the output. Let me re-read the output more carefully.

# From the output:
# Line 447: ## 12. REVISI TERBARU (Rev. 468–518 — 24 Oktober 2026 WIB)
# Line 448: (blank)
# Line 449: > **Verifikasi fresh dilakukan:** 24 Oktober 2026 (WIB, cron run) — query `sqlite3` ke `dev.db`, `npx tsc --noEmit`, `npx eslint .`, `npx next build`.
# Line 450: > **Verifikasi fresh kondisi repository + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 516 (data terkonsisten).**
# Line 451: > - **Commit count:** 0 / 0 (0 commits ahead origin_main). Local branch **0 commits ahead / 0 behind** origin_main. **origin/main:** `d36eb62911dc50d7d2e452ac1d37a801024dd3b6` (Rev. 517, in sync).
# Line 452: > - **Working tree:** `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 518 (final)); HEAD `d36eb62911dc50d7d2e452ac1d37a801024dd3b6` (Rev. 517 commit); seluruh file lain cocak dengan HEAD; untracked: 63 skrip utility (tidak terpantau dalam git). `git ls-files` = 187 file.
# Line 453: > - **Database (dev.db):** ...
# Line 454: > - **Build quality gate:** ...
# Line 455: > - **Source files:** ...
# Line 456: > - **M02a (NFC):** ...
# Line 457: > - **Auth hardcode:** ...
# Line 458: > - **Beranda hardcode:** ...
# Line 459: > - **Prisma schema:** ...
# Line 460: > - **Status:** dokumen PRD **REVISI** — rev 517: PRD fresh verification & stability confirmation (24 Oct 2026 WIB); HEAD `3b3751b972c70052b930f91011e1b01f84771ff7` (Rev. 516 commit); 0 / 0 (0 commits ahead origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 516 (data terkonsisten).
# Line 461: > **Verifikasi fresh kondisi repository + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 516 (data terkonsisten).**
# Line 462: > - **Commit count:** 0 / 0 (0 commits ahead origin_main). Local branch **0 commits ahead / 0 behind** origin_main. **origin/main:** `d36eb62911dc50d7d2e452ac1d37a801024dd3b6` (Rev. 517, in sync).
# Line 463: > - **Working tree:** `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 518 (final)); HEAD `d36eb62911dc50d7d2e452ac1d37a801024dd3b6` (Rev. 517 commit); seluruh file lain cocak dengan HEAD; untracked: 63 skrip utility (tidak terpantau dalam git). `git ls-files` = 187 file.
# Line 464: > - **Database (dev.db):** ...
# Line 465: > - **Build quality gate:** ...
# Line 466: > - **Source files:** ...
# Line 467: > - **M02a (NFC):** ...
# Line 468: > - **Auth hardcode:** ...
# Line 469: > - **Beranda hardcode:** ...
# Line 470: > - **Prisma schema:** ...
# Line 471: > - **Status:** dokumen PRD **REVISI** — rev 517: PRD fresh verification & stability confirmation (24 Oct 2026 WIB); HEAD `3b3751b972c70052b930f91011e1b01f84771ff7` (Rev. 516 commit); 0 / 0 (0 commits ahead origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 516 (data terkonsisten).
# Line 472: > - **Status:** dokumen PRD **REVISI** — rev 518: PRD fresh verification & stability confirmation (24 Oct 2026 WIB); HEAD `d36eb62911dc50d7d2e452ac1d37a801024dd3b6` (Rev. 517 commit); 0 / 0 (0 commits ahead origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 517 (data terkonsisten).
# Line 473: (blank)
# Line 474: ||- **Rev. 517 (final).** ...
# Line 475: ||- **Rev. 518 (final).** ...

# So the structure is:
# 1. "Verifikasi fresh dilakukan" (line 449)
# 2. "Verifikasi fresh kondisi" (line 450)
# 3. Commit count, Working tree, Database, Build quality gate, Source files, M02a, Auth hardcode, Beranda hardcode, Prisma schema, Status: rev 517, Status: rev 518 (lines 451-461)
# 4. "Verifikasi fresh kondisi" (line 462) - DUPLICATE
# 5. Commit count, Working tree, Database, Build quality gate, Source files, M02a, Auth hardcode, Beranda hardcode, Prisma schema, Status: rev 517, Status: rev 518 (lines 463-472)
# 6. Blank (line 473)
# 7. Individual entries (lines 474-475)

# The duplicate "Verifikasi fresh kondisi" at line 462 is a problem.
# Also, the "Status: rev 517" entries at lines 460 and 471 are STALE
# (should reference Rev. 517 commit with no changes, not Rev. 516 commit).
# And the "Status: rev 518" entries at lines 461 and 472 are correct.

# The fix should:
# 1. Remove the second "Verifikasi fresh kondisi" line (line 462)
# 2. Fix the stale "Status: rev 517" entries (lines 460 and 471) to be "Status: rev 518"
# 3. Add the missing "Rev. 518" entry to §11 (already done)

print("Starting fix...")

# Fix 1: Remove duplicate "Verifikasi fresh kondisi" line
# Pattern to match: "> - **Status:** dokumen PRD **REVISI** — rev 518: ... Rev. 517 ... \n> **Verifikasi fresh kondisi repository + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 516 (data terkonsisten).**"

old_dup = """> - **Status:** dokumen PRD **REVISI** — rev 518: PRD fresh verification & stability confirmation (24 Oct 2026 WIB); HEAD `d36eb62911dc50d7d2e452ac1d37a801024dd3b6` (Rev. 517 commit); 0 / 0 (0 commits ahead origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 517 (data terkonsisten).
> **Verifikasi fresh kondisi repository + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 516 (data terkonsisten).**"""

new_no_dup = """> - **Status:** dokumen PRD **REVISI** — rev 518: PRD fresh verification & stability confirmation (24 Oct 2026 WIB); HEAD `d36eb62911dc50d7d2e452ac1d37a801024dd3b6` (Rev. 517 commit); 0 / 0 (0 commits ahead origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 517 (data terkonsisten)."""

# Wait, the issue is that the second "Status: rev 518" entry is at line 472, and the "Verifikasi fresh kondisi" line is at line 462.
# Let me just remove the "Verifikasi fresh kondisi" line at line 462.

# Actually, let me look at the exact text around line 462.
# The text at line 461 is "> - **Status:** dokumen PRD **REVISI** — rev 518: ..."
# The text at line 462 is "> **Verifikasi fresh kondisi repository + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 516 (data terkonsisten).**"

# Let me match this pattern and remove the "Verifikasi fresh kondisi" line.
# The pattern is: "> - **Status:** dokumen PRD **REVISI** — rev 518: ... (line 461)\n> **Verifikasi fresh kondisi repository + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 516 (data terkonsisten).**\n> - **Commit count:** 0 / 0 (0 commits ahead origin_main). Local branch **0 commits ahead / 0 behind** origin_main. **origin/main:** `d36eb62911dc50d7d2e452ac1d37a801024dd3b6` (Rev. 517, in sync).\n> - **Working tree:** `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 518 (final)); HEAD `d36eb62911dc50d7d2e452ac1d37a801024dd3b6` (Rev. 517 commit); seluruh file lain cocak dengan HEAD; untracked: 63 skrip utility (tidak terpantau dalam git). `git ls-files` = 187 file."

# Wait, this is getting too complicated. Let me just use the patch tool to remove the duplicate.

# Actually, let me try a different approach. Let me just read the exact lines and make the fix.
print("Fix 2: Removing duplicate Verifikasi fresh kondisi line...")

# The duplicate line is:
# > **Verifikasi fresh kondisi repository + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 516 (data terkonsisten).**
# This appears at line 450 and line 462.
# We keep the first occurrence and remove the second.

# Find all occurrences of "Verifikasi fresh kondisi repository + dev.db"
import re
matches = list(re.finditer(r'> \*\*Verifikasi fresh kondisi repository \+ dev\.db.*?\./', content, re.DOTALL))
print(f"Found {len(matches)} occurrences of 'Verifikasi fresh kondisi'")

# Remove the second occurrence
if len(matches) >= 2:
    match2 = matches[1]
    # Find the start and end of this line
    start = match2.start()
    # Find the end of the line
    end = content.find('\n', start)
    end += 1  # Include the newline
    content = content[:start] + content[end:]
    print("Removed duplicate Verifikasi fresh kondisi line.")
else:
    print("No duplicate found.")

# Fix 3: Update stale "Status: rev 517" entries
# Line 460: "> - **Status:** dokumen PRD **REVISI** — rev 517: PRD fresh verification & stability confirmation (24 Oct 2026 WIB); HEAD `3b3751b972c70052b930f91011e1b01f84771ff7` (Rev. 516 commit); 0 / 0 (0 commits ahead origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 516 (data terkonsisten)."
# Should be changed to: "> - **Status:** dokumen PRD **REVISI** — rev 518: PRD fresh verification & stability confirmation (24 Oct 2026 WIB); HEAD `d36eb62911dc50d7d2e452ac1d37a801024dd3b6` (Rev. 517 commit); 0 / 0 (0 commits ahead origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 517 (data terkonsisten)."

# Find and replace the stale Status: rev 517 entries
stale_pattern = r'> - \*\*Status:\*\* dokumen PRD \*\*REVISI\*\* — rev 517: PRD fresh verification & stability confirmation \(24 Oct 2026 WIB\); HEAD `3b3751b972c70052b930f91011e1b01f84771ff7` \(Rev\. 516 commit\); 0 / 0 \(0 commits ahead origin_main\)\. State stabil, tidak ada perubahan signifikan dari Rev\. 516 \(data terkonsisten\)\.'

def replace_stale_status(match):
    return """> - **Status:** dokumen PRD **REVISI** — rev 518: PRD fresh verification & stability confirmation (24 Oct 2026 WIB); HEAD `d36eb62911dc50d7d2e452ac1d37a801024dd3b6` (Rev. 517 commit); 0 / 0 (0 commits ahead origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 517 (data terkonsisten)."""

# Count occurrences before replacement
stale_count = len(list(re.finditer(stale_pattern, content)))
print(f"Found {stale_count} stale Status: rev 517 entries.")
if stale_count > 0:
    content = re.sub(stale_pattern, replace_stale_status, content)
    print("Fixed stale Status: rev 517 entries.")

with open(path, 'w') as f:
    f.write(content)

print("File updated successfully.")
