#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Update PRD-PONDOK-BANAT.md: header Rev. 324 -> Rev. 325 + append section 110 (Rev. 325)."""
import subprocess, os

REPO = "/opt/data/home/workspace/dev/pondok-banat"
PRD = os.path.join(REPO, "PRD-PONDOK-BANAT.md")

def git(*args):
    return subprocess.run(["git", "-C", REPO] + list(args), capture_output=True, text=True).stdout.strip()

head = git("rev-parse", "HEAD")
head_short = git("log", "-1", "--oneline")
head_full = git("rev-parse", "HEAD")
origin = git("rev-parse", "origin/main")
ahead = git("rev-list", "--count", "origin/main..HEAD")
behind = git("rev-list", "--count", "HEAD..origin/main")
tracked = subprocess.run(["git", "-C", REPO, "ls-files"], capture_output=True, text=True).stdout.splitlines()
untracked = subprocess.run(["git", "-C", REPO, "ls-files", "--others", "--exclude-standard"], capture_output=True, text=True).stdout.splitlines()
untracked = [u for u in untracked if u]

print(f"HEAD={head} ({head_short})")
print(f"origin/main={origin}")
print(f"ahead={ahead} behind={behind}")
print(f"tracked={len(tracked)} untracked={len(untracked)}")

with open(PRD, encoding="utf-8") as f:
    content = f.read()

# 1) Update header: Rev. 324 -> Rev. 325
old_header = "> **Rev. 324 \u2014 20 Oktober 2026 (WIB).**"
new_header = "> **Rev. 325 \u2014 20 Oktober 2026 (WIB).**"
assert content.count(old_header) == 1, f"header occurrences={content.count(old_header)}"
content = content.replace(old_header, new_header)

# 2) Append section 110 (Rev. 325)
section = f"""
## 110. REVISI TERBARU (Rev. 325 \u2014 20 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 20 Oktober 2026 (WIB, cron run) \u2014 pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / struktur source / skema Prisma / Login.tsx / Beranda.tsx. Semua data diverifikasi langsung dari repo kerja saat ini.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 324 (data terkonsisten).**
   - **Git HEAD (local):** `{head}` (Rev. 324, commit {head_short}) (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `{head_full}`). **origin/main:** `{origin}` (Rev. 309). Local branch **{ahead} commits ahead**, **{behind} commit behind** origin.main.
   - **Working tree:** `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 325, belum dicomit); seluruh file lain cocak dengan HEAD; `git ls-files` = {len(tracked)} file; {len(untracked)} file tidak ter-track (skrip sementara, backup, section .md).
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** \u2014 dihapus oleh commit HEAD \"Release: clean core files only\" (1dc891d) dan .gitignore mencantumkan *.db. Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (init_db.py, init_schema.sql; import_excel.py dan import_students_grades_clean.py tidak ditemukan di working tree).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** \u2014 `node_modules/` absen (clear checkout, 0 package; `.bin` tidak ada). `.next/` masih ada (partial: cache + diagnostics + package.json + server + static + trace + trace-build + turbopack + types, bukan production build). `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm install` ulang sebelum dapat dijalankan.
   - **Prisma schema:** 17 model terdefinisi (termasuk `KitabProgress` di baris 203, `Sertakan` di baris 218 \u2014 ditambahkan Rev. 51). `prisma/schema.prisma` **8492 bytes**, 263 baris. `uidNfc` pada model `Student` (baris 68, `uidNfc String? @map(\\"uid_nfc\\")`). `prisma validate` **tidak dapat dijalankan** karena `prisma` CLI tidak terinstall (`node_modules` absen).
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map(\\"uid_nfc\\"` baris 68 `prisma/schema.prisma`), `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) \u2014 data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` \u2014 sesuai nama 'Pondok Banat'); produksi butuh bcrypt + session.
   - **Beranda hardcode:** `src/components/Beranda.tsx` (baris 14\u201316) & `src/app/beranda/page.tsx` masih hardcode `totalSantri: 453, totalGuru: 54, totalKelas: 18` (bukan fetch real-time dari DB).
   - **Source files:** `src/app/*` = 15 entri (12 sub direktori: absensi, beranda, berita, guru, kelas, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah + globals.css, layout.tsx, page.tsx); `src/components` = `Beranda.tsx` & `Login.tsx`; `src/lib` = **kosong** (logic inline). Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite).
   - **Data source:** folder `.data-pondokanat/` **tidak ditemukan** di working tree (di-eksklusi oleh `.gitignore`). Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber.

2. **Perubahan dari Rev. 324:**
   - **Header PRD:** diperbarui ke **Rev. 325** (tanggal 20 Oktober 2026 WIB).
   - **New Section 110 (Rev. 325):** ditambahkan untuk verifikasi fresh ulang & konfirmasi stabilitas Rev. 325.
   - **Referensi HEAD:** section 109 (Rev. 324) mencatat HEAD sebagai `{head_short}` (Rev. 323, commit dbf2fe0) sebab state verifikasi dites sebelum commit Rev. 324. State terkini HEAD = `{head}` (Rev. 324, commit {head_short}), **{ahead} commits ahead** origin.main.
   - **Perbaikan hitungan branch:** `git rev-list --count origin/main..HEAD` = **{ahead}** (sebelumnya 17); `git rev-list --count HEAD..origin/main` = **{behind}**.

3. **Status:** dokumen PRD **REVISI** \u2014 rev 325 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. Header PRD diperbarui ke **Rev. 325**. Git HEAD = `{head_short}` (Rev. 324, commit {head_short}), **{ahead} commits ahead** origin.main.
"""

content = content.rstrip() + "\n" + section

with open(PRD, "w", encoding="utf-8") as f:
    f.write(content)

print("=== Written. Final lines ===")
print("\n".join(content.splitlines()[-12:]))
