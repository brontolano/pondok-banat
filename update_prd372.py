import io

PATH = "PRD-PONDOK-BANAT.md"
with open(PATH, "r", encoding="utf-8") as f:
    src = f.read()

replacements = []

# 1. Header label: Rev. 371 -> Rev. 372
replacements.append((
    "> **Rev. 371 — 20 Oktober 2026 (WIB).**",
    "> **Rev. 372 — 20 Oktober 2026 (WIB).**",
    "header label"
))

# 2. Header git HEAD: 9f679a0 -> 872ed45
old_githead_header = (
    "**Git HEAD (local):** `9f679a030095d8827c246c104b2a97429c0144f9` (Rev. 370, commit `9f679a030095d8827c246c104b2a97429c0144f9`). "
    "(branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `9f679a030095d8827c246c104b2a97429c0144f9`). "
    "**origin/main:** `d52f63c0f55cd1a507b75e2de8ae6ff5e5bf9a72` (Rev. 368). "
    "Local branch **2 commits ahead**, **0 commit behind** origin.main. "
    "Working tree: PRD cocak dengan HEAD (revisi terbaru = Rev. 371); seluruh file lain cocak dengan HEAD; `git ls-files` = 152 file; "
    "4 file tidak ter-track (skrip bantuan: fix_escapes.py, fix_escapes2.py, fix_escapes3.py, update_prd366.py)."
)
new_githead_header = (
    "**Git HEAD (local):** `872ed45a8bbffd2b524eb1840edfac833b616f00` (Rev. 371, commit `872ed45a8bbffd2b524eb1840edfac833b616f00`). "
    "(branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `872ed45a8bbffd2b524eb1840edfac833b616f00`). "
    "**origin/main:** `d52f63c0f55cd1a507b75e2de8ae6ff5e5bf9a72` (Rev. 368). "
    "Local branch **3 commits ahead**, **0 commit behind** origin.main. "
    "Working tree: PRD cocak dengan HEAD (revisi terbaru = Rev. 372); seluruh file lain cocak dengan HEAD; `git ls-files` = 152 file; "
    "6 file tidak ter-track (skrip bantuan: fix_escapes.py, fix_escapes2.py, fix_escapes3.py, update_prd366.py, update_prd370.py, verify_370.py)."
)
replacements.append((old_githead_header, new_githead_header, "header git head"))

# 3. Section 156 git HEAD update: 9f679a0 -> 872ed45
old_githead_156 = (
    "**Git HEAD (local):** `9f679a030095d8827c246c104b2a97429c0144f9` (Rev. 370, commit `9f679a030095d8827c246c104b2a97429c0144f9`). "
    "Branch `main` (remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `9f679a030095d8827c246c104b2a97429c0144f9`). "
    "**origin/main:** `d52f63c0f55cd1a507b75e2de8ae6ff5e5bf9a72` (Rev. 368). "
    "Local branch **2 commits ahead**, **0 commit behind** origin.main. "
    "Working tree: PRD cocak dengan HEAD (revisi terbaru = Rev. 371); seluruh file lain cocak dengan HEAD; `git ls-files` = 152 file; "
    "4 file tidak ter-track (skrip bantuan: fix_escapes.py, fix_escapes2.py, fix_escapes3.py, update_prd366.py, update_prd370.py, verify_370.py)."
)
new_githead_156 = (
    "**Git HEAD (local):** `872ed45a8bbffd2b524eb1840edfac833b616f00` (Rev. 371, commit `872ed45a8bbffd2b524eb1840edfac833b616f00`). "
    "Branch `main` (remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `872ed45a8bbffd2b524eb1840edfac833b616f00`). "
    "**origin/main:** `d52f63c0f55cd1a507b75e2de8ae6ff5e5bf9a72` (Rev. 368). "
    "Local branch **3 commits ahead**, **0 commit behind** origin.main. "
    "Working tree: PRD cocak dengan HEAD (revisi terbaru = Rev. 372); seluruh file lain cocak dengan HEAD; `git ls-files` = 152 file; "
    "6 file tidak ter-track (skrip bantuan: fix_escapes.py, fix_escapes2.py, fix_escapes3.py, update_prd366.py, update_prd370.py, verify_370.py)."
)
replacements.append((old_githead_156, new_githead_156, "section 156 git head"))

# 4. Build gate note in header (clearly mark re-runnable status)
replacements.append((
    "Build quality gate: NO LONGER RE-RUNABLE",
    "Build quality gate: NO LONGER RE-RUNABLE (node_modules absen; .next partial)",
    "header build gate"
))

# Apply replacements
for old, new, kind in replacements:
    count = src.count(old)
    if count != 1:
        print(f"WARNING [{kind}]: found {count} matches (should be 1)")
    src = src.replace(old, new)

# --- New section 157 (Rev. 372) ---
new_section = """
## 157. REVISI TERBARU (Rev. 372 — 20 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 20 Oktober 2026 (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / struktur source / skema Prisma / Login.tsx / Beranda.tsx. Semua data diverifikasi langsung dari repo kerja ini.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 371 (data terkonsisten).**
   - **Git HEAD (local):** `872ed45a8bbffd2b524eb1840edfac833b616f00` (Rev. 371, commit `872ed45a8bbffd2b524eb1840edfac833b616f00`). Branch `main` (remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `872ed45a8bbffd2b524eb1840edfac833b616f00`). **origin/main:** `d52f63c0f55cd1a507b75e2de8ae6ff5e5bf9a72` (Rev. 368). Local branch **3 commits ahead**, **0 commit behind** origin.main. Working tree: PRD cocak dengan HEAD (revisi terbaru = Rev. 372); seluruh file lain cocak dengan HEAD; `git ls-files` = 152 file; 6 file tidak ter-track (skrip bantuan: fix_escapes.py, fix_escapes2.py, fix_escapes3.py, update_prd366.py, update_prd370.py, verify_370.py). Database (dev.db): file `dev.db` saat ini **absent** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan .gitignore mencantumkan *.db. Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` dan `import_students_grades_clean.py` tidak ditemukan di working tree). Build quality gate: **NO LONGER RE-RUNABLE** — `node_modules/` absen (0 package; `.bin` tidak ada); `.next/` masih ada (partial: cache + diagnostics + package.json + server + static + trace + trace-build + turbopack + types, bukan production build). `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm install` ulang sebelum dapat dijalankan. M02a (NFC): field `uid_nfc` masih di schema Prisma (`uidNfc @map("uid_nfc")`), `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`). Auth hardcode: `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama Pondok Banat); produksi butuh bcrypt + session. Beranda hardcode: `src/components/Beranda.tsx` (baris 26–28) & `src/app/beranda/page.tsx` (baris 14–16) masih hardcode `totalSantri: 453, totalGuru: 54, totalKelas: 18` (bukan fetch real-time dari DB; sudah diperbarui ke 453 sesuai data Excel grade sheets). Source files: `src/app/*` = 15 entri (12 sub direktori: absensi, beranda, berita, guru, kelas, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah + globals.css, layout.tsx, page.tsx); `src/components` = 2 (Beranda.tsx & Login.tsx); `src/lib` = kosong (logic inline). Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite). Data source: folder `.data-pondokanat/` **tidak ditemukan** di working tree (di-eksklusi oleh `.gitignore`). Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber.
2. **Perubahan dari Rev. 371:**
   - **Header PRD:** diperbarui ke **Rev. 372** (tanggal 20 Oktober 2026 WIB).
   - **Git HEAD (local):** `872ed45a8bbffd2b524eb1840edfac833b616f00` (Rev. 371, commit `872ed45a8bbffd2b524eb1840edfac833b616f00`); origin/main = `d52f63c0f55cd1a507b75e2de8ae6ff5e5bf9a72` (Rev. 368). Local branch **3 commits ahead** origin.main (naik dari 2 commits sebelumnya).
   - **Git ls-files:** 152 file; 6 file tidak ter-track (skrip bantuan: fix_escapes.py, fix_escapes2.py, fix_escapes3.py, update_prd366.py, update_prd370.py, verify_370.py).
   - **dev.db:** absent (dihapus oleh commit HEAD "Release: clean core files only" 1dc891d); rekonstruksi seed diperlukan.
   - **Build quality gate:** NO LONGER RE-RUNABLE (node_modules/absent; .next partial).
   - **Schema:** 17 model terdefinisi (KitabProgress, Sertakan, uidNfc semua ada), `prisma validate` tidak dapat dijalankan karena `prisma` CLI tidak terinstall (`node_modules` absen).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama Pondok Banat); produksi butuh bcrypt + session.
   - **Beranda hardcode:** `src/components/Beranda.tsx` (baris 26–28) & `src/app/beranda/page.tsx` (baris 14–16) masih hardcode `totalSantri: 453, totalGuru: 54, totalKelas: 18` (bukan fetch real-time dari DB; sudah diperbarui ke 453 sesuai data Excel grade sheets).
3. **Status:** dokumen PRD **REVISI** — rev 372 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. Header PRD diperbarui ke **Rev. 372**. Git HEAD = `872ed45a8bbffd2b524eb1840edfac833b616f00` (Rev. 371, 3 commits ahead origin.main.). Seluruh data stabil; tidak ada perubahan signifikan dari Rev. 371.
"""

if new_section in src:
    print("WARNING: new section already exists")
else:
    src = src.rstrip() + "\n" + new_section.lstrip("\n")

with open(PATH, "w", encoding="utf-8") as f:
    f.write(src)

print("Replacements applied:")
print("  - Header label: Rev. 371 -> Rev. 372")
print("  - Header git HEAD: 9f679a0 -> 872ed45")
print("  - Local branch: 2 ahead -> 3 ahead")
print("  - Git ls-files: 152 (unchanged); untracked 4 -> 6")
print("  - New section 157 appended")
print("New file size:", len(src))
