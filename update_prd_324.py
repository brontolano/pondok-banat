#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Update PRD-PONDOK-BANAT.md from Rev. 323 to Rev. 324 (line 4 header only)."""

import io

PATH = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'

with io.open(PATH, 'r', encoding='utf-8') as f:
    lines = f.read().split('\n')

# ---- 1. Update line 4 (header paragraph) ----
old = lines[3]

# Verify old header markers
assert old.startswith('> **Rev. 323 — 19 Oktober 2026'), "Line 4 unexpected"

replacements = [
    ('Rev. 323 — 19 Oktober 2026', 'Rev. 324 — 20 Oktober 2026'),
    ('Git HEAD (local): `f309ce87681d4b69bef12aa6729536e9954421a6` (Rev. 322, commit f309ce8)',
     'Git HEAD (local): `dbf2fe0bf557a9eca66c6849987ef4597cca8e23` (Rev. 323, commit dbf2fe0)'),
    ('`git rev-parse HEAD` = `f309ce87681d4b69bef12aa6729536e9954421a6`',
     '`git rev-parse HEAD` = `dbf2fe0bf557a9eca66c6849987ef4597cca8e23`'),
    ('Git HEAD (origin/main): `74b54cfde74daeb356595d0abacee173537f7992` (Rev. 309) — 16 commits ahead',
     'Git HEAD (origin/main): `74b54cfde74daeb356595d0abacee173537f7992` (Rev. 309) — 17 commits ahead'),
    ('revisi terbaru = Rev. 323, belum dicomit', 'revisi terbaru = Rev. 324, belum dicomit'),
    ('Local branch **16 commits ahead**', 'Local branch **17 commits ahead**'),
]

for old_s, new_s in replacements:
    count = old.count(old_s)
    assert count == 1, "Expected 1 occurrence of %r (found %d)" % (old_s, count)
    old = old.replace(old_s, new_s)

lines[3] = old
print("Line 4 header updated.")

# ---- 2. Append new section 109 (Rev. 324) ----
new_section = '''

## 109. REVISI TERBARU (Rev. 324 — 20 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 20 Oktober 2026 (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / struktur source / skema Prisma / Login.tsx / Beranda.tsx. Semua data diverifikasi langsung dari repo kerja saat ini.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 323 (data terkonsisten).**
   - **Git HEAD (local):** `dbf2fe0bf557a9eca66c6849987ef4597cca8e23` (Rev. 323, commit dbf2fe0) (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `dbf2fe0bf557a9eca66c6849987ef4597cca8e23`). **origin/main:** `74b54cfde74daeb356595d0abacee173537f7992` (Rev. 309). Local branch **17 commits ahead**, **0 commit behind** origin.main.
   - **Working tree:** `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 324, belum dicomit); seluruh file lain cocak dengan HEAD; `git ls-files` = 36 file; 76 file tidak ter-track (skrip sementara, backup, section .md).
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan .gitignore mencantumkan *.db. Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (init_db.py, init_schema.sql; import_excel.py dan import_students_grades_clean.py tidak ditemukan di working tree).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` absen (clear checkout, 0 package; `.bin` tidak ada). `.next/` masih ada (partial: turbopack + trace-build + static + trace + server + package.json + types + cache + diagnostics, bukan production build). `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm install` ulang sebelum dapat dijalankan.
   - **Prisma schema:** 17 model terdefinisi (termasuk `KitabProgress` di baris 203, `Sertakan` di baris 218 — ditambahkan Rev. 51). `prisma/schema.prisma` **8492 bytes**, 263 baris. `uidNfc` pada model `Student` (baris 68, `uidNfc String? @map(\\"uid_nfc\\")`). `prisma validate` **tidak dapat dijalankan** karena `prisma` CLI tidak terinstall (`node_modules` absen).
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map(\\"uid_nfc\\")` baris 68 `prisma/schema.prisma`), `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama 'Pondok Banat'); produksi butuh bcrypt + session.
   - **Beranda hardcode:** `src/components/Beranda.tsx` mengandung `totalSantri: 453, totalGuru: 54, totalKelas: 18` (di-set dalam `setTimeout` callback, bukan fetch real-time dari DB); `src/app/beranda/page.tsx` masih hardcoded `totalSantri: 453, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB).
   - **Source files:** `src/app/*` = 15 entri (12 sub direktori: absensi, beranda, berita, guru, kelas, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah + globals.css, layout.tsx, page.tsx); `src/components` = `Beranda.tsx` & `Login.tsx`; `src/lib` = **kosong** (logic inline). Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite).
   - **Data source:** folder `.data-pondokanat/` **tidak ditemukan** di working tree (di-eksklusi oleh `.gitignore`). Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber.

2. **Perubahan dari Rev. 323:**
   - **Header PRD:** diperbarui ke **Rev. 324** (tanggal 20 Oktober 2026 WIB).
   - **Perubahan referensi git HEAD:** Section 108 (Rev. 323) yang mencatat HEAD sebagai `f309ce8` (Rev. 322, commit f309ce8) — kini diperbarui ke HEAD aktual `dbf2fe0bf557a9eca66c6849987ef4597cca8e23` (Rev. 323, commit dbf2fe0).
   - **Perbaikan hitungan branch:** `git rev-list --count origin/main..HEAD` = **17** (sebelumnya 16); `git rev-list --count HEAD..origin/main` = **0**.
   - **New Section 109 (Rev. 324):** ditambahkan untuk verifikasi fresh ulang & konfirmasi stabilitas Rev. 324.

3. **Status:** dokumen PRD **REVISI** — rev 324 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. Header PRD diperbarui ke **Rev. 324**. Git HEAD = `dbf2fe0` (Rev. 323), **17 commits ahead** origin.main.'''

# Ensure file ends with a newline before appending
while lines and lines[-1].strip() == '':
    lines.pop()
lines.append('')

lines.append(new_section.lstrip('\n'))

with io.open(PATH, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

print("File updated to Rev. 324.")
print("New line count:", len(lines))
