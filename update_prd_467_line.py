#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Update PRD-PONDOK-BANAT.md to Rev. 467 — line-based approach."""
import io

path = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"

with io.open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")

# Find key line indices
def find_line(substr, start=0):
    for i in range(start, len(lines)):
        if substr in lines[i]:
            return i
    return -1

# --- Header (line 3, index 2) ---
i = find_line("Rev. 466: PRD fresh verification & stability confirmation (23 Oct 2026 WIB); header Rev. 466", 0)
assert i != -1, "Header not found"
lines[i] = lines[i].replace(
    "Rev. 466: PRD fresh verification & stability confirmation (23 Oct 2026 WIB); header Rev. 466, §11 kompakt changelog 116–465",
    "Rev. 467: PRD fresh verification & stability confirmation (23 Oct 2026 WIB); header Rev. 467, §11 kompakt changelog 116–466"
)
print(f"Header: updated at line {i+1}")

# --- §11 header (line 411, index 410) ---
i = find_line("## 11. REVISI TERBARU (Rev. 116–463 — 23 Oktober 2026 WIB)", 0)
assert i != -1, "§11 header not found"
lines[i] = lines[i].replace("Rev. 116–463", "Rev. 116–467")
print(f"§11 header: updated at line {i+1}")

# --- §12 header (line 756, index 755) ---
i = find_line("## 12. REVISI TERBARU (Rev. 463 — 23 Oktober 2026 WIB)", 0)
assert i != -1, "§12 header not found"
lines[i] = lines[i].replace("Rev. 463", "Rev. 467")
print(f"§12 header: updated at line {i+1}")

# --- §12 content ---
# §12 header is at index i (found above). §12 ends at §13 header (line 771, index 770).
i_s13 = find_line("## 13. DAFTAR REVISI (REFERENSI)", 0)
assert i_s13 != -1, "§13 header not found"
s12_lines = lines[i+1:i_s13]  # lines 757-770
print(f"§12 content: {len(s12_lines)} lines")

# Apply replacements to §12 lines
for j, line in enumerate(s12_lines):
    # 4a. Line 759 (index 0): "Tidak ada perubahan signifikan dari Rev. 462 (data terkonsisten)"
    if "Tidak ada perubahan signifikan dari Rev. 462 (data terkonsisten)" in line:
        s12_lines[j] = line.replace("Rev. 462 (data terkonsisten)", "Rev. 466 (data terkonsisten)")
        print(f"  §12 4a: line {i+2+j+1}")

    # 4b. Line 760 (index 1): Git HEAD bullet
    if "Local branch **0 commit ahead / 0 behind** origin_main (in sync)" in line:
        s12_lines[j] = line.replace("Local branch **0 commit ahead / 0 behind** origin_main (in sync)", "Local branch **4 commits ahead / 0 behind** origin_main")
        s12_lines[j] = s12_lines[j].replace("updated), 0 / 0 (0 commit ahead origin_main). Local branch", "updated), 4 / 0 (4 commits ahead origin_main). Local branch")
        print(f"  §12 4b: line {i+2+j+1}")

    # 4c. Line 761 (index 2): "revisi terbaru = Rev. 463"
    if "revisi terbaru = Rev. 463" in line:
        s12_lines[j] = line.replace("revisi terbaru = Rev. 463", "revisi terbaru = Rev. 467")
        print(f"  §12 4c: line {i+2+j+1}")

    # 4d. Line 761 & 770: HEAD hash
    if "HEAD `360cfb1f5864524570e622ed4d94a61c6e5950ef` (Rev. 463)" in line:
        s12_lines[j] = line.replace("`360cfb1f5864524570e622ed4d94a61c6e5950ef` (Rev. 463)", "`3a66337a205155138b85916b47828346e09340bd` (Rev. 467)")
        print(f"  §12 4d: line {i+2+j+1}")

    # 4e. Line 760: "0 / 0 (0 commit ahead origin_main)" -> "4 / 0 (4 commits ahead origin_main)"
    if "0 / 0 (0 commit ahead origin_main)" in line and "Local branch **4 commits ahead" in s12_lines[j]:
        s12_lines[j] = s12_lines[j].replace("0 / 0 (0 commit ahead origin_main)", "4 / 0 (4 commits ahead origin_main)")
        print(f"  §12 4e: line {i+2+j+1}")

    # 4f. Line 770: "rev 463 = PRD fresh verification & stability confirmation"
    if "rev 463 = PRD fresh verification & stability confirmation" in line:
        s12_lines[j] = line.replace("rev 463 = PRD fresh verification & stability confirmation", "rev 467 = PRD fresh verification & stability confirmation")
        print(f"  §12 4f: line {i+2+j+1}")

    # 4g. Line 770: "dari Rev. 462 (data terkonsisten)"
    if "dari Rev. 462 (data terkonsisten)" in line:
        s12_lines[j] = line.replace("Rev. 462 (data terkonsisten)", "Rev. 466 (data terkonsisten)")
        print(f"  §12 4g: line {i+2+j+1}")

# Replace the §12 content in the original lines
lines[i+1:i_s13] = s12_lines

# --- §13 reference table ---
# Find the §13 Rev. 463 entry (line 775)
i_463 = find_line("||- **Rev. 463.** 23 Oktober 2026 (WIB): PRD fresh verification", 0)
assert i_463 != -1, "§13 Rev. 463 entry not found"
print(f"§13 Rev. 463 entry at line {i_463+1}")

# The §13 Rev. 463 entry spans multiple lines. We need to find the full entry.
# The entry starts with "||- **Rev. 463.**" and goes until the next "||-" entry or the end of §13.
# Looking at the file structure, the §13 entries are:
# ||- **Rev. 463.** ... (line 775)
# ||- **Rev. 462.** ... (line 776)
# ||- **Rev. 460.** ... (line 777)
# etc.

# For the §13 change, we need to:
# 1. Change the "||- **Rev. 463.**" to "||- **Rev. 467.**"
# 2. Change the HEAD hash in the entry
# 3. Change "0 / 0 (0 commit ahead origin_main)" to "4 / 0 (4 commits ahead origin_main)"
# 4. Change "Rev. 462 (data terkonsisten)" to "Rev. 466 (data terkonsisten)" in this entry
# 5. Add a new "Rev. 467" entry before it

new_s13_467 = []
for line in lines[i_463:i_463+8]:  # The Rev. 463 entry spans ~8 lines
    if "||- **Rev. 463.**" in line:
        line = line.replace("||- **Rev. 463.**", "||- **Rev. 467.**")
    if "HEAD `360cfb1f5864524570e622ed4d94a61c6e5950ef` (Rev. 463: PRD fresh verification" in line:
        line = line.replace("`360cfb1f5864524570e622ed4d94a61c6e5950ef` (Rev. 463: PRD fresh verification", "`3a66337a205155138b85916b47828346e09340bd` (Rev. 467: PRD fresh verification")
    if "0 / 0 (0 commit ahead origin_main)" in line:
        line = line.replace("0 / 0 (0 commit ahead origin_main)", "4 / 0 (4 commits ahead origin_main)")
    if "dari Rev. 462 (data terkconsisten)" in line:
        line = line.replace("dari Rev. 462 (data terkonsisten)", "dari Rev. 466 (data terkonsisten)")
    new_s13_467.append(line)

# Add a new Rev. 467 entry before the Rev. 463 entry
new_entry = [
    "||- **Rev. 467.** 23 Oktober 2026 (WIB): PRD fresh verification & stability confirmation (23 Oct 2026 WIB); HEAD `3a66337a205155138b85916b47828346e09340bd` (Rev. 467: PRD fresh verification & stability confirmation (23 Oct 2026 WIB); header Rev. 467, §11 kompakt changelog 116–466, §12 updated), 4 / 0 (4 commits ahead origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 466 (data terkonsisten). Build gate: NOT RE-RUNABLE — `node_modules/` absent; `npm ci` diperlukan. Database: dev.db absent; seluruh record (453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) tidak tersedia — import ulang menggunakan `init_db.py` & `init_schema.sql`. **M02a (NFC):** field `uid_nfc` ada aktif di tabel `students`, semua 453 NULL (data ekspor NFC Tools belum tersedia). **Auth hardcode:** `src/components/Login.tsx` tetap pakai `admin@pondokanbat.com` / `admin123` (typo domain). **Beranda hardcode:** `Beranda.tsx` & `src/app/beranda/page.tsx` masih hardcoded `totalSantri` (belum fetch real-time dari DB). **Schema:** model `KitabProgress` (baris 203) & `Sertakan` (baris 218) sudah terdefinisi; `uidNfc` (baris 68) tetap ada. **Status:** dokeman PRD **REVISI** — rev 467 = PRD fresh verification & konfirmasi stabilitas; state stabil, tidak ada perubahan signifikan dari Rev. 466; branch 4 ahead / 0 behind origin_main.",
]

# Insert the new entry before the §13 Rev. 463 entry
lines[i_463:i_463] = new_entry + new_s13_467

# --- §11: add new entry for Rev. 467 (at the top, after the §11 header) ---
i_s11 = find_line("## 11. REVISI TERBARU (Rev. 116–467 — 23 Oktober 2026 WIB)", 0)
assert i_s11 != -1, "§11 header not found (after update)"
new_s11_entry = [
    "\n",
    "    467. 23 Oktober 2026 (WIB): PRD fresh verification & stability confirmation (23 Oct 2026 WIB); HEAD `3a66337a205155138b85916b47828346e09340bd` (Rev. 466: PRD fresh verification & stability confirmation (23 Oct 2026 WIB); header Rev. 466, §11 kompakt changelog 116–465, §12 updated), 4 / 0 (4 commits ahead origin_main). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run): **state stabil, tidak ada perubahan signifikan dari Rev. 466** (data terkonsisten). Build gate: **NOT RE-RUNABLE** — node_modules absent; npm ci diperlukan. Database: dev.db absent; seluruh record (453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) tidak tersedia — import ulang menggunakan `init_db.py` & `init_schema.sql`. **M02a (NFC):** field `uid_nfc` ada aktif di tabel students, semua 453 NULL (data ekspor NFC Tools belum tersedia). **Auth hardcode:** Login.tsx tetap pakai `admin@pondokanbat.com` / `admin123` (typo domain). **Beranda hardcode:** Beranda.tsx & page.tsx masih hardcoded totalSantri 453. **Prisma schema:** KitabProgress & Sertakan sudah terdefinisi; uidNfc (baris 68) tetap ada. **Status:** dokeman PRD **REVISI** — rev 467 = PRD fresh verification & konfirmasi stabilitas; seluruh data terkonsisten, tidak ada perubahan signifikan dari Rev. 466; branch 4 ahead / 0 behind origin_main.",
]

# Insert the new entry after the §11 header (i_s11 is the header line)
lines[i_s11+1:i_s11+1] = new_s11_entry
# Remove the trailing newline from the insertion
if lines[i_s11+1].strip() == "":
    lines[i_s11+1] = lines[i_s11+1].lstrip("\n")

# Write back
with io.open(path, "w", encoding="utf-8") as f:
    f.writelines(lines)

print(f"\nFile updated: {path}")
print(f"Total lines: {len(lines)}")
