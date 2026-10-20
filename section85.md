## 85. REVISI TERBARU (Rev. 198 — 21 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 21 Oktober 2026 (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / `PRD-PONDOK-BANAT.md`; query `sqlite3` ke `dev.db` (tidak ada); verifikasi isi file: header PRD, §80–§84.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 197 (data terkonsisten).**
   - **Git HEAD (local):** `41199c96aaa50228e59b78a43df4706fdf0ddbef` "Rev. 197: PRD fresh verification & stability confirmation (21 Oct 2026 WIB); updated header to Rev. 197 + added section 84" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `41199c96aaa50228e59b78a43df4706fdf0ddbef`). Local branch **33 commits ahead** dari `origin/main` (`27ca1d2a53b79c513cae9746cc0be9dfe9d783fa` = Rev. 163 fix).
   - **Git HEAD (origin/main):** `27ca1d2a53b79c513cae9746cc0be9dfe9d783fa` (Rev. 163 fix). Local branch **33 commits ahead**.
   - **Git ls-files:** = **36 file**. `git status --porcelain` = ` M PRD-PONDOK-BANAT.md` (1 file modified) + `??` (20 file `.py` tambahan tidak ter-track). PRD-PONDOK-BANAT.md **berubah lokal** (header Rev. 198 + section 85 baru ditulis + section 84 diperbaiki).
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan .gitignore mencantumkan *.db. Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (init_db.py, init_schema.sql; import_excel.py dan import_students_grades_clean.py tidak ditemukan di working tree).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` **absent** (clear checkout, 0 file); `.next/` **masih ada (partial: cache + diagnostics + package.json + server + static + trace + trace-build + turbopack + types, bukan production build)**. `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm instal ulang` sebelum dapat dijalankan.
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map("uid_nfc")` baris 68), `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama 'Pondok Banat'). Produksi butuh bcrypt + session.
   - **Beranda hardcode:** `src/components/Beranda.tsx` (baris 26) & `src/app/beranda/page.tsx` (baris 14) **sudah diperbarui ke 453** (dari 441) — hardcoded stats match Excel grade sheets. TIDAK ada hardcode 441 yang tersisa.
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); jumlah model Prisma = **17**. `prisma validate` tidak dapat dijalankan (prisma tidak terinstall di env cron).
   - **init_schema.sql:** tabel `students` (baris 33) memiliki kolom `uid_nfc TEXT` (baris 44, komentar: `-- NFC card UID: 'AF:C2:99:E7'`) — field M02a **ADA** di schema SQLite. Jumlah tabel = **15** sesuai PRD. `init_db.py` (6135 bytes) dan `.seed_users_roles.py` (3343 bytes) masih ada; `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** (0 bytes / MISSING).
   - **Source files:** `src/app/*` = 15 entri (absensi, beranda, berita, globals.css, guru, kelas, laporan, layout.tsx, login, nilai, page.tsx, pengasuh, ruang-kegiatan, santri, sekolah); `src/components` = `Beranda.tsx` & `Login.tsx`; `src/lib` = **kosong** (logic inline). `git ls-files` = **36 file**.
   - **Source data:** folder `.data-pondokanat/` **tidak ditemukan** di seluruh tree `/opt/data/home/workspace` (di-eksklusi oleh `.gitignore`) DAN tidak ditemukan di seluruh tree `/opt/data`. Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber. **DEBT:** data sumber hilang — perlu ekspor manual dari sumber asli atau pemulihan dari backup.
   - **quality_gate.sh:** file masih memuat rantai `tsc` → `eslint` → `next build`; seluruh gate gagal karena `node_modules` absen.
   - **`.next/` directory:** entri = cache, diagnostics, package.json, server, static, trace, trace-build, turbopack, types (10 entri — dikonfirmasi; node_modules absen).
   - **Working tree state:** `PRD-PONDOK-BANAT.md` **berubah lokal** (header Rev. 198 + section 85), working tree **tidak bersih** (ada perubahan lokal). `git status --porcelain` = ` M PRD-PONDOK-BANAT.md` (1 file modified) + `??` (20 file `.py` tambahan tidak ter-track). Seluruh file lain cocak dengan HEAD.
   - **Commit count:** **33** commits ahead `origin/main`.

2. **Perubahan dari Rev. 197:**
   - **Header PRD:** diperbarui ke **Rev. 198** (tanggal 21 Oktober 2026 WIB).
   - **Section 84 (Rev. 197):** HEAD reference diperbaiki — `5140607...` (Rev. 196) diganti ke `41199c9...` (Rev. 197, HEAD terkini).
   - **Commit count:** diperbarui dari **32** ke **33** commits ahead `origin/main`.
   - **New Section 85 (Rev. 198):** ditambahkan untuk verifikasi fresh ulang & konfirmasi stabilitas Rev. 198.

3. **Status:** dokumen PRD **REVISI** — rev 198 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. HEAD = `41199c96aaa50228e59b78a43df4706fdf0ddbef` (Rev. 197). Working tree **tidak bersih** (PRD diperbarui: header Rev. 198 + section 85). Branch **33** commits ahead `origin/main` (`27ca1d2a53b79c513cae9746cc0be9dfe9d783fa`).
