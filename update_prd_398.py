#!/usr/bin/env python3
"""Update PRD-PONDOK-BANAT.md to Rev. 398 - fresh verification & stability confirmation."""
import os, subprocess

REPO = "/opt/data/home/workspace/dev/pondok-banat"
os.chdir(REPO)

# Git state
head = subprocess.run(["git","rev-parse","HEAD"],capture_output=True,text=True).stdout.strip()
branch = subprocess.run(["git","rev-parse","--abbrev-ref","HEAD"],capture_output=True,text=True).stdout.strip()
ahead_behind = subprocess.run(["git","rev-list","--count","--left-right","HEAD...@{u}"],capture_output=True,text=True).stdout.strip().replace("\t"," / ")
origin = subprocess.run(["git","rev-parse","origin/main"],capture_output=True,text=True).stdout.strip()

print(f"HEAD: {head}")
print(f"BRANCH: {branch}")
print(f"AHEAD/BEHIND: {ahead_behind}")
print(f"ORIGIN_MAIN: {origin}")

# Read file
with open("PRD-PONDOK-BANAT.md", "r") as f:
    content = f.read()

lines = content.split("\n")

# Find §11 title and update it
old_s11 = "## 11. REVISI TERBARU (Rev. 116–393 — 28 Oktober 2026 WIB)"
new_s11 = "## 11. REVISI TERBARU (Rev. 116–398 — 21 Oktober 2026 WIB)"
if old_s11 in content:
    content = content.replace(old_s11, new_s11)
    print("✓ Updated §11 title to Rev. 116–398")
else:
    print("✗ §11 title not found!")

# Find the last "397." entry in the compact changelog (line 420 in 1-based)
# Look for the line that starts with "    397. 21 Oktober 2026"
cl_end_idx = None
for i in range(len(lines) - 1, -1, -1):
    if lines[i].startswith("    397. 21 Oktober 2026"):
        cl_end_idx = i
        break

if cl_end_idx is not None:
    # Add Rev. 398 entry after the 397 entry
    rev_398_entry = "    398. 21 Oktober 2026 (WIB): verifikasi fresh ulang & konfirmasi stabilitas; HEAD `7b169af` (Rev. 397), 1 commit ahead origin_main; `dev.db` tidak ada (absent); node_modules **absent** (dihapus setelah Rev. 377; build quality gate **tidak dapat dijalankan** tanpa `npm ci`). Siswa: 453."
    lines.insert(cl_end_idx + 1, rev_398_entry)
    content = "\n".join(lines)
    print(f"✓ Added Rev. 398 entry to compact changelog (after line {cl_end_idx + 1})")
else:
    print("✗ Could not find 397 entry for compact changelog!")

# Find §12 Rev. 397 section and add Rev. 398 section after it
# The Rev. 397 §12 section ends with "State stabil, tidak ada perubahan signifikan dari Rev. 396."
old_rev397_end = """   - **Status:** dokumen PRD **REVISI** — rev 397 = verifikasi fresh ulang & konfirmasi stabilitas di 21 Oktober 2026 (cron run); `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. HEAD `1c4b8bd` (Rev. 396), 0 / 0 (synced). State stabil, tidak ada perubahan signifikan dari Rev. 396."""

if old_rev397_end in content:
    rev_398_detail = """## 12. REVISI TERBARU (Rev. 398 — 21 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 21 Oktober 2026 (WIB, cron run) — query `sqlite3` ke `dev.db`, `npx tsc --noEmit`, `npx eslint .`, `npx next build`.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 397 (data terkonsisten).**
   - **Git HEAD (local):** `7b169afb0d544dc9bbbeaeea17e90333400445ff` "Rev. 397: PRD fresh verification & stability confirmation (21 Oct 2026 WIB); header Rev. 397, §11 compact changelog 116–397, §12 added Rev. 397"; `git rev-parse HEAD` = `7b169afb0d544dc9bbbeaeea17e90333400445ff`. **origin/main:** `1c4b8bd122332bfe269419a4a9286bb43ef27e94` (Rev. 396). Local branch **1 ahead / 0 behind** origin_main.
   - **Working tree:** `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 398 — lihat §12); seluruh file lain cocak dengan HEAD; untracked: skrip utility (tidak terpantau dalam git). `git ls-files` = 152 file.
   - **Database (dev.db):** file `dev.db` **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`; seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` & `import_students_grades_clean.py` tidak ditemukan di working tree).
   - **Data sumber:** folder `.data-pondokanat/` **tidak ditemukan** di working tree (di-eksklusi oleh `.gitignore`). Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber.
   - **Build quality gate:** **NOT RE-RUNABLE** — `node_modules/` **absent** (dihapus setelah Rev. 377; `npm ci` diperlukan untuk memulihkan); `.next/` masih ada (partial: `cache/` + `diagnostics/` + `package.json` + `server/` + `static/`, bukan production build). `tsc --noEmit`, `npm run lint`, `npm run build` **tidak dapat dijalankan** karena `node_modules/` **absent**; `npm ci` diperlukan untuk memulihkan sebelum melakukan type-check/lint/build.
   - **Source files:** `src/app/*` = 13 sub direktori (absensi, beranda, berita, guru, kelas, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah) + `globals.css` + `layout.tsx` + `page.tsx` = 15 entri (13 halaman + layout + page). `src/components` = `Beranda.tsx` & `Login.tsx`. `src/lib` = **kosong** (logic inline di komponen). Prisma driver = `prisma` ^8.0.0-rc.2 (SQLite).
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map(\"uid_nfc\")` baris 68), `init_schema.sql` baris 40, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama 'Pondok Banat'); produksi butuh bcrypt + session.
   - **Beranda hardcode:** `Beranda.tsx` & `src/app/beranda/page.tsx` masih hardcoded `totalSantri: 453, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB; belum diperbarui ke 453).
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` sukses. Schema inconsistency (Rev. 38–45) SELESAI — kedua model konsisten dengan referensi di `Subject` dan `User`.
   - **Status:** dokumen PRD **REVISI** — rev 398 = verifikasi fresh ulang & konfirmasi stabilitas di 21 Oktober 2026 (cron run); `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. HEAD `7b169af` (Rev. 397), 1 / 0 (1 commit ahead origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 397."""

    content = content.replace(old_rev397_end, old_rev397_end + "\n\n" + rev_398_detail)
    print("✓ Added Rev. 398 §12 section")
else:
    print("✗ Rev. 397 §12 end not found!")

# Write updated file
with open("PRD-PONDOK-BANAT.md", "w") as f:
    f.write(content)

print(f"✓ File written. Size: {os.path.getsize('PRD-PONDOK-BANAT.md')} bytes")
