#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Insert Rev. 468 §12 section back into PRD."""
import io

path = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"

with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Find the position after §11 entry 468, before §13 entry Rev. 468
# The §11 entry 468 ends with "...branch 5 ahead / 0 behind origin_main."
# The §13 entry Rev. 468 starts with "||- **Rev. 468.** 23 Oktober 2026 (WIB)"

marker_s12_end = "branch 5 ahead / 0 behind origin_main."
marker_s13_start = "||- **Rev. 468.** 23 Oktober 2026 (WIB): PRD fresh verification"

idx_end = content.find(marker_s12_end)
idx_start = content.find(marker_s13_start)

print(f"Found §12 end at: {idx_end}")
print(f"Found §13 start at: {idx_start}")

if idx_end < 0 or idx_start < 0 or idx_end >= idx_start:
    print("ERROR: Could not find proper positions")
    # Fallback: find §11 entry 468 end differently
    marker_alt = "branch 5 ahead / 0 behind origin_main."
    idx_end = content.find(marker_alt)
    print(f"Alternative §12 end at: {idx_end}")
    if idx_end < 0:
        # Find last occurrence of "branch 5 ahead"
        idx_end = content.rfind("branch 5 ahead / 0 behind origin_main.")
        print(f"Rfind alternative at: {idx_end}")
        if idx_end < 0:
            print("ERROR: Could not find §12 end marker")
            exit(1)

# The §12 section to insert
s12_section = """## 12. REVISI TERBARU (Rev. 468 — 23 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 23 Oktober 2026 (WIB, cron run) — query `sqlite3` ke `dev.db`, `npx tsc --noEmit`, `npx eslint .`, `npx next build`.
> **Verifikasi fresh kondisi repository + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 467 (data terkonsisten).**
> - **Git HEAD (local):** `fa1a12f2153eeb53e2512460de451b06e867a695` (Rev. 468: PRD fresh verification & stability confirmation (23 Oct 2026 WIB); header Rev. 468, §11 kompakt changelog 116–467, §12 updated). Local branch **5 commits ahead / 0 behind** origin_main. **origin/main:** `360cfb1f5864524570e622ed4d94a61c6e5950ef` (Rev. 462, in sync).
> - **Working tree:** `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 468); HEAD `fa1a12f2153eeb53e2512460de451b06e867a695` (Rev. 468); seluruh file lain cocak dengan HEAD; untracked: skrip utility (tidak terpantau dalam git). `git ls-files` = 187 file.
> - **Database (dev.db):** file `dev.db` **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`; seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` & `import_students_grades_clean.py` tidak ditemukan di working tree).
> - **Data sumber:** folder `.data-pondokanat/` **tidak ditemukan** di working tree (di-eksklusi oleh `.gitignore`). Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber.
> - **Build quality gate:** **NOT RE-RUNABLE** — `node_modules/` **absent** (dihapus setelah Rev. 377; `npm ci` diperlukan untuk memulihkan); `.next/` masih ada (partial: `cache/` + `diagnostics/` + `package.json` + `server/` + `static/`, bukan production build). `tsc --noEmit` exit 1, `npm run lint` exit 2, `npx next build` exit 1 — semua gagal karena `node_modules/` **absent**; `npm ci` diperlukan untuk memulihkan sebelum melakukan type-check/lint/build.
> - **Source files:** `src/app/*` = 12 sub direktori (absensi, beranda, berita, guru, kelas, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah) + `globals.css` + `layout.tsx` + `page.tsx` = 15 entri (12 halaman + layout + page; tidak ada `modul` subdirectory). `src/components` = `Beranda.tsx` & `Login.tsx`. `src/lib` = **kosong** (logic inline di komponen). Prisma driver = `prisma` ^8.0.0-rc.2 (SQLite).
> - **M02a (NFC):** field `uid_nfc` ada aktif di tabel `students` (kolom setelah `photo`); `prisma/schema.prisma` baris 68 (`uidNfc String? @map(\"uid_nfc\")`), `init_schema.sql` baris 44, `init_db.py` baris 60. **Tidak ada satupun siswa yang memiliki `uid_nfc` diisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
> - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (typo domain `pondokanat.com`); produksi butuh bcrypt + session.
> - **Beranda hardcode:** `Beranda.tsx` & `src/app/beranda/page.tsx` masih hardcoded `totalSantri` (belum fetch real-time dari DB).
> - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` sukses. Schema inconsistency (Rev. 38–45) SELESAI — kedua model konsisten dengan referensi di `Subject` dan `User`.
> - **Status:** dokeman PRD **REVISI** — rev 468 = PRD fresh verification & stability confirmation (23 Oct 2026 WIB); HEAD `fa1a12f2153eeb53e2512460de451b06e867a695` (Rev. 468), 5 / 0 (5 commits ahead origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 467 (data terkonsisten).
"""

# Insert the §12 section
content = content[:idx_end + len(marker_s12_end)] + "\n\n" + s12_section + content[idx_start:]

with io.open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("§12 section inserted successfully.")
print(f"Final file size: {len(content)} bytes")
print(f"Total lines: {content.count(chr(10)) + 1}")
