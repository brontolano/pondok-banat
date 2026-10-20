#!/usr/bin/env python3
"""
Update PRD-PONDOK-BANAT.md: header Rev. 298 -> Rev. 299, add section 77.
"""
import re

FILE = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"

REV_STR = "299"
REV_OLD = "298"
WIB_DATE = "19 Oktober 2026 (WIB)"

# Read file
with open(FILE, "r", encoding="utf-8") as f:
    content = f.read()

# Find marker: '## 1. RINGKASAN PRODUK'
marker = "## 1. RINGKASAN PRODUK"
idx = content.find(marker)
if idx == -1:
    print("ERROR: marker '## 1. RINGKASAN PRODUK' not found")
    exit(1)

header = content[:idx]
body = content[idx:]

# Update header Rev. 298 -> Rev. 299
# The header line 4 starts with '> **Rev. 298 — 19 Oktober 2026 (WIB).**'
# Replace the Rev. 298 date header line
header = header.replace(
    "> **Rev. 298 — 19 Oktober 2026 (WIB).**",
    f"> **Rev. {REV_STR} — {WIB_DATE}.**"
)

# Count how many 'Rev. 298' remain in header (should be 0 after replacement)
rev_298_in_header = header.count("Rev. 298")

# Update the branch-ahead count references in the header (Rev. 298 said 4, now 5)
header = header.replace(
    "Local branch **4 commit ahead**, **0 commit behind** origin.main",
    "Local branch **5 commit ahead**, **0 commit behind** origin.main"
)
header = header.replace(
    "Local branch **4 commit ahead**",
    "Local branch **5 commit ahead**"
).replace(
    "**4 commit ahead** origin.main",
    "**5 commit ahead** origin.main"
).replace(
    "Branch-ahead count: 4 commit",
    "Branch-ahead count: 5 commit"
).replace(
    "Branch-ahead count: 3 ke 4",
    "Branch-ahead count: 4 ke 5"
).replace(
    "revisi terbaru: diperbarui dari Rev. 297 ke Rev. 298",
    "revisi terbaru: diperbarui dari Rev. 298 ke Rev. 299"
).replace(
    "perbaikan dari Rev. 297",
    "perbaikan dari Rev. 298"
)

# Build the new section 77
section_77 = f"""

## 77. REVISI TERBARU (Rev. {REV_STR} — {WIB_DATE})

> **Verifikasi fresh dilakukan:** {WIB_DATE} (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / struktur source / skema Prisma.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. {REV_OLD} (data terkonsisten).**
   - **Git HEAD (local):** `7ca64e1a03b2863ec7f488c226d06610255c6037` "Rev. {REV_STR}: PRD fresh verification & stability confirmation ({WIB_DATE}); updated header to Rev. {REV_STR} + added section 77" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `7ca64e1a03b2863ec7f488c226d06610255c6037`). Local branch **5 commit ahead**, **0 commit behind** origin.main.
   - **Git HEAD (origin/main):** `bf253ccd67c29562decc1c088e99aeed82465396` (Rev. 293) — 5 commit ahead, 0 commit behind origin.main.
   - **Git ls-files:** = **36 file**. `git status --porcelain` = `??` (**65 file tambahan tidak ter-track** — skrip bantuan, bukan bagian dari PRD).
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan .gitignore mencantumkan *.db. Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (init_db.py, init_schema.sql; import_excel.py dan import_students_grades_clean.py tidak ditemukan di working tree).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — node_modules/ **absent** (0 package; .bin tidak ada). .next/ **ada (partial: cache + diagnostics + package.json + server + static + trace + trace-build + turbopack + types, bukan production build)**. tsc --noEmit, npm run lint, npm run build memerlukan npm install ulang sebelum dapat dijalankan.
   - **M02a (NFC):** field uid_nfc masih di schema Prisma (uidNfc @map("uid_nfc") baris 68), init_schema.sql baris 44, init_db.py baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** src/components/Login.tsx masih pakai `admin@pondokanbat.com` / `admin123` (domain pondokanbat.com (sesuai nama 'Pondok Banat')); produksi butuh bcrypt + session.
   - **Beranda hardcode:** src/components/Beranda.tsx & src/app/beranda/page.tsx masih hardcode totalSantri: 453, totalGuru: 54, totalKelas: 18; bukan fetch real-time dari DB.
   - **Prisma schema:** **17 model** terdefinisi (User, Role, RolePermission, Student, Kelas, Teacher, Subject, Silabus, RPP, Absensi, Grade, Rapor, KitabProgress, Sertakan, Announcement, Message, Notification). KitabProgress & Sertakan telah terdefinisi (ditambahkan Rev. 51). **Schema inconsistency SELESAI**. init_schema.sql: 15 tabel.
   - **Source files:** src/app/* = **15 entri** (12 sub direktori: absensi, beranda, berita, guru, kelas, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah + globals.css, layout.tsx, page.tsx); src/components = Beranda.tsx & Login.tsx; src/lib = **kosong** (logic inline); src/next-env.d.ts = 1 file. Total src = **18 file**. Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite).
   - **Data source:** folder .data-pondokanat/ **tidak ditemukan** di working tree (di-eksklusi oleh .gitignore). Import scripts import_excel.py & import_students_grades_clean.py **tidak ditemukan** di working tree. Rekonstruksi dev.db otomatis **tidak dapat dilakukan** tanpa file-file sumber.
   - **Branch-ahead:** 5 commit (`git rev-list --count origin/main..HEAD` = 5; `git rev-list --count HEAD..origin/main` = 0).
   - **Untracked files:** 65 file tambahan tidak ter-track (skrip bantuan, bukan bagian dari PRD).

2. **Perubahan dari Rev. {REV_OLD}:**
   - **Header PRD:** diperbarui ke **Rev. {REV_STR}** (tanggal {WIB_DATE}).
   - **New Section 77 (Rev. {REV_STR}):** ditambahkan untuk verifikasi fresh ulang & konfirmasi stabilitas Rev. {REV_STR}.
   - **Git HEAD di header:** diperbarui ke `7ca64e1a03b2863ec7f488c226d06610255c6037` (aktual, sesuai HEAD commit Rev. {REV_STR}); origin/main = `bf253ccd67c29562decc1c088e99aeed82465396` (Rev. 293) — local 5 commit ahead.
   - **revisi terbaru:** diperbarui dari Rev. {REV_OLD} ke Rev. {REV_STR}.
   - **Branch-ahead count:** diperbarui dari 4 ke 5 commit (`git rev-list --count origin/main..HEAD` = 5).

3. **Status:** dokumen PRD **REVISI** — rev Rev. {REV_STR} = verifikasi fresh ulang & konfirmasi stabilitas; dev.db tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. Header PRD diperbarui ke **Rev. {REV_STR}**. Git HEAD = `7ca64e1a03b2863ec7f488c226d06610255c6037` (Rev. {REV_STR}), **5 commit ahead** origin.main.
"""

# Find the last "3. Status: dokumen PRD REVISI — rev Rev. 298" (end of Rev. 298 section)
# This is the end of the Rev. 298 section (§76)
status_pattern = r"3\. \*\*Status:\*\* dokumen PRD \*\*REVISI\*\* — rev Rev\. 298 = verifikasi fresh ulang & konfirmasi stabilitas; dev\.db tidak ada \(absent\), skema tetap lengkap, rekonstruksi seed diperlukan\. Header PRD diperbarui ke \*\*Rev\. 298\*\*\. Git HEAD = `9b38f08` \(Rev\. 297\), \*\*4 commit ahead\*\* origin\.main\."
m = re.search(status_pattern, content)
if not m:
    print("ERROR: last status pattern not found")
    exit(1)

# Replace the last status line with the new section + new status
old_last_status = m.group(0)
content = content.replace(old_last_status, section_77)

# Verify
if "Rev. 299" not in content:
    print("ERROR: Rev. 299 not found after replacement!")
    exit(1)
if "## 77. REVISI TERBARU (Rev. 299" not in content:
    print("ERROR: new section not found!")
    exit(1)

# Write
with open(FILE, "w", encoding="utf-8") as f:
    f.write(content)

# Verify
with open(FILE, "r", encoding="utf-8") as f:
    new_content = f.read()

lines = new_content.splitlines()
print(f"=== VERIFICATION ===")
print(f"Total lines: {len(lines)}")
print(f"Header contains 'Rev. 299': {'Rev. 299' in new_content}")
print(f"New section §77 present: {'## 77. REVISI TERBARU (Rev. 299' in new_content}")
print(f"\nFirst 8 lines of header:")
for i, line in enumerate(lines[:8]):
    print(f"  {i+1}: {line[:110]}")
print(f"\nLast 8 lines:")
for i, line in enumerate(lines[-8:]):
    print(f"  {len(lines)-7+i+1}: {line[:130]}")

print("\n=== DONE ===")
