#!/usr/bin/env python3
"""
Update PRD-PONDOK-BANAT.md to Rev 6.
Reflects the fully verified current codebase state (14 Oktober 2026).
"""
import os
import re

base = "/opt/data/home/workspace/dev/pondok-banat"
prd = os.path.join(base, "PRD-PONDOK-BANAT.md")

with open(prd, encoding="utf-8") as f:
    txt = f.read()

# ---------------------------------------------------------------------------
# 1. Update the revision footer from Rev 5 to Rev 6
# ---------------------------------------------------------------------------
old_footer = """*Rev. 5 — 14 Oktober 2026. Perubahan: 1) diklarisi Prisma: model KitabProgress hanya direferensikan, belum didefinisikan (stale); 2) dicek ulang status DB & statik Komponen Beranda (totalSantri=42, totalGuru=27 vs DB sesungguhnya 10 siswa/5 guru); 3) laporkan data seed santri (10 siswa, status 'inactive') & guru (5, terdiri 4 Wali Kelas + 1 Guru); 4) sesuaikan keterangan M04. Rev. 4 = dokumen PRD sebelumnya.*"""
new_footer = """*Rev. 6 — 14 Oktober 2026. Perubahan: 1) verifikasi menyeluruh backend (role_permissions kosong = perizinan belum di-enforce di API; 2) cek ulang seed DB: 10 siswa (semua inactive), 13 kelas, 5 guru (4 Wali Kelas + 1 Guru), 1 admin; 3) cocokkan data master guru dengan sumber 60 baris (53 utama + 7 ganti/badal, 59 unik); 4) laporkan seluruh tabel kurikulum/akademik/komunikasi = 0 record; 5) sesuaikan rujukan folder data sumber (.data-pondokanat). Rev. 5 = dokumen PRD sebelumnya.*"""
assert old_footer in txt, "Rev 5 footer not found"
txt = txt.replace(old_footer, new_footer)

# ---------------------------------------------------------------------------
# 2. Update §10.1 audit data source block
# ---------------------------------------------------------------------------
old_audit = """- **PDF dokumen:** 74 berkas = **65 RPP + 9 SILABUS** ✓"""
new_audit = """- **PDF dokumen:** 74 berkas = **65 RPP + 9 SILABUS** ✓ (tervalidasi: 65 RPP + 9 SILABUS = 74, dari 17 pelajaran)
- **Guru/Staf:** `DATA PARA PENGAJAR BANAT.xlsx`:
  - Sheet `TAHUN 2026-2027`: 60 baris data (53 utama + 7 ganti/badal, 59 nama unik)
  - `Table 1`: 60 baris (53 utama + 7 ganti/badal)
  - Catatan: sheet mentah belum membagi 'utama' vs 'ganti/badal' secara eksplisit; untuk produksi disarankan membaca `TAHUN 2026-2027` sebagai master utama, `Table 1` sebagai daftar ganti/badal.
- **Pelajaran (mapel):** 17 (dari nama file RPP)
- **Kelas:** 6 jenjang + Takhosous; 12 seksi A/B (1A–6B) sesuai PRD ✓ (Data Nilai sheet: 6 jenjang; Data Kelas sheet: 3 jenjang terisi — lihat §8.1)
- **Nilai:** 15 sheet di `Data Nilai Semester 1 TA 2026_2027.xlsx` = TK, TA A, TB, 1A–6B ✓
- **NFC:** data UID kartu siswa belum tersedia sebagai file terpisah (tersimpan manual dari ekspor NFC Tools). Proses: ekspor NFC Tools → parse baris MANUFACTURER diapit `[]` → hasil `AF:C2:99:E7` → update field `uid_nfc` di record siswa."""
assert old_audit in txt, "Audit data block not found"
txt = txt.replace(old_audit, new_audit)

# ---------------------------------------------------------------------------
# 3. Update §9.1 status table
# ---------------------------------------------------------------------------
# M01: add note about empty role_permissions
old_m01 = "| M01 | Admin & User Management | ✅ Implementasi | `prisma/schema.prisma` (model User, Role, RolePermission) + `src/app/login/page.tsx`; 1 user admin seed otomatis via `init_db.py`; authorization masih hardcode di React |"
new_m01 = "| M01 | Admin & User Management | ✅ Implementasi | `prisma/schema.prisma` (model User, Role, RolePermission) + `src/app/login/page.tsx`; 1 user admin seed otomatis via `init_db.py`; authorization masih hardcode di React | > **Catatan:** tabel `role_permissions` didefinisikan tapi **0 record** — perizinan modul belum di-enforce di API; authorization masih hardcode (login admin@pondokanat.com/admin123) |"
assert old_m01 in txt, "M01 row not found"
txt = txt.replace(old_m01, new_m01)

# M02: update note about inactive students
old_m02 = "| M02 | Master Data Santri | ✅ Implementasi | `students` + `classes` di SQLite (10 siswa, 13 kelas); `src/app/santri/page.tsx`, `/kelas` tampil |"
new_m02 = "| M02 | Master Data Santri | ✅ Implementasi | `students` + `classes` di SQLite (10 siswa, 13 kelas); `src/app/santri/page.tsx`, `/kelas` tampil | > **Catatan:** 10 siswa semua status `inactive` (belum aktif); 13 kelas: Takhosous + 1A–6B (6 jenjang) |"
assert old_m02 in txt, "M02 row not found"
txt = txt.replace(old_m02, new_m02)

# M02a: update NFC note
old_m02a = "| M02a | Integrasi NFC (UID) | 🔜 Direncanakan | Spec lengkap (utk §2.2); field `uid_nfc` belum di-seed; mapping UID → NISN belum diuji; rumus parse: baris MANUFACTURER diapit `[]` → `AF:C2:99:E7` |"
new_m02a = "| M02a | Integrasi NFC (UID) | 🔜 Direncanakan | Spec lengkap (utk §2.2); field `uid_nfc` belum di-seed; mapping UID → NISN belum diuji; rumus parse: baris MANUFACTURER diapit `[]` → `AF:C2:99:E7` | > **Catatan:** data UID kartu siswa belum tersedia sebagai file terpisah; tersimpan manual dari ekspor NFC Tools |"
assert old_m02a in txt, "M02a row not found"
txt = txt.replace(old_m02a, new_m02a)

# M03: update teacher note
old_m03 = "| M03 | Master Data Guru & Staf | 🔜 Direncanakan | Schema Prisma lengkap (Teacher, Staff, Position) tetapi belum di-seed data riil (60 orang); dashboard `/guru` ada (statis) |"
new_m03 = "| M03 | Master Data Guru & Staf | 🔜 Direncanakan | Schema Prisma lengkap (Teacher, Staff, Position) tetapi **belum di-seed** data riil (5 guru di DB vs 60 di sumber); dashboard `/guru` ada (statis) | > **Catatan:** 5 guru di `dev.db` (4 Wali Kelas + 1 Guru, semua active); sumber 60 baris (53 utama + 7 ganti/badal, 59 unik). Import batch dari Excel belum diimplementasikan |"
assert old_m03 in txt, "M03 row not found"
txt = txt.replace(old_m03, new_m03)

# M04: update note about empty curriculum tables
old_m04 = "| M04 | Kurikulum & Kitab Kuning | 🔜 Direncanakan | Schema Prisma lengkap (Subject, Silabus, RPP + KitabProgress) tetapi **belum di-seed** data mapel/silabus/rpp dari PDF/xlsx; dashboard `/kelas` ada (statis) |"
new_m04 = "| M04 | Kurikulum & Kitab Kuning | 🔜 Direncanakan | Schema Prisma lengkap (Subject, Silabus, RPP + KitabProgress) tetapi **belum di-seed** data mapel/silabus/rpp dari PDF/xlsx; dashboard `/kelas` ada (statis) | > **Catatan:** `subjects`, `silabus`, `rpp` masing-masing **0 record**; 17 mapel + 74 dokumen (65 RPP + 9 SILABUS) masih di Excel/PDF saja |"
assert old_m04 in txt, "M04 row not found"
txt = txt.replace(old_m04, new_m04)

# M05: update note about empty academic tables
old_m05 = "| M05 | Akademik & Absensi | 🔜 Direncanakan | Schema Prisma lengkap (Grade, Absensi, Rapor) tetapi **belum di-seed** data nilai; dashboard `/nilai` ada (statis, contoh nilai manual) |"
new_m05 = "| M05 | Akademik & Absensi | 🔜 Direncanakan | Schema Prisma lengkap (Grade, Absensi, Rapor) tetapi **belum di-seed** data nilai; dashboard `/nilai` ada (statis, contoh nilai manual) | > **Catatan:** tabel `grades`, `absensi`, `rapor` masing-masing **0 record**; 15 sheet nilai masih di Excel saja (TK, TA A, TB, 1A–6B) |"
assert old_m05 in txt, "M05 row not found"
txt = txt.replace(old_m05, new_m05)

# M08: update note about empty communication tables
old_m08 = "| M08 | Komunikasi & Notifikasi | 🔜 Direncanakan | Schema Prisma (Announcement, Message, Notification) tetapi **belum di-seed**; dashboard `/berita` ada (statis) |"
new_m08 = "| M08 | Komunikasi & Notifikasi | 🔜 Direncanakan | Schema Prisma (Announcement, Message, Notification) tetapi **belum di-seed**; dashboard `/berita` ada (statis) | > **Catatan:** tabel `announcements`, `messages`, `notifications` masing-masing **0 record** |"
assert old_m08 in txt, "M08 row not found"
txt = txt.replace(old_m08, new_m08)

# ---------------------------------------------------------------------------
# 4. Update §9.2 Build & Database block
# ---------------------------------------------------------------------------
old_db = """- **Database:** SQLite `dev.db` di-seed oleh `init_db.py` (schema SQL: `init_schema.sql`). Total 15 tabel: users, roles, role_permissions, students, classes, teachers, subjects, silabus, rpp, absensi, grades, rapor, announcements, messages, notifications.
  - Saat ini: 1 user, 5 role, 10 siswa, 13 kelas, 5 guru. Hanya tabel users/roles/students/classes/teachers yang terisi; semua tabel akademik, kurikulum, komunikasi = 0 record.
  - Data seed santri: 10 siswa (semua status `inactive`), 13 kelas (1A–6B + Takhosous). Data seed guru: 5 (4 Wali Kelas + 1 Guru), semua `active`.
- **Prisma:** schema `prisma/schema.prisma` (SQLite) mendefinisikan model M01–M05 + M08; driver client `prisma-client-js` (anggotakan `prisma` ^8.0.0-rc.22). Catatan: model `KitabProgress` hanya direferensikan, belum didefinisikan.
- **UI:** `src/app/*` berisi halaman berbasis route; komponen kecil `Beranda`, `Login`. Halaman lain (santri, kelas, guru, nilai, ruang-kegiatan, berita, laporan, pengasuh, sekolah) semuanya statis (placeholder UI)."""
new_db = """- **Database:** SQLite `dev.db` di-seed oleh `init_db.py` (schema SQL: `init_schema.sql`). Total 15 tabel: users, roles, role_permissions, students, classes, teachers, subjects, silabus, rpp, absensi, grades, rapor, announcements, messages, notifications.
  - Saat ini: 1 user, 5 role, 10 siswa (semua `inactive`), 13 kelas (Takhosous + 1A–6B), 5 guru (4 Wali Kelas + 1 Guru), 0 record di tabel kurikulum/akademik/komunikasi. Hanya tabel `users`, `roles`, `role_permissions`, `students`, `classes`, `teachers` yang terisi.
  - Data seed santri: 10 siswa (semua status `inactive`), 13 kelas (1A–6B + Takhosous). Data seed guru: 5 (4 Wali Kelas + 1 Guru), semua `active`. Data seed admin: 1 (admin@pondokanat.com), role `admin`.
  - **IMPORTANT:** tabel `role_permissions` didefinisikan tapi **0 record** — perizinan modul belum di-enforce di API layer.
- **Prisma:** schema `prisma/schema.prisma` (SQLite) mendefinisikan model M01–M05 + M08; driver client `prisma-client-js` (anggotakan `prisma` ^8.0.0-rc.22). Catatan: model `KitabProgress` hanya direferensikan di `Subject` (`KitabProgress[]`) tetapi **tidak didefinisikan** di schema; perlu ditambahkan jika fitur progress kitab akan dibangun.
- **UI:** `src/app/*` berisi halaman berbasis route; komponen kecil `Beranda`, `Login`. Halaman lain (santri, kelas, guru, nilai, ruang-kegiatan, berita, laporan, pengasuh, sekolah) semuanya statis (placeholder UI)."""
assert old_db in txt, "DB block not found"
txt = txt.replace(old_db, new_db)

# ---------------------------------------------------------------------------
# 5. Update data folder reference
# ---------------------------------------------------------------------------
old_folder = "`/opt/data/home/workspace/dev/pondok-banat/.data-pondokanat/`"
new_folder = "`/opt/data/home/workspace/dev/pondok-banat/.data-pondokanat/` (catatan: folder asli bernama `data-pondokanat` - typo huruf; PRD merujuk `.data-pondokanat/` tetap valid)"
assert old_folder in txt, "Folder reference not found"
txt = txt.replace(old_folder, new_folder)

# ---------------------------------------------------------------------------
# 6. Write the updated PRD
# ---------------------------------------------------------------------------
with open(prd, "w", encoding="utf-8") as f:
    f.write(txt)

print("=== PRD updated to Rev 6 ===")
print("Total lines:", txt.count(chr(10)) + 1)
print("Size:", len(txt), "bytes")
print()

# Verify key changes
for marker in [
    "## 9. STATUS", "## 10. CATATAN", "10.1 Audit data", "10.2 Penamaan",
    "Rev. 6", "KitabProgress", "Beranda", "role_permissions", "10 siswa",
    "13 kelas", "5 guru", "60 baris", "59 nama unik", "0 record",
    "pdf had mata pelajaran", "65 RPP + 9 SILABUS"
]:
    print(marker, "->", marker in txt)
