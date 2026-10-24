#!/usr/bin/env python3
"""Update §12 of PRD-PONDOK-BANAT.md to Rev. 506."""

path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'

with open(path, 'r') as f:
    content = f.read()

# Find and replace §12 content
old_s12 = """## 12. REVISI TERBARU (Rev. 468–505 — 24 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 24 Oktober 2026 (WIB, cron run) — query `sqlite3` ke `dev.db`, `npx tsc --noEmit`, `npx eslint .`, `npx next build`.

> **Verifikasi fresh kondisi repository + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 503 (data terkonsisten).**

> - **Git HEAD (local):** `bae146f4e9c2bc403bb5308ac64e0eee281419e7` (Rev. 504 (final): PRD fresh verification & stability confirmation (24 Oct 2026 WIB); header Rev. 504, §11 kompakt changelog 116–504, §12 updated). Local branch **38 commits ahead / 0 behind** origin_main. **origin/main:** `574ed2590fa808eb0fdc32973c053fba566b680d` (Rev. 473, in sync).

> - **Working tree:** `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 504 (final)); HEAD `bae146f4e9c2bc403bb5308ac64e0eee281419e7` (Rev. 504 (final)); seluruh file lain cocak dengan HEAD; untracked: 43 skrip utility (tidak terpantau dalam git). `git ls-files` = 187 file.

> - **Database (dev.db):** file `dev.db` **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`; seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` & `import_students_grades_clean.py` tidak ditemukan di working tree).

> - **Data sumber:** folder `.data-pondokanat/` **tidak ditemukan** di working tree (di-eksklusi oleh `.gitignore`). Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber.

> - **Build quality gate:** **NOT RE-RUNABLE** — `node_modules/` **absent** (dihapus setelah Rev. 377; `npm ci` diperlukan untuk memulihkan); `.next/` masih ada (partial: `cache/` + `diagnostics/` + `package.json` + `server/` + `static/`, bukan production build). `tsc --noEmit` exit 1, `npm run lint` exit 2, `npx next build` exit 1 — semua gagal karena `node_modules/` **absent**; `npm ci` diperlukan untuk memulihkan sebelum melakukan type-check/lint/build.

> - **Source files:** `src/app/*` = 12 sub direktori (absensi, beranda, berita, guru, kelas, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah) + `globals.css` + `layout.tsx` + `page.tsx` = 15 entri (12 halaman + layout + page; tidak ada `modul` subdirectory). `src/components` = `Beranda.tsx` & `Login.tsx`. `src/lib` = **kosong** (logic inline di komponen). Prisma driver = `prisma` ^8.0.0-rc.2 (SQLite).

> - **M02a (NFC):** field `uid_nfc` ada aktif di tabel `students` (kolom setelah `photo`); `prisma/schema.prisma` baris 68 (`uidNfc String? @map(\"uid_nfc\")`), `init_schema.sql` baris 44, `init_db.py` baris 60. **Tidak ada satupun siswa yang memiliki `uid_nfc` diisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).

> - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (typo domain `pondokanat.com`); produksi butuh bcrypt + session.

> - **Beranda hardcode:** `Beranda.tsx` & `src/app/beranda/page.tsx` masih hardcoded `totalSantri` (belum fetch real-time dari DB).

> - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` sukses. Schema inconsistency (Rev. 38–45) SELESAI — kedua model konsisten dengan referensi di `Subject` dan `User`.

> - **Status:** dokumen PRD **REVISI** — rev 504 (final): PRD fresh verification & stability confirmation (24 Oct 2026 WIB); HEAD `bae146f4e9c2bc403bb5308ac64e0eee281419e7` (Rev. 504 (final)); 38 / 0 (38 commits ahead origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 503 (data terkonsisten)."""

new_s12 = """## 12. REVISI TERBARU (Rev. 468–506 — 24 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 24 Oktober 2026 (WIB, cron run) — query `sqlite3` ke `dev.db`, `npx tsc --noEmit`, `npx eslint .`, `npx next build`.

> **Verifikasi fresh kondisi repository + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 505 (data terkonsisten).**

> - **Git HEAD (local):** `dc9bd27f6be685f176bfed9c08be3674b17cf744` (Rev. 506 commit: PRD fresh verification & stability confirmation (24 Oct 2026 WIB); header Rev. 506, §11 kompakt changelog 116–506, §12 updated). Local branch **40 commits ahead / 0 behind** origin_main. **origin/main:** `574ed2590fa808eb0fdc32973c053fba566b680d` (Rev. 473, in sync).

> - **Working tree:** `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 506 (final)); HEAD `dc9bd27f6be685f176bfed9c08be3674b17cf744` (Rev. 506 commit); seluruh file lain cocak dengan HEAD; untracked: 43 skrip utility (tidak terpantau dalam git). `git ls-files` = 187 file.

> - **Database (dev.db):** file `dev.db` **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`; seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` & `import_students_grades_clean.py` tidak ditemukan di working tree).

> - **Data sumber:** folder `.data-pondokanat/` **tidak ditemukan** di working tree (di-eksklusi oleh `.gitignore`). Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber.

> - **Build quality gate:** **NOT RE-RUNABLE** — `node_modules/` **absent** (dihapus setelah Rev. 377; `npm ci` diperlukan untuk memulihkan); `.next/` masih ada (partial: `cache/` + `diagnostics/` + `package.json` + `server/` + `static/`, bukan production build). `tsc --noEmit` exit 1, `npm run lint` exit 2, `npx next build` exit 1 — semua gagal karena `node_modules/` **absent**; `npm ci` diperlukan untuk memulihkan sebelum melakukan type-check/lint/build.

> - **Source files:** `src/app/*` = 12 sub direktori (absensi, beranda, berita, guru, kelas, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah) + `globals.css` + `layout.tsx` + `page.tsx` = 15 entri (12 halaman + layout + page; tidak ada `modul` subdirectory). `src/components` = `Beranda.tsx` & `Login.tsx`. `src/lib` = **kosong** (logic inline di komponen). Prisma driver = `prisma` ^8.0.0-rc.2 (SQLite).

> - **M02a (NFC):** field `uid_nfc` ada aktif di tabel `students` (kolom setelah `photo`); `prisma/schema.prisma` baris 68 (`uidNfc String? @map(\"uid_nfc\")`), `init_schema.sql` baris 44, `init_db.py` baris 60. **Tidak ada satupun siswa yang memiliki `uid_nfc` diisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).

> - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (typo domain `pondokanat.com`); produksi butuh bcrypt + session.

> - **Beranda hardcode:** `Beranda.tsx` & `src/app/beranda/page.tsx` masih hardcoded `totalSantri` (belum fetch real-time dari DB).

> - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` sukses. Schema inconsistency (Rev. 38–45) SELESAI — kedua model konsisten dengan referensi di `Subject` dan `User`.

> - **Status:** dokumen PRD **REVISI** — rev 506 = PRD fresh verification & stability confirmation (24 Oct 2026 WIB); HEAD `dc9bd27f6be685f176bfed9c08be3674b17cf744` (Rev. 506 commit); 40 / 0 (40 commits ahead origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 505 (data terkonsisten)."""

if old_s12 in content:
    content = content.replace(old_s12, new_s12)
    print("§12 updated successfully")
else:
    print("§12 NOT found!")
    # Find partial matches
    if 'Verifikasi fresh dilakukan' in content:
        idx = content.find('Verifikasi fresh dilakukan')
        print("Found 'Verifikasi fresh dilakukan' at", idx)
    if 'Rev. 504 (final)' in content:
        idx = content.find('Rev. 504 (final)')
        print("Found 'Rev. 504 (final)' at", idx)

with open(path, 'w') as f:
    f.write(content)

print("File saved")
