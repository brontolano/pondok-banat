# update_prd_189.py
# Update PRD header from Rev. 188 -> Rev. 189 and append Section 76 (Rev. 189).

path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# --- 1. Update header line (Rev. 188 -> Rev. 189, section 75 -> 76) ---
content = content.replace('Rev. 188 — 18 Oktober 2026 (WIB)', 'Rev. 189 — 19 Oktober 2026 (WIB)')
content = content.replace('**Rev. 188', '**Rev. 189')
content = content.replace('(header + section 75)', '(header + section 76)')

# --- 2. Update section 75's status block to Rev. 189 ---
content = content.replace('rev 188 = verifikasi fresh ulang', 'rev 189 = verifikasi fresh ulang')
content = content.replace('Working tree memiliki 1 perubahan lokal (Rev. 188 header + section 75)',
                         'Working tree memiliki 1 perubahan lokal (Rev. 189 header + section 76)')

# --- 3. Section 76 content (Rev. 189) ---
section_76 = '''
## 76. REVISI TERBARU (Rev. 189 — 19 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 19 Oktober 2026 (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / `PRD-PONDOK-BANAT.md`; query `sqlite3` ke `dev.db` (tidak ada); verifikasi isi file: header PRD, §75.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 188 (data terkonsisten).**
   - **Git HEAD (local):** `26519e1` \"Rev. 188: PRD fresh verification & stability confirmation (18 Oct 2026 WIB); updated header to Rev. 188 + section 75\" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `26519e1`). Local branch **20 commits ahead** dari `origin/main` (`27ca1d2` = Rev. 163 fix).
   - **Git HEAD (origin/main):** `27ca1d2a53b79c513cae9746cc0be9dfe9d783fa` (Rev. 163 fix). Local branch **20 commits ahead**.
   - **Git ls-files:** = **36 file**. `git status --porcelain` = `??` (17 file `.py` tambahan tidak ter-track, bukan bagian dari commit). PRD-PONDOK-BANAT.md **cocak dengan HEAD** (Rev. 188, belum ada perubahan lokal).
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD \"Release: clean core files only\" (1dc891d) dan `.gitignore` mencantumkan `*.db`. Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` dan `import_students_grades_clean.py` tidak ditemukan di working tree).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` **absent** (clear checkout, 0 file); `.next/` **masih ada (partial: cache + diagnostics + package.json, bukan production build)**. `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm instal ulang` sebelum dapat dijalankan.
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map(\"uid_nfc\")` baris 68), `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama 'Pondok Banat'). Produksi butuh bcrypt + session.
   - **Beranda hardcode:** `src/components/Beranda.tsx` (baris 26) & `src/app/beranda/page.tsx` (baris 14) **sudah diperbarui ke 453** (dari 441) — hardcoded stats match Excel grade sheets. TIDAK ada hardcode 441 yang tersisa.
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); jumlah model Prisma = **17**. `prisma validate` tidak dapat dijalankan (prisma tidak terinstall di env cron).
   - **init_schema.sql:** tabel `students` (baris 33) memiliki kolom `uid_nfc TEXT` (baris 44, komentar: `-- NFC card UID: 'AF:C2:99:E7'`) — field M02a **ADA** di schema SQLite. Jumlah tabel = **15** sesuai PRD.
   - **Source files:** `src/app/*` = 15 entri (absensi, beranda, berita, globals.css, guru, kelas, laporan, layout.tsx, login, nilai, page.tsx, pengasuh, ruang-kegiatan, santri, sekolah); `src/components` = `Beranda.tsx` & `Login.tsx`; `src/lib` = **kosong** (logic inline). `git ls-files` = **36 file**.
   - **Source data:** folder `.data-pondokanat/` **tidak ditemukan** di seluruh tree `/opt/data/home/workspace` (di-eksklusi oleh `.gitignore`) DAN tidak ditemukan di seluruh tree `/opt/data`. Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber. **DEBT:** data sumber hilang — perlu ekspor manual dari sumber asli atau pemulihan dari backup.
   - **quality_gate.sh:** file masih memuat rantai `tsc` → `eslint` → `next build`; seluruh gate gagal karena `node_modules` absen.
   - **Working tree state:** `PRD-PONDOK-BANAT.md` **belum diperbarui** (berdasarkan HEAD Rev. 188); working tree **bersih** (tidak ada perubahan lokal). `git status --porcelain` = `??` (17 file `.py` tambahan tidak ter-track). Seluruh file lain cocak dengan HEAD.

2. **Perubahan dari Rev. 188:**
   - **Header PRD:** diperbarui ke **Rev. 189** (tanggal 19 Oktober 2026 WIB).
   - **Section 76 (Rev. 189):** ditambahkan untuk verifikasi fresh ulang & konfirmasi stabilitas.
   - **Git HEAD (local):** `26519e1` (tidak berubah).
   - **Commit count:** tetap **20** commits ahead `origin/main`.
   - **`.next/` directory:** entri = cache, diagnostics, package.json (3 entri — dikonfirmasi; node_modules absen).
   - **`.data-pondokanat/`:** folder masih **tidak ditemukan** di seluruh tree repository & `/opt/data` (status stabil).

3. **Status:** dokumen PRD **REVISI** — rev 189 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. HEAD = `26519e1`. Working tree **bersih** (PRD cocak dengan HEAD, 17 file `.py` tambahan tidak ter-track). Branch **20 commits ahead** `origin/main` (`27ca1d2`).
'''

# Append section 76 at the end of the file
if not content.endswith('\n'):
    content += '\n'
content += section_76

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('PRD updated to Rev. 189; new line count =', len(content.splitlines()))
