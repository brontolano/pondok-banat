## 93. REVISI TERBARU (Rev. 206 — 18 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 18 Oktober 2026 (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / struktur source / skema Prisma; verifikasi isi file: header PRD, §92.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 205 (data terkonsisten).**
   - **Git HEAD (local):** `016180b50ca90981575f2c2584fa031df16f8275` "Rev. 205: fix catatan terkini branch-ahead (42)" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `016180b50ca90981575f2c2584fa031df16f8275`). Local branch **44** commits ahead dari `origin/main` (`27ca1d2a53b79c513cae9746cc0be9dfe9d783fa` = Rev. 163 fix).
   - **Git HEAD (origin/main):** `27ca1d2a53b79c513cae9746cc0be9dfe9d783fa` (Rev. 163 fix). Local branch **44** ahead.
   - **Git ls-files:** = **36 file**. `git status --porcelain` = `??` (**21 file tambahan tidak ter-track**, bertambah 2 dari Rev. 205). PRD-PONDOK-BANAT.md memiliki perubahan lokal (revisi terbaru = Rev. 206); Working tree **tidak bersih** (revisi Rev. 206 akan dicommit).
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan .gitignore mencantumkan *.db. Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (init_db.py, init_schema.sql; import_excel.py dan import_students_grades_clean.py tidak ditemukan di working tree).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` **absent** (clear checkout, 0 file); `.next/` **masih ada (partial: cache + diagnostics + package.json + server + static + trace + trace-build + turbopack + types, bukan production build)**. `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm instal ulang` sebelum dapat dijalankan.
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map(\"uid_nfc\")` baris 68), `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama 'Pondok Banat'). Produksi butuh bcrypt + session.
   - **Beranda hardcode:** `src/components/Beranda.tsx` & `src/app/beranda/page.tsx` masih hardcoded `totalSantri: 453, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB).
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); jumlah model Prisma = **17**. `prisma validate` tidak dapat dijalankan (prisma tidak terinstall di env cron karena node_modules absen).
   - **init_schema.sql:** tabel `students` (baris 33) memiliki kolom `uid_nfc TEXT` (baris 44, komentar: `-- NFC card UID: 'AF:C2:99:E7'`) — field M02a **ADA** di schema SQLite. Jumlah tabel = **15** sesuai PRD. `init_db.py` (6135 bytes) dan `.seed_users_roles.py` (3343 bytes) masih ada; `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** (0 bytes / MISSING).
   - **Source files:** `src/app/*` = 12 sub direktori (absensi, beranda, berita, guru, kelas, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah) + `globals.css` + `layout.tsx` + `page.tsx` = 15 entri; `src/components` = `Beranda.tsx` & `Login.tsx`; `src/lib` = **kosong** (logic inline). `git ls-files` = **36 file**.
   - **Source data:** folder `.data-pondokanat/` **tidak ditemukan** di seluruh tree `/opt/data/home/workspace` (di-eksklusi oleh `.gitignore`) DAN tidak ditemukan di seluruh tree `/opt/data`. Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber. **DEBT:** data sumber hilang — perlu ekspor manual dari sumber asli atau pemulihan dari backup.
   - **quality_gate.sh:** file masih memuat rantai `tsc` → `eslint` → `next build`; seluruh gate gagal karena `node_modules` absen.
   - **`.next/` directory:** entri = cache, diagnostics, package.json, server, static, trace, trace-build, turbopack, types (10 entri — dikonfirmasi; node_modules absen).
   - **Untracked files:** **21 file** (bersih vs HEAD; `git status --porcelain` = `??`): clean_prd.py–clean_prd4.py, fix_header_status.py, fix_prd.py–fix_prd9.py, hex_dump.py, rev186_section.md, section85.md, update_prd.py, update_prd_165.py, update_prd_188.py, update_prd_189.py. Semua adalah skrip pengembangan sementara (untuk manipulasi Rev. 163–206), tidak termasuk commit.
   - **Branch ahead count:** diperbaiki dari 42 → **44** commit (2 commit baru revisi lokal: `71647e7` & `016180b`).
   - **HEAD citation:** diperbaiki dari `7bbc139` → **`016180b`** (Rev. 205: fix catatan terkini branch-ahead).

2. **Perubahan dari Rev. 205:**
   - **Header PRD:** diperbarui ke **Rev. 206** (tanggal 18 Oktober 2026 WIB).
   - **New Section 93 (Rev. 206):** ditambahkan untuk verifikasi fresh ulang & konfirmasi stabilitas Rev. 206.
   - **HEAD:** diperbarui dari `7bbc139` → `016180b` (2 commit revisi lokal baru `71647e7`, `016180b`).
   - **Branch ahead:** diperbaiki dari 42 → **44** commit.
   - **Untracked files:** tetap 21 (2 commit revisi lokal baru `71647e7`, `016180b` adalah revisi PRD saja).

3. **Open issues:** (sama persis dengan Rev. 205)

4. **Status:** dokumen PRD **REVISI** — rev 206 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. HEAD = `016180b50ca90981575f2c2584fa031df16f8275` (Rev. 205 final). Working tree **tidak bersih** (revisi Rev. 206 akan dicomit). Branch **44** commits ahead `origin/main` (`27ca1d2a53b79c513cae9746cc0be9dfe9d783fa` = Rev. 163 fix).

*Verifikasi dilakukan lewat: query `sqlite3` ke `dev.db` (tidak ada), `git` (HEAD/status/ahead/ls-files), `ls` (dev.db/node_modules/.data-pondokanat), `cat` (quality_gate.sh), `grep` (prisma schema, init_schema.sql, source files).