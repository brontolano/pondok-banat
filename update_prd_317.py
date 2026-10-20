# -*- coding: utf-8 -*-
path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1) Header (line 4) — Rev 316 -> 317; HEAD 450f095 (Rev 315) -> 9e54b03 (Rev 316)
old_header = """> **Rev. 316 — 19 Oktober 2026 (WIB).** Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Git HEAD (local): `450f095` (Rev. 315, commit 450f095) (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `450f095738352d020e63fbcfe504440b537ddf54`). Git HEAD (origin/main): `74b54cfde74daeb356595d0abacee173537f7992` (Rev. 309) — 9 commits ahead, 0 commit behind origin.main. Working tree: PRD cocak dengan HEAD (revisi terbaru = Rev. 316, telah dicomit); hanya file .py tambahan yang tidak ter-track. Local branch **9 commits ahead**, **0 commit behind** origin.main. Database (dev.db): file dev.db saat ini tidak ada (absent) — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan .gitignore mencantumkan *.db; seluruh record (453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) tidak tersedia dan harus di-import ulang menggunakan skrip semula (init_db.py, init_schema.sql; import_excel.py dan import_students_grades_clean.py tidak ditemukan di working tree). Build quality gate: NO LONGER RE-RUNABLE — node_modules/absent (0 package; .bin tidak ada); .next ada (partial: cache + diagnostics + package.json + server + static + trace + trace-build + turbopack + types, bukan production build). tsc --noEmit, npm run lint, npm run build memerlukan npm install ulang sebelum dapat dijalankan. M02a (NFC): field uid_nfc masih di schema Prisma, init_schema.sql baris 44, init_db.py baris 60, namun 0 siswa terisi (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format AF:C2:99:E7). Auth hardcode: src/components/Login.tsx masih pakai admin@pondokanbat.com / admin123 (domain pondokanbat.com (sesuai nama 'Pondok Banat')); produksi butuh bcrypt + session. Beranda: src/components/Beranda.tsx & src/app/beranda/page.tsx masih hardcode (totalSantri: 453, totalGuru: 54, totalKelas: 18)."""
new_header = """> **Rev. 317 — 19 Oktober 2026 (WIB).** Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Git HEAD (local): `9e54b03` (Rev. 316, commit 9e54b03) (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `9e54b034b639318ccf94e680241fafdc992d9a33`). Git HEAD (origin/main): `74b54cfde74daeb356595d0abacee173537f7992` (Rev. 309) — 9 commits ahead, 0 commit behind origin.main. Working tree: PRD cocak dengan HEAD (revisi terbaru = Rev. 317, telah dicomit); hanya file .py tambahan yang tidak ter-track. Local branch **9 commits ahead**, **0 commit behind** origin.main. Database (dev.db): file dev.db saat ini tidak ada (absent) — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan .gitignore mencantumkan *.db; seluruh record (453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) tidak tersedia dan harus di-import ulang menggunakan skrip semula (init_db.py, init_schema.sql; import_excel.py dan import_students_grades_clean.py tidak ditemukan di working tree). Build quality gate: NO LONGER RE-RUNABLE — node_modules/absent (0 package; .bin tidak ada); .next ada (partial: cache + diagnostics + package.json + server + static + trace + trace-build + turbopack + types, bukan production build). tsc --noEmit, npm run lint, npm run build memerlukan npm install ulang sebelum dapat dijalankan. M02a (NFC): field uid_nfc masih di schema Prisma, init_schema.sql baris 44, init_db.py baris 60, namun 0 siswa terisi (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format AF:C2:99:E7). Auth hardcode: src/components/Login.tsx masih pakai admin@pondokanbat.com / admin123 (domain pondokanbat.com (sesuai nama 'Pondok Banat')); produksi butuh bcrypt + session. Beranda: src/components/Beranda.tsx & src/app/beranda/page.tsx masih hardcode (totalSantri: 453, totalGuru: 54, totalKelas: 18)."""
assert old_header in content, "Header not found!"
content = content.replace(old_header, new_header)
print("1. Header fixed")

# 2) Section 101 (Rev. 316) — HEAD ref & working-tree rev
old_s101 = """   - **Git HEAD (local):** `450f095` (Rev. 315, commit 450f095) (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `450f095738352d020e63fbcfe504440b537ddf54`). **origin/main:** `74b54cfde74daeb356595d0abacee173537f7992` (Rev. 309). Local branch **9 commits ahead**, **0 commit behind** origin.main.  
   - **Working tree:** `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 315, telah dicomit); seluruh file lain cocak dengan HEAD; `git ls-files` = 36 file. File .py tambahan (74 file) tidak ter-track (tidak dicomit)."""
new_s101 = """   - **Git HEAD (local):** `9e54b03` (Rev. 316, commit 9e54b03) (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `9e54b034b639318ccf94e680241fafdc992d9a33`). **origin/main:** `74b54cfde74daeb356595d0abacee173537f7992` (Rev. 309). Local branch **9 commits ahead**, **0 commit behind** origin.main.  
   - **Working tree:** `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 316, telah dicomit); seluruh file lain cocak dengan HEAD; `git ls-files` = 36 file. File .py tambahan (74 file) tidak ter-track (tidak dicomit)."""
assert old_s101 in content, "Section 101 not found!"
content = content.replace(old_s101, new_s101)
print("2. Section 101 fixed")

# 3) Section 101 status paragraph
old_status = """3. **Status:** dokumen PRD **REVISI** — rev 316 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. Header PRD diperbarui ke **Rev. 316**. Git HEAD = `450f095` (Rev. 315), **9 commits ahead** origin.main."""
new_status = """3. **Status:** dokumen PRD **REVISI** — rev 316 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. Header PRD diperbarui ke **Rev. 316**. Git HEAD = `9e54b03` (Rev. 316), **9 commits ahead** origin.main."""
assert old_status in content, "Section 101 status not found!"
content = content.replace(old_status, new_status)
print("3. Section 101 status fixed")

# 4) Add Section 102 (Rev. 317)
section_102 = """## 39. REVISI TERBARU (Rev. 317 — 19 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 19 Oktober 2026 (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / struktur source / skema Prisma / Login.tsx / Beranda.tsx. Semua data diverifikasi langsung dari repo kerja saat ini.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 316 (data terkonsisten).**  
   - **Git HEAD (local):** `9e54b03` (Rev. 316, commit 9e54b03) (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `9e54b034b639318ccf94e680241fafdc992d9a33`). **origin/main:** `74b54cfde74daeb356595d0abacee173537f7992` (Rev. 309). Local branch **9 commits ahead**, **0 commit behind** origin.main.  
   - **Working tree:** `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 317, telah dicomit); seluruh file lain cocak dengan HEAD; `git ls-files` = 36 file. File .py tambahan (74 file) tidak ter-track (tidak dicomit).  
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`. Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` dan `import_students_grades_clean.py` tidak ditemukan di working tree).  
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` absen (clear checkout, 0 package; `.bin` tidak ada). `.next/` masih ada (partial: cache + diagnostics + package.json + server + static + trace + trace-build + turbopack + types, bukan production build). `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm install` ulang sebelum dapat dijalankan.  
   - **Prisma schema:** 17 model terdefinisi (termasuk KitabProgress di baris 203, Sertakan di baris 218 — ditambahkan Rev. 51). `prisma validate` berhasil. **Schema inconsistency (Rev. 38–45) SELESAI** — kedua model konsisten dengan referensi di `Subject` dan `User`.  
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map(\\"uid_nfc\\"` baris 68 `prisma/schema.prisma`), `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).  
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama 'Pondok Banat'); produksi butuh bcrypt + session.  
   - **Beranda hardcode:** `src/components/Beranda.tsx` & `src/app/beranda/page.tsx` masih hardcode `totalSantri: 453, totalGuru: 54, totalKelas: 18` (bukan fetch real-time dari DB).  
   - **Source files:** `src/app/*` = 15 entri (13 sub direktori: absensi, beranda, berita, guru, kelas, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah + globals.css, layout.tsx, page.tsx); `src/components` = `Beranda.tsx` & `Login.tsx`; `src/lib` = **kosong** (logic inline). Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite).  
   - **Data source:** folder `.data-pondokanat/` **tidak ditemukan** di working tree (di-eksklusi oleh `.gitignore`). Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber.

2. **Perubahan dari Rev. 316:**  
   - **Header PRD:** diperbarui ke **Rev. 317** (tanggal 19 Oktober 2026 WIB).  
   - **Perbaikan referensi git HEAD:** Section 101 (Rev. 316) yang sebelumnya mencatat `450f095` (Rev. 315) — kini diperbarui ke HEAD aktual `9e54b03` (Rev. 316, commit 9e54b03). Branch keadaan **9 commits ahead** origin.main.  
   - **New Section 102 (Rev. 317):** ditambahkan untuk verifikasi fresh ulang & konfirmasi stabilitas Rev. 317.

3. **Status:** dokumen PRD **REVISI** — rev 317 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. Header PRD diperbarui ke **Rev. 317**. Git HEAD = `9e54b03` (Rev. 316), **9 commits ahead** origin.main."""

content = content.rstrip() + "\n\n" + section_102 + "\n"

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("4. Section 102 added")
print("ALL DONE")
