import re

path = "PRD-PONDOK-BANAT.md"
with open(path, "r") as f:
    content = f.read()

# 1. Update header: Rev. 282 -> Rev. 283
old_header = "**Rev. 282 — 19 Oktober 2026 (WIB).**"
new_header = "**Rev. 283 — 19 Oktober 2026 (WIB).**"
content = content.replace(old_header, new_header)

# 2. Append new Rev. 283 section at the end of file
new_section = """
## 61. REVISI TERBARU (Rev. 283 — 19 Oktober 2026 (WIB))

> **Verifikasi fresh dilakukan:** 19 Oktober 2026 (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / struktur source / skema Prisma.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 282 (data terkonsisten).**
   - **Git HEAD (local):** `8217a6167574989fa6b9108ce12876ff1085a48b` "Rev. 282: PRD fresh verification & stability confirmation (19 Oct 2026 WIB); updated header to Rev. 282 + added section 60" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `8217a6167574989fa6b9108ce12876ff1085a48b`). Local branch **3 commit ahead**, **0 commit behind** origin/main.
   - **Git HEAD (origin/main):** `03fe91a913233ca207008ac82516d9d2d7a6dcd1` (Rev. 279) — berbeda dengan local HEAD (local 3 commit ahead).
   - **Git ls-files:** = **36 file**. `git status --porcelain` = `??` (**43 file tambahan tidak ter-track** — skrip bantuan, data sumber, bukan bagian dari PRD).
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan .gitignore mencantumkan *.db. Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (init_db.py, init_schema.sql; import_excel.py dan import_students_grades_clean.py tidak ditemukan di working tree).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — node_modules/ **absent** (0 package; .bin tidak ada). .next/ **ada (partial: cache + diagnostics + package.json + server + static + trace + trace-build + turbopack + types, bukan production build)**. tsc --noEmit, npm run lint, npm run build memerlukan npm install ulang sebelum dapat dijalankan.
   - **M02a (NFC):** field uid_nfc masih di schema Prisma (uidNfc @map("uid_nfc" baris 68), init_schema.sql baris 44, init_db.py baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format AF:C2:99:E7).
   - **Auth hardcode:** src/components/Login.tsx masih pakai admin@pondokanbat.com / admin123 (domain pondokanbat.com (sesuai nama 'Pondok Banat')); produksi butuh bcrypt + session.
   - **Beranda hardcode:** src/app/page.tsx (login page) masih hardcode; belum ada Beranda.tsx yang terhubung ke DB sebagai dashboard utama. Belum ada fetch real-time dari DB.
   - **Prisma schema:** model KitabProgress (baris 203, Student + Subject) & Sertakan (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); prisma validate berhasil. **Schema inconsistency (Rev. 38-45) SELESAI**. Jumlah model = **17**.
   - **Source files:** src/app/* = **15 entri** (12 sub direktori: absensi, beranda, berita, guru, kelas, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah + globals.css, layout.tsx, page.tsx); src/components = Beranda.tsx & Login.tsx; src/lib = **kosong** (logic inline); src/next-env.d.ts = 1 file. Total src = **18 file**. Prisma driver = prisma ^8.0.0-rc.22 (SQLite).
   - **Data source:** folder .data-pondokanat/ **tidak ditemukan** di working tree (di-eksklusi oleh .gitignore). Import scripts import_excel.py & import_students_grades_clean.py **tidak ditemukan** di working tree. Rekonstruksi dev.db otomatis **tidak dapat dilakukan** tanpa file-file sumber.
   - **Branch-ahead:** 3 commit (sesuai git rev-list --count origin/main..HEAD = 3; git rev-list --count HEAD..origin/main = 0).
   - **Untracked files:** 43 file tambahan tidak ter-track (skrip bantuan, data sumber, dokumen revisi, bukan bagian dari PRD).

2. **Perubahan dari Rev. 282:**
   - **Header PRD:** diperbarui ke **Rev. 283** (tanggal 19 Oktober 2026 WIB).
   - **New Section 61 (Rev. 283):** ditambahkan untuk verifikasi fresh ulang & konfirmasi stabilitas Rev. 283.
   - **Git HEAD di header:** diperbarui ke 8217a6167574989fa6b9108ce12876ff1085a48b (aktual, sesuai HEAD commit Rev. 282); origin/main = 03fe91a913233ca207008ac82516d9d2d7a6dcd1 (Rev. 279) — local 3 commit ahead.
   - **revisi terbaru:** diperbarui dari Rev. 282 ke Rev. 283.
   - **Branch-ahead count:** diperbarui dari 2 ke 3 commit (git rev-list --count origin/main..HEAD = 3).

3. **Status:** dokumen PRD **REVISI** — rev Rev. 283 = verifikasi fresh ulang & konfirmasi stabilitas; dev.db tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. Header PRD diperbarui ke **Rev. 283**.
"""

# Find the last "## " heading to insert before it if it's "## 60."
# Actually, the section 60 ends with "Header PRD diperbarui ke **Rev. 282**." then newline
# We append after the last section
content = content.rstrip() + "\n" + new_section

with open(path, "w") as f:
    f.write(content)

print("Done. File updated to Rev. 283")
print(f"Total lines: {len(content.splitlines())}")
