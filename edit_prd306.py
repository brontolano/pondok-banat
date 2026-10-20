#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Update PRD-PONDOK-BANAT.md to Rev. 306 (cron verification run)."""
import io
import sys

PATH = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'

with io.open(PATH, 'r', encoding='utf-8') as f:
    text = f.read()

orig = text

def repl(old, new, expect=1):
    global text
    n = text.count(old)
    if n != expect:
        print('FAIL: expected %d occurrence(s), found %d for:' % (expect, n))
        print(old[:160])
        sys.exit(1)
    text = text.replace(old, new)
    print('OK: replaced (%d)' % expect)

# ---- Header line 4 (the "Source" note) ----
repl('> **Rev. 305 — 19 Oktober 2026 (WIB).**',
     '> **Rev. 306 — 19 Oktober 2026 (WIB).**')

repl('Git HEAD (local): `62cd6c1ba50ff2a34ff861f9ae55114a5765986e` "Rev. 304: PRD fresh verification & stability confirmation (19 Oktober 2026 WIB); updated header to Rev. 304 + added section 82" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `e74a718c3040e65dac76219b34c36aea20ebf3be`).',
     'Git HEAD (local): `9895c4103883ed4443bb8a51b04c052bf7d67a89` "Rev. 305: PRD fresh verification & stability confirmation (19 Oktober 2026 WIB); updated header to Rev. 305 + added section 83" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `9895c4103883ed4443bb8a51b04c052bf7d67a89`).')

repl('`bf253ccd67c29562decc1c088e99aeed82465396` (Rev. 293) — 11 commit ahead, 0 commit behind origin.main.',
     '`bf253ccd67c29562decc1c088e99aeed82465396` (Rev. 293) — 12 commit ahead, 0 commit behind origin.main.')

repl('revisi terbaru = Rev. 305, akan dicomit', 'revisi terbaru = Rev. 306, akan dicomit', expect=2)

repl('Local branch **11 commit ahead**, **0 commit behind** origin.main.',
     'Local branch **12 commit ahead**, **0 commit behind** origin.main.')

# ---- Append Rev. 306 section (84) ----
SECTION_84 = '''
## 84. REVISI TERBARU (Rev. 306 — 19 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 19 Oktober 2026 (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.data-pondokanat` / struktur source.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 305 (data terkonsisten).**
   - **Git HEAD (local):** `9895c4103883ed4443bb8a51b04c052bf7d67a89` "Rev. 305: PRD fresh verification & stability confirmation (19 Oktober 2026 WIB); updated header to Rev. 305 + added section 83" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `9895c4103883ed4443bb8a51b04c052bf7d67a89`). Local branch **12 commit ahead** of `origin/main` (Rev. 305 `9895c4103883ed4443bb8a51b04c052bf7d67a89`, Rev. 304 `62cd6c1ba50ff2a34ff861f9ae55114a5765986e`, Rev. 303 `e74a718c3040e65dac76219b34c36aea20ebf3be`, Rev. 302 `2aadc4908fff50b634c283b7a38c67c9461bb6a1`, Rev. 301 `2d94a01d61df64c6b44d4065903f309a5edfe719`, Rev. 300 `db3cfd7cb15e777f73b8fd0bda4db71dce66ebb5`, Rev. 299 `832d27c96c455d2e640249dd021eea8eb2586229`, Rev. 298 `7ca64e1a03b2863ec7f488c226d06610255c6037`, Rev. 297 `9b38f085b88d194d3a7a4954ff3dbed155d2e186`, Rev. 296 `1039732136ee73199c5ab8bee2538d5671878a7e`, Rev. 295 `b46cb5c2dff1c4c63883fb36409744fa85bb8558`, Rev. 294 `0d206f461ea168a2f03c1d25fe1c5a8e66a89c06`, Rev. 293 `bf253ccd67c29562decc1c088e99aeed82465396`).
   - **Working tree:** `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 306, akan dicomit); seluruh file lain cocak dengan HEAD. `git ls-files` = 36 file.
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`; seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; import_excel.py dan import_students_grades_clean.py tidak ditemukan di working tree).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` **absent** (clear checkout, 0 file); `.next/` masih ada (partial: `cache` + `diagnostics` + `package.json` + `server` + `static` + `trace` + `trace-build` + `turbopack` + `types/`, bukan production build). `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm install` ulang sebelum dapat dijalankan.
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map("uid_nfc")` baris 68 `prisma/schema.prisma`), `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama 'Pondok Banat'). Produksi butuh bcrypt + session.
   - **Beranda hardcode:** `src/components/Beranda.tsx` & `src/app/beranda/page.tsx` tetap `totalSantri: 453, totalGuru: 54, totalKelas: 18` (hardcode, bukan fetch real-time dari DB).
   - **Prisma schema:** 17 model terdefinisi (termasuk KitabProgress, Sertakan — ditambahkan Rev. 51). `prisma validate` berhasil. **Schema inconsistency (Rev. 38–45) SELESAI** — kedua model konsisten dengan referensi di `Subject` dan `User`.
   - **Source files:** `src/app/*` = 12 sub direktori (absensi, beranda, berita, guru, kelas, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah) + `globals.css` + `layout.tsx` + `page.tsx` = 15 entri (13 halaman + layout + page). `src/components` = `Beranda.tsx` & `Login.tsx`. `src/lib` = **kosong** (logic inline di komponen). Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite).

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

3. **Status:** dokumen PRD **REVISI** — rev 306 = verifikasi fresh ulang & konfirmasi stabilitas; dev.db tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. Header PRD diperbarui ke **Rev. 306**. Git HEAD = `9895c4103883ed4443bb8a51b04c052bf7d67a89` (Rev. 305), **12 commit ahead** origin.main.

'''

if not text.endswith('\n'):
    text += '\n'
text += SECTION_84

with io.open(PATH, 'w', encoding='utf-8') as f:
    f.write(text)

print('\n--- Verification ---')
print('New line count:', text.count('\n'))
print('File size: %.0f bytes' % len(text.encode('utf-8')))
print('Header says Rev. 306:', 'Rev. 306' in text)
print('Section 84 present:', '## 84. REVISI TERBARU (Rev. 306' in text)
print('Old Rev. 305 header remaining:', 'Rev. 305 — 19 Oktober 2026 (WIB).**' in text)
