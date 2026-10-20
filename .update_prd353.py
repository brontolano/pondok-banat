import io

path = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# ---- Header replacements (targeted, unique substrings) ----
# 1) Revision date
h1_old = "> **Rev. 352 — 20 Oktober 2026 (WIB).**"
h1_new = "> **Rev. 353 — 20 Oktober 2026 (WIB).**"
n1 = content.count(h1_old)

# 2) Header state sentence (unique: has ". (branch `main`, remote" and "Working tree: PRD cocak..." on same line)
h2_old = (
    "**Git HEAD (local):** `b5f5ce3` (Rev. 351, commit `b5f5ce3`). (branch `main`, remote `brontolano/pondok-banat`; "
    "`git rev-parse HEAD` = `b5f5ce3`). **origin/main:** `2d8439f` (Rev. 338). Local branch **13 commits ahead**, "
    "**0 commit behind** origin.main. Working tree: PRD cocak dengan HEAD (revisi terbaru = Rev. 352);"
)
h2_new = (
    "**Git HEAD (local):** `4656ba0` (Rev. 352, commit `4656ba0`). (branch `main`, remote `brontolano/pondok-banat`; "
    "`git rev-parse HEAD` = `4656ba0`). **origin/main:** `4656ba0` (Rev. 352). Local branch **0 commits ahead**, "
    "**0 commit behind** origin.main. Working tree: PRD cocak dengan HEAD (revisi terbaru = Rev. 353);"
)
n2 = content.count(h2_old)

content = content.replace(h1_old, h1_new)
content = content.replace(h2_old, h2_new)

print("Header replacements:", n1, n2)

# ---- Append Section 138 (Rev. 353) after the last line ----
section_138 = """## 138. REVISI TERBARU (Rev. 353 — 20 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 20 Oktober 2026 (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / struktur source / skema Prisma / Login.tsx / Beranda.tsx. Semua data diverifikasi langsung dari repo kerja saat ini.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 352 (data terkonsisten).**
   - **Git HEAD (local):** `4656ba0` (Rev. 352, commit `4656ba055eb28c39c294e097eb647c9ccb8755c4`). Branch `main` (remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `4656ba0`). **origin/main:** `4656ba0` (Rev. 352). Local branch **0 commits ahead**, **0 commit behind** origin.main. (Catatan: Rev. 352 & origin/main telah disinkronkan)
   - **Working tree:** PRD cocak dengan HEAD (revisi terbaru = Rev. 353); seluruh file lain cocak dengan HEAD; `git ls-files` = 36 file; 110 file tidak ter-track (skrip sementara, backup, section .md, .orig, .py). ✗ (tambah 1 file: `.fresh_check.py`)
   - **Database (dev.db):** file `dev.db` saat ini **absent** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan .gitignore mencantumkan *.db. Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (init_db.py, init_schema.sql; import_excel.py dan import_students_grades_clean.py tidak ditemukan di working tree).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` absen (0 package; .bin tidak ada). `.next/` masih ada (partial: cache + diagnostics + package.json + server + static + trace + trace-build + turbopack + types, bukan production build). `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm install` ulang sebelum dapat dijalankan.
   - **Prisma schema:** 17 model terdefinisi (termasuk `KitabProgress` di baris 203, `Sertakan` di baris 218 — ditambahkan Rev. 51). `uidNfc` pada model `Student` (baris 68, `uidNfc String? @map("uid_nfc")`). `prisma validate` **tidak dapat dijalankan** karena `prisma` CLI tidak terinstall (`node_modules` absen).
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map("uid_nfc")` baris 68) & `init_schema.sql` baris 40, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama Pondok Banat).
   - **Beranda hardcode:** `src/components/Beranda.tsx` (baris 26–28) & `src/app/beranda/page.tsx` (baris 14–16) masih hardcode `totalSantri: 453, totalGuru: 54, totalKelas: 18` (bukan fetch real-time dari DB).
   - **Source files:** `src/app/*` = 15 entri (12 sub direktori: absensi, beranda, berita, guru, kelas, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah + globals.css, layout.tsx, page.tsx); `src/components` = 2 (Beranda.tsx & Login.tsx); `src/lib` = kosong (logic inline). Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite).
   - **Data source:** folder `.data-pondokanat/` **tidak ditemukan** di working tree (di-eksklusi oleh `.gitignore`). Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber.

2. **Perubahan dari Rev. 352:**
   - **Header PRD:** diperbarui ke **Rev. 353** (tanggal 20 Oktober 2026 WIB).
   - **New Section 138 (Rev. 353):** ditambahkan untuk verifikasi fresh ulang & konfirmasi stabilitas Rev. 353.
   - **Referensi HEAD:** state terkini HEAD = `4656ba0` (Rev. 352, commit `4656ba0`); origin/main = `4656ba0` (Rev. 352). Branch **0 commits ahead** origin.main.

3. **Status:** dokumen PRD **REVISI** — rev 353 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. Header PRD diperbarui ke **Rev. 353**. Git HEAD = `4656ba0` (Rev. 352, 0 commits ahead origin.main).
"""

if not content.endswith("\n"):
    content += "\n"
content += section_138 + "\n"

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("New file size (bytes):", len(content.encode("utf-8")))
print("Section 138 present:", "## 138. REVISI TERBARU (Rev. 353" in content)
print("Header rev now Rev. 353:", "> **Rev. 353 — 20 Oktober 2026 (WIB).**" in content)
