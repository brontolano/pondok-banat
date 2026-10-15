#!/usr/bin/env python3
"""
Update PRD-PONDOK-BANAT.md to Rev 3.
Reflects the actual current codebase state (date: 14 Oktober 2026).
"""
import os

base = "/opt/data/home/workspace/dev/pondok-banat"
prd = os.path.join(base, "PRD-PONDOK-BANAT.md")
with open(prd, encoding="utf-8") as f:
    txt = f.read()

# ---- 1. Add hardcoded login security finding after the §9.1 status table ----
# Insert before "### 9.2 Build & Database"
anchor_m11 = "| ❌ Tidak aktif (MVP) | Gatsby mobile — tidak termasuk MVP; tertunda |\n\n"
assert anchor_m11 in txt, "M11 anchor not found in PRD"
new_m07_section = anchor_m11 + "> **Catatan keamanan:** Autentikasi saat ini hardcode — email `admin@pondokanat.com` / password `admin123` terekam di `src/components/Login.tsx`. Ini hanya untuk demo; sebelum production wajib diganti dengan bcrypt + session management yang aman (lihat backlog §9.3).\n"
txt = txt.replace(anchor_m11, new_m07_section)

# ---- 2. Update §9.2 database line: confirm 15 tables ----
old_db_line = """- **Database:** SQLite `dev.db` di-seed oleh `init_db.py` (schema SQL: `init_schema.sql`).
  - Saat ini: 1 user, 5 role, 10 siswa, 13 kelas, 5 guru.
  - Tabel akademik/komunikasi **ada di schema tapi 0 record**: subjects=0, silabus=0, rpp=0, absensi=0, grades=0, rapor=0, announcements=0, messages=0, notifications=0."""
new_db_line = """- **Database:** SQLite `dev.db` di-seed oleh `init_db.py` (schema SQL: `init_schema.sql`). Total 15 tabel: users, roles, role_permissions, students, classes, teachers, subjects, silabus, rpp, absensi, grades, rapor, announcements, messages, notifications.
  - Saat ini: 1 user, 5 role, 10 siswa, 13 kelas, 5 guru. Hanya tabel users/roles/students/classes/teachers yang terisi; semua tabel akademik, kurikulum, komunikasi = 0 record."""
assert old_db_line in txt, "DB line not found"
txt = txt.replace(old_db_line, new_db_line)

# ---- 3. Update revision footer to Rev 3 ----
old_footer = "*Rev. 2 — 14 Oktober 2026. Perubahan: 1) ditambah §9 Status Implementasi Saat Ini; 2) ditambah §10 Catatan Pengembang & audit data; 3) diperhalus klarifikasi §8.1. Rev. 1 = dokumen PRD asli.*"
new_footer = "*Rev. 3 — 14 Oktober 2026. Perubahan: 1) ditambah catatan keamanan demo login hardcoded; 2) diperhalus §9.2 (15 tabel DB); 3) konsistensi penamaan folder data. Rev. 2 = dokumen PRD sebelumnya.*"
assert old_footer in txt, "footer not found"
txt = txt.replace(old_footer, new_footer)

with open(prd, "w", encoding="utf-8") as f:
    f.write(txt)

print("=== PRD updated to Rev 3 ===")
print("Total lines:", txt.count(chr(10)) + 1)
print("Size:", len(txt), "bytes")
print()
# Verify key changes
for marker in ["## 9. STATUS", "## 10. CATATAN", "10.1 Audit data", "10.2 Penamaan", "hardcoded", "15 tabel", "Rev. 3"]:
    print(marker, "->", marker in txt)
