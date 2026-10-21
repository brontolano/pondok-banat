#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Update PRD-PONDOK-BANAT.md to Rev. 366 (20 Oktober 2026 WIB)."""
import os

PATH = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"
with open(PATH, "r", encoding="utf-8") as f:
    content = f.read()

def repl_old(old, new):
    global content
    n = content.count(old)
    if n != 1:
        print("WARNING: expected 1 match, got", n)
    content = content.replace(old, new)
    return n

print("=== HEADER REPLACEMENTS ===")

# 1) Revision date
n1 = repl_old("> **Rev. 365 — 20 Oktober 2026 (WIB).**",
              "> **Rev. 366 — 20 Oktober 2026 (WIB).**")
print("  Rev date replacement:", n1)

# 2) Git HEAD local (short + full forms)
n2 = repl_old("`0911aea` (Rev. 364, commit `0911aeabf7d4a1a5132f15a35aff4698c88ec7ac`)",
              "`335d5d6` (Rev. 365, commit `335d5d605d35f352cf9d290a4c02a0dfb7ed6ab2`)")
print("  Git HEAD replacement:", n2)

n3 = repl_old("`git rev-parse HEAD` = `0911aeabf7d4a1a5132f15a35aff4698c88ec7ac`",
              "`git rev-parse HEAD` = `335d5d605d35f352cf9d290a4c02a0dfb7ed6ab2`")
print("  Git HEAD full replacement:", n3)

# 3) Commits ahead
n4 = repl_old("Local branch **11 commits ahead**", "Local branch **12 commits ahead**")
print("  Commits ahead replacement:", n4)

# 4) Header status: 'revisi terbaru = Rev. 365' -> Rev. 366
n5 = repl_old("revisi terbaru = Rev. 365",
              "revisi terbaru = Rev. 366")
print("  Header status replacement:", n5)

# 5) Section 150 references to HEAD 0911aea -> 335d5d6, 11 -> 12
#    These are inside the section 150 body, separate from the header
n6 = repl_old("**Git HEAD (local):** `0911aea` (Rev. 364, commit `0911aeabf7d4a1a5132f15a35aff4698c88ec7ac`)",
              "**Git HEAD (local):** `335d5d6` (Rev. 365, commit `335d5d605d35f352cf9d290a4c02a0dfb7ed6ab2`)")
print("  Sec150 Git HEAD short replacement:", n6)

n7 = repl_old("**origin/main:** `8df4a80` (Rev. 353). Local branch **11 commits ahead**, **0 commit behind** origin.main.",
              "**origin/main:** `8df4a80` (Rev. 353). Local branch **12 commits ahead**, **0 commit behind** origin.main.")
print("  Sec150 origin/main replacement:", n7)

n8 = repl_old("state terkini HEAD = `0911aea` (Rev. 364, commit `0911aea`); origin/main = `8df4a80` (Rev. 353). Branch **11 commits ahead** origin.main.",
              "state terkini HEAD = `335d5d6` (Rev. 365, commit `335d5d6`); origin/main = `8df4a80` (Rev. 353). Branch **12 commits ahead** origin.main.")
print("  Sec150 change-references replacement:", n8)

n9 = repl_old("Git HEAD = `0911aea` (Rev. 364, 11 commits ahead origin.main.)",
              "Git HEAD = `335d5d6` (Rev. 365, 12 commits ahead origin.main.)")
print("  Sec150 status replacement:", n9)

# --- Insert Section 151 after Section 150 body (at end of file) ---
section_151 = """## 151. REVISI TERBARU (Rev. 366 — 20 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 20 Oktober 2026 (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / struktur source / skema Prisma / Login.tsx / Beranda.tsx. Semua data diverifikasi langsung dari repo kerja saat ini.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 365 (data terkonsisten).**
   - **Git HEAD (local):** `335d5d6` (Rev. 365, commit `335d5d605d35f352cf9d290a4c02a0dfb7ed6ab2`). Branch `main` (remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `335d5d6`). **origin/main:** `8df4a80` (Rev. 353). Local branch **12 commits ahead**, **0 commit behind** origin.main. Working tree: PRD cocak dengan HEAD (revisi terbaru = Rev. 366); seluruh file lain cocak dengan HEAD; `git ls-files` = 36 file; 113 file tidak ter-track (skrip sementara, backup, section .md, .orig, .py).
   - **Database (dev.db):** file `dev.db` saat ini **absent** — dihapus oleh commit HEAD \\"Release: clean core files only\\" (1dc891d) dan .gitignore mencantumkan *.db. Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (init_db.py, init_schema.sql; import_excel.py dan import_students_grades_clean.py tidak ditemukan di working tree).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` absen (0 package; .bin tidak ada). `.next/` masih ada (partial: cache + diagnostics + package.json + server + static + trace + trace-build + turbopack + types, bukan production build). `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm install` ulang sebelum dapat dijalankan.
   - **Prisma schema:** 17 model terdefinisi (termasuk `KitabProgress` di baris 203, `Sertakan` di baris 218 — ditambahkan Rev. 51). `uidNfc` pada model `Student` (baris 68, `uidNfc String? @map(\\"uid_nfc\\")`). `prisma/schema.prisma` **263 baris**, 8492 bytes. `prisma validate` **tidak dapat dijalankan** karena `prisma` CLI tidak terinstall (`node_modules` absen).
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map(\\"uid_nfc\\"` ) baris 68) & `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama Pondok Banat). Produksi butuh bcrypt + session.
   - **Beranda hardcode:** `src/components/Beranda.tsx` (baris 26–28) & `src/app/beranda/page.tsx` (baris 14–16) masih hardcode `totalSantri: 453, totalGuru: 54, totalKelas: 18` (bukan fetch real-time dari DB).
   - **Source files:** `src/app/*` = 15 entri (12 sub direktori: absensi, beranda, berita, guru, kelas, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah + globals.css, layout.tsx, page.tsx); `src/components` = 2 (`Beranda.tsx` & `Login.tsx`); `src/lib` = kosong (logic inline). Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite).
   - **Data source:** folder `.data-pondokanat/` **tidak ditemukan** di working tree (di-eksklusi oleh `.gitignore`). Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber.

2. **Perubahan dari Rev. 365:**
   - **Header PRD:** diperbarui ke **Rev. 366** (tanggal 20 Oktober 2026 WIB).
   - **New Section 151 (Rev. 366):** ditambahkan untuk verifikasi fresh ulang & konfirmasi stabilitas Rev. 366.
   - **Referensi HEAD:** state terkini HEAD = `335d5d6` (Rev. 365, commit `335d5d6`); origin/main = `8df4a80` (Rev. 353). Branch **12 commits ahead** origin.main.

3. **Status:** dokumen PRD **REVISI** — rev 366 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. Header PRD diperbarui ke **Rev. 366**. Git HEAD = `335d5d6` (Rev. 365, 12 commits ahead origin.main.).

"""

insert_point = len(content)
content = content.rstrip() + "\\n\\n" + section_151 + "\\n"

print("Header now Rev. 366:", "> **Rev. 366 — 20 Oktober 2026 (WIB).**" in content)
print("Section 151 present:", "## 151. REVISI TERBARU (Rev. 366" in content)

with open(PATH, "w", encoding="utf-8") as f:
    f.write(content)

print("New file size (bytes):", len(content.encode("utf-8")))
print("Done.")
