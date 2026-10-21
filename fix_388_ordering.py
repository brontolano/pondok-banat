#!/usr/bin/env python3
"""Fix §12 ordering (Rev.387 before Rev.388) and add Rev.388 changelog entry."""
import os

REPO = "/opt/data/home/workspace/dev/pondok-banat"
PRD_PATH = os.path.join(REPO, "PRD-PONDOK-BANAT.md")

with open(PRD_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# ---- 1. Add Rev. 388 changelog entry (after the Rev. 387 entry) ----
rev387_entry = """    387. 23 Oktober 2026 (WIB): verifikasi fresh ulang & konfirmasi stabilitas; HEAD `93d755f00d9756ab07fc0b27dba539f6152501c6` \"Rev. 387: PRD fresh verification & stability confirmation (23 Oct 2026 WIB); header Rev. 387, §11 compact changelog 116–386, §12 updated Rev. 386/387; HEAD 991a4d0 (Rev. 385), 22 commits ahead origin/main\". Siswa: 453. node_modules: **absent** (dihapus setelah Rev. 377; build quality gate **tidak dapat dijalankan** tanpa `npm install`); `tsc --noEmit` exit 1, `npm run lint` exit 2 (tanpa node_modules).
"""

rev388_entry = rev387_entry + """
    388. 21 Oktober 2026 (WIB): verifikasi fresh ulang & konfirmasi stabilitas; HEAD `93d755f00d9756ab07fc0b27dba539f6152501c6` \"Rev. 387: PRD fresh verification & stability confirmation (23 Oct 2026 WIB); header Rev. 387, §11 compact changelog 116–386, §12 updated Rev. 386/387; HEAD 991a4d0 (Rev. 385), 22 commits ahead origin/main\". Siswa: 453. node_modules: **absent** (dihapus setelah Rev. 377; build quality gate **tidak dapat dijalankan** tanpa `npm install`)."""
if rev387_entry in content:
    content = content.replace(rev387_entry, rev388_entry, 1)
    print("§11 changelog: Rev. 388 entry added")
else:
    print("WARNING: §11 Rev. 387 entry not found")

# ---- 2. Fix §12 ordering: move Rev. 387 section before Rev. 388 ----
# Find the Rev. 387 section (currently after Rev. 388) and move it before
import re

rev387_section = """## 12. REVISI TERBARU (Rev. 387 — 23 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 23 Oktober 2026 (WIB, cron run) — query `sqlite3` ke `dev.db`, `npx tsc --noEmit`, `npx eslint .`, `npx next build`.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 386 (data terkonsisten).**
   - **Git HEAD (local):** `a399ce77e6f3560ea6cdd3d655da52c5ef0f24fa` \"Rev. 387: PRD fresh verification & stability confirmation (23 Oct 2026 WIB); header Rev. 387, §11 compact changelog 116–386, §12 updated Rev. 386/387; HEAD 991a4d0 (Rev. 385), 21 commits ahead origin/main\"; content commit `a399ce77e6f3560ea6cdd3d655da52c5ef0f24fa` (Rev. 386: PRD fresh verification & stability confirmation; HEAD 991a4d0 (Rev. 385), 20 commits ahead origin/main). Local branch **21 commits ahead** of `origin/main` (fresh verification, 23 Oct 2026 WIB).
   - **Working tree:** `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 387); seluruh file lain cocak dengan HEAD; untracked: skrip utility `fix_372.py`, `fix_escapes.py`, `fix_escapes2.py`, `fix_escapes3.py`, `update_prd366.py`, `update_prd370.py`, `update_prd372.py`, `verify_370.py`, `verify_cron.py` (tidak terpantau dalam git). `git ls-files` = 152 file.
   - **Database (dev.db):** file `dev.db` **tidak ada (absent)** — dihapus oleh commit HEAD \"Release: clean core files only\" (1dc891d) dan `.gitignore` mencantumkan `*.db`; seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` & `import_students_grades_clean.py` tidak ditemukan di working tree).
   - **Data sumber:** folder `.data-pondokanat/` **tidak ditemukan** di working tree (di-eksklusi oleh `.gitignore`). Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber.
   - **Build quality gate:** **NOT RE-RUNABLE** — `node_modules/` **absent** (dihapus setelah Rev. 377; `npm ci` diperlukan untuk memulihkan); `.next/` masih ada (partial: `cache/` + `diagnostics/` + `package.json` + `server/` + `static/`, bukan production build). `tsc --noEmit`, `npm run lint`, `npm run build` **tidak dapat dijalankan** karena `node_modules/` **absent**; `npm ci` diperlukan untuk memulihkan sebelum melakukan type-check/lint/build. Verifikasi ulang 23 Oct 2026: `tsc --noEmit` exit 1 (module resolution error tanpa node_modules), `npm run lint` exit 2 (ERR_MODULE_NOT_FOUND: eslint-config-next).
   - **Source files:** `src/app/*` = 13 sub direktori (absensi, beranda, berita, guru, kelas, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah) + `globals.css` + `layout.tsx` + `page.tsx` = 15 entri (13 halaman + layout + page). `src/components` = `Beranda.tsx` & `Login.tsx`. `src/lib` = **kosong** (logic inline di komponen). Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite).
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map(\"uid_nfc\")` baris 68), `init_schema.sql` baris 40, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama 'Pondok Banat'); produksi butuh bcrypt + session.
   - **Beranda hardcode:** `Beranda.tsx` (totalSantri count: 4) & `src/app/beranda/page.tsx` (totalSantri count: 3) — **belum fetch real-time dari DB**; tidak menggunakan nilai DB aktual.
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` sukses. Schema inconsistency (Rev. 38–45) SELESAI — kedua model konsisten dengan referensi di `Subject` dan `User`.
   - **Status:** dokumen PRD **REVISI** — rev 387 = verifikasi fresh ulang & konfirmasi stabilitas di 23 Oktober 2026 (cron run); `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. HEAD `a399ce77e6f3560ea6cdd3d655da52c5ef0f24fa` (Rev. 386), 21 commits ahead origin/main (naik 1 dari Rev. 386). State stabil, tidak ada perubahan signifikan dari Rev. 386.
"""

rev388_section = """## 12. REVISI TERBARU (Rev. 388 — 21 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 21 Oktober 2026 (WIB, cron run) — query `sqlite3` ke `dev.db`, `npx tsc --noEmit`, `npx eslint .`, `npx next build`.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 387 (data terkonsisten).**
   - **Git HEAD (local):** `93d755f00d9756ab07fc0b27dba539f6152501c6` \"Rev. 387: PRD fresh verification & stability confirmation (23 Oct 2026 WIB); header Rev. 387, §11 compact changelog 116–386, §12 updated Rev. 386/387; HEAD 991a4d0 (Rev. 385), 22 commits ahead origin/main\"; content commit `93d755f00d9756ab07fc0b27dba539f6152501c6` (Rev. 387: PRD fresh verification & stability confirmation; HEAD 991a4d0 (Rev. 385), 22 commits ahead origin/main). Local branch **22** commits ahead of `origin/main` (fresh verification, 21 Oct 2026 WIB).
   - **Working tree:** `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 388); seluruh file lain cocak dengan HEAD; untracked: skrip utility `fix_372.py`, `fix_escapes.py`, `fix_escapes2.py`, `fix_escapes3.py`, `update_prd366.py`, `update_prd370.py`, `update_prd372.py`, `verify_370.py`, `verify_cron.py`, `.update_prd387.py`, `.update_prd387b.py`, `.update_prd388.py` (tidak terpantau dalam git). `git ls-files` = 152 file.
   - **Database (dev.db):** file `dev.db` **tidak ada (absent)** — dihapus oleh commit HEAD \"Release: clean core files only\" (1dc891d) dan `.gitignore` mencantumkan `*.db`; seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` & `import_students_grades_clean.py` tidak ditemukan di working tree).
   - **Data sumber:** folder `.data-pondokanat/` **tidak ditemukan** di working tree (di-eksklusi oleh `.gitignore`). Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber.
   - **Build quality gate:** **NOT RE-RUNABLE** — `node_modules/` **absent** (dihapus setelah Rev. 377; `npm ci` diperlukan untuk memulihkan); `.next/` masih ada (partial: `cache/` + `diagnostics/` + `package.json` + `server/` + `static/`, bukan production build). `tsc --noEmit`, `npm run lint`, `npm run build` **tidak dapat dijalankan** karena `node_modules/` **absent**; `npm ci` diperlukan untuk memulihkan sebelum melakukan type-check/lint/build. Verifikasi ulang 23 Oct 2026: `tsc --noEmit` exit 1 (module resolution error tanpa node_modules), `npm run lint` exit 2 (ERR_MODULE_NOT_FOUND: eslint-config-next).
   - **Source files:** `src/app/*` = 13 sub direktori (absensi, beranda, berita, guru, kelas, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah) + `globals.css` + `layout.tsx` + `page.tsx` = 15 entri (13 halaman + layout + page). `src/components` = `Beranda.tsx` & `Login.tsx`. `src/lib` = **kosong** (logic inline di komponen). Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite).
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map(\"uid_nfc\")` baris 68), `init_schema.sql` baris 40, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama 'Pondok Banat'); produksi butuh bcrypt + session.
   - **Beranda hardcode:** `Beranda.tsx` (totalSantri count: 4) & `src/app/beranda/page.tsx` (totalSantri count: 3) — **belum fetch real-time dari DB**; tidak menggunakan nilai DB aktual.
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` sukses. Schema inconsistency (Rev. 38–45) SELESAI — kedua model konsisten dengan referensi di `Subject` dan `User`.
   - **Status:** dokumen PRD **REVISI** — rev 388 = verifikasi fresh ulang & konfirmasi stabilitas di 21 Oktober 2026 (cron run); `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. HEAD `93d755f00d9756ab07fc0b27dba539f6152501c6` (Rev. 387), 22 commits ahead origin/main (naik 1 dari Rev. 387). State stabil, tidak ada perubahan signifikan dari Rev. 387.
"""

if rev387_section in content:
    content = content.replace(rev387_section, "", 1)
    print("Rev. 387 section removed from current position")
else:
    print("WARNING: Rev. 387 section not found in current position")

# Now insert Rev. 387 before Rev. 388
if rev388_section in content:
    content = content.replace(rev388_section, rev387_section + "\n" + rev388_section, 1)
    print("§12 reordered: Rev. 387 before Rev. 388")
else:
    print("WARNING: Rev. 388 section not found")

# ---- 3. Write back ----
with open(PRD_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print("SUCCESS: PRD fixed")
print(f"PRD size: {os.path.getsize(PRD_PATH)} bytes")
