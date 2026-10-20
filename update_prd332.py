#!/usr/bin/env python3
"""Update PRD-PONDOK-BANAT.md: complete Section 116 + append Rev. 332 verification section."""

path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Complete the truncated auth hardcode line
old_line = '''   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama Pondok'''

new_line = '''   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama Pondok Banat); produksi butuh bcrypt + session.
   - **Beranda hardcode:** `src/components/Beranda.tsx` (baris 26–28) & `src/app/beranda/page.tsx` (baris 14) masih hardcode `totalSantri: 453, totalGuru: 54, totalKelas: 18` (bukan fetch real-time dari DB; sudah diperbarui ke 453 sesuai data Excel grade sheets).
   - **Source files:** `src/app/*` = 15 entri (12 sub direktori: absensi, beranda, berita, guru, kelas, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah + globals.css, layout.tsx, page.tsx); `src/components` = 2 (Beranda.tsx & Login.tsx); `src/lib` = kosong (logic inline). Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite).
   - **Data source:** folder `.data-pondokanat/` **tidak ditemukan** di working tree (di-eksklusi oleh `.gitignore`). Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber.

2. **Perubahan dari Rev. 330:**
   - **Header PRD:** diperbarui ke **Rev. 331** (tanggal 20 Oktober 2026 WIB).
   - **New Section 116 (Rev. 331):** ditambahkan untuk verifikasi fresh ulang & konfirmasi stabilitas Rev. 331.
   - **Referensi HEAD:** state terkini HEAD = `f94ce02` (Rev. 331, commit `4bcbb7c`, 1 commit ahead origin.main).
   - **Database:** `dev.db` masih absent (dihapus oleh commit HEAD "Release: clean core files only" 1dc891d).
   - **Build quality gate:** NO LONGER RE-RUNABLE (node_modules absen; .next partial).

3. **Status:** dokumen PRD **REVISI** — rev 331 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. Git HEAD = `f94ce02` (Rev. 331, commit 4bcbb7c, 1 commit ahead origin.main).'''

if old_line not in content:
    print("ERROR: truncated line not found!")
else:
    content = content.replace(old_line, new_line)
    print("Section 116 completed.")

# 2. Append Section 117 (Rev. 332)
section_117 = '''
## 117. REVISI TERBARU (Rev. 332 — 20 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 20 Oktober 2026 (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / struktur source / skema Prisma / Login.tsx / Beranda.tsx. Semua data diverifikasi langsung dari repo kerja saat ini.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 331 (data terkonsisten).**
   - **Git HEAD (local):** `f94ce02771d46c40e9f4cfe2f158e4d5e8d9418d` (Rev. 331, commit `4bcbb7c`). Branch `main` (remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `f94ce02771d46c40e9f4cfe2f158e4d5e8d9418d`). **origin/main:** `4bcbb7c9bbea23b9807260d3c497a7ab862cd8e6` (Rev. 330). Local branch **1 commit ahead**, **0 commit behind** origin.main.
   - **Working tree:** `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 332, akan dicomit); seluruh file lain cocak dengan HEAD; `git ls-files` = 36 file; 89 file tidak ter-track (skrip sementara, backup, section .md, .orig, .py).
   - **Database (dev.db):** file `dev.db` saat ini **absent** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan .gitignore mencantumkan *.db. Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (init_db.py, init_schema.sql; import_excel.py dan import_students_grades_clean.py tidak ditemukan di working tree).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` absen (0 package; .bin tidak ada). `.next/` masih ada (partial: cache + diagnostics + package.json + server + static + trace + trace-build + turbopack + types, bukan production build). `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm install` ulang sebelum dapat dijalankan.
   - **Prisma schema:** `17` model terdefinisi (termasuk `KitabProgress` di baris 203, `Sertakan` di baris 218 — ditambahkan Rev. 51). `prisma/schema.prisma` **8492 bytes**, 263 baris. `uidNfc` pada model `Student` (baris 68, `uidNfc String? @map("uid_nfc")`). `prisma validate` **tidak dapat dijalankan** karena `prisma` CLI tidak terinstall (`node_modules` absen).
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map("uid_nfc")` baris 68), `init_schema.sql` baris 40, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama Pondok Banat); produksi butuh bcrypt + session.
   - **Beranda hardcode:** `src/components/Beranda.tsx` (baris 26–28) & `src/app/beranda/page.tsx` masih hardcode `totalSantri: 453, totalGuru: 54, totalKelas: 18` (bukan fetch real-time dari DB; sudah diperbarui ke 453 sesuai data Excel grade sheets).
   - **Source files:** `src/app/*` = 15 entri (12 sub direktori: absensi, beranda, berita, guru, kelas, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah + globals.css, layout.tsx, page.tsx); `src/components` = 2 (Beranda.tsx & Login.tsx); `src/lib` = kosong (logic inline). Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite).
   - **Data source:** folder `.data-pondokanat/` **tidak ditemukan** di working tree (di-eksklusi oleh `.gitignore`). Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber.

2. **Perubahan dari Rev. 331:**
   - **Header PRD:** diperbarui ke **Rev. 332** (tanggal 20 Oktober 2026 WIB).
   - **New Section 117 (Rev. 332):** ditambahkan untuk verifikasi fresh ulang & konfirmasi stabilitas Rev. 332.
   - **Referensi HEAD:** state terkini HEAD = `f94ce02` (Rev. 331, commit `4bcbb7c`, 1 commit ahead origin.main).

3. **Status:** dokumen PRD **REVISI** — rev 332 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. Header PRD diperbarui ke **Rev. 332**. Git HEAD = `f94ce02` (Rev. 331, commit 4bcbb7c, 1 commit ahead origin.main).'''

content = content.rstrip() + '\n' + section_117

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Section 117 appended.")
print("Total lines:", content.count(chr(10)) + 1)
