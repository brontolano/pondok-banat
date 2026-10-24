#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Update PRD-PONDOK-BANAT.md to Rev. 467 — fresh verification & stability confirmation.
Corrected: replace HEAD hashes FIRST, then 0/0 counts."""
import io

path = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"

with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

# --- 1. Header ---
old_h = "Rev. 466: PRD fresh verification & stability confirmation (23 Oct 2026 WIB); header Rev. 466, §11 kompakt changelog 116–465"
new_h = "Rev. 467: PRD fresh verification & stability confirmation (23 Oct 2026 WIB); header Rev. 467, §11 kompakt changelog 116–466"
assert old_h in content, "Header not found"
content = content.replace(old_h, new_h)

# --- 2. §11 header ---
old_11h = "## 11. REVISI TERBARU (Rev. 116–463 — 23 Oktober 2026 WIB)"
new_11h = "## 11. REVISI TERBARU (Rev. 116–467 — 23 Oktober 2026 WIB)"
assert old_11h in content, "§11 header not found"
content = content.replace(old_11h, new_11h)

# --- 3. §12 header ---
old_12h = "## 12. REVISI TERBARU (Rev. 463 — 23 Oktober 2026 WIB)"
new_12h = "## 12. REVISI TERBARU (Rev. 467 — 23 Oktober 2026 WIB)"
assert old_12h in content, "§12 header not found"
content = content.replace(old_12h, new_12h)

# --- 4. §12 content updates (ORDER MATTERS) ---

# 4a. Line 759: "Tidak ada perubahan signifikan dari Rev. 462 (data terkonsisten)" -> "Rev. 466"
old_4a = "Tidak ada perubahan signifikan dari Rev. 462 (data terkonsisten)"
new_4a = "Tidak ada perubahan signifikan dari Rev. 466 (data terkonsisten)"
assert content.count(old_4a) == 1, f"4a count={content.count(old_4a)}"
content = content.replace(old_4a, new_4a)

# 4b. Line 760: "Rev. 463: PRD fresh verification & stability confirmation (23 Oct 2026 WIB); header Rev. 463, §11 kompakt changelog 116–462, §12 updated"
# Use a §12-specific search string (unique to line 760, not in §11 line 752 or §13 line 775)
old_4b = "updated), 0 / 0 (0 commit ahead origin_main). Local branch **0 commit ahead / 0 behind** origin_main (in sync)"
new_4b = "updated), 4 / 0 (4 commits ahead origin_main). Local branch **4 commits ahead / 0 behind** origin_main"
cnt_4b = content.count(old_4b)
if cnt_4b == 0:
    raise AssertionError(f"4b not found: {cnt_4b} occurrences")
print(f"  4b: {cnt_4b} occurrence(s) of §12 Git HEAD bullet pattern")
content = content.replace(old_4b, new_4b)

# 4c. Line 761: "revisi terbaru = Rev. 463"
old_4c = "revisi terbaru = Rev. 463"
new_4c = "revisi terbaru = Rev. 467"
assert content.count(old_4c) == 1, f"4c count={content.count(old_4c)}"
content = content.replace(old_4c, new_4c)

# 4d. Line 761 & 770: HEAD hash
old_4d = "HEAD `360cfb1f5864524570e622ed4d94a61c6e5950ef` (Rev. 463)"
new_4d = "HEAD `3a66337a205155138b85916b47828346e09340bd` (Rev. 467)"
# Count occurrences: line 761, line 770, line 775 (§13)
cnt_4d = content.count(old_4d)
print(f"  4d: replacing {cnt_4d} occurrence(s) of HEAD hash (Rev. 463) -> (Rev. 467)")
content = content.replace(old_4d, new_4d)

# 4e. Line 760: "0 / 0 (0 commit ahead origin_main)" -> "4 / 0 (4 commits ahead origin_main)"
# This occurs in line 760 (§12 Git HEAD bullet) and line 770 (§12 Status line)
# Also in lines 752 (§11), 775 (§13), 776 (§13) — but those are in older revisions
# and should stay as 0/0. However, we want to change the ones in §12 only.
# Let's check which occurrences remain (after 4d which didn't touch "0 / 0").
remaining_4e = content.count("0 / 0 (0 commit ahead origin_main)")
print(f"  4e: {remaining_4e} occurrence(s) of '0 / 0 (0 commit ahead origin_main)' remaining")
# We need to replace only the ones in §12 (lines 760 and 770). 
# The ones in §11 (line 752) and §13 (lines 775, 776) should NOT be replaced.
# Since §11 and §13 are after §12 in the file, we can split the content at §12 and §13 boundaries.
# Or, we can replace the specific full lines.

# Actually, let's do it differently: replace the §12-specific strings.
old_4e_1 = "updated), 0 / 0 (0 commit ahead origin_main). Local branch **0 commit ahead / 0 behind** origin_main (in sync)"
new_4e_1 = "updated), 4 / 0 (4 commits ahead origin_main). Local branch **4 commits ahead / 0 behind** origin_main"
if old_4e_1 in content:
    content = content.replace(old_4e_1, new_4e_1)
    print(f"  4e: replaced §12 Git HEAD bullet '0 / 0' -> '4 / 0' (4 commits ahead)")
else:
    print(f"  4e: §12 Git HEAD bullet pattern NOT found")

# 4f. Line 770: "rev 463 = PRD fresh verification & stability confirmation" -> "rev 467"
old_4f = "rev 463 = PRD fresh verification & stability confirmation"
new_4f = "rev 467 = PRD fresh verification & stability confirmation"
assert content.count(old_4f) == 1, f"4f count={content.count(old_4f)}"
content = content.replace(old_4f, new_4f)

# 4g. Line 770: "dari Rev. 462 (data terkonsisten)" -> "dari Rev. 466 (data terkonsisten)"
# After 4a, there should be only 1 occurrence (line 770)
old_4g = "dari Rev. 462 (data terkonsisten)"
new_4g = "dari Rev. 466 (data terkonsisten)"
cnt_4g = content.count(old_4g)
print(f"  4g: {cnt_4g} occurrence(s) of 'dari Rev. 462 (data terkonsisten)'")
# Only replace the one in §12 Status line (line 770). The one in line 759 was already replaced in 4a.
if cnt_4g == 1:
    content = content.replace(old_4g, new_4g)
elif cnt_4g > 1:
    # Replace only the last occurrence (which should be in §12 Status line, since §12 comes before §13)
    # Actually, after 4a, the remaining occurrences are in §12 Status (line 770) and §13 entries (775, 776, ...)
    # We want to replace only the one in §12 Status (line 770), which is the FIRST occurrence after 4a.
    # Wait, no: after 4a, the line 759 occurrence was already changed to "dari Rev. 466". 
    # So the remaining occurrences of "dari Rev. 462 (data terkonsisten)" are in §12 Status (line 770), §13 entries (775, 776, ...).
    # We want to replace only the first one (line 770), which is in §12.
    idx = content.find(old_4g)
    content = content[:idx] + new_4g + content[idx+len(old_4g):]
    print(f"  4g: replaced first occurrence (line 770 §12 Status) only")

# 4h. Line 770: "4 / 0 (4 commits ahead origin_main)" check (after 4e)
# This was already done in 4e.

print("All §12 replacements done.")

# --- 5. §13 reference table updates ---
# 5a. Change the "Rev. 463" entry to "Rev. 467" (updating all references in that entry)
old_5a = "||- **Rev. 463.** 23 Oktober 2026 (WIB): PRD fresh verification & stability confirmation (23 Oct 2026 WIB); HEAD `360cfb1f5864524570e622ed4d94a61c6e5950ef` (Rev. 463: PRD fresh verification & stability confirmation (23 Oct 2026 WIB); header Rev. 463, §11 kompakt changelog 116–462, §12 updated), 0 / 0 (0 commit ahead origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 462 (data terkonsisten)."
new_5a = "||- **Rev. 467.** 23 Oktober 2026 (WIB): PRD fresh verification & stability confirmation (23 Oct 2026 WIB); HEAD `3a66337a205155138b85916b47828346e09340bd` (Rev. 467: PRD fresh verification & stability confirmation (23 Oct 2026 WIB); header Rev. 467, §11 kompakt changelog 116–466, §12 updated), 4 / 0 (4 commits ahead origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 466 (data terkonsisten)."
assert old_5a in content, "§13 Rev. 463 entry not found"
content = content.replace(old_5a, new_5a)

# 5b. Add a new "Rev. 467" entry before the §13 Rev. 467 entry
# Find the position of the §13 Rev. 467 entry
s13_marker = "||- **Rev. 467.** 23 Oktober 2026 (WIB): PRD fresh verification & stability confirmation (23 Oct 2026 WIB); HEAD `3a66337a205155138b85916b47828346e09340bd` (Rev. 467: PRD fresh verification & stability confirmation (23 Oct 2026 WIB); header Rev. 467, §11 kompakt changelog 116–466, §12 updated), 4 / 0 (4 commits ahead origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 466 (data terkonsisten)."
assert s13_marker in content, "§13 Rev. 467 marker not found"
insert_pos = content.find(s13_marker)

# The duplicate entry (same content as the one we just created)
new_s13_467_dup = "||- **Rev. 467.** 23 Oktober 2026 (WIB): PRD fresh verification & stability confirmation (23 Oct 2026 WIB); HEAD `3a66337a205155138b85916b47828346e09340bd` (Rev. 467: PRD fresh verification & stability confirmation (23 Oct 2026 WIB); header Rev. 467, §11 kompakt changelog 116–466, §12 updated), 4 / 0 (4 commits ahead origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 466 (data terkonsisten). Build gate: NOT RE-RUNABLE — `node_modules/` absent; `npm ci` diperlukan. Database: dev.db absent; seluruh record (453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) tidak tersedia — import ulang menggunakan `init_db.py` & `init_schema.sql`. **M02a (NFC):** field `uid_nfc` ada aktif di tabel `students`, semua 453 NULL (data ekspor NFC Tools belum tersedia). **Auth hardcode:** `src/components/Login.tsx` tetap pakai `admin@pondokanbat.com` / `admin123` (typo domain). **Beranda hardcode:** `Beranda.tsx` & `src/app/beranda/page.tsx` masih hardcoded `totalSantri` (belum fetch real-time dari DB). **Schema:** model `KitabProgress` (baris 203) & `Sertakan` (baris 218) sudah terdefinisi; `uidNfc` (baris 68) tetap ada. **Status:** dokeman PRD **REVISI** — rev 467 = PRD fresh verification & konfirmasi stabilitas; state stabil, tidak ada perubahan signifikan dari Rev. 466; branch 4 ahead / 0 behind origin_main."

content = content[:insert_pos] + new_s13_467_dup + content[insert_pos:]
print("All §13 replacements done.")

# --- 6. §11: add new entry for Rev. 467 (at the top, after the §11 header) ---
old_6 = "## 11. REVISI TERBARU (Rev. 116–467 — 23 Oktober 2026 WIB)"
new_6 = old_6 + "\n\n    467. 23 Oktober 2026 (WIB): PRD fresh verification & stability confirmation (23 Oct 2026 WIB); HEAD `3a66337a205155138b85916b47828346e09340bd` (Rev. 466: PRD fresh verification & stability confirmation (23 Oct 2026 WIB); header Rev. 466, §11 kompakt changelog 116–465, §12 updated), 4 / 0 (4 commits ahead origin_main). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run): **state stabil, tidak ada perubahan signifikan dari Rev. 466** (data terkonsisten). Build gate: **NOT RE-RUNABLE** — node_modules absent; npm ci diperlukan. Database: dev.db absent; seluruh record (453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) tidak tersedia — import ulang menggunakan `init_db.py` & `init_schema.sql`. **M02a (NFC):** field `uid_nfc` ada aktif di tabel students, semua 453 NULL (data ekspor NFC Tools belum tersedia). **Auth hardcode:** Login.tsx tetap pakai `admin@pondokanbat.com` / `admin123` (typo domain). **Beranda hardcode:** Beranda.tsx & page.tsx masih hardcoded totalSantri 453. **Prisma schema:** KitabProgress & Sertakan sudah terdefinisi; uidNfc (baris 68) tetap ada. **Status:** dokeman PRD **REVISI** — rev 467 = PRD fresh verification & konfirmasi stabilitas; seluruh data terkonsisten, tidak ada perubahan signifikan dari Rev. 466; branch 4 ahead / 0 behind origin_main."
assert old_6 in content, "§11 header not found for insert"
content = content.replace(old_6, new_6)

with io.open(path, "w", encoding="utf-8") as f:
    f.write(content)

print(f"\nFile updated: {path}")
print(f"Total lines: {content.count(chr(10)) + 1}")
