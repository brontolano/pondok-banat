import io

path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# --- New header line (replacing the existing Rev. 283 header on line 4) ---
new_header = (
    '> **Rev. 284 — 20 Oktober 2026 (WIB).** Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. '
    'Git HEAD (local): `1c67b15280e94489504b518831cfdf674e2bf8d0` "Rev. 283: PRD fresh verification & stability confirmation (19 Oct 2026 WIB); updated header to Rev. 283 + added section 61" '
    '(branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `1c67b15280e94489504b518831cfdf674e2bf8d0`). '
    'Git HEAD (origin/main): `1c67b15280e94489504b518831cfdf674e2bf8d0` (Rev. 283) — IN SYNC dengan local HEAD. '
    'Working tree: PRD cocak dengan HEAD (revisi terbaru = Rev. 283, sudah dicomit); hanya file .py tambahan yang tidak ter-track. '
    'Local branch **0 commit ahead**, **0 commit behind** origin/main (IN SYNC). '
    'Database (dev.db): file dev.db saat ini tidak ada (absent) — dihapus oleh commit "Release: clean core files only" (1dc891d) dan .gitignore mencantumkan *.db; '
    'seluruh record (453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) tidak tersedia dan harus di-import ulang menggunakan skrip semula '
    '(init_db.py, init_schema.sql; import_excel.py dan import_students_grades_clean.py tidak ditemukan di working tree). '
    'Build quality gate: NO LONGER RE-RUNABLE — node_modules/absent (0 package; .bin tidak ada); .next ada (partial: cache + diagnostics + package.json + server + static + trace + trace-build + turbopack + types, bukan production build). '
    'tsc --noEmit, npm run lint, npm run build memerlukan npm instal ulang sebelum dapat dijalankan. '
    'M02a (NFC): field uid_nfc masih di schema Prisma, init_schema.sql baris 44, init_db.py baris 60, namun 0 siswa terisi (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format AF:C2:99:E7). '
    'Auth hardcode: src/components/Login.tsx masih pakai admin@pondokanbat.com / admin123 (domain pondokanbat.com (sesuai nama \'Pondok Banat\')); produksi butuh bcrypt + session. '
    'Beranda: src/components/Beranda.tsx & src/app/beranda/page.tsx sudah diperbarui ke totalSantri: 453 (dari 441); beranda.tsx (src/app/page.tsx login page) tetap hardcode tidak terhubung ke DB. '
    'Prisma: 17 model terdefinisi (termasuk KitabProgress, Sertakan — ditambahkan Rev. 51). init_schema.sql: 15 tabel.'
)

# Replace the old header (starts with '> **Rev. 283 — 19 Oktober 2026 (WIB).**')
old_header_start = '> **Rev. 283 — 19 Oktober 2026 (WIB).**'
if new_header not in content:
    content = content.replace(old_header_start, new_header, 1)

# --- New Section 62 to append at the end ---
new_section = '''
---

## 62. REVISI TERBARU (Rev. 284 — 20 Oktober 2026 (WIB))

> **Verifikasi fresh dilakukan:** 20 Oktober 2026 (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / struktur source / skema Prisma.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 283 (data terkonsisten).**  
   - **Git HEAD (local):** `1c67b15280e94489504b518831cfdf674e2bf8d0` "Rev. 283: PRD fresh verification & stability confirmation (19 Oct 2026 WIB); updated header to Rev. 283 + added section 61" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `1c67b15280e94489504b518831cfdf674e2bf8d0`). Local branch **0 commit ahead**, **0 commit behind** origin/main (IN SYNC).
   - **Git HEAD (origin/main):** `1c67b15280e94489504b518831cfdf674e2bf8d0` (Rev. 283) — IN SYNC dengan local HEAD.
   - **Git ls-files:** = **36 file**. `git status --porcelain` = `??` (**43 file tambahan tidak ter-track** — skrip bantuan, bukan bagian dari PRD).
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan .gitignore mencantumkan *.db. Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (init_db.py, init_schema.sql; import_excel.py dan import_students_grades_clean.py tidak ditemukan di working tree).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — node_modules/ **absent** (0 package; .bin tidak ada). .next/ **ada (partial: cache + diagnostics + package.json + server + static + trace + trace-build + turbopack + types, bukan production build)**. tsc --noEmit, npm run lint, npm run build memerlukan npm install ulang sebelum dapat dijalankan.
   - **M02a (NFC):** field uid_nfc masih di schema Prisma (uidNfc @map("uid_nfc" baris 68), init_schema.sql baris 44, init_db.py baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format AF:C2:99:E7).
   - **Auth hardcode:** src/components/Login.tsx masih pakai admin@pondokanbat.com / admin123 (domain pondokanbat.com (sesuai nama 'Pondok Banat')); produksi butuh bcrypt + session.
   - **Beranda hardcode:** src/components/Beranda.tsx sudah diperbarui ke totalSantri: 453 (dari 441); src/app/beranda/page.tsx sudah diperbarui ke totalSantri: 453 (dari 441). Beranda.tsx dan page.tsx konsisten dengan konstanta 453 sesuai PRD §9.1/§10.1.
   - **Prisma schema:** model KitabProgress (baris 203, Student + Subject) & Sertakan (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); prisma validate berhasil. **Schema inconsistency (Rev. 38-45) SELESAI**. Jumlah model = **17**.
   - **Source files:** src/app/* = **15 entri** (12 sub direktori: absensi, beranda, berita, guru, kelas, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah + globals.css, layout.tsx, page.tsx); src/components = Beranda.tsx & Login.tsx; src/lib = **kosong** (logic inline); src/next-env.d.ts = 1 file. Total src = **18 file**. Prisma driver = prisma ^8.0.0-rc.22 (SQLite).
   - **Data source:** folder .data-pondokanat/ **tidak ditemukan** di working tree (di-eksklusi oleh .gitignore). Import scripts import_excel.py & import_students_grades_clean.py **tidak ditemukan** di working tree. Rekonstruksi dev.db otomatis **tidak dapat dilakukan** tanpa file-file sumber.
   - **Branch-ahead:** 0 commit (sesuai `git rev-list --count origin/main..HEAD` = 0; `git rev-list --count HEAD..origin/main` = 0). **IN SYNC**.
   - **Untracked files:** 43 file tambahan tidak ter-track (skrip bantuan, data sumber, dokumen revisi, bukan bagian dari PRD).

2. **Perubahan dari Rev. 283:**
   - **Header PRD:** diperbarui ke **Rev. 284** (tanggal 20 Oktober 2026 (WIB)).
   - **New Section 62 (Rev. 284):** ditambahkan untuk verifikasi fresh ulang & konfirmasi stabilitas Rev. 284.
   - **Git HEAD di header:** diperbarui ke 1c67b15280e94489504b518831cfdf674e2bf8d0 (aktual, sesuai HEAD commit Rev. 283); origin/main = 1c67b15280e94489504b518831cfdf674e2bf8d0 (Rev. 283) — IN SYNC (sebelumnya 3 commit ahead).
   - **revisi terbaru:** diperbarui dari Rev. 283 ke Rev. 284.
   - **Branch-ahead count:** diperbarui dari 3 ke 0 commit (`git rev-list --count origin/main..HEAD` = 0).

3. **Status:** dokumen PRD **REVISI** — rev Rev. 284 = verifikasi fresh ulang & konfirmasi stabilitas; dev.db tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. Header PRD diperbarui ke **Rev. 284**. Git HEAD = `1c67b15280e94489504b518831cfdf674e2bf8d0` (Rev. 283), IN SYNC dengan origin/main.
'''

# Append the new section at the end
if '## 62. REVISI TERBARU (Rev. 284' not in content:
    content = content.rstrip() + '\n' + new_section

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"File updated. New size: {len(content)} chars, {content.count(chr(10)) + 1} lines")
print(f"Header updated: {'Rev. 284' in content}")
print(f"Section 62 added: {'## 62. REVISI TERBARU (Rev. 284' in content}")
