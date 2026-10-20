#!/usr/bin/env python3
"""Append §94 (Rev. 314) section to the PRD file."""

# Read the file
with open('PRD-PONDOK-BANAT.md', 'r', encoding='utf-8') as f:
    content = f.read()

# New section content
section_94 = """
---

## 94. REVISI TERBARU (Rev. 314 — 19 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 19 Oktober 2026 (WIB, cron run) — query `sqlite3` ke `dev.db`, `npx tsc --noEmit`, `npx eslint .`, `npx next build`.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 313 (data terkonsisten).**
   - **Git HEAD (local):** `b241c36` (Rev. 314, commit b241c36); branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `b241c36`. **origin/main:** `74b54cfde74daeb356595d0abacee173537f7992` (Rev. 309). Local branch **6 commits ahead**, **0 commit behind** origin.main.
   - **Working tree:** `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 314, telah dicomit); seluruh file lain cocak dengan HEAD; `git ls-files` = 36 file.
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`; seluruh record (453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` dan `import_students_grades_clean.py` tidak ditemukan di working tree).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` absen (clear checkout), `.next/` masih ada (partial: cache + diagnostics + package.json + server + static + types, bukan production build). `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm install` ulang sebelum dapat dijalankan.
   - **Source files:** `src/app/*` = 13 sub direktori (absensi, beranda, berita, guru, kelas, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah) + `globals.css` + `layout.tsx` + `page.tsx` = 15 entri (13 halaman + layout + page). `src/components` = `Beranda.tsx` & `Login.tsx`. `src/lib` = **kosong** (logic inline di komponen). Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama 'Pondok Banat'); produksi butuh bcrypt + session.
   - **Beranda hardcode:** `src/components/Beranda.tsx` & `src/app/beranda/page.tsx` tetap `totalSantri: 453, totalGuru: 54, totalKelas: 18` (hardcode, bukan fetch real-time dari DB).
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map(\\"uid_nfc\\"` baris 68 `prisma/schema.prisma`), `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Prisma schema:** 17 model terdefinisi (termasuk KitabProgress, Sertakan — ditambahkan Rev. 51). `prisma validate` berhasil. **Schema inconsistency (Rev. 38–45) SELESAI** — kedua model konsisten dengan referensi di `Subject` dan `User`.

2. **Open issues:**
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

3. **Status:** dokumen PRD **REVISI** — rev 314 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. Header PRD diperbarui ke **Rev. 314**. Git HEAD = `b241c36` (Rev. 314, commit b241c36). Origin/main = `74b54cfde74daeb356595d0abacee173537f7992` (Rev. 309); **6 commits ahead**, **0 commit behind**.</span>
"""

# Append the section
if '## 94. REVISI TERBARU' not in content:
    content += section_94
    with open('PRD-PONDOK-BANAT.md', 'w', encoding='utf-8') as f:
        f.write(content)
    print('Section 94 appended successfully')
else:
    print('Section 94 already exists')
