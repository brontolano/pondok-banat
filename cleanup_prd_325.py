#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rebuild section 110 cleanly: cut at item-2 marker, keep items 1.. end-of-item1."""
import os
REPO = "/opt/data/home/workspace/dev/pondok-banat"
PRD = os.path.join(REPO, "PRD-PONDOK-BANAT")

with open(PRD, encoding="utf-8") as f:
    content = f.read()

marker = "## 110. REVISI TERBARU (Rev. 325"
idx = content.find(marker)
assert idx != -1, "section 110 not found"

intro = """## 110. REVISI TERBARU (Rev. 325 \u2014 20 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 20 Oktober 2026 (WIB, cron run) \u2014 pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / struktur source / skema Prisma / Login.tsx / Beranda.tsx. Semua data diverifikasi langsung dari repo kerja saat ini.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 324 (data terkonsisten).**
   - **Git HEAD (local):** `4b246510265ea3b38962d400cba6426a68105458` (Rev. 324, commit 4b24651) (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `4b246510265ea3b38962d400cba6426a68105458`). **origin/main:** `74b54cfde74daeb356595d0abacee173537f7992` (Rev. 309). Local branch **18 commits ahead**, **0 commit behind** origin.main.
   - **Working tree:** `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 325, belum dicomit); seluruh file lain cocak dengan HEAD; `git ls-files` = 36 file; 78 file tidak ter-track (skrip sementara, backup, section .md).
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** \u2014 dihapus oleh commit HEAD \"Release: clean core files only\" (1dc891d) dan .gitignore mencantumkan *.db. Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (init_db.py, init_schema.sql; import_excel.py dan import_students_grades_clean.py tidak ditemukan di working tree).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** \u2014 `node_modules/` absen (clear checkout, 0 package; `.bin` tidak ada). `.next/` masih ada (partial: cache + diagnostics + package.json + server + static + trace + trace-build + turbopack + types, bukan production build). `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm install` ulang sebelum dapat dijalankan.
   - **Prisma schema:** 17 model terdefinisi (termasuk `KitabProgress` di baris 203, `Sertakan` di baris 218 \u2014 ditambahkan Rev. 51). `prisma/schema.prisma` **8492 bytes**, 263 baris. `uidNfc` pada model `Student` (baris 68, `uidNfc String? @map(\\"uid_nfc\\)`). `prisma validate` **tidak dapat dijalankan** karena `prisma` CLI tidak terinstall (`node_modules` absen).
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map(\\"uid_nfc\\"` baris 68 `prisma/schema.prisma`), `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) \u2014 data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` \u2014 sesuai nama 'Pondok Banat'); produksi butuh bcrypt + session.
   - **Beranda hardcode:** `src/components/Beranda.tsx` (baris 14\u201316) & `src/app/beranda/page.tsx` masih hardcode `totalSantri: 453, totalGuru: 54, totalKelas: 18` (bukan fetch real-time dari DB).
   - **Source files:** `src/app/*` = 15 entri (12 sub direktori: absensi, beranda, berita, guru, kelas, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah + globals.css, layout.tsx, page.tsx); `src/components` = `Beranda.tsx` & `Login.tsx`; `src/lib` = **kosong** (logic inline). Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite).
   - **Data source:** folder `.data-pondokanat/` **tidak ditemukan** di working tree (di-eksklusi oleh `.gitignore`). Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber.

"""

# Find the blank line JUST BEFORE item 2's heading (i.e., after the Data source bullet of item 1)
item2 = "2. **Perubahan dari Rev. 324:**"
cut = content.find(item2)
assert cut != -1, "item 2 marker not found"
clean_prefix = content[:cut]  # includes the blank line ending item 1

tail = """2. **Perubahan dari Rev. 324:**
   - **Header PRD:** diperbarui ke **Rev. 325** (tanggal 20 Oktober 2026 WIB).
   - **New Section 110 (Rev. 325):** ditambahkan untuk verifikasi fresh ulang & konfirmasi stabilitas Rev. 325.
   - **Referensi HEAD:** section 109 (Rev. 324) mencatat HEAD sebagai `dbf2fe0` (Rev. 323, commit dbf2fe0) sebab state verifikasi dites sebelum commit Rev. 324. State terkini HEAD = `4b24651` (Rev. 324, commit 4b24651), **18 commits ahead** origin.main.
   - **Perbaikan hitungan branch:** `git rev-list --count origin/main..HEAD` = **18** (sebelumnya 17); `git rev-list --count HEAD..origin/main` = **0**.

3. **Status:** dokumen PRD **REVISI** \u2014 rev 325 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. Header PRD diperbarui ke **Rev. 325**. Git HEAD = `4b24651` (Rev. 324, commit 4b24651), **18 commits ahead** origin.main.
"""

new_content = clean_prefix + tail

with open(PRD, "w", encoding="utf-8") as f:
    f.write(new_content)
print("Rebuilt section 110. Verifying tail:")
print("\n".join(new_content.splitlines()[-8:]))
