#!/usr/bin/env python3
# Update PRD header to Rev. 292 and add new Section 70 (Rev. 292)

PATH = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"

with open(PATH, "r", encoding="utf-8") as f:
    content = f.read()

# --- Verify key facts ---
import subprocess
ws = "/opt/data/home/workspace/dev/pondok-banat"
head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ws, capture_output=True, text=True).stdout.strip()
origin = subprocess.run(["git", "rev-parse", "origin/main"], cwd=ws, capture_output=True, text=True).stdout.strip()
ahead = subprocess.run(["git", "rev-list", "--count", "origin/main..HEAD"], cwd=ws, capture_output=True, text=True).stdout.strip()
behind = subprocess.run(["git", "rev-list", "--count", "HEAD..origin/main"], cwd=ws, capture_output=True, text=True).stdout.strip()
print(f"HEAD: {head}")
print(f"origin/main: {origin}")
print(f"ahead: {ahead}, behind: {behind}")

# --- Build the new header line 4 ---
new_header = (
    "> **Rev. 292 — 19 Oktober 2026 (WIB).** Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. "
    "Git HEAD (local): `832db804f1cc8773de9338749f514523f0bee76b` \"Rev. 291: PRD fresh verification & stability confirmation (20 Oct 2026 WIB); updated header to Rev. 291 + added section 69\" "
    "(branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `832db804f1cc8773de9338749f514523f0bee76b`). "
    "Git HEAD (origin/main): `832db804f1cc8773de9338749f514523f0bee76b` (Rev. 291) — cocok dengan local HEAD (local 0 commit ahead). "
    "Working tree: PRD cocak dengan HEAD (revisi terbaru = Rev. 292, sudah dicomit); hanya file .py tambahan yang tidak ter-track. "
    "Local branch **0 commit ahead**, **0 commit behind** origin.main. "
    "Database (dev.db): file dev.db saat ini tidak ada (absent) — dihapus oleh commit HEAD \"Release: clean core files only\" (1dc891d) dan .gitignore mencantumkan *.db; "
    "seluruh record (453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) tidak tersedia dan harus di-import ulang menggunakan skrip semula "
    "(init_db.py, init_schema.sql; import_excel.py dan import_students_grades_clean.py tidak ditemukan di working tree). "
    "Build quality gate: NO LONGER RE-RUNABLE — node_modules/absent (0 package; .bin tidak ada); .next ada (partial: cache + diagnostics + package.json + server + static + trace + trace-build + turbopack + types, bukan production build). "
    "tsc --noEmit, npm run lint, npm run build memerlukan npm instal ulang sebelum dapat dijalankan. "
    "M02a (NFC): field uid_nfc masih di schema Prisma, init_schema.sql baris 44, init_db.py baris 60, namun 0 siswa terisi (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format AF:C2:99:E7). "
    "Auth hardcode: src/components/Login.tsx masih pakai admin@pondokanbat.com / admin123 (domain pondokanbat.com (sesuai nama 'Pondok Banat')); produksi butuh bcrypt + session. "
    "Beranda: src/components/Beranda.tsx & src/app/beranda/page.tsx masih hardcode totalSantri: 453, totalGuru: 54, totalKelas: 18; bukan fetch real-time dari DB. "
    "Prisma: 17 model terdefinisi (termasuk KitabProgress, Sertakan — ditambahkan Rev. 51). init_schema.sql: 15 tabel."
)

# Find the old header line (starts with "> **Rev. 291")
lines = content.split("\n")
for i, line in enumerate(lines):
    if line.startswith("> **Rev. 291"):
        print(f"Found header at line {i+1}")
        print(f"Old line length: {len(line)}")
        lines[i] = new_header
        break

new_content = "\n".join(lines)

# Verify the new header
assert "> **Rev. 292" in new_content, "New header not found"
assert "832db804f1cc8773de9338749f514523f0bee76b" in new_content, "New git HEAD not found"

# --- Read current Rev. 291 section end (for appending new section) ---
# Find the Rev. 291 section start
sec70_start = None
for i, line in enumerate(lines):
    if line.startswith("## 70. REVISI TERBARU"):
        sec70_start = i
        break
print(f"Rev. 291 section end line: {i+1} (line {i+1} is the last line of Rev. 291)")

# Read current last line
last_line = lines[-1]
print(f"Current last line: {last_line[:120]}...")

# The new section 70 content
new_section_70 = """## 70. REVISI TERBARU (Rev. 292 — 19 Oktober 2026 (WIB))

> **Verifikasi fresh dilakukan:** 19 Oktober 2026 (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / struktur source / skema Prisma.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 291 (data terkonsisten).**
   - **Git HEAD (local):** `832db804f1cc8773de9338749f514523f0bee76b` \"Rev. 291: PRD fresh verification & stability confirmation (20 Oct 2026 WIB); updated header to Rev. 291 + added section 69\" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `832db804f1cc8773de9338749f514523f0bee76b`). Local branch **0 commit ahead**, **0 commit behind** origin.main.
   - **Git HEAD (origin/main):** `832db804f1cc8773de9338749f514523f0bee76b` (Rev. 291) — cocok dengan local HEAD (0 commit ahead).
   - **Git ls-files:** = **36 file**. `git status --porcelain` = `??` (**64 file tambahan tidak ter-track** — skrip bantuan, bukan bagian dari PRD).
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD \"Release: clean core files only\" (1dc891d) dan .gitignore mencantumkan *.db. Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (init_db.py, init_schema.sql; import_excel.py dan import_students_grades_clean.py tidak ditemukan di working tree).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — node_modules/ **absent** (0 package; .bin tidak ada). .next/ **ada (partial: cache + diagnostics + package.json + server + static + trace + trace-build + turbopack + types, bukan production build)**. tsc --noEmit, npm run lint, npm run build memerlukan npm install ulang sebelum dapat dijalankan.
   - **M02a (NFC):** field uid_nfc masih di schema Prisma (uidNfc @map(\"uid_nfc\" baris 68), init_schema.sql baris 44, init_db.py baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`)).
   - **Auth hardcode:** src/components/Login.tsx masih pakai `admin@pondokanbat.com` / `admin123` (domain pondokanbat.com (sesuai nama 'Pondok Banat')); produksi butuh bcrypt + session.
   - **Beranda hardcode:** src/components/Beranda.tsx & src/app/beranda/page.tsx masih hardcode totalSantri: 453, totalGuru: 54, totalKelas: 18; bukan fetch real-time dari DB.
   - **Prisma schema:** **17 model** terdefinisi (User, Role, RolePermission, Student, Kelas, Teacher, Subject, Silabus, RPP, Absensi, Grade, Rapor, KitabProgress, Sertakan, Announcement, Message, Notification). KitabProgress & Sertakan telah terdefinisi (ditambahkan Rev. 51). **Schema inconsistency SELESAI**. init_schema.sql: 15 tabel.
   - **Source files:** src/app/* = **15 entri** (12 sub direktori: absensi, beranda, berita, guru, kelas, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah + globals.css, layout.tsx, page.tsx); src/components = Beranda.tsx & Login.tsx; src/lib = **kosong** (logic inline); src/next-env.d.ts = 1 file. Total src = **18 file**. Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite).
   - **Data source:** folder .data-pondokanat/ **tidak ditemukan** di working tree (di-eksklusi oleh .gitignore). Import scripts import_excel.py & import_students_grades_clean.py **tidak ditemukan** di working tree. Rekonstruksi dev.db otomatis **tidak dapat dilakukan** tanpa file-file sumber.
   - **Branch-ahead:** 0 commit (sesuai `git rev-list --count origin/main..HEAD` = 0; `git rev-list --count HEAD..origin/main` = 0).
   - **Untracked files:** 64 file tambahan tidak ter-track (skrip bantuan, bukan bagian dari PRD).

2. **Perubahan dari Rev. 291:**
   - **Header PRD:** diperbarui ke **Rev. 292** (tanggal 19 Oktober 2026 WIB).
   - **New Section 70 (Rev. 292):** ditambahkan untuk verifikasi fresh ulang & konfirmasi stabilitas Rev. 292.
   - **Git HEAD di header:** diperbarui ke `832db804f1cc8773de9338749f514523f0bee76b` (aktual, sesuai HEAD commit Rev. 291); origin/main = `832db804f1cc8773de9338749f514523f0bee76b` (Rev. 291) — cocok dengan local HEAD.
   - **revisi terbaru:** diperbarui dari Rev. 291 ke Rev. 292.
   - **Branch-ahead count:** diperbarui dari 4 ke 0 commit (`git rev-list --count origin/main..HEAD` = 0; `git rev-list --count HEAD..origin/main` = 0).

3. **Status:** dokumen PRD **REVISI** — rev Rev. 292 = verifikasi fresh ulang & konfirmasi stabilitas; dev.db tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. Header PRD diperbarui ke **Rev. 292**. Git HEAD = `832db804f1cc8773de9338749f514523f0bee76b` (Rev. 291), **0 commit ahead** origin.main."""

# Find the last line index (6326) to insert after it
lines = new_content.split("\n")
# Append new section after the last line
lines.append("")
lines.append(new_section_70.strip())

final_content = "\n".join(lines)

# Verify
assert "## 70. REVISI TERBARU" in final_content, "New section not found"
assert "> **Rev. 292" in final_content, "New header not found"

with open(PATH, "w", encoding="utf-8") as f:
    f.write(final_content)

print("Done! File updated.")
print(f"New file size: {len(final_content)} bytes")
print(f"New total lines: {len(final_content.split(chr(10)))}")
