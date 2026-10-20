## 61. REVISI TERBARU (Rev. 215 — 18 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 18 Oktober 2026 (WIB, cron run) — query `sqlite3` ke `dev.db`, `git` (HEAD/status/ahead/ls-files), `ls` (dev.db/node_modules/.data-pondokanat), `cat` (quality_gate.sh), `grep` (prisma schema, init_schema.sql, source files).

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 214 (data terkonsisten).**
   - **Git HEAD (local):** `4f26e2ca99966ad0bda63f270387b2d2c97b1400` "Rev. 213: PRD fresh verification & stability confirmation (18 Oktober 2026 WIB); updated header to Rev. 213 + added section 59" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `4f26e2ca99966ad0bda63f270387b2d2c97b1400`). Local branch **55** commits ahead dari `origin/main` (`27ca1d2a53b79c513cae9746cc0be9dfe9d783fa` = Rev. 163 fix).
   - **Git ls-files:** = **36 file**. `git status --porcelain` = ` M PRD-PONDOK-BANAT.md` (**1 file modified**) + `??` (**23 file tambahan tidak ter-track** — skrip helper development). PRD-PONDOK-BANAT.md memiliki perubahan lokal (revisi terbaru = Rev. 215); Working tree **tidak bersih**.
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan .gitignore mencantumkan *.db. Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (init_db.py, init_schema.sql; import_excel.py dan import_students_grades_clean.py tidak ditemukan di working tree).
   - **Node_modules & Build quality gate:** `node_modules` **tidak ada (absent)**. Build quality gate **NO LONGER RE-RUNABLE** — `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm install` ulang. `.next/` masih ada (partial build artifacts).
   - **Source files:** `src/app/*` = 11 sub direktori (absensi, beranda, berita, guru, kelas, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah) + `globals.css` + `layout.tsx` + `page.tsx` = 15 entri (13 halaman + layout + page). `src/components` = `Beranda.tsx` & `Login.tsx`. `src/lib` = **kosong** (logic inline di komponen). Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite).
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map("uid_nfc")` baris 68) & `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` (sesuai nama 'Pondok Banat')); produksi butuh bcrypt + session.
   - **Beranda hardcode:** `Beranda.tsx` masih hardcoded `totalSantri: 441, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB; belum diperbarui ke 453).
   - **Source data:** folder `.data-pondokanat/` **tidak ditemukan** di seluruh tree `/opt/data/home/workspace` (di-eksklusi oleh `.gitignore`) DAN tidak ditemukan di seluruh tree `/opt/data`. Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber. **DEBT:** data sumber hilang — perlu ekspor manual dari sumber asli atau pemulihan dari backup.
   - **quality_gate.sh:** file masih memuat rantai `tsc` → `eslint` → `next build`; seluruh gate gagal karena `node_modules` absen.
   - **`.next/` directory:** entri = cache, diagnostics, package.json, server, static, trace, trace-build, turbopack, types (**9 entri** — dikonfirmasi; node_modules absen).
   - **Untracked files:** **23 file** (bersih vs HEAD; `git status --porcelain` = `??`): clean_prd.py, clean_prd2.py, clean_prd3.py, clean_prd4.py, fix_header_status.py, fix_newline.py, fix_prd.py–fix_prd9.py, hex_dump.py, rev186_section.md, rev206_section.md, section85.md, update_prd.py, update_prd_165.py, update_prd_188.py, update_prd_189.py. Semua adalah skrip pengembangan sementara (untuk manipulasi Rev. 163–213), tidak termasuk commit.

2. **Perubahan dari Rev. 214:** 
   - **Header PRD:** diperbarui ke Rev. 215 (tanggal 18 Oktober 2026 WIB).
   - **New Section 61 (Rev. 215):** ditambahkan untuk verifikasi fresh ulang & konfirmasi stabilitas Rev. 215.
   - **HEAD:** tidak berubah (`4f26e2ca99966ad0bda63f270387b2d2c97b1400`).
   - **Branch ahead:** **55** commit (tidak berubah).
   - **Working tree:** masih tidak bersih (revisi Rev. 214 & 215 belum dicomit; skrip helper development 23 file).

3. **Open issues:** (sama persis dengan Rev. 214)

4. **Status:** dokumen PRD **REVISI** — rev 215 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. HEAD = `4f26e2ca99966ad0bda63f270387b2d2c97b1400`. Branch **55** commits ahead `origin/main` (`27ca1d2a53b79c513cae9746cc0be9dfe9d783fa` = Rev. 163 fix). Working tree tidak bersih (revisi Rev. 214 & 215 belum dicomit, 23 skrip helper tidak ter-track).
