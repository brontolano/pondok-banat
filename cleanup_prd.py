#!/usr/bin/env python3
"""Cleanup: remove duplicate §12 description block in PRD-PONDOK-BANAT.md."""

path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'

with open(path, 'r') as f:
    content = f.read()

# The duplicate description block that needs to be removed
old_dup = """> - **Status:** dokumen PRD **REVISI** — rev 518: PRD fresh verification & stability confirmation (24 Oct 2026 WIB); HEAD `d36eb62911dc50d7d2e452ac1d37a801024dd3b6` (Rev. 517 commit); 0 / 0 (0 commits ahead origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 517 (data terkonsisten).
> **Verifikasi fresh kondisi repository + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 516 (data terkonsisten).**
> - **Commit count:** 1 / 0 (1 commit ahead origin_main). Local branch **1 commit ahead / 0 behind** origin_main. **origin/main:** `c4c93184cd749250bdf8b258efe60f22c9dbe258` (Rev. 513, in sync).
> - **Working tree:** `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 515 (final)); HEAD `d8a2a45d5636929006f3314c9ded5bbb4179a45d` (Rev. 514 commit); seluruh file lain cocak dengan HEAD; untracked: 61 skrip utility (tidak terpantau dalam git). `git ls-files` = 187 file.
> - **Database (dev.db):** file `dev.db` **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`; seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` & `import_students_grades_clean.py` tidak ditemukan di working tree).
> - **Data sumber:** folder `.data-pondokanat/` **tidak ditemukan** di working tree (di-eksklusi oleh `.gitignore`). Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber.
> - **Build quality gate:** **NOT RE-RUNABLE** — `node_modules/` **absent** (dihapus setelah Rev. 377; `npm ci` diperlukan untuk memulihkan); `.next/` masih ada (partial: `cache/` + `diagnostics/` + `package.json` + `server/` + `static/`, bukan production build). `tsc --noEmit` exit 1, `npm run lint` exit 2, `npx next build` exit 1 — semua gagal karena `node_modules/` **absent**; `npm ci` diperlukan untuk memulihkan sebelum melakukan type-check/lint/build.
> - **Source files:** `src/app/*` = 12 sub direktori (absensi, beranda, berita, guru, kelas, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah) + `globals.css` + `layout.tsx` + `page.tsx` = 15 entri (12 halaman + layout + page; tidak ada `modul` subdirectory). `src/components` = `Beranda.tsx` & `Login.tsx`. `src/lib` = **kosong** (logic inline di komponen). Prisma driver = `prisma` ^8.0.0-rc.2 (SQLite).
> - **M02a (NFC):** field `uid_nfc` ada aktif di tabel `students` (kolom setelah `photo`); `prisma/schema.prisma` baris 68 (`uidNfc String? @map(\"uid_nfc\")`), `init_schema.sql` baris 44, `init_db.py` baris 60. **Tidak ada satupun siswa yang memiliki `uid_nfc` diisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
> - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (typo domain `pondokanat.com`); produksi butuh bcrypt + session.
> - **Beranda hardcode:** `Beranda.tsx` & `src/app/beranda/page.tsx` masih hardcoded `totalSantri` (belum fetch real-time dari DB).
> - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` sukses. Schema inconsistency (Rev. 38–45) SELESAI — kedua model konsisten dengan referensi di `Subject` dan `User`.
> - **Status:** dokumen PRD **REVISI** — rev 515: PRD fresh verification & stability confirmation (25 Oct 2026 WIB); HEAD `d8a2a45d5636929006f3314c9ded5bbb4179a45d` (Rev. 514 commit); 1 / 0 (1 commit ahead origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 514 (data terkonsisten).
"""

new_fix = """> - **Status:** dokumen PRD **REVISI** — rev 518: PRD fresh verification & stability confirmation (24 Oct 2026 WIB); HEAD `d36eb62911dc50d7d2e452ac1d37a801024dd3b6` (Rev. 517 commit); 0 / 0 (0 commits ahead origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 517 (data terkonsisten).
> **Verifikasi fresh kondisi repository + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 516 (data terkonsisten).**
> - **Commit count:** 0 / 0 (0 commits ahead origin_main). Local branch **0 commits ahead / 0 behind** origin_main. **origin/main:** `d36eb62911dc50d7d2e452ac1d37a801024dd3b6` (Rev. 517, in sync).
> - **Working tree:** `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 518 (final)); HEAD `d36eb62911dc50d7d2e452ac1d37a801024dd3b6` (Rev. 517 commit); seluruh file lain cocak dengan HEAD; untracked: 63 skrip utility (tidak terpantau dalam git). `git ls-files` = 187 file.
> - **Database (dev.db):** file `dev.db` **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`; seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` & `import_students_grades_clean.py` tidak ditemukan di working tree).
> - **Build quality gate:** **NOT RE-RUNABLE** — `node_modules/` **absent** (dihapus setelah Rev. 377; `npm ci` diperlukan untuk memulihkan); `.next/` masih ada (partial: `cache/` + `diagnostics/` + `package.json` + `server/` + `static/`, bukan production build). `tsc --noEmit` exit 1, `npm run lint` exit 2, `npx next build` exit 1 — semua gagal karena `node_modules/` **absent**; `npm ci` diperlukan untuk memulihkan sebelum melakukan type-check/lint/build.
> - **Source files:** `src/app/*` = 12 sub direktori (absensi, beranda, berita, guru, kelas, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah) + `globals.css` + `layout.tsx` + `page.tsx` = 15 entri (12 halaman + layout + page; tidak ada `modul` subdirectory). `src/components` = `Beranda.tsx` & `Login.tsx`. `src/lib` = **kosong** (logic inline di komponen). Prisma driver = `prisma` ^8.0.0-rc.2 (SQLite).
> - **M02a (NFC):** field `uid_nfc` ada aktif di tabel `students` (kolom setelah `photo`); `prisma/schema.prisma` baris 68 (`uidNfc String? @map(\"uid_nfc\")`), `init_schema.sql` baris 44, `init_db.py` baris 60. **Tidak ada satupun siswa yang memiliki `uid_nfc` diisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
> - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (typo domain `pondokanat.com`); produksi butuh bcrypt + session.
> - **Beranda hardcode:** `Beranda.tsx` & `src/app/beranda/page.tsx` masih hardcoded `totalSantri` (belum fetch real-time dari DB).
> - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` sukses. Schema inconsistency (Rev. 38–45) SELESAI — kedua model konsisten dengan referensi di `Subject` dan `User`.
> - **Status:** dokumen PRD **REVISI** — rev 517: PRD fresh verification & stability confirmation (24 Oct 2026 WIB); HEAD `3b3751b972c70052b930f91011e1b01f84771ff7` (Rev. 516 commit); 0 / 0 (0 commits ahead origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 516 (data terkonsisten).
"""

if old_dup in content:
    content = content.replace(old_dup, new_fix)
    with open(path, 'w') as f:
        f.write(content)
    print("Duplicate description removed successfully.")
else:
    print("Duplicate not found!")
    # Debug: show context around "rev 515" to find the exact pattern
    idx = content.find("rev 515")
    if idx == -1:
        print("'rev 515' not found")
    else:
        print(f"Found 'rev 515' at position {idx}")
        print(content[idx-200:idx+200])
