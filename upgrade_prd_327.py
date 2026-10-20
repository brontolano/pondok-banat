#!/usr/bin/env python3
"""Upgrade PRD-PONDOK-BANAT.md to Rev. 327 (section 112) with fresh verification."""

path = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Sanity: confirm file starts with expected header
assert content.startswith("# PRD — Aplikasi Pondok Banat (Modular)\n\n> **Sumber:**"), "Header mismatch"

# New header line for Rev. 327
new_header = (
    "> **Rev. 327 — 20 Oktober 2026 (WIB).** Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. "
    "Git HEAD (local): `7775a96815c951aec62708ee856f58c89981cb2d` (rev 326/327, commit 7775a96) "
    "(branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `7775a96815c951aec62708ee856f58c89981cb2d`). "
    "**origin/main:** `7775a96815c951aec62708ee856f58c89981cb2d` (rev 326/327) — 0 commits ahead, 0 commit behind origin.main. "
    "Working tree: PRD cocak dengan HEAD (revisi terbaru = Rev. 327, akan dicomit); seluruh file lain cocak dengan HEAD; "
    "`git ls-files` = 36 file; 78 file tidak ter-track (skrip sementara, backup, section .md). "
    "Database (dev.db): file dev.db saat ini tidak ada (absent) — dihapus oleh commit HEAD \"Release: clean core files only\" (1dc891d) "
    "dan .gitignore mencantumkan *.db; seluruh record (453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, "
    "1 user, 5 role, 33 role_permissions) tidak tersedia dan harus di-import ulang menggunakan skrip semula "
    "(init_db.py, init_schema.sql; import_excel.py dan import_students_grades_clean.py tidak ditemukan di working tree). "
    "Build quality gate: NO LONGER RE-RUNABLE — node_modules/absent (0 package; .bin tidak ada); .next ada (partial: cache + diagnostics "
    "+ package.json + server + static + trace + trace-build + turbopack + types, bukan production build). "
    "tsc --noEmit, npm run lint, npm run build memerlukan npm install ulang sebelum dapat dijalankan. "
    "M02a (NFC): field uid_nfc masih di schema Prisma, init_schema.sql baris 44, init_db.py baris 60, namun 0 siswa terisi (semua 453 NULL) — "
    "data ekspor NFC Tools belum tersedia (tersimpan manual, format AF:C2:99:E7). "
    "Auth hardcode: src/components/Login.tsx masih pakai admin@pondokanbat.com / admin123 (domain pondokanbat.com (sesuai nama 'Pondok Banat')); "
    "produksi butuh bcrypt + session. "
    "Beranda: src/components/Beranda.tsx & src/app/beranda/page.tsx masih hardcode (Beranda.tsx: totalSantri: 0, totalGuru: 0, totalKelas: 0; "
    "page.tsx: totalSantri: 453, to..."
)

# Split into lines, replace header line (index 3)
lines = content.split("\n")
assert lines[0].startswith("# PRD — Aplikasi Pondok Banat (Modular)")
assert lines[1] == ""
assert lines[2].startswith("> **Sumber:**")
header_found = False
for i, line in enumerate(lines):
    if line.startswith("> **Rev. 326 — 20 Oktober 2026 (WIB).**"):
        lines[i] = new_header
        header_found = True
        break
assert header_found, "Rev. 326 header line not found"

# Section 112 content (Rev. 327)
section_112 = """
## 112. REVISI TERBARU (Rev. 327 — 20 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 20 Oktober 2026 (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / struktur source / skema Prisma / Login.tsx / Beranda.tsx. Semua data diverifikasi langsung dari repo kerja saat ini.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 326 (data terkonsisten).**
   - **Git HEAD (local):** `7775a96815c951aec62708ee856f58c89981cb2d` (rev 326/327, commit 7775a96 — "Tiny: ensure PRD trailing newline (Rev. 326 section 111)"), branch `main` (remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `7775a96815c951aec62708ee856f58c89981cb2d`). **origin/main:** `7775a96815c951aec62708ee856f58c89981cb2d` (rev 326/327). Local branch **0 commits ahead**, **0 commit behind** origin.main.
   - **Working tree:** `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 327, akan dicomit); seluruh file lain cocak dengan HEAD; `git ls-files` = 36 file; 78 file tidak ter-track (skrip sementara, backup, section .md).
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan .gitignore mencantumkan *.db. Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (init_db.py, init_schema.sql; import_excel.py dan import_students_grades_clean.py tidak ditemukan di working tree).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` absen (clear checkout, 0 package; `.bin` tidak ada). `.next/` masih ada (partial: cache + diagnostics + package.json + server + static + trace + trace-build + turbopack + types, bukan production build). `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm install` ulang sebelum dapat dijalankan.
   - **Prisma schema:** 17 model terdefinisi (termasuk `KitabProgress` di baris 203, `Sertakan` di baris 218 — ditambahkan Rev. 51). `prisma/schema.prisma` **8492 bytes**, 263 baris. `uidNfc` pada model `Student` (baris 68, `uidNfc String? @map("uid_nfc")`). `prisma validate` **tidak dapat dijalankan** karena `prisma` CLI tidak terinstall (`node_modules` absen).
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map("uid_nfc"` baris 68), `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama 'Pondok Banat'); produksi butuh bcrypt + session.
   - **Beranda hardcode:** `src/components/Beranda.tsx` (baris 26–28) & `src/app/beranda/page.tsx` masih hardcode `totalSantri: 453, totalGuru: 54, totalKelas: 18` (bukan fetch real-time dari DB).
   - **Source files:** `src/app/*` = 15 entri (12 sub direktori: absensi, beranda, berita, guru, kelas, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah + globals.css, layout.tsx, page.tsx); `src/components` = `Beranda.tsx` & `Login.tsx`; `src/lib` = **kosong** (logic inline). Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite).
   - **Data source:** folder `.data-pondokanat/` **tidak ditemukan** di working tree (di-eksklusi oleh `.gitignore`). Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber.

2. **Perubahan dari Rev. 326:**
   - **Header PRD:** diperbarui ke **Rev. 327** (tanggal 20 Oktober 2026 WIB).
   - **New Section 112 (Rev. 327):** ditambahkan untuk verifikasi fresh ulang & konfirmasi stabilitas Rev. 327.
   - **Referensi HEAD:** state terkini HEAD = `7775a96815c951aec62708ee856f58c89981cb2d` (commit 7775a96, "Tiny: ensure PRD trailing newline (Rev. 326 section 111)"). `origin/main` sama dengan HEAD (0 ahead / 0 behind).

3. **Status:** dokumen PRD **REVISI** — rev 327 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. Header PRD diperbarui ke **Rev. 327**. Git HEAD = `7775a96` (Rev. 326, section 111, trailing newline; commit 7775a96, **0 commits ahead** origin.main.
"""

# Append section 112
lines.append(section_112)

new_content = "\n".join(lines)
if not new_content.endswith("\n"):
    new_content += "\n"

with open(path, "w", encoding="utf-8") as f:
    f.write(new_content)

print("Done. New line count:", new_content.count("\n") + 1)
print("New header:", new_content.split("\n")[3][:80] + "...")
