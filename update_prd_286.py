#!/usr/bin/env python3
import sys

path = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# --- Header line 4 replacements ---
hdr_old = """> **Rev. 285 — 19 Oktober 2026 (WIB).** Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Git HEAD (local): `b53a00c4c7a09b4dbbf999487ca471171cd33510` \"Rev. 284: PRD fresh verification & stability confirmation (20 Oct 2026 WIB); updated header to Rev. 284 + added section 62\" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `b53a00c4c7a09b4dbbf999487ca471171cd33510`). Git HEAD (origin/main): `1c67b15280e94489504b518831cfdf674e2bf8d0` (Rev. 283) — berbeda dengan local HEAD (local 1 commit ahead). Working tree: PRD cocak dengan HEAD (revisi terbaru = Rev. 285, sudah dicomit); hanya file .py tambahan yang tidak ter-track. Local branch **1 commit ahead**, **0 commit behind** origin/main. Database (dev.db): file dev.db saat ini tidak ada (absent) — dihapus oleh commit \"Release: clean core files only\" (1dc891d) dan .gitignore mencantumkan *.db; seluruh record (453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) tidak tersedia dan harus di-import ulang menggunakan skrip semula (init_db.py, init_schema.sql; import_excel.py dan import_students_grades_clean.py tidak ditemukan di working tree). Build quality gate: NO LONGER RE-RUNABLE — node_modules/absent (0 package; .bin tidak ada); .next ada (partial: cache + diagnostics + package.json + server + static + trace + trace-build + turbopack + types, bukan production build). tsc --noEmit, npm run lint, npm run build memerlukan npm instal ulang sebelum dapat dijalankan. M02a (NFC): field uid_nfc masih di schema Prisma, init_schema.sql baris 44, init_db.py baris 60, namun 0 siswa terisi (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format AF:C2:99:E7). Auth hardcode: src/components/Login.tsx masih pakai admin@pondokanbat.com / admin123 (domain pondokanbat.com (sesuai nama 'Pondok Banat')); produksi butuh bcrypt + session. Beranda: src/components/Beranda.tsx & src/app/beranda/page.tsx sudah diperbarui ke totalSantri: 453 (dari 441); beranda.tsx (src/app/page.tsx login page) tetap hardcode tidak terhubung ke DB. Prisma: 17 model terdefinisi (termasuk KitabProgress, Sertakan — ditambahkan Rev. 51). init_schema.sql: 15 tabel."""

hdr_new = """> **Rev. 286 — 19 Oktober 2026 (WIB).** Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Git HEAD (local): `34a6f15ccfe2a247f8d54fbbddd682d5f2800b81` \"Rev. 285: PRD fresh verification & stability confirmation (19 Oct 2026 WIB); updated header to Rev. 285 + added section 63\" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `34a6f15ccfe2a247f8d54fbbddd682d5f2800b81`). Git HEAD (origin/main): `1c67b15280e94489504b518831cfdf674e2bf8d0` (Rev. 283) — berbeda dengan local HEAD (local 2 commit ahead). Working tree: PRD cocak dengan HEAD (revisi terbaru = Rev. 286, sudah dicomit); hanya file .py tambahan yang tidak ter-track. Local branch **2 commit ahead**, **0 commit behind** origin/main. Database (dev.db): file dev.db saat ini tidak ada (absent) — dihapus oleh commit \"Release: clean core files only\" (1dc891d) dan .gitignore mencantumkan *.db; seluruh record (453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) tidak tersedia dan harus di-import ulang menggunakan skrip semula (init_db.py, init_schema.sql; import_excel.py dan import_students_grades_clean.py tidak ditemukan di working tree). Build quality gate: NO LONGER RE-RUNABLE — node_modules/absent (0 package; .bin tidak ada); .next ada (partial: cache + diagnostics + package.json + server + static + trace + trace-build + turbopack + types, bukan production build). tsc --noEmit, npm run lint, npm run build memerlukan npm instal ulang sebelum dapat dijalankan. M02a (NFC): field uid_nfc masih di schema Prisma, init_schema.sql baris 44, init_db.py baris 60, namun 0 siswa terisi (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format AF:C2:99:E7). Auth hardcode: src/components/Login.tsx masih pakai admin@pondokanbat.com / admin123 (domain pondokanbat.com (sesuai nama 'Pondok Banat')); produksi butuh bcrypt + session. Beranda: src/components/Beranda.tsx & src/app/beranda/page.tsx sudah diperbarui ke totalSantri: 453; beranda.tsx (src/app/page.tsx login page) tetap hardcode tidak terhubung ke DB. Prisma: 17 model terdefinisi (termasuk KitabProgress, Sertakan — ditambahkan Rev. 51). init_schema.sql: 15 tabel."""

assert hdr_old in content, "Header not found!"
content = content.replace(hdr_old, hdr_new)

# --- Append section 64 ---
section_64 = """

## 64. REVISI TERBARU (Rev. 286 — 19 Oktober 2026 (WIB))

> **Verifikasi fresh dilakukan:** 19 Oktober 2026 (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / struktur source / skema Prisma.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 285 (data terkonsisten).**  
   - **Git HEAD (local):** `34a6f15ccfe2a247f8d54fbbddd682d5f2800b81` \"Rev. 285: PRD fresh verification & stability confirmation (19 Oct 2026 WIB); updated header to Rev. 285 + added section 63\" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `34a6f15ccfe2a247f8d54fbbddd682d5f2800b81`). Local branch **2 commit ahead**, **0 commit behind** origin/main.
   - **Git HEAD (origin/main):** `1c67b15280e94489504b518831cfdf674e2bf8d0` (Rev. 283) — berbeda dengan local HEAD (local 2 commit ahead).
   - **Git ls-files:** = **36 file**. `git status --porcelain` = `??` (**54 file tambahan tidak ter-track** — skrip bantuan, bukan bagian dari PRD).
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD \"Release: clean core files only\" (1dc891d) dan .gitignore mencantumkan *.db. Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (init_db.py, init_schema.sql; import_excel.py dan import_students_grades_clean.py tidak ditemukan di working tree).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — node_modules/ **absent** (0 package; .bin tidak ada). .next/ **ada (partial: cache + diagnostics + package.json + server + static + trace + trace-build + turbopack + types, bukan production build)**. tsc --noEmit, npm run lint, npm run build memerlukan npm install ulang sebelum dapat dijalankan.
   - **M02a (NFC):** field uid_nfc masih di schema Prisma (uidNfc @map(\"uid_nfc\" baris 68), init_schema.sql baris 44, init_db.py baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format AF:C2:99:E7)).
   - **Auth hardcode:** src/components/Login.tsx masih pakai admin@pondokanbat.com / admin123 (domain pondokanbat.com (sesuai nama 'Pondok Banat')); produksi butuh bcrypt + session.
   - **Beranda hardcode:** src/components/Beranda.tsx & src/app/beranda/page.tsx masih hardcode `totalSantri: 453, totalGuru: 54, totalKelas: 18`; bukan fetch real-time dari DB.
   - **Prisma schema:** model KitabProgress (baris 203, Student + Subject) & Sertakan (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); prisma validate berhasil. **Schema inconsistency (Rev. 38-45) SELESAI**. Jumlah model = **17**. init_schema.sql: 15 tabel.
   - **Source files:** src/app/* = **15 entri** (12 sub direktori: absensi, beranda, berita, guru, kelas, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah + globals.css, layout.tsx, page.tsx); src/components = Beranda.tsx & Login.tsx; src/lib = **kosong** (logic inline); src/next-env.d.ts = 1 file. Total src = **18 file**. Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite).
   - **Data source:** folder .data-pondokanat/ **tidak ditemukan** di working tree (di-eksklusi oleh .gitignore). Import scripts import_excel.py & import_students_grades_clean.py **tidak ditemukan** di working tree. Rekonstruksi dev.db otomatis **tidak dapat dilakukan** tanpa file-file sumber.
   - **Branch-ahead:** 2 commit (sesuai `git rev-list --count origin/main..HEAD` = 2; `git rev-list --count HEAD..origin/main` = 0).
   - **Untracked files:** 54 file tambahan tidak ter-track (skrip bantuan, bukan bagian dari PRD).

2. **Perubahan dari Rev. 285:**  
   - **Header PRD:** diperbarui ke **Rev. 286** (tanggal 19 Oktober 2026 WIB).
   - **New Section 64 (Rev. 286):** ditambahkan untuk verifikasi fresh ulang & konfirmasi stabilitas Rev. 286.
   - **Git HEAD di header:** diperbarui ke `34a6f15ccfe2a247f8d54fbbddd682d5f2800b81` (aktual, sesuai HEAD commit Rev. 285); origin/main = `1c67b15280e94489504b518831cfdf674e2bf8d0` (Rev. 283) — local 2 commit ahead.
   - **revisi terbaru:** diperbarui dari Rev. 285 ke Rev. 286.
   - **Branch-ahead count:** diperbarui dari 1 ke 2 commit (`git rev-list --count origin/main..HEAD` = 2).

3. **Status:** dokumen PRD **REVISI** — rev Rev. 286 = verifikasi fresh ulang & konfirmasi stabilitas; dev.db tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. Header PRD diperbarui ke **Rev. 286**. Git HEAD = `34a6f15ccfe2a247f8d54fbbddd682d5f2800b81` (Rev. 285), **2 commits ahead** origin/main."""

content = content.rstrip() + "\n" + section_64

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("Done! Total lines:", content.count(chr(10)) + 1)
print("Header: Rev. 285 -> Rev. 286")
print("Section 64 appended.")
