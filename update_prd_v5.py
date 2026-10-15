#!/usr/bin/env python3
"""
Update PRD-PONDOK-BANAT.md to Rev 5.
Reflects the actual current codebase state verified on 14 Oktober 2026.
"""
import os
import re

base = "/opt/data/home/workspace/dev/pondok-banat"
prd = os.path.join(base, "PRD-PONDOK-BANAT.md")

with open(prd, encoding="utf-8") as f:
    txt = f.read()

# ---------------------------------------------------------------------------
# 1. Update the revision footer from Rev 4 to Rev 5
# ---------------------------------------------------------------------------
old_footer = "*Rev. 4 — 14 Oktober 2026. Perubahan: 1) perbaiki catatan kelas (Data Kelas sheet terisi 3 jenjang; Data Nilai sheet 6 jenjang — diskrepansi sumber data); 2) klarifikasi §8.1 & §10.1 kelas. Rev. 3 = dokumen PRD sebelumnya.*"
new_footer = """*Rev. 5 — 14 Oktober 2026. Perubahan: 1) diklarisi Prisma: model KitabProgress hanya direferensikan, belum didefinisikan (stale); 2) dicek ulang status DB & statik Komponen Beranda (totalSantri=42, totalGuru=27 vs DB sesungguhnya 10 siswa/5 guru); 3) laporkan data seed santri (10 siswa, status 'inactive') & guru (5, terdiri 4 Wali Kelas + 1 Guru); 4) sesuaikan keterangan M04. Rev. 4 = dokumen PRD sebelumnya.*"""
assert old_footer in txt, "Rev 4 footer not found"
txt = txt.replace(old_footer, new_footer)

# ---------------------------------------------------------------------------
# 2. Add a note about KitabProgress in Prisma (M04)
# ---------------------------------------------------------------------------
# Insert after the M04 row in the status table
m04_row = "| M04 | Kurikulum & Kitab Kuning | 🔜 Direncanakan | Schema Prisma lengkap (Subject, Silabus, RPP + KitabProgress) tetapi **belum di-seed** data mapel/silabus/rpp dari PDF/xlsx; dashboard `/kelas` ada (statis) |"
m04_note = m04_row + " > **Catatan Prisma:** model `KitabProgress` hanya direferensikan di `Subject` (`KitabProgress[]`) tetapi **tidak didefinisikan** di schema; perlu ditambahkan jika fitur progress kitab akan dibangun. |"
assert m04_row in txt, "M04 row not found"
txt = txt.replace(m04_row, m04_note)

# ---------------------------------------------------------------------------
# 3. Add a note about Beranda stats (static placeholder) — a small paragraph
#    after the M01 row (or after §9.2). Insert after M01 row.
# ---------------------------------------------------------------------------
m01_row = "| M01 | Admin & User Management | ✅ Implementasi | `prisma/schema.prisma` (model User, Role, RolePermission) + `src/app/login/page.tsx`; 1 user admin seed otomatis via `init_db.py`; authorization masih hardcode di React |"
m01_note = m01_row + " > **Catatan statis:** Komponen `Beranda` menunjukkan `totalSantri: 42`, `totalGuru: 27` (placeholder statis), tidak mencerminkan jumlah sesungguhnya di `dev.db` (10 siswa, 5 guru). |"
assert m01_row in txt, "M01 row not found"
txt = txt.replace(m01_row, m01_note)

# ---------------------------------------------------------------------------
# 4. Update §9.2 Build & Database to reflect the actual seed data
# ---------------------------------------------------------------------------
old_db = """- **Database:** SQLite `dev.db` di-seed oleh `init_db.py` (schema SQL: `init_schema.sql`). Total 15 tabel: users, roles, role_permissions, students, classes, teachers, subjects, silabus, rpp, absensi, grades, rapor, announcements, messages, notifications.
  - Saat ini: 1 user, 5 role, 10 siswa, 13 kelas, 5 guru. Hanya tabel users/roles/students/classes/teachers yang terisi; semua tabel akademik, kurikulum, komunikasi = 0 record.
- **Prisma:** schema `prisma/schema.prisma` (SQLite) mendefinisikan model M01–M05 + M08; driver client `prisma-client-js` (anggotakan `prisma` ^8.0.0-rc.22).
- **UI:** `src/app/*` berisi halaman berbasis route; komponen kecil `Beranda`, `Login`."""
new_db = """- **Database:** SQLite `dev.db` di-seed oleh `init_db.py` (schema SQL: `init_schema.sql`). Total 15 tabel: users, roles, role_permissions, students, classes, teachers, subjects, silabus, rpp, absensi, grades, rapor, announcements, messages, notifications.
  - Saat ini: 1 user, 5 role, 10 siswa, 13 kelas, 5 guru. Hanya tabel users/roles/students/classes/teachers yang terisi; semua tabel akademik, kurikulum, komunikasi = 0 record.
  - Data seed santri: 10 siswa (semua status `inactive`), 13 kelas (1A–6B + Takhosous). Data seed guru: 5 (4 Wali Kelas + 1 Guru), semua `active`.
- **Prisma:** schema `prisma/schema.prisma` (SQLite) mendefinisikan model M01–M05 + M08; driver client `prisma-client-js` (anggotakan `prisma` ^8.0.0-rc.22). Catatan: model `KitabProgress` hanya direferensikan, belum didefinisikan.
- **UI:** `src/app/*` berisi halaman berbasis route; komponen kecil `Beranda`, `Login`. Halaman lain (santri, kelas, guru, nilai, ruang-kegiatan, berita, laporan, pengasuh, sekolah) semuanya statis (placeholder UI)."""
assert old_db in txt, "DB block not found"
txt = txt.replace(old_db, new_db)

# ---------------------------------------------------------------------------
# 5. Write the updated PRD
# ---------------------------------------------------------------------------
with open(prd, "w", encoding="utf-8") as f:
    f.write(txt)

print("=== PRD updated to Rev 5 ===")
print("Total lines:", txt.count(chr(10)) + 1)
print("Size:", len(txt), "bytes")
print()

# Verify key changes
for marker in [
    "## 9. STATUS", "## 10. CATATAN", "10.1 Audit data", "10.2 Penamaan",
    "Rev. 5", "KitabProgress", "Beranda", "totalSantri", "10 siswa, 13 kelas, 5 guru"
]:
    print(marker, "->", marker in txt)
