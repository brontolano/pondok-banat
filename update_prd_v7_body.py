#!/usr/bin/env python3
"""
Update PRD-PONDOK-BANAT.md body (not footer) to Rev 7.
Footer already updated to Rev 7 in update_footer_v7.py.
"""
import os

base = "/opt/data/home/workspace/dev/pondok-banat"
prd = os.path.join(base, "PRD-PONDOK-BANAT.md")

with open(prd, encoding="utf-8") as f:
    txt = f.read()

# ---------------------------------------------------------------------------
# 2. Update §9.1 status table rows
# ---------------------------------------------------------------------------
# M01: unchanged but add note about empty role_permissions
old_m01 = "| M01 | Admin & User Management | ✅ Implementasi | `prisma/schema.prisma` (model User, Role, RolePermission) + `src/app/login/page.tsx`; 1 user admin seed otomatis via `init_db.py`; authorization masih hardcode di React|"
new_m01 = "| M01 | Admin & User Management | ✅ Implementasi | `prisma/schema.prisma` (model User, Role, RolePermission) + `src/app/login/page.tsx`; 1 user admin seed otomatis via `init_db.py`; authorization masih hardcode di React | > **Catatan:** tabel `role_permissions` didefinisikan tapi **0 record** — perizinan modul belum di-enforce di API; authorization masih hardcode (login admin@pondokanat.com/admin123) |"
assert old_m01 in txt, "M01 row not found"
txt = txt.replace(old_m01, new_m01)

# M02: unchanged
old_m02 = "| M02 | Master Data Santri | ✅ Implementasi | `students` + `classes` di SQLite (10 siswa, 13 kelas); `src/app/santri/page.tsx`, `/kelas` tampil |"
new_m02 = "| M02 | Master Data Santri | ✅ Implementasi | `students` + `classes` di SQLite (10 siswa, 13 kelas); `src/app/santri/page.tsx`, `/kelas` tampil | > **Catatan:** 10 siswa semua status `inactive` (belum aktif); 13 kelas: Takhosous + 1A–6B (6 jenjang) |"
assert old_m02 in txt, "M02 row not found"
txt = txt.replace(old_m02, new_m02)

# M02a: unchanged
old_m02a = "| M02a | Integrasi NFC (UID) | 🔜 Direncanakan | Spec lengkap (utk §2.2); field `uid_nfc` belum di-seed; mapping UID → NISN belum diuji; rumus parse: baris MANUFACTURER diapit `[]` → `AF:C2:99:E7` |"
new_m02a = "| M02a | Integrasi NFC (UID) | 🔜 Direncanakan | Spec lengkap (utk §2.2); field `uid_nfc` belum di-seed; mapping UID → NISN belum diuji; rumus parse: baris MANUFACTURER diapit `[]` → `AF:C2:99:E7` | > **Catatan:** data UID kartu siswa belum tersedia sebagai file terpisah; tersimpan manual dari ekspor NFC Tools |"
assert old_m02a in txt, "M02a row not found"
txt = txt.replace(old_m02a, new_m02a)

# M03: status → 📋 Implementasi (schema + seed + static dashboard)
old_m03 = "| M03 | Master Data Guru & Staf | 🔜 Direncanakan | Schema Prisma lengkap (Teacher, Staff, Position) tetapi **belum di-seed** data riil (5 guru di DB vs 60 di sumber); dashboard `/guru` ada (statis) |"
new_m03 = "| M03 | Master Data Guru & Staf | 📋 Implementasi (statis) | Schema Prisma lengkap (Teacher, Staff, Position) + dashboard `/guru` (statis, hardcoded 5 guru); data dari DB belum di-bind | > **Catatan:** 5 guru di `dev.db` (4 Wali Kelas + 1 Guru, semua active); sumber 60 baris (53 utama + 7 ganti/badal, 59 unik). Import batch dari Excel belum diimplementasikan |"
assert old_m03 in txt, "M03 row not found"
txt = txt.replace(old_m03, new_m03)

# M04: status → 📋 Implementasi (schema + static dashboard)
old_m04 = "| M04 | Kurikulum & Kitab Kuning | 🔜 Direncanakan | Schema Prisma lengkap (Subject, Silabus, RPP + KitabProgress) tetapi **belum di-seed** data mapel/silabus/rpp dari PDF/xlsx; dashboard `/kelas` ada (statis) |"
new_m04 = "| M04 | Kurikulum & Kitab Kuning | 📋 Implementasi (statis) | Schema Prisma lengkap (Subject, Silabus, RPP + KitabProgress) + dashboard `/kelas` (statis, hardcoded 4 pelajaran: AG, BINDO, MAT, IPS); data dari DB belum di-bind | > **Catatan:** `subjects`, `silabus`, `rpp` masing-masing **0 record**; 17 mapel + 74 dokumen (65 RPP + 9 SILABUS) masih di Excel/PDF saja |"
assert old_m04 in txt, "M04 row not found"
txt = txt.replace(old_m04, new_m04)

# M05: status → 📋 Implementasi (schema + static dashboard)
old_m05 = "| M05 | Akademik & Absensi | 🔜 Direncanakan | Schema Prisma lengkap (Grade, Absensi, Rapor) tetapi **belum di-seed** data nilai; dashboard `/nilai` ada (statis, contoh nilai manual) |"
new_m05 = "| M05 | Akademik & Absensi | 📋 Implementasi (statis) | Schema Prisma lengkap (Grade, Absensi, Rapor) + dashboard `/nilai` (statis, contoh nilai manual); data dari DB belum di-bind | > **Catatan:** tabel `grades`, `absensi`, `rapor` masing-masing **0 record**; 15 sheet nilai masih di Excel saja (TK, TA A, TB, 1A–6B) |"
assert old_m05 in txt, "M05 row not found"
txt = txt.replace(old_m05, new_m05)

# M06: unchanged
old_m06 = "| M06 | Hifz/Quran Memorization | ❌ Tidak aktif (MVP) | Tidak ada schema/seed/release; tertunda di roadmap iterasi 2 |"
new_m06 = "| M06 | Hifz/Quran Memorization | ❌ Tidak aktif (MVP) | Tidak ada schema/seed/release; tertunda di roadmap iterasi 2 |"
assert old_m06 in txt, "M06 row not found"
txt = txt.replace(old_m06, new_m06)

# M07: status → 📋 Implementasi (static UI)
old_m07 = "| M07 | Kesiswaan & Tunggangan | 🔜 Direncanakan | Schema Prisma tidak ada; `src/app/ruang-kegiatan/page.tsx` ada tapi konten statis (ruangan, kegiatan) |"
new_m07 = "| M07 | Kesiswaan & Tunggangan | 📋 Implementasi (statis) | `src/app/ruang-kegiatan/page.tsx` ada tapi konten statis (6 ruang: asrama, musala, perpustakaan, aula, surga, masjid); schema Prisma belum dilengkapi |"
assert old_m07 in txt, "M07 row not found"
txt = txt.replace(old_m07, new_m07)

# M08: status → 📋 Implementasi (schema + static dashboard)
old_m08 = "| M08 | Komunikasi & Notifikasi | 🔜 Direncanakan | Schema Prisma (Announcement, Message, Notification) tetapi **belum di-seed**; dashboard `/berita` ada (statis) |"
new_m08 = "| M08 | Komunikasi & Notifikasi | 📋 Implementasi (statis) | Schema Prisma (Announcement, Message, Notification) + dashboard `/berita` (statis); data dari DB belum di-bind | > **Catatan:** tabel `announcements`, `messages`, `notifications` masing-masing **0 record** |"
assert old_m08 in txt, "M08 row not found"
txt = txt.replace(old_m08, new_m08)

# M09: status → 📋 Implementasi (static UI)
old_m09 = "| M09 | Laporan & Analytics | 🔜 Direncanakan | UI `/laporan/page.tsx` punya tombol ekspor, **generative PDF belum ada** |"
new_m09 = "| M09 | Laporan & Analytics | 📋 Implementasi (statis) | UI `/laporan/page.tsx` punya tombol ekspor, **generative PDF belum ada**; data laporan statis |"
assert old_m09 in txt, "M09 row not found"
txt = txt.replace(old_m09, new_m09)

# M10: unchanged
old_m10 = "| M10 | Payment/Keuangan | ❌ Tidak aktif (MVP) | Tertunda roadmap iterasi 3 |"
new_m10 = "| M10 | Payment/Keuangan | ❌ Tidak aktif (MVP) | Tertunda roadmap iterasi 3 |"
assert old_m10 in txt, "M10 row not found"
txt = txt.replace(old_m10, new_m10)

# M11: unchanged
old_m11 = "| M11 | Mobile & Offline | ❌ Tidak aktif (MVP) | Gatsby mobile — tidak termasuk MVP; tertunda |"
new_m11 = "| M11 | Mobile & Offline | ❌ Tidak aktif (MVP) | Gatsby mobile — tidak termasuk MVP; tertunda |"
assert old_m11 in txt, "M11 row not found"
txt = txt.replace(old_m11, new_m11)

# ---------------------------------------------------------------------------
# 3. Update §9.2 Build & Database block
# ---------------------------------------------------------------------------
old_db = """- **Database:** SQLite `dev.db` di-seed oleh `init_db.py` (schema SQL: `init_schema.sql`). Total 15 tabel: users, roles, role_permissions, students, classes, teachers, subjects, silabus, rpp, absensi, grades, rapor, announcements, messages, notifications.
  - Saat ini: 1 user, 5 role, 10 siswa (semua `inactive`), 13 kelas (Takhosous + 1A–6B), 5 guru (4 Wali Kelas + 1 Guru), 0 record di tabel kurikulum/akademik/komunikasi. Hanya tabel `users`, `roles`, `role_permissions`, `students`, `classes`, `teachers` yang terisi.
  - Data seed santri: 10 siswa (semua status `inactive`), 13 kelas (1A–6B + Takhosous). Data seed guru: 5 (4 Wali Kelas + 1 Guru), semua `active`. Data seed admin: 1 (admin@pondokanat.com), role `admin`.
  - **IMPORTANT:** tabel `role_permissions` didefinisikan tapi **0 record** — perizinan modul belum di-enforce di API layer.
- **Prisma:** schema `prisma/schema.prisma` (SQLite) mendefinisikan model M01–M05 + M08; driver client `prisma-client-js` (anggotakan `prisma` ^8.0.0-rc.22). Catatan: model `KitabProgress` hanya direferensikan di `Subject` (`KitabProgress[]`) tetapi **tidak didefinisikan** di schema; perlu ditambahkan jika fitur progress kitab akan dibangun.
- **UI:** `src/app/*` berisi halaman berbasis route; komponen kecil `Beranda`, `Login`. Halaman lain (santri, kelas, guru, nilai, ruang-kegiatan, berita, laporan, pengasuh, sekolah) semuanya statis (placeholder UI)."""
new_db = """- **Database:** SQLite `dev.db` di-seed oleh `init_db.py` (schema SQL: `init_schema.sql`). Total 15 tabel: users, roles, role_permissions, students, classes, teachers, subjects, silabus, rpp, absensi, grades, rapor, announcements, messages, notifications.
  - Saat ini: 1 user, 5 role, 10 siswa (`inactive`), 13 kelas (Takhosous + 1A–6B), 5 guru (semua Wali Kelas), 0 record di tabel kurikulum/akademik/komunikasi. Hanya tabel `users`, `roles`, `role_permissions`, `students`, `classes`, `teachers` yang terisi.
  - Data seed santri: 10 siswa (semua status `inactive`), 13 kelas (1A–6B + Takhosous). Data seed guru: 5 (semua Wali Kelas, semua `active`). Data seed admin: 1 (admin@pondokanat.com), role `admin`.
  - **IMPORTANT:** tabel `role_permissions` didefinisikan tapi **0 record** — perizinan modul belum di-enforce di API layer.
- **Prisma:** schema `prisma/schema.prisma` (SQLite) mendefinisikan model M01–M05 + M08; driver client `prisma-client-js` (anggotakan `prisma` ^8.0.0-rc.22). Catatan: model `KitabProgress` hanya direferensikan di `Subject` (`KitabProgress[]`) tetapi **tidak didefinisikan** di schema; perlu ditambahkan jika fitur progress kitab akan dibangun.
- **UI:** `src/app/*` berisi halaman berbasis route; komponen kecil `Beranda`, `Login`. Halaman lain (santri, kelas, guru, nilai, ruang-kegiatan, berita, laporan, pengasuh, sekolah) semuanya statis (placeholder UI). **Data statis** di halaman-halaman ini (mis. `Beranda` totalSantri=42, totalGuru=27) **tidak** diambil dari DB (DB: 10 siswa, 5 guru, 13 kelas)."""
assert old_db in txt, "DB block not found"
txt = txt.replace(old_db, new_db)

# ---------------------------------------------------------------------------
# 4. Update §10.1 audit data source block (small corrections)
# ---------------------------------------------------------------------------
old_guru = """- **Guru/Staf:** `DATA PARA PENGAJAR BANAT.xlsx` punya beberapa sheet:
  - `TAHUN 2026-2027`: 56 data baris
  - `Table 1`: 53 baris utama (52 unik + 1 header \"NAMA PENGAJAR\") + 7 baris ganti/badal = 60 baris, 59 nama unik
  - Angka \"58 guru/staff (51 utama + 7 ganti/badal)\" adalah hasil interpretasi tim; catat bahwa sheet mentah tidak membagi 'utama' vs 'ganti/badal' secara eksplisit. Untuk produksi, disarankan membaca `TAHUN 2026-2027` sebagai master utama, dan `Table 1` sebagai daftar ganti/badal."""
new_guru = """- **Guru/Staf:** `DATA PARA PENGAJAR BANAT.xlsx` punya beberapa sheet:
  - `TAHUN 2026-2027`: 56 data baris
  - `Table 1`: 53 baris utama (52 unik + 1 header \"NAMA PENGAJAR\") + 7 baris ganti/badal = 60 baris, 59 nama unik
  - Angka \"58 guru/staff (51 utama + 7 ganti/badal)\" adalah hasil interpretasi tim; catat bahwa sheet mentah tidak membagi 'utama' vs 'ganti/badal' secara eksplisit. Untuk produksi, disarankan membaca `TAHUN 2026-2027` sebagai master utama, dan `Table 1` sebagai daftar ganti/badal."""
assert old_guru in txt, "Guru audit block not found"
txt = txt.replace(old_guru, new_guru)

# ---------------------------------------------------------------------------
# 5. Write the updated PRD
# ---------------------------------------------------------------------------
with open(prd, "w", encoding="utf-8") as f:
    f.write(txt)

print("=== PRD body updated to Rev 7 ===")
print("Total lines:", txt.count(chr(10)) + 1)
print("Size:", len(txt), "bytes")
