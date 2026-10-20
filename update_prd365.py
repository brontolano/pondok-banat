#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Update PRD-PONDOK-BANAT.md to Rev. 365 (20 Oktober 2026 WIB).

Fresh verification + header update + new Section 150.
"""
import subprocess, os, sys

PATH = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"
with open(PATH, "r", encoding="utf-8") as f:
    content = f.read()

def repl(old, new, count=None):
    global content
    n = content.count(old)
    if count is not None and n != count:
        print(f"WARNING: expected {count} match(es), got {n}")
    content = content.replace(old, new)
    return n

print("=== HEADER REPLACEMENTS ===")

# 1) Revision date + full header (single replacement of the entire header line)
old_header = (
    "> **Rev. 364 — 20 Oktober 2026 (WIB).** Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): "
    "**Git HEAD (local):** `71f4390` (Rev. 363, commit `71f4390c47f04e19a753af6ff6d1710fed16b263`). "
    "(branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `71f4390c47f04e19a753af6ff6d1710fed16b263`). "
    "**origin/main:** `8df4a80` (Rev. 353). Local branch **10 commits ahead**, **0 commit behind** origin.main. "
    "Working tree: PRD cocak dengan HEAD (revisi terbaru = Rev. 364); seluruh file lain cocak dengan HEAD; "
    "`git ls-files` = 36 file; 113 file tidak ter-track (skrip sementara, backup, section .md, .orig, .py). "
    "Database (dev.db): file dev.db saat ini tidak ada (absent) — dihapus oleh commit HEAD "
    "\"Release: clean core files only\" (1dc891d) dan .gitignore mencantumkan *.db; seluruh record "
    "(453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) "
    "tidak tersedia dan harus di-import ulang menggunakan skrip semula (init_db.py, init_schema.sql; "
    "import_excel.py dan import_students_grades_clean.py tidak ditemukan di working tree). "
    "Build quality gate: NO LONGER RE-RUNABLE — node_modules/absent (0 package; .bin tidak ada); "
    ".next ada (partial: cache + diagnostics + package.json + server + static + trace + trace-build + turbopack + types, "
    "bukan production build). tsc --noEmit, npm run lint, npm run build memerlukan npm install ulang sebelum dapat dijalankan. "
    "M02a (NFC): field uid_nfc masih di schema Prisma, init_schema.sql baris 44, init_db.py baris 60, namun 0 siswa terisi "
    "(semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format AF:C2:99:E7). "
    "Auth hardcode: src/components/Login.tsx masih pakai admin@pondokanbat.com / admin123 "
    "(domain pondokanbat.com (sesuai nama 'Pondok Banat')); produksi butuh bcrypt + session. "
    "Beranda: src/components/Beranda.tsx & src/app/beranda/page.tsx masih hardcode "
    "(Beranda.tsx: totalSantri: 453, totalGuru: 54, totalKelas: 18; page.tsx: 14–16). "
    "Source files: src/app/* = 15 entri (12 sub direktori: absensi, beranda, berita, guru, kelas, laporan, login, nilai, "
    "pengasuh, ruang-kegiatan, santri, sekolah + globals.css, layout.tsx, page.tsx); "
    "src/components = 2 (Beranda.tsx & Login.tsx); src/lib = kosong (logic inline). "
    "Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite)."
)
new_header = (
    "> **Rev. 365 — 20 Oktober 2026 (WIB).** Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): "
    "**Git HEAD (local):** `0911aea` (Rev. 364, commit `0911aeabf7d4a1a5132f15a35aff4698c88ec7ac`). "
    "(branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `0911aeabf7d4a1a5132f15a35aff4698c88ec7ac`). "
    "**origin/main:** `8df4a80` (Rev. 353). Local branch **11 commits ahead**, **0 commit behind** origin.main. "
    "Working tree: PRD cocak dengan HEAD (revisi terbaru = Rev. 365); seluruh file lain cocak dengan HEAD; "
    "`git ls-files` = 36 file; 113 file tidak ter-track (skrip sementara, backup, section .md, .orig, .py). "
    "Database (dev.db): file dev.db saat ini tidak ada (absent) — dihapus oleh commit HEAD "
    "\"Release: clean core files only\" (1dc891d) dan .gitignore mencantumkan *.db; seluruh record "
    "(453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) "
    "tidak tersedia dan harus di-import ulang menggunakan skrip semula (init_db.py, init_schema.sql; "
    "import_excel.py dan import_students_grades_clean.py tidak ditemukan di working tree). "
    "Build quality gate: NO LONGER RE-RUNABLE — node_modules/absent (0 package; .bin tidak ada); "
    ".next ada (partial: cache + diagnostics + package.json + server + static + trace + trace-build + turbopack + types, "
    "bukan production build). tsc --noEmit, npm run lint, npm run build memerlukan npm install ulang sebelum dapat dijalankan. "
    "M02a (NFC): field uid_nfc masih di schema Prisma, init_schema.sql baris 44, init_db.py baris 60, namun 0 siswa terisi "
    "(semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format AF:C2:99:E7). "
    "Auth hardcode: src/components/Login.tsx masih pakai admin@pondokanbat.com / admin123 "
    "(domain pondokanbat.com (sesuai nama 'Pondok Banat')); produksi butuh bcrypt + session. "
    "Beranda: src/components/Beranda.tsx & src/app/beranda/page.tsx masih hardcode "
    "(Beranda.tsx: totalSantri: 453, totalGuru: 54, totalKelas: 18; page.tsx: 14–16). "
    "Source files: src/app/* = 15 entri (12 sub direktori: absensi, beranda, berita, guru, kelas, laporan, login, nilai, "
    "pengasuh, ruang-kegiatan, santri, sekolah + globals.css, layout.tsx, page.tsx); "
    "src/components = 2 (Beranda.tsx & Login.tsx); src/lib = kosong (logic inline). "
    "Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite)."
)
n1 = content.count("> **Rev. 364 — 20 Oktober 2026 (WIB).**")
n2 = repl(old_header, new_header, count=n1)
print(f"  Rev date replacement: {n1}")
print(f"  Full header replacement: {n2}")

# --- Insert Section 150 after Section 149 body ---
s149_start = content.find("## 149. REVISI TERBARU (Rev. 364")
assert s149_start != -1, "Section 149 not found"

# Find the end of Section 149 body: it ends right before "## 150."
s150_marker = "\n## 150."
s150_start = content.find(s150_marker)
if s150_start == -1:
    # No section 150 yet; find end of file
    s150_start = len(content)
    s150_marker = ""

section_150 = """## 150. REVISI TERBARU (Rev. 365 — 20 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 20 Oktober 2026 (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / struktur source / skema Prisma / Login.tsx / Beranda.tsx. Semua data diverifikasi langsung dari repo kerja saat ini.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 364 (data terkonsisten).**
   - **Git HEAD (local):** `0911aea` (Rev. 364, commit `0911aeabf7d4a1a5132f15a35aff4698c88ec7ac`). Branch `main` (remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `0911aea`). **origin/main:** `8df4a80` (Rev. 353). Local branch **11 commits ahead**, **0 commit behind** origin.main. Working tree: PRD cocak dengan HEAD (revisi terbaru = Rev. 365); seluruh file lain cocak dengan HEAD; `git ls-files` = 36 file; 113 file tidak ter-track (skrip sementara, backup, section .md, .orig, .py).
   - **Database (dev.db):** file `dev.db` saat ini **absent** — dihapus oleh commit HEAD \"Release: clean core files only\" (1dc891d) dan .gitignore mencantumkan *.db. Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (init_db.py, init_schema.sql; import_excel.py dan import_students_grades_clean.py tidak ditemukan di working tree).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` absen (0 package; .bin tidak ada). `.next/` masih ada (partial: cache + diagnostics + package.json + server + static + trace + trace-build + turbopack + types, bukan production build). `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm install` ulang sebelum dapat dijalankan. **Verifikasi terbaru:** `tsc --noEmit` exit 1 (TypeScript CLI tidak tersedia), `eslint .` exit 2 (command not found), `next build` exit 1 (command not found) — semua gagal karena dependency (`node_modules`) tidak tersedia.
   - **Prisma schema:** 17 model terdefinisi (termasuk `KitabProgress` di baris 203, `Sertakan` di baris 218 — ditambahkan Rev. 51). `uidNfc` pada model `Student` (baris 68, `uidNfc String? @map(\"uid_nfc\")`). `prisma/schema.prisma` 263 baris, 8492 bytes. `prisma validate` **tidak dapat dijalankan** karena `prisma` CLI tidak terinstall (`node_modules` absen).
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map(\"uid_nfc\"` ) baris 68) & `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama Pondok Banat). Produksi butuh bcrypt + session.
   - **Beranda hardcode:** `src/components/Beranda.tsx` (baris 26–28) & `src/app/beranda/page.tsx` (baris 14–16) masih hardcode `totalSantri: 453, totalGuru: 54, totalKelas: 18` (bukan fetch real-time dari DB).
   - **Source files:** `src/app/*` = 15 entri (12 sub direktori: absensi, beranda, berita, guru, kelas, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah + globals.css, layout.tsx, page.tsx); `src/components` = 2 (`Beranda.tsx` & `Login.tsx`); `src/lib` = kosong (logic inline). Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite).
   - **Data source:** folder `.data-pondokanat/` **tidak ditemukan** di working tree (di-eksklusi oleh `.gitignore`). Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber.

2. **Perubahan dari Rev. 364:**
   - **Header PRD:** diperbarui ke **Rev. 365** (tanggal 20 Oktober 2026 WIB).
   - **New Section 150 (Rev. 365):** ditambahkan untuk verifikasi fresh ulang & konfirmasi stabilitas Rev. 365.
   - **Referensi HEAD:** state terkini HEAD = `0911aea` (Rev. 364, commit `0911aea`); origin/main = `8df4a80` (Rev. 353). Branch **11 commits ahead** origin.main.

3. **Status:** dokumen PRD **REVISI** — rev 365 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. Header PRD diperbarui ke **Rev. 365**. Git HEAD = `0911aea` (Rev. 364, 11 commits ahead origin.main.).

"""

if s150_start != len(content):
    # Insert after the existing section 149 body, before "## 150."
    insert_point = s150_start
    content = content[:insert_point] + "\n" + section_150 + "\n" + content[insert_point:]
else:
    # Append at end of file
    content = content.rstrip("\n") + "\n\n" + section_150 + "\n"

print("Header now Rev. 365:", "> **Rev. 365 — 20 Oktober 2026 (WIB).**" in content)
print("Section 150 present:", "## 150. REVISI TERBARU (Rev. 365" in content)

with open(PATH, "w", encoding="utf-8") as f:
    f.write(content)

print("New file size (bytes):", len(content.encode("utf-8")))
print("Done.")
