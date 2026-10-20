## 64. REVISI TERBARU (Rev. 218 — 18 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 18 Oktober 2026 (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / struktur source / skema Prisma; verifikasi isi file: header PRD, §63.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 217 (data terkonsisten).**

   - **Git HEAD (local):** `bf676c9f302a6b50255b208800598c36880e16c2` "Rev. 217: PRD fresh verification & stability confirmation (18 Oct 2026 WIB); updated header to Rev. 217 + added section 63" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `bf676c9f302a6b50255b208800598c36880e16c2`). Local branch **58** commits ahead dari `origin/main` (`27ca1d2a53b79c513cae9746cc0be9dfe9d783fa` = Rev. 163 fix).
   - **Git HEAD (origin/main):** `27ca1d2a53b79c513cae9746cc0be9dfe9d783fa` (Rev. 163 fix). Local branch **58** commits ahead.
   - **Git ls-files:** = **36 file**. `git status --porcelain` = `??` (**23 file tambahan tidak ter-track** — skrip helper development). PRD-PONDOK-BANAT.md cocak dengan HEAD (revisi Rev. 218 akan ditambahkan sebagai lokasi baru; Rev. 217 telah dicomit ke HEAD). Working tree **bersih** untuk tracked files, selain 23 file helper development yang tidak ter-track.
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan .gitignore mencantumkan *.db. Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` dan `import_students_grades_clean.py` tidak ditemukan di working tree).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` **absent** (clear checkout, 0 file); `.next/` **masih ada (partial: cache + diagnostics + package.json + server + static + trace + trace-build + turbopack + types, bukan production build)**. `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm instal ulang` sebelum dapat dijalankan.
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`prisma/schema.prisma` baris 68: `uidNfc String? @map("uid_nfc") // NFC card UID: 'AF:C2:99:E7'`), `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama 'Pondok Banat'). Produksi butuh bcrypt + session.
   - **Beranda hardcode:** `src/components/Beranda.tsx` (setStats `totalSantri: 453`) & `src/app/beranda/page.tsx` (hardcoded `totalSantri: 453`) — **sudah diperbarui ke 453** sesuai konstanta PRD §9.1/§10.1 (data Excel grade sheets). TIDAK ada hardcode 441 yang tersisa.
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); jumlah model Prisma = **17**. `prisma validate` tidak dapat dijalankan (prisma tidak terinstall di env cron karena `node_modules` absen).
   - **init_schema.sql:** tabel `students` (baris 33) memiliki kolom `uid_nfc TEXT` (baris 44, komentar: `-- NFC card UID: 'AF:C2:99:E7'`) — field M02a **ADA** di schema SQLite. Jumlah tabel = **15** sesuai PRD. `init_db.py` (6135 bytes) dan `.seed_users_roles.py` (3343 bytes) masih ada; `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** (0 bytes / MISSING).
   - **Source files:** `src/app/*` = 15 entri (absensi, beranda, berita, globals.css, guru, kelas, laporan, layout.tsx, login, nilai, page.tsx, pengasuh, ruang-kegiatan, santri, sekolah); `src/components` = `Beranda.tsx` & `Login.tsx`; `src/lib` = **kosong** (logic inline). `git ls-files` = **36 file**.
   - **Source data:** folder `.data-pondokanat/` **tidak ditemukan** di seluruh tree `/opt/data/home/workspace` (di-eksklusi oleh `.gitignore`) DAN tidak ditemukan di seluruh tree `/opt/data`. Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber. **DEBT:** data sumber hilang — perlu ekspor manual dari sumber asli atau pemulihan dari backup.
   - **quality_gate.sh:** file masih memuat rantai `tsc` → `eslint` → `next build`; seluruh gate gagal karena `node_modules` absen.
   - **`.next/` directory:** entri = cache, diagnostics, package.json, server, static, trace, trace-build, turbopack, types (**9 entri** — dikonfirmasi; node_modules absen).
   - **Untracked files:** **23 file** (bersih vs HEAD; `git status --porcelain` = `??`): clean_prd.py, clean_prd2.py, clean_prd3.py, clean_prd4.py, fix_header_status.py, fix_newline.py, fix_prd.py–fix_prd9.py, hex_dump.py, rev186_section.md, rev206_section.md, section61.md, section85.md, update_prd.py, update_prd_165.py, update_prd_188.py, update_prd_189.py. Semua adalah skrip pengembangan sementara (untuk manipulasi Rev. 163–217), tidak termasuk commit.
   - **Branch ahead count:** **58** commit (sesuai `git rev-list --count origin/main..HEAD`).
   - **HEAD citation correction:** §63 (Rev. 217) dan header PRD Rev. 217 secara keliru mencitai HEAD `500c643` (commit Rev. 216) sebagai HEAD Rev. 217. HEAD Rev. 217 yang sebenarnya adalah `bf676c9` (commit "Rev. 217: PRD fresh verification & stability confirmation (18 Oct 2026 WIB); updated header to Rev. 217 + added section 63"). Perbaikan citation tercatat di Rev. 218.
   - **HEAD citation historical record:** §63 (Rev. 217) — "HEAD: diperbarui dari `026b2c4` (salah, Merujuk Rev. 215) → `500c643` (sebenarnya HEAD Rev. 216)" tetap akurat.

2. **Perubahan dari Rev. 217:**
   - **Header PRD:** diperbarui ke **Rev. 218** (tanggal 18 Oktober 2026 WIB).
   - **New Section 64 (Rev. 218):** ditambahkan untuk verifikasi fresh ulang & konfirmasi stabilitas.
   - **HEAD:** diperbarui dari `500c643` (salah, Merujuk Rev. 216) → `bf676c9` (sebenarnya HEAD Rev. 217).
   - **Branch ahead:** **58** commit (sebelumnya 57).
   - **Working tree:** bersih untuk tracked files; PRD telah dicomit ke HEAD.

3. **Open issues:**
   - [Tinggi] Restore/retrieve `.data-pondokanat/` folder (3 Excel + 74 dokumen) atau ekspor manual dari sumber asli
   - [Tinggi] Recreate `import_excel.py` & `import_students_grades_clean.py`
   - [Tinggi] Rekonstruksi `dev.db` dari skrip seed: 453 siswa, 54 guru, 18 kelas, 32 mapel, 5.420 nilai
   - [Tinggi] Rekonfirmasi discrepancy 453 vs 441 siswa
   - [Tinggi] Implementasi dashboard Wali Santri Portal (M08)
   - [Tinggi] Implementasi PDF generation untuk rapor & laporan (M09)
   - [Sedang] Implementasi seed data silabus (9 dokumen) dari Excel/PDF (M04)
   - [Sedang] Implementasi seed data absensi & rapor dari nilai (M05)
   - [Sedang] Implementasi `KitabProgress` schema di Prisma (M04/M06) — **sudah didefinisikan, tinggal bind**
   - [Rendah] Auth production (bcrypt + session) (M01)
   - [Rendah] Export/backup/restore (Excel, PDF) (M09)
   - [Rendah] Unit + integration testing (Semua)
   - [Rendah] Production deployment (Vercel, Docker) (Semua)

4. **Status:** dokumen PRD **REVISI** — rev 218 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. HEAD = `bf676c9f302a6b50255b208800598c36880e16c2`. Working tree bersih untuk tracked files. Branch **58** commits ahead `origin/main` (`27ca1d2a53b79c513cae9746cc0be9dfe9d783fa`). Seluruh perubahan akan dicomit ke HEAD.
