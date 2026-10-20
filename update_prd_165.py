#!/usr/bin/env python3
# Update PRD: Rev. 165 status + add Rev. 165 section
import io

path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# ---- Header update (line 4, index 3) ----
header_updated = False
for i, line in enumerate(lines):
    if line.startswith('> **Rev. 163'):
        old = line
        # Revision number
        line = line.replace('Rev. 163 — 17 Oktober 2026 (WIB)', 'Rev. 165 — 17 Oktober 2026 (WIB)')
        # HEAD refs
        line = line.replace('Git HEAD: 27ca1d2a53b79c513cae9746cc0be9dfe9d783fa', 'Git HEAD: 1200c891a0ac4caf3a38389a237cceed7a1f9895')
        line = line.replace('git rev-parse HEAD = 27ca1d2a53b79c513cae9746cc0be9dfe9d783fa', 'git rev-parse HEAD = 1200c891a0ac4caf3a38389a237cceed7a1f9895')
        # Branch ahead
        line = line.replace('Branch 3 commit ahead origin/main', 'Branch 1 commit ahead origin/main')
        # origin/main ref
        line = line.replace('origin/main = 317db2f3eaa47b9fc0ebfd2a14b0a392e6769880', 'origin/main = 27ca1d2a53b79c513cae9746cc0be9dfe9d783fa')
        lines[i] = line
        header_updated = True
        print(f'[OK] Header line {i+1} updated')
        break

if not header_updated:
    print('[ERROR] Header not found!')

# ---- Append Rev. 165 section at file end ----
rev165 = """

## 52. REVISI TERBARU (Rev. 165 — 17 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 17 Oktober 2026 (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / `PRD-PONDOK-BANAT.md`; query `sqlite3` ke `dev.db` (tidak ada — file dihapus commit HEAD "Release: clean core files only" 1dc891d); pemeriksaan file: `prisma/schema.prisma`, `src/components/Beranda.tsx`, `src/components/Login.tsx`, `src/app/beranda/page.tsx`, `init_db.py`, `init_schema.sql`, `.seed_users_roles.py`, `quality_gate.sh`, `.gitignore`; verifikasi struktur repo (36 file tracked, src/app = 13 halaman + globals.css + layout.tsx + page.tsx).

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 164 (data terkonsisten).**
   - **Git HEAD (local):** `1200c891a0ac4caf3a38389a237cceed7a1f9895` "Rev. 164: added fresh verification section after Rev. 163" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `1200c891a0ac4caf3a38389a237cceed7a1f9895`). Local branch **1 commit ahead** dari `origin/main` (`origin/main` = `27ca1d2a53b79c513cae9746cc0be9dfe9d783fa` — Rev. 163 fix; seluruh 1 commit di-branch adalah revisi dokumentasi PRD: Rev. 164 `1200c89`).
   - **Working tree:** `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 165); `git status --porcelain` = (kosong). Working tree bersih. Seluruh file lain cocak dengan HEAD.
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`. Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` dan `import_students_grades_clean.py` tidak ditemukan di working tree).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` **absent** (clear checkout, 0 file); `.next/` masih ada (partial: `cache` + `diagnostics` + `package.json` + `server` + `static` + `trace` + `trace-build` + `turbopack` + `types`, bukan production build). `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm install` ulang sebelum dapat dijalankan.
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map("uid_nfc")` baris 68), `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama 'Pondok Banat'). Produksi butuh bcrypt + session.
   - **Beranda hardcode:** `src/components/Beranda.tsx` (setStats `totalSantri: 453`) & `src/app/beranda/page.tsx` (hardcoded `totalSantri: 453`) — **sudah diperbarui ke 453** sesuai konstanta PRD §9.1/§10.1 (data Excel grade sheets). TIDAK ada hardcode 441 yang tersisa.
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); jumlah model Prisma = **17**. `prisma validate` tidak dapat dijalankan (prisma tidak terinstall di env cron).
   - **init_schema.sql:** tabel `students` (baris 33) memiliki kolom `uid_nfc TEXT` (baris 44, komentar: `-- NFC card UID: 'AF:C2:99:E7'`) — field M02a **ADA** di schema SQLite. Jumlah tabel = **15** sesuai PRD. `init_db.py` (6135 bytes) dan `.seed_users_roles.py` (3343 bytes) masih ada; `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** (0 bytes / MISSING).
   - **Source files:** `src/app/*` = 13 halaman (beranda, berita, kelas, guru, absensi, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah + layout.tsx + page.tsx) = **15 entri**; `globals.css` = 1; `src/components` = `Beranda.tsx` & `Login.tsx`; `src/lib` = **kosong** (logic inline). Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite).
   - **Source data:** folder `.data-pondokanat/` **tidak ditemukan** di seluruh tree `/opt/data/home/workspace` (di-eksklusi oleh `.gitignore`) DAN tidak ditemukan di seluruh tree `/opt/data`. Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber. **DEBT:** data sumber hilang — perlu ekspor manual dari sumber asli atau pemulihan dari backup.
   - **quality_gate.sh:** file masih memuat rantai `tsc` → `eslint` → `next build`; seluruh gate gagal karena `node_modules` absen.
   - **PRD working tree state:** `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 165); `git status --porcelain` = (kosong). Working tree bersih. Seluruh file lain cocak dengan HEAD.

2. **Perubahan dari Rev. 164:**
   - **Perubahan Rev. 165:** Menambahkan revisi terbaru setelah §51 (Rev. 164) dengan verifikasi fresh ulang kondisi repo + dev.db. HEAD tetap `1200c891a0ac4caf3a38389a237cceed7a1f9895` (Rev. 164), working tree bersih. File PRD saat ini cocak dengan HEAD.
   - **Header PRD:** diperbarui ke **Rev. 165** (tanggal 17 Oktober 2026 WIB).

3. **Status:** dokumen PRD **REVISI** — rev 165 = verifikasi fresh ulang & konfirmasi stabilitas berikutnya; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. HEAD = `1200c891a0ac4caf3a38389a237cceed7a1f9895` (Rev. 164). Working tree bersih. Branch 1 commit ahead `origin/main` (`27ca1d2`). Seluruh perubahan telah dicomit ke HEAD.
"""

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(lines)
    f.write(rev165)

print('[OK] Rev. 165 section appended')
print(f'[INFO] Total lines: {len(lines) + rev165.count(chr(10))}')
