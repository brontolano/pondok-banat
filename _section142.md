## 142. REVISI TERBARU (Rev. 357 — 20 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 20 Oktober 2026 (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / struktur source / skema Prisma / Login.tsx / Beranda.tsx. Semua data diverifikasi langsung dari repo kerja saat ini.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 356 (data terkonsisten).**

   - **Git HEAD (local):** `f0fd099` (Rev. 356, commit `f0fd099e93e112926f53417ab4e3cec150139219`). Branch `main` (remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `f0fd099`). **origin/main:** `8df4a80` (Rev. 353). Local branch **3 commits ahead**, **0 commit behind** origin.main.
   - **Working tree:** PRD cocak dengan HEAD (revisi terbaru = Rev. 357); seluruh file lain cocak dengan HEAD; `git ls-files` = 36 file; 112 file tidak ter-track (skrip sementara, backup, section .md, .orig, .py).
   - **Database (dev.db):** file `dev.db` saat ini **absent** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan .gitignore mencantumkan *.db. Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (init_db.py, init_schema.sql; import_excel.py dan import_students_grades_clean.py tidak ditemukan di working tree).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` absen (0 package; .bin tidak ada). `.next/` masih ada (partial: cache + diagnostics + package.json + server + static + trace + trace-build + turbopack + types, bukan production build). `tsc --noEmit` → exit 1; `eslint .` → exit 2; `next build` → exit 1 (semua gagal karena dependency tidak tersedia, memerlukan `npm install` ulang).
   - **Prisma schema:** 17 model terdefinisi (termasuk `KitabProgress` di baris 203, `Sertakan` di baris 218 — ditambahkan Rev. 51). `uidNfc` pada model `Student` (baris 68, `uidNfc String? @map("uid_nfc")`). `prisma/schema.prisma` **8488 bytes**, 264 baris. `prisma validate` **tidak dapat dijalankan** karena `prisma` CLI tidak terinstall (`node_modules` absen).
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map("uid_nfc")` baris 68) & `init_schema.sql` baris 40, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama Pondok Banat).
   - **Beranda hardcode:** `src/components/Beranda.tsx` (baris 26–28) & `src/app/beranda/page.tsx` (baris 14–16) masih hardcode `totalSantri: 453, totalGuru: 54, totalKelas: 18` (bukan fetch real-time dari DB; sudah diperbarui ke 453 sesuai data Excel grade sheets).
   - **Source files:** `src/app/*` = 15 entri (12 sub direktori: absensi, beranda, berita, guru, kelas, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah + globals.css, layout.tsx, page.tsx); `src/components` = 2 (Beranda.tsx & Login.tsx); `src/lib` = kosong (logic inline). Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite).
   - **Data source:** folder `.data-pondokanat/` **tidak ditemukan** di working tree (di-eksklusi oleh `.gitignore`). Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber.

2. **Perubahan dari Rev. 356:**
   - **Header PRD:** diperbarui ke **Rev. 357** (tanggal 20 Oktober 2026 WIB).
   - **New Section 142 (Rev. 357):** ditambahkan untuk verifikasi fresh ulang & konfirmasi stabilitas Rev. 357.
   - **Referensi HEAD:** state terkini HEAD = `f0fd099` (Rev. 356, commit `f0fd099`); origin/main = `8df4a80` (Rev. 353). Branch **3 commits ahead** origin.main.

3. **Status:** dokumen PRD **REVISI** — rev 357 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. Header PRD diperbarui ke **Rev. 357**. Git HEAD = `f0fd099` (Rev. 356, 3 commits ahead origin.main).
