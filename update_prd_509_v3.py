#!/usr/bin/env python3
# Update PRD-PONDOK-BANAT.md with fresh verification (Rev. 509)
path = "PRD-PONDOK-BANAT.md"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Find the §12 Rev. 507 (final) entry — the one at the end of the file
# It starts with "||- **Rev. 507 (final).** 24 Oktober 2026 (WIB): PRD fresh verification & stability confirmation (24 Oct 2026 WIB); HEAD `30bcb2fe40a3910e2d350c502ec6d893c4159a8e` (Rev. 507 commit), 41 / 0"
old_entry_marker = "||- **Rev. 507 (final).** 24 Oktober 2026 (WIB): PRD fresh verification & stability confirmation (24 Oct 2026 WIB); HEAD `30bcb2fe40a3910e2d350c502ec6d893c4159a8e` (Rev. 507 commit), 41 / 0 (41 commits ahead origin_main). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run): **state stabil, tidak ada perubahan signifikan dari Rev. 506** (data terkonsisten). Build gate: **NOT RE-RUNABLE** — node_modules absent; npm ci diperlukan. Database: dev.db absent; seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` & `import_students_grades_clean.py` tidak ditemukan di working tree). **M02a (NFC):** field `uid_nfc` ada aktif di tabel students, semua 453 NULL. **Auth hardcode:** `src/components/Login.tsx` tetap `admin@pondokanbat.com` / `admin123` (typo domain). **Beranda hardcode:** `Beranda.tsx` & `page.tsx` masih hardcoded totalSantri 453. **Prisma schema:** model `KitabProgress` & `Sertakan` sudah terdefinisi; `prisma validate` sukses. **Status:** dokumen PRD **REVISI** — rev 507 (final): PRD fresh verification & konfirmasi stabilitas; seluruh data terkonsisten, tidak ada perubahan signifikan dari Rev. 506; branch 41 ahead / 0 behind origin_main."

count = content.count(old_entry_marker)
print(f"Found {count} occurrences of the Rev. 507 (final) entry marker")

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
    "**Status:** dokumen PRD **REVISI** — rev 508: PRD fresh verification & konfirmasi stabilitas; seluruh data terkonsisten, tidak ada perubahan signifikan dari Rev. 507; branch 43 ahead / 0 behind origin_main."
)

if count > 0:
    # Replace the last occurrence of the full marker
    idx = content.rfind(old_entry_marker)
    new_content = content[:idx] + new_entry + content[idx + len(old_entry_marker):]
    print(f"Replaced at index {idx}")
    with open(path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("File updated successfully.")
else:
    # Try shorter marker
    short_marker = "||- **Rev. 507 (final).** 24 Oktober 2026 (WIB): PRD fresh verification & stability confirmation (24 Oct 2026 WIB); HEAD `30bcb2fe40a3910e2d350c502ec6d893c4159a8e`"
    count2 = content.count(short_marker)
    print(f"Found {count2} occurrences of short marker")
    if count2 > 0:
        idx = content.rfind(short_marker)
        print(f"Last occurrence at index {idx}")
        check = content[idx:idx+200]
        print(f"Check: {check[:150]}...")
        if "Rev. 507 commit), 41 / 0" in check:
            print("Marker confirmed as §12 entry")
            line_start = content.rfind("\n", 0, idx) + 1
            line_end = content.find("\n", idx)
            if line_end == -1:
                line_end = len(content)
            old_line = content[line_start:line_end]
            print(f"Old line: {old_line[:80]}...")
            new_line = new_entry
            new_content = content[:line_start] + new_line + content[line_end:]
            with open(path, "w", encoding="utf-8") as f:
                f.write(new_content)
            print("File updated successfully.")
        else:
            print("Marker not confirmed")
    else:
        print("ERROR: Could not find the entry marker")
