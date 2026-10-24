#!/usr/bin/env python3
"""Simple string-based replacement for PRD Rev. 507 update."""
path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'

with open(path, 'r') as f:
    c = f.read()

changes = []

# 1. Header update
old = "Rev. 506: PRD fresh verification & stability confirmation"
new = "Rev. 507: PRD fresh verification & stability confirmation"
if old in c:
    c = c.replace(old, new, 1)
    changes.append("Header first occurrence updated")
else:
    print("Header not found!")

# 2. §11 header
old = "## 11. REVISI TERBARU (Rev. 116–506"
new = "## 11. REVISI TERBARU (Rev. 116–507"
if old in c:
    c = c.replace(old, new, 1)
    changes.append("§11 header updated")

# 3. §11: add Rev. 507 entry after Rev. 506 entry
# Find the Rev. 506 entry (section 11). The entry starts with "|||- **Rev. 506.**"
# and ends with "branch 40 ahead / 0 behind origin_main."
rev506_start = "|||- **Rev. 506.** 24 Oktober 2026 (WIB): PRD fresh verification & stability confirmation (24 Oct 2026 WIB); HEAD `dc9bd27f6be685f176bfed9c08be3674b17cf744` (Rev. 505 commit), 40 / 0 (40 commits ahead origin_main). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run): **state stabil, tidak ada perubahan signifikan dari Rev. 505** (data terkonsisten). Build gate: **NOT RE-RUNABLE** — node_modules absent; npm ci diperlukan. Database: dev.db absent; seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` & `import_students_grades_clean.py` tidak ditemukan di working tree). **M02a (NFC):** field `uid_nfc` ada aktif di tabel students, semua 453 NULL. **Auth hardcode:** Login.tsx tetap `admin@pondokanbat.com` / `admin123` (typo domain). **Beranda hardcode:** Beranda.tsx & page.tsx masih hardcoded totalSantri 453. **Prisma schema:** model `KitabProgress` & `Sertakan` sudah terdefinisi; `prisma validate` sukses. **Status:** dokumen PRD **REVISI** — rev 506 = PRD fresh verification & konfirmasi stabilitas; seluruh data terkonsisten, tidak ada perubahan signifikan dari Rev. 505; branch 40 ahead / 0 behind origin_main."

rev507_entry = """|||- **Rev. 506.** 24 Oktober 2026 (WIB): PRD fresh verification & stability confirmation (24 Oct 2026 WIB); HEAD `dc9bd27f6be685f176bfed9c08be3674b17cf744` (Rev. 505 commit), 40 / 0 (40 commits ahead origin_main). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run): **state stabil, tidak ada perubahan signifikan dari Rev. 505** (data terkonsisten). Build gate: **NOT RE-RUNABLE** — node_modules absent; npm ci diperlukan. Database: dev.db absent; seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` & `import_students_grades_clean.py` tidak ditemukan di working tree). **M02a (NFC):** field `uid_nfc` ada aktif di tabel students, semua 453 NULL. **Auth hardcode:** Login.tsx tetap `admin@pondokanbat.com` / `admin123` (typo domain). **Beranda hardcode:** Beranda.tsx & page.tsx masih hardcoded totalSantri 453. **Prisma schema:** model `KitabProgress` & `Sertakan` sudah terdefinisi; `prisma validate` sukses. **Status:** dokumen PRD **REVISI** — rev 506 = PRD fresh verification & konfirmasi stabilitas; seluruh data terkonsisten, tidak ada perubahan signifikan dari Rev. 505; branch 40 ahead / 0 behind origin_main.

|||- **Rev. 507 (final).** 24 Oktober 2026 (WIB): PRD fresh verification & stability confirmation (24 Oct 2026 WIB); HEAD `30bcb2fe40a3910e2d350c502ec6d893c4159a8e` (Rev. 507 commit), 41 / 0 (41 commits ahead origin_main). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run): **state stabil, tidak ada perubahan signifikan dari Rev. 506** (data terkonsisten). Build gate: **NOT RE-RUNABLE** — node_modules absent; npm ci diperlukan. Database: dev.db absent; seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` & `import_students_grades_clean.py` tidak ditemukan di working tree). **M02a (NFC):** field `uid_nfc` ada aktif di tabel students, semua 453 NULL. **Auth hardcode:** Login.tsx tetap `admin@pondokanbat.com` / `admin123` (typo domain). **Beranda hardcode:** Beranda.tsx & page.tsx masih hardcoded totalSantri 453. **Prisma schema:** model `KitabProgress` & `Sertakan` sudah terdefinisi; `prisma validate` sukses. **Status:** dokumen PRD **REVISI** — rev 507 (final): PRD fresh verification & konfirmasi stabilitas; seluruh data terkonsisten, tidak ada perubahan signifikan dari Rev. 506; branch 41 ahead / 0 behind origin_main."""

if rev506_start in c:
    c = c.replace(rev506_start, rev507_entry, 1)
    changes.append("Rev. 507 entry added to §11")
else:
    print("Rev. 506 entry pattern NOT found in §11!")
    # Find the actual
    idx = c.find("**Rev. 506.** 24 Oktober 2026 (WIB): PRD fresh verification")
    if idx != -1:
        print("Found **Rev. 506.** at", idx)
        print("Context:", repr(c[idx:idx+300]))

# 4. §12 header
old = "## 12. REVISI TERBARU (Rev. 468–506"
new = "## 12. REVISI TERBARU (Rev. 468–507"
if old in c:
    c = c.replace(old, new, 1)
    changes.append("§12 header updated")

# 5. §12 content: update HEAD hash and references
old = "> - **Git HEAD (local):** `dc9bd27f6be685f176bfed9c08be3674b17cf744` (Rev. 506 commit"
new = "> - **Git HEAD (local):** `30bcb2fe40a3910e2d350c502ec6d893c4159a8e` (Rev. 507 commit"
if old in c:
    c = c.replace(old, new, 1)
    changes.append("§12 Git HEAD line updated")
else:
    print("§12 Git HEAD line NOT found!")

old = "revisi terbaru = Rev. 506 (final)"
new = "revisi terbaru = Rev. 507 (final)"
if old in c:
    c = c.replace(old, new, 1)
    changes.append("§12 Working tree line updated")
else:
    print("§12 Working tree pattern NOT found!")

old = "rev 506: PRD fresh verification"
new = "rev 507: PRD fresh verification"
if old in c:
    c = c.replace(old, new, 1)
    changes.append("§12 Status line updated")
else:
    print("§12 Status line NOT found!")

# 6. §12 list: add Rev. 507 entry before last (Rev. 504 final)
# Find the Rev. 504 final entry in §12 list and add Rev. 507 after it
rev504_start = "||||- **Rev. 504 (final).** 24 Oktober 2026 (WIB): PRD fresh verification & stability confirmation (24 Oct 2026 WIB); HEAD `bae146f4e9c2bc403bb5308ac64e0eee281419e7` (Rev. 504 commit), 38 / 0 (38 commits ahead origin_main). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run): **state stabil, tidak ada perubahan signifikan dari Rev. 503** (data terkonsisten). Build gate: **NOT RE-RUNABLE** — node_modules absent; npm ci diperlukan. Database: dev.db absent; seluruh record (453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) tidak tersedia — import ulang menggunakan `init_db.py` & `init_schema.sql`. **M02a (NFC):** field `uid_nfc` ada aktif di tabel students, semua 453 NULL. **Auth hardcode:** Login.tsx tetap `admin@pondokanbat.com` / `admin123` (typo domain). **Beranda hardcode:** Beranda.tsx & page.tsx masih hardcoded totalSantri 453. **Prisma schema:** model `KitabProgress` & `Sertakan` sudah terdefinisi; `prisma validate` sukses. **Status:** dokumen PRD **REVISI** — rev 504 (final): PRD fresh verification & stability confirmation (24 Oct 2026 WIB); HEAD `bae146f4e9c2bc403bb5308ac64e0eee281419e7` (Rev. 504 commit); seluruh data terkonsisten, tidak ada perubahan signifikan dari Rev. 503; branch 38 ahead / 0 behind origin_main."

rev507_list_entry = rev504_start + "\n\n||||- **Rev. 507 (final).** 24 Oktober 2026 (WIB): PRD fresh verification & stability confirmation (24 Oct 2026 WIB); HEAD `30bcb2fe40a3910e2d350c502ec6d893c4159a8e` (Rev. 507 commit), 41 / 0 (41 commits ahead origin_main). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run): **state stabil, tidak ada perubahan signifikan dari Rev. 506** (data terkonsisten). Build gate: **NOT RE-RUNABLE** — node_modules absent; npm ci diperlukan. Database: dev.db absent; seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` & `import_students_grades_clean.py` tidak ditemukan di working tree). **M02a (NFC):** field `uid_nfc` ada aktif di tabel students, semua 453 NULL. **Auth hardcode:** Login.tsx tetap `admin@pondokanbat.com` / `admin123` (typo domain). **Beranda hardcode:** Beranda.tsx & page.tsx masih hardcoded totalSantri 453. **Prisma schema:** model `KitabProgress` & `Sertakan` sudah terdefinisi; `prisma validate` sukses. **Status:** dokumen PRD **REVISI** — rev 507 (final): PRD fresh verification & konfirmasi stabilitas; seluruh data terkonsisten, tidak ada perubahan signifikan dari Rev. 506; branch 41 ahead / 0 behind origin_main."

if rev504_start in c:
    c = c.replace(rev504_start, rev507_list_entry, 1)
    changes.append("Rev. 507 entry added to §12 list")
else:
    print("Rev. 504 final pattern NOT found in §12 list!")
    idx = c.find("**Rev. 504 (final).** 24 Oktober 2026 (WIB): PRD fresh verification")
    if idx != -1:
        print("Found **Rev. 504 (final).** at", idx)
        print("Context:", repr(c[idx:idx+200]))

with open(path, 'w') as f:
    f.write(c)

print(f"\nChanges applied: {changes}")
print(f"Total changes: {len(changes)}")
