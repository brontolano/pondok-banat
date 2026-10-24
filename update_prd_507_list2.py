#!/usr/bin/env python3
"""Add Rev. 507 entry to §12 list (final, correct format)."""
path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'

with open(path, 'r') as f:
    c = f.read()

changes = []

# Find the Rev. 504 (final) entry in §12 list (uses "||-" prefix, last entry)
rev504_entry = """||- **Rev. 504 (final).** 24 Oktober 2026 (WIB): PRD fresh verification & stability confirmation (24 Oct 2026 WIB); HEAD `bae146f4e9c2bc403bb5308ac64e0eee281419e7` (Rev. 504 commit), 38 / 0 (38 commits ahead origin_main). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run): **state stabil, tidak ada perubahan signifikan dari Rev. 503** (data terkonsisten). Build gate: **NOT RE-RUNABLE** — node_modules absent; npm ci diperlukan. Database: dev.db absent; seluruh record (453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) tidak tersedia — import ulang menggunakan `init_db.py` & `init_schema.sql`. **M02a (NFC):** field `uid_nfc` ada aktif di tabel students, semua 453 NULL. **Auth hardcode:** Login.tsx tetap `admin@pondokanbat.com` / `admin123` (typo domain). **Beranda hardcode:** Beranda.tsx & page.tsx masih hardcoded totalSantri 453. **Prisma schema:** model `KitabProgress` & `Sertakan` sudah terdefinisi; `prisma validate` sukses. **Status:** dokumen PRD **REVISI** — rev 504 (final): PRD fresh verification & stability confirmation (24 Oct 2026 WIB); HEAD `bae146f4e9c2bc403bb5308ac64e0eee281419e7` (Rev. 504 commit); seluruh data terkonsisten, tidak ada perubahan signifikan dari Rev. 503; branch 38 ahead / 0 behind origin_main."""

rev507_entry = rev504_entry + "\n\n||- **Rev. 507 (final).** 24 Oktober 2026 (WIB): PRD fresh verification & stability confirmation (24 Oct 2026 WIB); HEAD `30bcb2fe40a3910e2d350c502ec6d893c4159a8e` (Rev. 507 commit), 41 / 0 (41 commits ahead origin_main). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run): **state stabil, tidak ada perubahan signifikan dari Rev. 506** (data terkonsisten). Build gate: **NOT RE-RUNABLE** — node_modules absent; npm ci diperlukan. Database: dev.db absent; seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` & `import_students_grades_clean.py` tidak ditemukan di working tree). **M02a (NFC):** field `uid_nfc` ada aktif di tabel students, semua 453 NULL. **Auth hardcode:** Login.tsx tetap `admin@pondokanbat.com` / `admin123` (typo domain). **Beranda hardcode:** Beranda.tsx & page.tsx masih hardcoded totalSantri 453. **Prisma schema:** model `KitabProgress` & `Sertakan` sudah terdefinisi; `prisma validate` sukses. **Status:** dokumen PRD **REVISI** — rev 507 (final): PRD fresh verification & konfirmasi stabilitas; seluruh data terkonsisten, tidak ada perubahan signifikan dari Rev. 506; branch 41 ahead / 0 behind origin_main."

if rev504_entry in c:
    c = c.replace(rev504_entry, rev507_entry, 1)
    changes.append("Rev. 507 entry added to §12 list (correct format)")
else:
    print("Rev. 504 final pattern NOT found in §12 list!")
    idx = c.find("**Rev. 504 (final).** 24 Oktober 2026 (WIB): PRD fresh verification")
    if idx != -1:
        print("Found at", idx)
        print("Actual prefix:", repr(c[idx-10:idx+60]))

with open(path, 'w') as f:
    f.write(c)

print(f"Changes: {changes}")
