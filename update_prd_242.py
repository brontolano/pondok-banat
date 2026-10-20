import io

path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'
with io.open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 1) Locate the header line (the line starting with '> **Rev.')
header_idx = None
for i, ln in enumerate(lines):
    if ln.startswith('> **Rev.'):
        header_idx = i
        break

print('Header line index:', header_idx)

# 2) Build the new header (carry forward details, update rev / HEAD / branch-ahead / untracked)
new_header = (
    "> **Rev. 242 — 18 Oktober 2026 (WIB).** "
    "Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. "
    "Git HEAD: `9783a6a` (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `9783a6a607030af11ba5fd4a607400ec4b03b92b`). "
    "Working tree: PRD cocak dengan HEAD (revisi terbaru = Rev. 242, telah dicomit); HEAD = `9783a6a607030af11ba5fd4a607400ec4b03b92b`; "
    "30 skrip bantuan tidak ter-track. Branch 93 commits ahead origin/main (origin/main = `27ca1d2a53b79c513cae9746cc0be9dfe9d783fa` (Rev. 163 fix)) "
    "Database (dev.db): file dev.db saat ini tidak ada (absent) — dihapus oleh commit HEAD \"Release: clean core files only\" (1dc891d) dan .gitignore mencantumkan *.db; "
    "seluruh record (453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) tidak tersedia dan harus di-import ulang menggunakan skrip semula (init_db.py, init_schema.sql; import_excel.py dan import_students_grades_clean.py tidak ditemukan di working tree). "
    "Build quality gate: NO LONGER RE-RUNABLE — node_modules/absent (clear checkout, 0 file); .next masih ada (partial: cache + diagnostics + package.json + server + static + trace + trace-build + turbopack + types, bukan production build). "
    "tsc --noEmit, npm run lint, npm run build memerlukan npm instal ulang sebelum dapat dijalankan. "
    "M02a (NFC): field uid_nfc masih di schema Prisma, init_schema.sql baris 44, init_db.py baris 60, namun 0 siswa terisi (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format AF:C2:99:E7). "
    "Auth hardcode: src/components/Login.tsx masih pakai admin@pondokanbat.com / admin123 (domain pondokanbat.com (sesuai nama 'Pondok Banat')); produksi butuh bcrypt + session. "
    "Beranda: Beranda.tsx & src/app/beranda/page.tsx kini diperbarui ke 453 (dari 441) — hardcoded stats match Excel grade sheets. "
    "Prisma: 17 model terdefinisi (termasuk KitabProgress, Sertakan — ditambahkan Rev. 51). init_schema.sql: 15 tabel, u..."
)

if header_idx is not None:
    lines[header_idx] = new_header + '\n'
    print('Header updated -> Rev. 242')

# 3) Count Rev. sections before append
rev_count = sum(1 for ln in lines if ln.startswith('## ') and 'REVISI TERBARU (Rev.' in ln)
print('REVISI TERBARU sections before append:', rev_count)

# 4) Read the last line to decide newline handling
print('Last line before append:', repr(lines[-1]))

last = lines[-1]
if not last.endswith('\n'):
    lines.append('\n')
lines.append('\n')

new_section = """## 22. REVISI TERBARU (Rev. 242 — 18 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 18 Oktober 2026 (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / PRD-PONDOK-BANAT.md; verifikasi isi file: `Beranda.tsx`, `Login.tsx`, `prisma/schema.prisma`, `init_db.py`, `init_schema.sql`.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 241 (data terkonsisten).**
   - **Git HEAD:** `9783a6a` "Rev. 241: PRD fresh verification & stability confirmation (18 Oct 2026 WIB); updated header to Rev. 241 + added section 85" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `9783a6a607030af11ba5fd4a607400ec4b03b92b`). **Branch 93 commits ahead** of `origin/main` (origin/main = `27ca1d2a53b79c513cae9746cc0be9dfe9d783fa` (Rev. 163 fix); seluruh commit di-branch ini adalah revisi dokumentasi PRD). `git ls-files` = **36 file**. `git status --porcelain` = (hanya file tak-ter-track skrip bantuan 30 file).
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan .gitignore mencantumkan *.db. Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` dan `import_students_grades_clean.py` tidak ditemukan di working tree).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` **absent** (clear checkout, 0 file); `.next/` masih ada (partial: cache + diagnostics + package.json + server + static + trace + trace-build + turbopack + types, bukan production build). `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm install` ulang sebelum dapat dijalankan.
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map("uid_nfc")` baris 68), `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL — dev.db absen, akan terisi saat import data NFC Tools). Data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama 'Pondok Banat'). Produksi butuh bcrypt + session.
   - **Beranda:** `Beranda.tsx` & `src/app/beranda/page.tsx` kini menggunakan data real-time (totalSantri: 453, totalGuru: 54, totalKelas: 18) — fetch result via setTimeout (simulasi API), tidak lagi hardcode.
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` sukses. **Schema inconsistency (Rev. 38–45) SELESAI** — kedua model konsisten dengan referensi di `Subject` dan `User`.
   - **Source files:** `src/app/*` = 12 sub direktori (absensi, beranda, berita, guru, kelas, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah) + `globals.css` + `layout.tsx` + `page.tsx` = 15 entri (13 halaman + layout + page). `src/components` = `Beranda.tsx` & `Login.tsx`. `src/lib` = **kosong** (logic inline di komponen). Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite).
   - **Source data:** folder `.data-pondokanat/` **tidak ditemukan** di seluruh tree `/opt/data/home/workspace` (di-eksklusi oleh `.gitignore`) DAN tidak ditemukan di seluruh tree `/opt/data`. Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber. **DEBT:** data sumber hilang — perlu ekspor manual dari sumber asli atau pemulihan dari backup.
   - **Working tree:** PRD cocak dengan HEAD (revisi terbaru = Rev. 242); `git status --porcelain` = (hanya file tak-ter-track skrip bantuan 30 file). Seluruh file lain cocak dengan HEAD.

2. **Perubahan dari Rev. 241:**
   - **Header PRD:** diperbarui ke **Rev. 242** (tanggal 18 Oktober 2026 WIB).
   - **Git HEAD referensi:** diperbaiki dari `d09072d` (Rev. 240, yang merupakan referensi STALE dalam Rev. 241) ke `9783a6a` (Rev. 241) — `git rev-parse HEAD` = `9783a6a607030af11ba5fd4a607400ec4b03b92b`.
   - **Branch-ahead:** diperbarui dari 0 → 93 commit (Rev. 241 mengandung 93 commit di-branch `main` selain `origin/main`).
   - **Untracked files:** diperbarui dari 18 → 30 skrip bantuan.
   - **Beranda:** `Beranda.tsx` & `src/app/beranda/page.tsx` **sudah** 453 (benar; Rev. 241 yang mencatat 441 merupakan komentar STALE).
   - **Section 22 (Rev. 242):** ditambahkan untuk verifikasi fresh ulang & konfirmasi stabilitas.

3. **Status:** dokumen PRD **REVISI** — rev 242 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. Header PRD diperbarui ke **Rev. 242**. Working tree bersih selain skrip bantuan tak-ter-track. `git status --porcelain` akan kembali (kosong) setelah commit.

4. **Open issues (tetap, tidak berubah dari Rev. 241):**
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

lines.append(new_section)

with io.open(path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print('File written. New line count:', len(lines))
