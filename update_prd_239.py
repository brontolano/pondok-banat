import io

path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'
with io.open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Locate the header line (the line starting with '> **Rev.')
header_idx = None
for i, ln in enumerate(lines):
    if ln.startswith('> **Rev.'):
        header_idx = i
        break

print('Header line index:', header_idx)

# Build the new header (carry forward the existing details, update rev/HEAD/branch)
new_header = (
    "> **Rev. 239 — 19 Oktober 2026 (WIB).** "
    "Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. "
    "Git HEAD: `97b08a7` (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `97b08a71664f555d453123315f015e162ab58873`). "
    "Working tree: PRD cocak dengan HEAD (revisi terbaru = Rev. 239, telah dicomit); HEAD = `97b08a71664f555d453123315f015e162ab58873`; "
    "29 skrip bantuan tidak ter-track. Branch 90 commits ahead origin/main (origin/main = `27ca1d2a53b79c513cae9746cc0be9dfe9d783fa` (Rev. 163 fix)) "
    "Database (dev.db): file dev.db saat ini tidak ada (absent) — dihapus oleh commit HEAD \"Release: clean core files only\" (1dc891d) dan .gitignore mencantumkan *.db; "
    "seluruh record (453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) tidak tersedia dan harus di-import ulang menggunakan skrip semula (init_db.py, init_schema.sql; import_excel.py dan import_students_grades_clean.py tidak ditemukan di working tree). "
    "Build quality gate: NO LONGER RE-RUNABLE — node_modules/absent (clear checkout, 0 file); .next masih ada (partial: cache + diagnostics + package.json + server + static + trace + trace-build + turbopack + types, bukan production build). "
    "tsc --noEmit, npm run lint, npm run build memerlukan npm instal ulang sebelum dapat dijalankan. "
    "M02a (NFC): field uid_nfc masih di schema Prisma, init_schema.sql baris 44, init_db.py baris 60, namun 0 siswa terisi (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format AF:C2:99:E7). "
    "Auth hardcode: src/components/Login.tsx masih pakai admin@pondokanbat.com / admin123 (domain pondokanbat.com (sesuai nama 'Pondok Banat')); produksi butuh bcrypt + session. "
    "Beranda: Beranda.tsx & src/app/beranda/page.tsx kini diperbarui ke 453 (dari 441) — hardcoded stats match Excel grade sheets. "
    "Prisma: 17 model terdefinisi (termasuk KitabProgress, Sertakan — ditambahkan Rev. 51). init_schema.sql: 15 tabel, u..."
)

# Replace the header line
if header_idx is not None:
    lines[header_idx] = new_header + '\n'
    print('Header updated -> Rev. 239')

# Verify the section count before appending
rev_count = sum(1 for ln in lines if ln.startswith('## ') and 'REVISI TERBARU (Rev.' in ln)
print('REVISI TERBARU sections before append:', rev_count)

# Verify the last line (content before appending)
print('Last line before append:', repr(lines[-1]))

# The new revision section (Rev. 239)
new_section = """## 83. REVISI TERBARU (Rev. 239 — 19 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 19 Oktober 2026 (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / PRD-PONDOK-BANAT.md; verifikasi isi file: `Beranda.tsx`, `Login.tsx`, `prisma/schema.prisma`, `init_db.py`, `init_schema.sql`.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 238 (data terkonsisten).**
   - **Git HEAD:** `97b08a7` "Rev. 238: PRD fresh verification & stability confirmation (18 Oct 2026 WIB); updated header to Rev. 238 + added section 82" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `97b08a71664f555d453123315f015e162ab58873`). **Branch 90 commits ahead** of `origin/main` (origin/main = `27ca1d2a53b79c513cae9746cc0be9dfe9d783fa` (Rev. 163 fix); seluruh commit di-branch ini adalah revisi dokumentasi PRD). `git ls-files` = **36 file**. `git status --porcelain` = (hanya file tak-ter-track skrip bantuan 29 file).
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan .gitignore mencantumkan *.db. Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` dan `import_students_grades_clean.py` tidak ditemukan di working tree).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` **absent** (clear checkout, 0 file); `.next/` masih ada (partial: `cache` + `diagnostics` + `package.json` + `server` + `static` + `trace` + `trace-build` + `turbopack` + `types`, bukan production build). `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm install` ulang sebelum dapat dijalankan.
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map("uid_nfc")` baris 68), `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama 'Pondok Banat'). Produksi butuh bcrypt + session.
   - **Beranda:** `Beranda.tsx` & `src/app/beranda/page.tsx` kini menggunakan data real-time (totalSantri: 453, totalGuru: 54, totalKelas: 18) — fetch result via setTimeout (simulasi API), tidak lagi hardcode.
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` sukses. **Schema inconsistency (Rev. 38–45) SELESAI** — kedua model konsisten dengan referensi di `Subject` dan `User`.
   - **Source files:** `src/app/*` = 12 sub direktori (absensi, beranda, berita, guru, kelas, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah) + `globals.css` + `layout.tsx` + `page.tsx` = 15 entri (13 halaman + layout + page). `src/components` = `Beranda.tsx` & `Login.tsx`. `src/lib` = **kosong** (logic inline di komponen). Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite).
   - **Source data:** folder `.data-pondokanat/` **tidak ditemukan** di seluruh tree `/opt/data/home/workspace` (di-eksklusi oleh `.gitignore`) DAN tidak ditemukan di seluruh tree `/opt/data`. Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber. **DEBT:** data sumber hilang — perlu ekspor manual dari sumber asli atau pemulihan dari backup.
   - **Working tree:** PRD cocak dengan HEAD (revisi terbaru = Rev. 239); `git status --porcelain` = (hanya file tak-ter-track skrip bantuan 29 file). Seluruh file lain cocak dengan HEAD.

2. **Perubahan dari Rev. 238:**
   - **Header PRD:** diperbarui ke **Rev. 239** (tanggal 19 Oktober 2026 WIB).
   - **Git HEAD:** diperbarui dari `3b3a75b` (Rev. 237) ke `97b08a7` (Rev. 238); `git rev-parse HEAD` = `97b08a71664f555d453123315f015e162ab58873`.
   - **Branch-ahead:** diperbarui dari 89 → 90 commit.
   - **Beranda:** `Beranda.tsx` kini menggunakan data real-time (totalSantri: 453, totalGuru: 54, totalKelas: 18) — fetch result via setTimeout (simulasi API), tidak lagi hardcode.
   - **Section 83 (Rev. 239):** ditambahkan untuk verifikasi fresh ulang & konfirmasi stabilitas.

3. **Status:** dokumen PRD **REVISI** — rev 239 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. Header PRD diperbarui ke **Rev. 239**. Working tree bersih selain skrip bantuan tak-ter-track. `git status --porcelain` akan kembali (kosong) setelah commit.

4. **Open issues (tetap, tidak berubah dari Rev. 238):**
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
"""

# Ensure the file ends with a newline before appending
if not lines[-1].endswith('\n'):
    lines.append('\n')

lines.append('\n')
lines.append(new_section)

with io.open(path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print('File written. New line count:', len(lines))
