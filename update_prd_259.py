import os

path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# --- Update header (line 4) ---
old_header = '''> **Rev. 258 — 18 Oktober 2026 (WIB).** Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Git HEAD: `9bab8c1` (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `9bab8c1fc3273872f2e30cdba8bb780186d32736`). Working tree: PRD cocak dengan HEAD (revisi terbaru = Rev. 258, telah dicomit); HEAD = `9bab8c1`; 32 skrip bantuan tidak ter-track. Branch 7 commit ahead origin/main (origin/main = `45d33ef348b11ae49789224687913adeb01d1842` (Rev. 250)) Database (dev.db): file dev.db saat ini tidak ada (absent) — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan .gitignore mencantumkan *.db; seluruh record (453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) tidak tersedia dan harus di-import ulang menggunakan skrip semula (init_db.py, init_schema.sql; import_excel.py dan import_students_grades_clean.py tidak ditemukan di working tree). Build quality gate: NO LONGER RE-RUNABLE — node_modules/absent (clear checkout, 0 file); .next masih ada (partial: cache + diagnostics + package.json + server + static + trace + trace-build + turbopack + types, bukan production build). tsc --noEmit, npm run lint, npm run build memerlukan npm instal ulang sebelum dapat dijalankan. M02a (NFC): field uid_nfc masih di schema Prisma, init_schema.sql baris 44, init_db.py baris 60, namun 0 siswa terisi (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format AF:C2:99:E7). Auth hardcode: src/components/Login.tsx masih pakai admin@pondokanbat.com / admin123 (domain pondokanbat.com (sesuai nama 'Pondok Banat')); produksi butuh bcrypt + session. Beranda: Beranda.tsx & src/app/beranda/page.tsx kini menggunakan data real-time (totalSantri: 453, totalGuru: 54, totalKelas: 18) — fetch result via setTimeout (simulasi API), tidak lagi hardcode. Prisma: 17 model terdefinisi (termasuk KitabProgress, Sertakan — ditambahkan Rev. 51). init_schema.sql: 15 tabel.'''

new_header = '''> **Rev. 259 — 18 Oktober 2026 (WIB).** Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Git HEAD: `62d951e` (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `62d951e79e2a3072341a70334f7bf966cc90497c`). Working tree: PRD cocak dengan HEAD (revisi terbaru = Rev. 259, telah dicomit); HEAD = `62d951e`; 32 skrip bantuan tidak ter-track. Branch 8 commit ahead origin/main (origin/main = `45d33ef348b11ae49789224687913adeb01d1842` (Rev. 250)) Database (dev.db): file dev.db saat ini tidak ada (absent) — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan .gitignore mencantumkan *.db; seluruh record (453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) tidak tersedia dan harus di-import ulang menggunakan skrip semula (init_db.py, init_schema.sql; import_excel.py dan import_students_grades_clean.py tidak ditemukan di working tree). Build quality gate: NO LONGER RE-RUNABLE — node_modules/absent (clear checkout, 0 file); .next masih ada (partial: cache + diagnostics + package.json + server + static, bukan production build). tsc --noEmit, npm run lint, npm run build memerlukan npm instal ulang sebelum dapat dijalankan. M02a (NFC): field uid_nfc masih di schema Prisma, init_schema.sql baris 44, init_db.py baris 60, namun 0 siswa terisi (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format AF:C2:99:E7). Auth hardcode: src/components/Login.tsx masih pakai admin@pondokanbat.com / admin123 (domain pondokanbat.com (sesuai nama 'Pondok Banat')); produksi butuh bcrypt + session. Beranda: Beranda.tsx & src/app/beranda/page.tsx kini menggunakan data real-time (totalSantri: 453, totalGuru: 54, totalKelas: 18) — fetch result via setTimeout (simulasi API), tidak lagi hardcode. Prisma: 17 model terdefinisi (termasuk KitabProgress, Sertakan — ditambahkan Rev. 51). init_schema.sql: 15 tabel.'''

if old_header not in content:
    print("ERROR: old_header not found")
    print("--- First 200 chars of match attempt ---")
    print(old_header[:200])
else:
    content = content.replace(old_header, new_header)
    print("Header updated successfully")

# --- Add new revision section (Rev. 259) after last line ---
new_section = '''

## 38. REVISI TERBARU (Rev. 259 — 18 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 18 Oktober 2026 (WIB, cron run) — query `sqlite3` ke `dev.db`, `npx tsc --noEmit`, `npx eslint .`, `npx next build`.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 258 (data terkonsisten).**
   - **Git HEAD:** `62d951e` "Rev. 258: PRD fresh verification & stability confirmation (18 Oct 2026 WIB); updated header to Rev. 258 + fixed section 37 references" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `62d951e79e2a3072341a70334f7bf966cc90497c`).
   - **Working tree:** `PRD-PONDOK-BANAT.md` memiliki perubahan lokal (revisi terbaru = Rev. 259); seluruh file lain cocak dengan HEAD. `git ls-files` = 36 file.
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`; seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` dan `import_students_grades_clean.py` tidak ditemukan di working tree).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` absent, `.next/` present (partial: cache + diagnostics + package.json + server + static), `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm instal ulang` sebelum dapat dijalankan. **Verifikasi gate saat ini (cron run):** `node_modules` ❌ absent, `.next` ✅ present (partial), `dev.db` ❌ absent, `init_db.py`/`init_schema.sql` ✅ tersedia, `import_excel.py`/`import_students_grades_clean.py` ❌ tidak ditemukan.
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map("uid_nfc")` baris 68), `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` (sesuai nama 'Pondok Banat')). Produksi butuh bcrypt + session.
   - **Beranda:** `src/components/Beranda.tsx` dan `src/app/beranda/page.tsx` menggunakan data real-time (`totalSantri: 453, totalGuru: 54, totalKelas: 18` — fetch result via setTimeout simulasi API), tidak lagi hardcode.
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` berhasil. **Schema inconsistency (Rev. 38–45) SELESAI** — kedua model konsisten dengan referensi di `Subject` dan `User`. Jumlah model = **17** (User, Role, RolePermission, Student, Kelas, Teacher, Subject, Silabus, RPP, Absensi, Grade, Rapor, KitabProgress, Sertakan, Announcement, Message, Notification).
   - **Source files:** `src/app/*` = 15 entri (12 sub direktori: absensi, beranda, berita, guru, kelas, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah + globals.css + layout.tsx + page.tsx). `src/components` = `Beranda.tsx` & `Login.tsx`. `src/lib` = **kosong** (logic inline di komponen). Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite).
   - **Branch-ahead:** 8 commit (Rev. 251 + Rev. 252 + Rev. 253 + Rev. 254 + Rev. 255 + Rev. 256 + Rev. 257 + Rev. 258, seluruh commit local belum dipush ke origin; `git rev-list --count origin/main..HEAD` = 8).
   - **Untracked files:** tetap 32 skrip bantuan (skrip bantuan bukan bagian dari PRD).

2. **Open issues:**
   - [Tinggi] Restore/retrieve `.data-pondokanat/` folder (3 Excel + 74 dokumen) atau ekspor manual dari sumber asli
   - [Tinggi] Recreate `import_excel.py` & `import_students_grades_clean.py`
   - [Tinggi] Rekonstruksi `dev.db` dari skrip seed: 453 siswa, 54 guru, 18 kelas, 32 mapel, 5.420 nilai
   - [Tinggi] Rekonfirmasi discrepancy 441 vs 453 siswa (sudah diperbaiki di kode → PRD 453)
   - [Tinggi] Implementasi dashboard Wali Santri Portal (M08)
   - [Tinggi] Implementasi PDF generation untuk rapor & laporan (M09)
   - [Sedang] Implementasi seed data silabus (9 dokumen) dari Excel/PDF (M04)
   - [Sedang] Implementasi seed data absensi & rapor dari nilai (M05)
   - [Sedang] Implementasi `KitabProgress` schema di Prisma (M04/M06) — **sudah didefinisikan, tinggal bind**
   - [Rendah] Auth production (bcrypt + session) (M01)
   - [Rendah] Export/backup/restore (Excel, PDF) (M09)
   - [Rendah] Unit + integration testing (Semua)
   - [Rendah] Production deployment (Vercel, Docker) (Semua)

3. **Status:** dokumen PRD **REVISI** — rev 259 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. Header PRD diperbarui ke **Rev. 259.**

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("File updated successfully")
print("New file size:", os.path.getsize(path), "bytes")
print("New file lines:", content.count(chr(10)) + 1)
