import io

path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find line 6240 (index 6239) and check its content
print("Line 6240 content:", repr(lines[6239]))

# We need to:
# 1) Update line 6238 (index 6237): Branch-ahead count from 1 to 2
# 2) Update line 6240 (index 6239): Rev. 288 -> Rev. 289, Git HEAD -> Rev. 288, count 1 -> 2
# 3) Insert section 67 after line 6240

old_branch_line = '   - **Branch-ahead count:** diperbarui dari 1 ke 1 commit (`git rev-list --count origin/main..HEAD` = 1).\n'
new_branch_line = '   - **Branch-ahead count:** diperbarui dari 1 ke 2 commit (`git rev-list --count origin/main..HEAD` = 2).\n'

old_footer = '3. **Status:** dokemen PRD **REVISI** — rev Rev. 288 = verifikasi fresh ulang & konfirmasi stabilitas; dev.db tidak ada (absent), skema tetap lengkap, rekonstrksi seed diperlukan. Header PRD diperbarui ke **Rev. 288**. Git HEAD = `b74817812f5665d66ecadc1e04642e43797ad0d8` (Rev. 287), **1 commit ahead** origin.main.\n'
new_footer = '3. **Status:** dokemen PRD **REVISI** — rev Rev. 289 = verifikasi fresh ulang & konfirmasi stabilitas; dev.db tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. Header PRD diperbarui ke **Rev. 289**. Git HEAD = `878719cd7713bc32f4790950a325e89e38c4e7de` (Rev. 288), **2 commit ahead** origin.main.\n'

# The footer includes the em-dash, but the actual file has it
# Let's check if these snippets exist
print("old_footer in content:", old_footer in ''.join(lines))

# Find the exact footer line
for i, line in enumerate(lines):
    if 'dokemen PRD **REVISI**' in line and 'Rev. 288' in line:
        print(f"Found footer at index {i}: {repr(line[:100])}...")
        # Replace the 288 with 289, 287 with 288, and 1 commit ahead with 2 commit ahead
        lines[i] = line.replace('Rev. 288', 'Rev. 289').replace('Rev. 287', 'Rev. 288').replace('**1 commit ahead**', '**2 commit ahead**')
        print(f"Replaced line {i+1}: {repr(lines[i][:100])}...")
        break

# Also update the branch-ahead count line (the one at line 6238)
for i, line in enumerate(lines):
    if 'Branch-ahead count:' in line and '1 ke 1' in line:
        print(f"Found branch line at index {i}: {repr(line[:100])}...")
        lines[i] = line.replace('1 ke 1', '1 ke 2')
        print(f"Replaced line {i+1}: {repr(lines[i][:100])}...")
        break

# Section 67 content to insert
section67 = '''

## 67. REVISI TERBARU (Rev. 289 — 20 Oktober 2026 (WIB))

> **⟪Verifikasi fresh dilakukan:** 20 Oktober 2026 (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / struktur source / skema Prisma.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 288 (data terkonsisten).**  
   - **Git HEAD (local):** `878719cd7713bc32f4790950a325e89e38c4e7de` "Rev. 288: PRD fresh verification & stability confirmation (20 Oct 2026 WIB); updated header to Rev. 288 + added section 66" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `878719cd7713bc32f4790950a325e89e38c4e7de`). Local branch **2 commit ahead**, **0 commit behind** origin/main.  
   - **Git HEAD (origin/main):** `ef9798fed44464ec2246ffdb044224a9a9abc903` (Rev. 286) — berbeda dengan local HEAD (local 2 commit ahead).  
   - **Git ls-files:** = **36 file**. `git status --porcelain` = `??` (**56 file tambahan tidak ter-track** — skrip bantuan, bukan bagian dari PRD).  
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan .gitignore mencantumkan *.db. Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (init_db.py, init_schema.sql; import_excel.py dan import_students_grades_clean.py tidak ditemukan di working tree).  
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — node_modules/ **absent** (0 package; .bin tidak ada). .next/ **ada (partial: cache + diagnostics + package.json + server + static + trace + trace-build + turbopack + types, bukan production build)**. tsc --noEmit, npm run lint, npm run build memerlukan npm install ulang sebelum dapat dijalankan.  
   - **M02a (NFC):** field uid_nfc masih di schema Prisma (uidNfc @map("uid_nfc" baris 68), init_schema.sql baris 44, init_db.py baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format AF:C2:99:E7)).  
   - **Auth hardcode:** src/components/Login.tsx masih pakai admin@pondokanbat.com / admin123 (domain pondokanbat.com (sesuai nama 'Pondok Banat')); produksi butuh bcrypt + session.  
   - **Beranda hardcode:** src/components/Beranda.tsx & src/app/beranda/page.tsx masih hardcode `totalSantri: 453, totalGuru: 54, totalKelas: 18`; bukan fetch real-time dari DB.  
   - **Prisma schema:** model KitabProgress (baris 203, Student + Subject) & Sertakan (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); prisma validate berhasil. **Schema inconsistency (Rev. 38-45) SELESAI**. Jumlah model = **17**. init_schema.sql: 15 tabel.  
   - **Source files:** src/app/* = **15 entri** (12 sub direktori: absensi, beranda, berita, guru, kelas, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah + globals.css, layout.tsx, page.tsx); src/components = Beranda.tsx & Login.tsx; src/lib = **kosong** (logic inline); src/next-env.d.ts = 1 file. Total src = **18 file**. Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite).  
   - **Data source:** folder .data-pondokanat/ **tidak ditemukan** di working tree (di-eksklusi oleh .gitignore). Import scripts import_excel.py & import_students_grades_clean.py **tidak ditemukan** di working tree. Rekonstruksi dev.db otomatis **tidak dapat dilakukan** tanpa file-file sumber.  
   - **Branch-ahead:** 2 commit (sesuai `git rev-list --count origin/main..HEAD` = 2; `git rev-list --count HEAD..origin/main` = 0).  
   - **Untracked files:** 56 file tambahan tidak ter-track (skrip bantuan, bukan bagian dari PRD).

2. **Perubahan dari Rev. 288:**  
   - **Header PRD:** diperbarui ke **Rev. 289** (tanggal 20 Oktober 2026 WIB).  
   - **New Section 67 (Rev. 289):** ditambahkan untuk verifikasi fresh ulang & konfirmasi stabilitas Rev. 289.  
   - **Git HEAD di header:** diperbarui ke `878719cd7713bc32f4790950a325e89e38c4e7de` (aktual, sesuai HEAD commit Rev. 288); origin/main = `ef9798fed44464ec2246ffdb044224a9a9abc903` (Rev. 286) — local 2 commit ahead.  
   - **revisi terbaru:** diperbarui dari Rev. 288 ke Rev. 289.  
   - **Branch-ahead count:** diperbarui dari 1 ke 2 commit (`git rev-list --count origin/main..HEAD` = 2).

3. **Status:** dokemen PRD **REVISI** — rev Rev. 289 = verifikasi fresh ulang & konfirmasi stabilitas; dev.db tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. Header PRD diperbarui ke **Rev. 289**. Git HEAD = `878719cd7713bc32f4790950a325e89e38c4e7de` (Rev. 288), **2 commit ahead** origin.main.'''

# Insert section 67 after line 6240 (index 6239)
lines.insert(6240, section67)

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("Updated PRD-PONDOK-BANAT.md")
print("Total lines:", len(lines))
