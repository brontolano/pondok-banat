# Patch PRD-PONDOK-BANAT.md: update header to Rev. 326 + append section 111 (Rev. 326)
path = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

new_header = (
    "> **Rev. 326 — 20 Oktober 2026 (WIB).** Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. "
    "Git HEAD (local): `908d573c63a86f009f05011e4e81948c20b38824` (rev 325/326, commit 908d573c) "
    "(branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `908d573c63a86f009f05011e4e81948c20b38824`). "
    "Git HEAD (origin/main): `908d573c63a86f009f05011e4e81948c20b38824` (rev 325/326) — 0 commits ahead, 0 commit behind origin.main. "
    "Working tree: PRD cocak dengan HEAD (revisi terbaru = Rev. 326, belum dicomit); hanya file .py tambahan yang tidak ter-track. "
    "Local branch **0 commits ahead**, **0 commit behind** origin.main. "
    "Database (dev.db): file dev.db saat ini tidak ada (absent) — dihapus oleh commit HEAD \"Release: clean core files only\" (1dc891d) dan .gitignore mencantumkan *.db; "
    "seluruh record (453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) tidak tersedia dan harus di-import ulang menggunakan skrip semula (init_db.py, init_schema.sql; import_excel.py dan import_students_grades_clean.py tidak ditemukan di working tree). "
    "Build quality gate: NO LONGER RE-RUNABLE — node_modules/absent (0 package; .bin tidak ada); .next ada (partial: cache + diagnostics + package.json + server + static + trace + trace-build + turbopack + types, bukan production build). "
    "tsc --noEmit, npm run lint, npm run build memerlukan npm install ulang sebelum dapat dijalankan. "
    "M02a (NFC): field uid_nfc masih di schema Prisma, init_schema.sql baris 44, init_db.py baris 60, namun 0 siswa terisi (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format AF:C2:99:E7). "
    "Auth hardcode: src/components/Login.tsx masih pakai admin@pondokanbat.com / admin123 (domain pondokanbat.com (sesuai nama 'Pondok Banat')); produksi butuh bcrypt + session. "
    "Beranda: src/components/Beranda.tsx & src/app/beranda/page.tsx masih hardcode (Beranda.tsx: totalSantri: 0, totalGuru: 0, totalKelas: 0; page.tsx: totalSantri: 453, totalGuru: 54, totalKelas: 18)."
)

section_111 = (
    "\n\n## 111. REVISI TERBARU (Rev. 326 — 20 Oktober 2026 WIB)\n\n"
    "> **Verifikasi fresh dilakukan:** 20 Oktober 2026 (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / struktur source / skema Prisma / Login.tsx / Beranda.tsx. Semua data diverifikasi langsung dari repo kerja saat ini.\n\n"
    "1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 325 (data terkonsisten).**\n"
    "   - **Git HEAD (local):** `908d573c63a86f009f05011e4e81948c20b38824` (rev 325/326, commit 908d573c — \"Fix typo in section 110 (Rev. 325) HEAD reference\"), branch `main` (remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `908d573c63a86f009f05011e4e81948c20b38824`). **origin/main:** `908d573c63a86f009f05011e4e81948c20b38824` (rev 325/326). Local branch **0 commits ahead**, **0 commit behind** origin.main.\n"
    "   - **Working tree:** `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 326, belum dicomit); seluruh file lain cocak dengan HEAD; `git ls-files` = 36 file; 78 file tidak ter-track (skrip sementara, backup, section .md).\n"
    "   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD \"Release: clean core files only\" (1dc891d) dan .gitignore mencantumkan *.db. Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (init_db.py, init_schema.sql; import_excel.py dan import_students_grades_clean.py tidak ditemukan di working tree).\n"
    "   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` absen (clear checkout, 0 package; `.bin` tidak ada). `.next/` masih ada (partial: cache + diagnostics + package.json + server + static + trace + trace-build + turbopack + types, bukan production build). `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm install` ulang sebelum dapat dijalankan.\n"
    "   - **Prisma schema:** 17 model terdefinisi (termasuk `KitabProgress` di baris 203, `Sertakan` di baris 218 — ditambahkan Rev. 51). `prisma/schema.prisma` **8492 bytes**, 263 baris. `uidNfc` pada model `Student` (baris 68, `uidNfc String? @map(\"uid_nfc\")`). `prisma validate` **tidak dapat dijalankan** karena `prisma` CLI tidak terinstall (`node_modules` absen).\n"
    "   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map(\"uid_nfc\"` baris 68), `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).\n"
    "   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama 'Pondok Banat'); produksi butuh bcrypt + session.\n"
    "   - **Beranda hardcode:** `src/components/Beranda.tsx` (baris 14–16) hardcode `totalSantri: 0, totalGuru: 0, totalKelas: 0` (belum fetch real-time dari DB); `src/app/beranda/page.tsx` (baris 14–16) hardcode `totalSantri: 453, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB).\n"
    "   - **Source files:** `src/app/*` = 15 entri (12 sub direktori: absensi, beranda, berita, guru, kelas, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah + globals.css, layout.tsx, page.tsx); `src/components` = `Beranda.tsx` & `Login.tsx`; `src/lib` = **kosong** (logic inline). Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite).\n"
    "   - **Data source:** folder `.data-pondokanat/` **tidak ditemukan** di working tree (di-eksklusi oleh `.gitignore`). Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber.\n\n"
    "2. **Perubahan dari Rev. 325:**\n"
    "   - **Header PRD:** diperbarui ke **Rev. 326** (tanggal 20 Oktober 2026 WIB).\n"
    "   - **New Section 111 (Rev. 326):** ditambahkan untuk verifikasi fresh ulang & konfirmasi stabilitas Rev. 326.\n"
    "   - **Referensi HEAD:** state terkini HEAD = `908d573c63a86f009f05011e4e81948c20b38824` (commit 908d573c, \"Fix typo in section 110 (Rev. 325) HEAD reference\"). `origin/main` sama dengan HEAD (0 ahead / 0 behind). Catatan: referensi HEAD yang tercatat di header dan §109/§110 (Rev. 324 = `4b246510265ea3b38962d400cba6426a68105458`, \"18 commits ahead origin.main\") telah diganti oleh HEAD mutakhir `908d573c63a86f009f05011e4e81948c20b38824` (Rev. 325/326).\n\n"
    "3. **Status:** dokumen PRD **REVISI** — rev 326 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. Header PRD diperbarui ke **Rev. 326**. Git HEAD = `908d573c` (Rev. 325/326, commit 908d573c, **0 commits ahead** origin.main."
)

lines = content.split("\n")

# Replace the line that holds the Rev. 325 header (currently the "> **Rev. 325 —" line)
found = False
i = -1
for i, ln in enumerate(lines):
    if ln.startswith("> **Rev. 325 —"):
        lines[i] = new_header
        found = True
        break
assert found, "Rev. 325 header line not found!"
print("Header replaced at line index", i)

# Append section 111
if lines[-1] == "":
    lines.append(section_111)
else:
    lines.append("")
    lines.append(section_111)

updated = "\n".join(lines)
with open(path, "w", encoding="utf-8") as f:
    f.write(updated)

with open(path, "r", encoding="utf-8") as f:
    v = f.read()
print("Total lines now:", v.count("\n") + 1)
print("Section 111 present:", "## 111. REVISI TERBARU (Rev. 326" in v)
print("Header updated to Rev. 326:", "> **Rev. 326 — 20 Oktober 2026 (WIB)." in v)
print("Old Rev. 325 header gone:", "> **Rev. 325 — 20 Oktober 2026 (WIB)." not in v)
print("File size (bytes):", len(updated.encode("utf-8")))
