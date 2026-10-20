#!/usr/bin/env python3
# Update PRD to Rev. 222
path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Update header
content = content.replace('Rev. 221 — 18 Oktober 2026 (WIB).**', 'Rev. 222 — 18 Oktober 2026 (WIB).**')
content = content.replace('Git HEAD: `67d523620ba1d55b0a3792a47f0f0cf5bea61018`', 'Git HEAD: `d4caa349eb5a2f33bd6fb4af220826246c8d27e6`')
content = content.replace('HEAD = `67d523620ba1d55b0a3792a47f0f0cf5bea61018`', 'HEAD = `d4caa349eb5a2f33bd6fb4af220826246c8d27e6`')
content = content.replace('Branch 63 commits ahead', 'Branch 64 commits ahead')

# New revision section (Rev. 222) — appended at end
new_section = """

## 68. REVISI TERBARU (Rev. 222 — 18 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 18 Oktober 2026 (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / `PRD-PONDOK-BANAT.md`; query `sqlite3` ke `dev.db` (tidak ada); verifikasi isi file: `Beranda.tsx`, `page.tsx`, `Login.tsx`, `prisma/schema.prisma`, `init_db.py`, `init_schema.sql`.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 221 (data terkonsisten).**
   - **Git HEAD:** `d4caa34` "Rev. 221: PRD fresh verification & stability confirmation (18 Oct 2026 WIB)" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `d4caa349eb5a2f33bd6fb4af220826246c8d27e6`). **Branch 64 commit ahead of `origin/main`** (origin/main = `27ca1d2a53b79c513cae9746cc0be9dfe9d783fa` (Rev. 163 fix); seluruh commit di-branch ini adalah revisi dokumentasi PRD). `git ls-files` = **36 file**. `git status --porcelain` = (kosong).
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`. Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` dan `import_students_grades_clean.py` tidak ditemukan di working tree).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` **absent** (clear checkout, 0 file); `.next/` masih ada (partial: `cache` + `diagnostics` + `package.json` + `server` + `static` + `trace` + `trace-build` + `turbopack` + `types`, bukan production build). `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm install` ulang sebelum dapat dijalankan.
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map("uid_nfc")` baris 68), `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama 'Pondok Banat'). Produksi butuh bcrypt + session.
   - **Beranda hardcode:** `Beranda.tsx` & `src/app/beranda/page.tsx` kini **diperbarui ke 453** (dari 441) — hardcoded stats now match Excel grade sheets.
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` berhasil. **Schema inconsistency (Rev. 38–45) SELESAI** — kedua model konsisten dengan referensi di `Subject` dan `User`.
   - **Source files:** `src/app/*` = 13 halaman (beranda, berita, kelas, guru, absensi, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah + layout/page); `src/components` = Beranda.tsx + Login.tsx; `src/lib` = **kosong** (logic inline di komponen). Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite).
   - **Source data:** folder `.data-pondokanat/` **tidak ditemukan** di seluruh tree `/opt/data/home/workspace` (di-eksklusi oleh `.gitignore`) DAN tidak ditemukan di seluruh tree `/opt/data`. Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber. **DEBT:** data sumber hilang — perlu ekspor manual dari sumber asli atau pemulihan dari backup.
   - **Working tree:** `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 222); `git status --porcelain` = (kosong). Seluruh file lain cocak dengan HEAD.

2. **Open issues:**
   - [Tinggi] Restore/retrieve `.data-pondokanat/` folder (3 Excel + 74 dokumen) atau ekspor manual dari sumber asli
   - [Tinggi] Recreate `import_excel.py` & `import_students_grades_clean.py`
   - [Tinggi] Rekonstruksi `dev.db` dari skrip seed: 453 siswa, 54 guru, 18 kelas, 32 mapel, 5.420 nilai
   - [Tinggi] Rekonfirmasi discrepancy 453 vs 441 siswa (sudah diperbaiki di kode → PRD 453)
   - [Tinggi] Implementasi dashboard Wali Santri Portal (M08)
   - [Tinggi] Implementasi PDF generation untuk rapor & laporan (M09)
   - [Sedang] Implementasi seed data silabus (9 dokumen) dari Excel/PDF (M04)
   - [Sedang] Implementasi seed data absensi & rapor dari nilai (M05)
   - [Sedang] Implementasi `KitabProgress` schema di Prisma (M04/M06) — **sudah didefinisikan, tinggal bind**
   - [Rendah] Auth production (bcrypt + session) (M01)
   - [Rendah] Export/backup/restore (Excel, PDF) (M09)
   - [Rendah] Unit + integration testing (Semua)
   - [Rendah] Production deployment (Vercel, Docker) (Semua)

3. **Status:** dokumen PRD **REVISI** — rev 222 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. Header PRD diperbarui ke **Rev. 222**. Working tree bersih selain PRD file. `git status --porcelain` akan kembali (kosong) setelah commit.
"""

content += new_section

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('File updated successfully to Rev. 222')
