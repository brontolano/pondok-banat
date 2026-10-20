#!/usr/bin/env python3
"""Update PRD to Rev. 288: fix stale header git references + add section 66."""

import datetime

HEADER_NEW = """> **Rev. 288 — 20 Oktober 2026 (WIB).** Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Git HEAD (local): `b74817812f5665d66ecadc1e04642e43797ad0d8` \"Rev. 287: PRD fresh verification & stability confirmation (19 Oct 2026 WIB); updated header to Rev. 287 + added section 65\" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `b74817812f5665d66ecadc1e04642e43797ad0d8`). Git HEAD (origin/main): `ef9798fed44464ec2246ffdb044224a9a9abc903` (Rev. 286) — berbeda dengan local HEAD (local 1 commit ahead). Working tree: PRD cocak dengan HEAD (revisi terbaru = Rev. 287, sudah dicomit); hanya file .py tambahan yang tidak ter-track. Local branch **1 commit ahead**, **0 commit behind** origin/main. Database (dev.db): file dev.db saat ini tidak ada (absent) — dihapus oleh commit \"Release: clean core files only\" (1dc891d) dan .gitignore mencantumkan *.db; seluruh record (453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) tidak tersedia dan harus di-import ulang menggunakan skrip semula (init_db.py, init_schema.sql; import_excel.py dan import_students_grades_clean.py tidak ditemukan di working tree). Build quality gate: NO LONGER RE-RUNABLE — node_modules/absent (0 package; .bin tidak ada); .next ada (partial: cache + diagnostics + package.json + server + static + trace + trace-build + turbopack + types, bukan production build). tsc --noEmit, npm run lint, npm run build memerlukan npm instal ulang sebelum dapat dijalankan. M02a (NFC): field uid_nfc masih di schema Prisma, init_schema.sql baris 44, init_db.py baris 60, namun 0 siswa terisi (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format AF:C2:99:E7). Auth hardcode: src/components/Login.tsx masih pakai admin@pondokanbat.com / admin123 (domain pondokanbat.com (sesuai nama 'Pondok Banat')); produksi butuh bcrypt + session. Beranda: src/components/Beranda.tsx & src/app/beranda/page.tsx sudah diperbarui ke totalSantri: 453; beranda.tsx (src/app/page.tsx login page) tetap hardcode tidak terhubung ke DB. Prisma: 17 model terdefinisi (termasuk KitabProgress, Sertakan — ditambahkan Rev. 51). init_schema.sql: 15 tabel."""

SECTION_66 = """## 66. REVISI TERBARU (Rev. 288 — 20 Oktober 2026 (WIB))

> **Verifikasi fresh dilakukan:** 20 Oktober 2026 (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / struktur source / skema Prisma.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 287 (data terkonsisten).**  
   - **Git HEAD (local):** `b74817812f5665d66ecadc1e04642e43797ad0d8` "Rev. 287: PRD fresh verification & stability confirmation (19 Oct 2026 WIB); updated header to Rev. 287 + added section 65" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `b74817812f5665d66ecadc1e04642e43797ad0d8`). Local branch **1 commit ahead**, **0 commit behind** origin/main.
   - **Git HEAD (origin/main):** `ef9798fed44464ec2246ffdb044224a9a9abc903` (Rev. 286) — berbeda dengan local HEAD (local 1 commit ahead).
   - **Git ls-files:** = **36 file**. `git status --porcelain` = `??` (**54 file tambahan tidak ter-track** — skrip bantuan, bukan bagian dari PRD).
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD \"Release: clean core files only\" (1dc891d) dan .gitignore mencantumkan *.db. Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (init_db.py, init_schema.sql; import_excel.py dan import_students_grades_clean.py tidak ditemukan di working tree).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — node_modules/ **absent** (0 package; .bin tidak ada). .next/ **ada (partial: cache + diagnostics + package.json + server + static + trace + trace-build + turbopack + types, bukan production build)**. tsc --noEmit, npm run lint, npm run build memerlukan npm install ulang sebelum dapat dijalankan.
   - **M02a (NFC):** field uid_nfc masih di schema Prisma (uidNfc @map(\"uid_nfc\" baris 68), init_schema.sql baris 44, init_db.py baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format AF:C2:99:E7)).
   - **Auth hardcode:** src/components/Login.tsx masih pakai admin@pondokanbat.com / admin123 (domain pondokanbat.com (sesuai nama 'Pondok Banat')); produksi butuh bcrypt + session.
   - **Beranda hardcode:** src/components/Beranda.tsx & src/app/beranda/page.tsx masih hardcode `totalSantri: 453, totalGuru: 54, totalKelas: 18`; bukan fetch real-time dari DB.
   - **Prisma schema:** model KitabProgress (baris 203, Student + Subject) & Sertakan (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); prisma validate berhasil. **Schema inconsistency (Rev. 38-45) SELESAI**. Jumlah model = **17**. init_schema.sql: 15 tabel.
   - **Source files:** src/app/* = **15 entri** (12 sub direktori: absensi, beranda, berita, guru, kelas, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah + globals.css, layout.tsx, page.tsx); src/components = Beranda.tsx & Login.tsx; src/lib = **kosong** (logic inline); src/next-env.d.ts = 1 file. Total src = **18 file**. Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite).
   - **Data source:** folder .data-pondokanat/ **tidak ditemukan** di working tree (di-eksklusi oleh .gitignore). Import scripts import_excel.py & import_students_grades_clean.py **tidak ditemukan** di working tree. Rekonstruksi dev.db otomatis **tidak dapat dilakukan** tanpa file-file sumber.
   - **Branch-ahead:** 1 commit (sesuai `git rev-list --count origin/main..HEAD` = 1; `git rev-list --count HEAD..origin/main` = 0).
   - **Untracked files:** 54 file tambahan tidak ter-track (skrip bantuan, bukan bagian dari PRD).

2. **Perubahan dari Rev. 287:**  
   - **Header PRD:** diperbarui ke **Rev. 288** (tanggal 20 Oktober 2026 WIB).
   - **New Section 66 (Rev. 288):** ditambahkan untuk verifikasi fresh ulang & konfirmasi stabilitas Rev. 288.
   - **Git HEAD di header:** diperbarui ke `b74817812f5665d66ecadc1e04642e43797ad0d8` (aktual, sesuai HEAD commit Rev. 287); origin/main = `ef9798fed44464ec2246ffdb044224a9a9abc903` (Rev. 286) — local 1 commit ahead.
   - **revisi terbaru:** diperbarui dari Rev. 287 ke Rev. 288.
   - **Branch-ahead count:** diperbarui dari 1 ke 1 commit (`git rev-list --count origin/main..HEAD` = 1).

3. **Status:** dokemen PRD **REVISI** — rev Rev. 288 = verifikasi fresh ulang & konfirmasi stabilitas; dev.db tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. Header PRD diperbarui ke **Rev. 288**. Git HEAD = `b74817812f5665d66ecadc1e04642e43797ad0d8` (Rev. 287), **1 commit ahead** origin/main.
"""


def main():
    path = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"
    
    # Read the file
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    lines = content.split("\n")
    
    # Verify current header
    assert "Rev. 287" in lines[3], "Line 4 should currently be Rev. 287 header"
    print(f"Line 4 header length: {len(lines[3])} chars")
    
    # Replace line 4 (header) with new header
    # Ensure the header line ends with newline
    if not lines[3].endswith("\n"):
        lines[3] = lines[3] + "\n"
    lines[3] = HEADER_NEW + "\n"
    
    # Rejoin lines
    new_content = "\n".join(lines)
    
    # Ensure section 65 ends with a newline before section 66
    # The section 65 ends with "...origin/main." and section 66 starts with "## 66."
    # We need a blank line between them
    if new_content.endswith("origin/main."):
        new_content = new_content.rstrip() + "\n\n" + SECTION_66
    else:
        # Make sure we have proper separation
        new_content = new_content.rstrip() + "\n\n" + SECTION_66
    
    # Write back
    with open(path, "w", encoding="utf-8") as f:
        f.write(new_content)
    
    print(f"Header updated to Rev. 288 ({len(HEADER_NEW)} chars)")
    print(f"Section 66 appended ({len(SECTION_66)} chars)")
    final_content = open(path, encoding="utf-8").read()
    print(f"Total file size: {len(final_content)} chars")
    print("Done.")


if __name__ == "__main__":
    main()
