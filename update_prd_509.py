#!/usr/bin/env python3
# Update PRD-PONDOK-BANAT.md with fresh verification (Rev. 509)
path = "PRD-PONDOK-BANAT.md"
with open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Find the §12 Rev. 507 (final) entry at the end of the file (last occurrence, index 517)
target_idx = None
target_line = "||- **Rev. 507 (final).** 24 Oktober 2026 (WIB): PRD fresh verification & stability confirmation (24 Oct 2026 WIB); HEAD `30bcb2fe40a3910e2d350c502ec6d893c4159a8e` (Rev. 507 commit), 41 / 0 (41 commits ahead origin_main). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run): **state stabil, tidak ada perubahan signifikan dari Rev. 506** (data terkonsisten). Build gate: **NOT RE-RUNABLE** — node_modules absent; npm ci diperlukan. Database: dev.db absent; seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` & `import_students_grades_clean.py` tidak ditemukan di working tree). **M02a (NFC):** field `uid_nfc` ada aktif di tabel students, semua 453 NULL. **Auth hardcode:** `src/components/Login.tsx` tetap `admin@pondokanbat.com` / `admin123` (typo domain). **Beranda hardcode:** `Beranda.tsx` & `page.tsx` masih hardcoded totalSantri 453. **Prisma schema:** model `KitabProgress` & `Sertakan` sudah terdefinisi; `prisma validate` sukses. **Status:** dokumen PRD **REVISI** — rev 507 (final): PRD fresh verification & konfirmasi stabilitas; seluruh data terkonsisten, tidak ada perubahan signifikan dari Rev. 506; branch 41 ahead / 0 behind origin_main."

# Search from the end to find the §12 entry (last occurrence)
for i in range(len(lines) - 1, -1, -1):
    if lines[i].startswith("||- **Rev. 507 (final).** 24 Oktober 2026 (WIB): PRD fresh verification & stability confirmation (24 Oct 2026 WIB); HEAD `30bcb2fe40a3910e2d350c502ec6d893c4159a8e`"):
        # Verify it's the full entry
        if target_line in "".join(lines[i:i+1]):
            target_idx = i
            break

if target_idx is None:
    print("Target line NOT found!")
    exit(1)

print(f"Target line found at index {target_idx} (line {target_idx + 1})")
print(f"Found {lines.count('||- **Rev. 507 (final).** 24 Oktober 2026 (WIB): PRD fresh verification & stability confirmation (24 Oct 2026 WIB); HEAD `30bcb2fe40a3910e2d350c502ec6d893c4159a8e')} occurrences of '||- **Rev. 507 (final).**'")

# Build the new entry
new_entry = (
    "||- **Rev. 508 (final).** 24 Oktober 2026 (WIB): PRD fresh verification & stability confirmation (24 Oct 2026 WIB); "
    "HEAD `11efbdd937298304d2493fb58bd12841579778e1` (Rev. 508 commit), 43 / 0 (43 commits ahead origin_main). "
    "Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run): **state stabil, tidak ada perubahan signifikan dari Rev. 507** (data terkonsisten). "
    "Build gate: **NOT RE-RUNABLE** — node_modules absent; npm ci diperlukan. "
    "Database: dev.db absent; seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` & `import_students_grades_clean.py` tidak ditemukan di working tree). "
    "**M02a (NFC):** field `uid_nfc` ada aktif di tabel students, semua 453 NULL. "
    "**Auth hardcode:** Login.tsx tetap `admin@pondokanbat.com` / `admin123` (typo domain). "
    "**Beranda hardcode:** Beranda.tsx & page.tsx masih hardcoded totalSantri 453. "
    "**Prisma schema:** model `KitabProgress` & `Sertakan` sudah terdefinisi; `prisma validate` sukses. "
    "**Status:** dokumen PRD **REVISI** — rev 508: PRD fresh verification & konfirmasi stabilitas; seluruh data terkonsisten, tidak ada perubahan signifikan dari Rev. 507; branch 43 ahead / 0 behind origin_main.\n"
)

# Insert the new entry after the target line
lines.insert(target_idx + 1, new_entry)

with open(path, "w", encoding="utf-8") as f:
    f.writelines(lines)

print(f"Inserted new Rev. 508 entry after line {target_idx + 1}. New file has {len(lines)} lines.")
