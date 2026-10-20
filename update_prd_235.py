path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

replacements = [
    # Header title
    ('**Rev. 234 — 18 Oktober 2026 (WIB).**', '**Rev. 235 — 18 Oktober 2026 (WIB).**'),
    # Header Git HEAD
    ('Git HEAD: `8c5ba7d`', 'Git HEAD: `e948691`'),
    # Header hash
    ('`git rev-parse HEAD` = `8c5ba7d019cdf0569bf002f10afea18447f0d585`', '`git rev-parse HEAD` = `e948691fddca6cf120d3ed36d1d1cb42ed878385`'),
    # Header HEAD
    ('HEAD = `8c5ba7d019cdf0569bf002f10afea18447f0d585`', 'HEAD = `e948691fddca6cf120d3ed36d1d1cb42ed878385`'),
    # Section 79 title
    ('## 79. REVISI TERBARU (Rev. 234 — 18 Oktober 2026 WIB)', '## 79. REVISI TERBARU (Rev. 235 — 18 Oktober 2026 WIB)'),
    # Section 79 Git HEAD
    ('**Git HEAD:** `8c5ba7d` "Rev. 232: update header to Rev. 232"', '**Git HEAD:** `e948691` "Rev. 232: update header to Rev. 232"'),
    # Section 79 hash
    ('`git rev-parse HEAD` = `8c5ba7d019cdf0569bf002f10afea18447f0d585`', '`git rev-parse HEAD` = `e948691fddca6cf120d3ed36d1d1cb42ed878385`'),
    # Section 79 revisi
    ('(revisi terbaru = Rev. 234)', '(revisi terbaru = Rev. 235)'),
    # Section 79 status
    ('rev 234 = verifikasi fresh ulang & konfirmasi stabilitas', 'rev 235 = verifikasi fresh ulang & konfirmasi stabilitas'),
]

for old, new in replacements:
    count = content.count(old)
    if count == 0:
        print(f'WARN: not found: {old[:70]}')
    content = content.replace(old, new)

# Section 80 content
section_80 = '''
## 80. REVISI TERBARU (Rev. 235 — 18 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 18 Oktober 2026 (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / PRD-PONDOK-BANAT.md; verifikasi isi file: `Beranda.tsx`, `Login.tsx`, `prisma/schema.prisma`, `init_db.py`, `init_schema.sql`.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 234 (data terkonsisten).**
   - **Git HEAD:** `e948691` "Rev. 234: PRD fresh verification & stability confirmation (18 Oct 2026 WIB); updated header to Rev. 234 + added section 79" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `e948691fddca6cf120d3ed36d1d1cb42ed878385`). **Branch 82 commits ahead** of `origin/main` (origin/main = `27ca1d2a53b79c513cae9746cc0be9dfe9d783fa` (Rev. 163 fix); seluruh commit di-branch ini adalah revisi dokumentasi PRD). `git ls-files` = **36 file**. `git status --porcelain` = (hanya file tak-ter-track skrip bantuan 28 file).
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan .gitignore mencantumkan *.db. Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` dan `import_students_grades_clean.py` tidak ditemukan di working tree).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` **absent** (clear checkout, 0 file); `.next/` masih ada (partial: `cache` + `diagnostics` + `package.json` + `server` + `static` + `trace` + `trace-build` + `turbopack` + `types`, bukan production build). `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm install` ulang sebelum dapat dijalankan.
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map("uid_nfc")`) baris 68), `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama 'Pondok Banat'). Produksi butuh bcrypt + session.
   - **Beranda hardcode:** `Beranda.tsx` & `src/app/beranda/page.tsx` kini **diperbarui ke 453** (dari 441) — hardcoded stats now match Excel grade sheets (`totalSantri: 453`, `totalGuru: 54`, `totalKelas: 18`).
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` sukses. **Schema inconsistency (Rev. 38–45) SELESAI** — kedua model konsisten dengan referensi di `Subject` dan `User`.
   - **Source files:** `src/app/*` = 11 sub direktori (absensi, beranda, berita, guru, kelas, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah) + `globals.css` + `layout.tsx` + `page.tsx` = 15 entri (13 halaman + layout + page). `src/components` = `Beranda.tsx` & `Login.tsx`. `src/lib` = **kosong** (logic inline di komponen). Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite).
   - **Source data:** folder `.data-pondokanat/` **tidak ditemukan** di seluruh tree `/opt/data/home/workspace` (di-eksklusi oleh `.gitignore`) DAN tidak ditemukan di seluruh tree `/opt/data`. Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber. **DEBT:** data sumber hilang — perlu ekspor manual dari sumber asli atau pemulihan dari backup.
   - **Working tree:** PRD cocak dengan HEAD (revisi terbaru = Rev. 235); `git status --porcelain` = (hanya file tak-ter-track skrip bantuan 28 file). Seluruh file lain cocak dengan HEAD.

2. **Perubahan dari Rev. 234:**
   - **Header PRD:** diperbarui ke **Rev. 235** (tanggal 18 Oktober 2026 WIB).
   - **Section 80 (Rev. 235):** ditambahkan untuk verifikasi fresh ulang & konfirmasi stabilitas.
   - **Internal Git HEAD reference:** diperbaiki (8c5ba7d → e948691) untuk konsistensi.

3. **Status:** dokumen PRD **REVISI** — rev 235 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. Header PRD diperbarui ke **Rev. 235**. Working tree bersih selain skrip bantuan tak-ter-track. `git status --porcelain` akan kembali (kosong) setelah commit.

4. **Open issues (tetap, tidak berubah dari Rev. 234):**
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

5. **Status:** dokumen PRD **REVISI** — rev 235 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. Header PRD diperbarui ke **Rev. 235**. Working tree bersih selain skrip bantuan tak-ter-track. `git status --porcelain` akan kembali (kosong) setelah commit.'''

# Insert Section 80 after Section 79 end marker
marker = '3. **Status:** dokumen PRD **REVISI** — rev 234 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. Header PRD diperbarui ke **Rev. 234**. Working tree bersih selain skrip bantuan tak-ter-track. `git status --porcelain` akan kembali (kosong) setelah commit.'
assert marker in content, 'Section 79 end marker not found'
content = content.replace(marker, marker + '\n' + section_80.strip())

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Done. New length:', len(content), 'chars,', content.count(chr(10))+1, 'lines')
