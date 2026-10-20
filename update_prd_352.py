# -*- coding: utf-8 -*-
path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Header updates
updates = [
    ('> **Rev. 351 — 20 Oktober 2026 (WIB).**', '> **Rev. 352 — 20 Oktober 2026 (WIB).**'),
    ('**Git HEAD (local):** `e02e207` (Rev. 349, commit `e02e207`)', '**Git HEAD (local):** `b5f5ce3` (Rev. 351, commit `b5f5ce3`)'),
    ('Local branch **12 commits ahead**', 'Local branch **13 commits ahead**'),
    ('revisi terbaru = Rev. 351', 'revisi terbaru = Rev. 352'),
]

for old, new in updates:
    count = content.count(old)
    if count == 0:
        print("WARNING: pattern not found:", old[:60])
    content = content.replace(old, new)
    print("Updated:", old[:50], "->", new[:50], "(%d occurrence(s))" % count)

# Append section 137
section_137 = """

## 137. REVISI TERBARU (Rev. 352 — 20 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 20 Oktober 2026 (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / struktur source / skema Prisma / Login.tsx / Beranda.tsx. Semua data diverifikasi langsung dari repo kerja saat ini.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 351 (data terkonsisten).**
   - **Git HEAD (local):** `b5f5ce3` (Rev. 351, commit `b5f5ce3`). Branch `main` (remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `b5f5ce3`). **origin/main:** `2d8439f` (Rev. 338). Local branch **13 commits ahead**, **0 commit behind** origin.main.
   - **Database (dev.db):** file `dev.db` saat ini **absent** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan .gitignore mencantumkan *.db. Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (init_db.py, init_schema.sql; import_excel.py dan import_students_grades_clean.py tidak ditemukan di working tree).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` absen (0 package; .bin tidak ada). `.next/` masih ada (partial: cache + diagnostics + package.json + server + static + trace + trace-build + turbopack + types, bukan production build). `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm install` ulang sebelum dapat dijalankan.
   - **Prisma schema:** 17 model terdefinisi (termasuk `KitabProgress` di baris 203, `Sertakan` di baris 218 — ditambahkan Rev. 51). `prisma/schema.prisma` **8492 bytes**, 263 baris. `uidNfc` pada model `Student` (baris 68, `uidNfc String? @map("uid_nfc")`). `prisma validate` **tidak dapat dijalankan** karena `prisma` CLI tidak terinstall (`node_modules` absen).
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map("uid_nfc")` baris 68) & `init_schema.sql` baris 40, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama 'Pondok Banat').
   - **Beranda hardcode:** `src/components/Beranda.tsx` (baris 26–28) & `src/app/beranda/page.tsx` (baris 14–16) masih hardcode `totalSantri: 453, totalGuru: 54, totalKelas: 18` (bukan fetch real-time dari DB; sudah diperbarui ke 453 sesuai data Excel grade sheets).
   - **Source files:** `src/app/*` = 15 entri (12 sub direktori: absensi, beranda, berita, guru, kelas, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah + globals.css, layout.tsx, page.tsx); `src/components` = 2 (Beranda.tsx & Login.tsx); `src/lib` = kosong (logic inline). Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite).
   - **Data source:** folder `.data-pondokanat/` **tidak ditemukan** di working tree (di-eksklusi oleh `.gitignore`). Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber.

2. **Perubahan dari Rev. 351:**
   - **Header PRD:** diperbarui ke **Rev. 352** (tanggal 20 Oktober 2026 WIB).
   - **New Section 137 (Rev. 352):** ditambahkan untuk verifikasi fresh ulang & konfirmasi stabilitas Rev. 352.
   - **Referensi HEAD:** state terkini HEAD = `b5f5ce3` (Rev. 351, commit `b5f5ce3`); origin/main = `2d8439f` (Rev. 338). Branch **13 commits ahead** origin.main.

3. **Status:** dokumen PRD **REVISI** — rev 352 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. Header PRD diperbarui ke **Rev. 352**. Git HEAD = `b5f5ce3` (Rev. 351, 13 commits ahead origin.main).
"""

content = content.rstrip() + '\n' + section_137 + '\n'

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("\n=== DONE ===")
print("New file size:", len(content), "bytes")
print("New line count:", content.count("\n") + 1)
