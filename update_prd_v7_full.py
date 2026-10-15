#!/usr/bin/env python3
"""
Comprehensive Rev 7 update for PRD-PONDOK-BANAT.md.
Fixes: missing M03/M04 rows, updates all module statuses, DB block, footer (already done).
"""
import os

base = "/opt/data/home/workspace/dev/pondok-banat"
prd = os.path.join(base, "PRD-PONDOK-BANAT.md")

with open(prd, encoding="utf-8") as f:
    txt = f.read()

# ---------------------------------------------------------------------------
# 1. Fix M03 row (was missing in v6 script)
# ---------------------------------------------------------------------------
# Find the M02a row to know where M03 should be
old_m02a = "| M02a | Integrasi NFC (UID) | 🔜 Direncanakan | Spec lengkap (utk §2.2); field `uid_nfc` belum di-seed; mapping UID → NISN belum diuji; rumus parse: baris MANUFACTURER diapit `[]` → `AF:C2:99:E7` | > **Catatan:** data UID kartu siswa belum tersedia sebagai file terpisah; tersimpan manual dari ekspor NFC Tools |"

# M03 row that should come after M02a
new_m03 = """| M03 | Master Data Guru & Staf | 📋 Implementasi (statis) | Schema Prisma lengkap (Teacher, Staff, Position) + dashboard `/guru` (statis, hardcoded 5 guru); data dari DB belum di-bind | > **Catatan:** 5 guru di `dev.db` (4 Wali Kelas + 1 Guru, semua active); sumber 60 baris (53 utama + 7 ganti/badal, 59 unik). Import batch dari Excel belum diimplementasikan |"""

# Insert M03 after M02a
if old_m02a in txt:
    txt = txt.replace(old_m02a, old_m02a + "\n" + new_m03)
    print("M03 row inserted after M02a")
else:
    print("M02a row not found - checking alternatives")
    # Try to find M02a differently
    idx = txt.find("M02a | Integrasi NFC")
    if idx >= 0:
        print("Found M02a at", idx)
        print(repr(txt[idx:idx+300]))

# ---------------------------------------------------------------------------
# 2. Fix M04 row (was missing in v6 script)
# ---------------------------------------------------------------------------
old_m05 = "| M05 | Akademik & Absensi | 🔜 Direncanakan | Schema Prisma lengkap (Grade, Absensi, Rapor) tetapi **belum di-seed** data nilai; dashboard `/nilai` ada (statis, contoh nilai manual) |"
new_m04 = """| M04 | Kurikulum & Kitab Kuning | 📋 Implementasi (statis) | Schema Prisma lengkap (Subject, Silabus, RPP + KitabProgress) + dashboard `/kelas` (statis, hardcoded 4 pelajaran: AG, BINDO, MAT, IPS); data dari DB belum di-bind | > **Catatan:** `subjects`, `silabus`, `rpp` masing-masing **0 record**; 17 mapel + 74 dokumen (65 RPP + 9 SILABUS) masih di Excel/PDF saja |"""

if old_m05 in txt:
    txt = txt.replace(old_m05, new_m04)
    print("M04 row inserted (replaced M05)")
else:
    print("M05 row not found")
    # Show what's near line 306
    idx = txt.find("M05 | Akademik")
    if idx >= 0:
        print(repr(txt[idx:idx+300]))

# ---------------------------------------------------------------------------
# 3. Fix M01 row (no trailing space before |)
# ---------------------------------------------------------------------------
old_m01 = "| M01 | Admin & User Management | ✅ Implementasi | `prisma/schema.prisma` (model User, Role, RolePermission) + `src/app/login/page.tsx`; 1 user admin seed otomatis via `init_db.py`; authorization masih hardcode di React|"
new_m01 = "| M01 | Admin & User Management | ✅ Implementasi | `prisma/schema.prisma` (model User, Role, RolePermission) + `src/app/login/page.tsx`; 1 user admin seed otomatis via `init_db.py`; authorization masih hardcode di React | > **Catatan:** tabel `role_permissions` didefinisikan tapi **0 record** — perizinan modul belum di-enforce di API; authorization masih hardcode (login admin@pondokanat.com/admin123) |"
if old_m01 in txt:
    txt = txt.replace(old_m01, new_m01)
    print("M01 row fixed")
else:
    print("M01 row pattern not found - checking")
    idx = txt.find("M01 | Admin")
    if idx >= 0:
        print(repr(txt[idx:idx+250]))

# ---------------------------------------------------------------------------
# 4. Fix M02 row (add note about inactive students)
# ---------------------------------------------------------------------------
old_m02 = "| M02 | Master Data Santri | ✅ Implementasi | `students` + `classes` di SQLite (10 siswa, 13 kelas); `src/app/santri/page.tsx`, `/kelas` tampil |"
new_m02 = "| M02 | Master Data Santri | ✅ Implementasi | `students` + `classes` di SQLite (10 siswa, 13 kelas); `src/app/santri/page.tsx`, `/kelas` tampil | > **Catatan:** 10 siswa semua status `inactive` (belum aktif); 13 kelas: Takhosous + 1A–6B (6 jenjang) |"
if old_m02 in txt:
    txt = txt.replace(old_m02, new_m02)
    print("M02 row fixed")
else:
    print("M02 row not found")

# ---------------------------------------------------------------------------
# 5. Update §9.2 DB block
# ---------------------------------------------------------------------------
old_db = """- **Database:** SQLite `dev.db` di-seed oleh `init_db.py` (schema SQL: `init_schema.sql`). Total 15 tabel: users, roles, role_permissions, students, classes, teachers, subjects, silabus, rpp, absensi, grades, rapor, announcements, messages, notifications.
  - Saat ini: 1 user, 5 role, 10 siswa, 13 kelas, 5 guru. Hanya tabel users/roles/students/classes/teachers yang terisi; semua tabel akademik, kurikulum, komunikasi = 0 record.
  - Data seed santri: 10 siswa (semua status `inactive`), 13 kelas (1A–6B + Takhosous). Data seed guru: 5 (4 Wali Kelas + 1 Guru), semua `active`."""
new_db = """- **Database:** SQLite `dev.db` di-seed oleh `init_db.py` (schema SQL: `init_schema.sql`). Total 15 tabel: users, roles, role_permissions, students, classes, teachers, subjects, silabus, rpp, absensi, grades, rapor, announcements, messages, notifications.
  - Saat ini: 1 user, 5 role, 10 siswa (`inactive`), 13 kelas (Takhosous + 1A–6B), 5 guru (semua Wali Kelas), 0 record di tabel kurikulum/akademik/komunikasi. Hanya tabel `users`, `roles`, `role_permissions`, `students`, `classes`, `teachers` yang terisi.
  - Data seed santri: 10 siswa (semua status `inactive`), 13 kelas (1A–6B + Takhosous). Data seed guru: 5 (semua Wali Kelas, semua `active`). Data seed admin: 1 (admin@pondokanat.com), role `admin`.
  - **IMPORTANT:** tabel `role_permissions` didefinisikan tapi **0 record** — perizinan modul belum di-enforce di API layer."""
if old_db in txt:
    txt = txt.replace(old_db, new_db)
    print("DB block updated")
else:
    print("DB block not found")
    idx = txt.find("**Saat ini:**")
    if idx >= 0:
        print(repr(txt[idx:idx+300]))

# ---------------------------------------------------------------------------
# 6. Write the updated PRD
# ---------------------------------------------------------------------------
with open(prd, "w", encoding="utf-8") as f:
    f.write(txt)

print()
print("=== PRD updated to Rev 7 ===")
print("Total lines:", txt.count(chr(10)) + 1)
print("Size:", len(txt), "bytes")
