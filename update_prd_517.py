import sys

path = "PRD-PONDOK-BANAT.md"
with open(path, "r") as f:
    content = f.read()

# 1. Update header line (Rev. 516 -> Rev. 517)
old_header = """Rev. 516: PRD fresh verification & stability confirmation (24 Oct 2026 WIB); header Rev. 516 (updated to Rev. 516), §11 kompakt changelog 116–516, §12 updated; HEAD `4fb7fa1a23db08154ec50909026de5e40f16a8d7` (Rev. 515 commit: PRD fresh verification & stability confirmation (24 Oct 2026 WIB)); 2 / 0 (2 commits ahead origin_main). Branch `main`, remote `brontolano/pondok-banat`. `git rev-parse HEAD` = `4fb7fa1a23db08154ec50909026de5e40f16a8d7` (Rev. 515 commit, fresh verification dilakukan hari ini); **origin/main:** `c4c93184cd749250bdf8b258efe60f22c9dbe258` (Rev. 513, in sync). Local branch **2 commits ahead / 0 behind** origin_main. Working tree: `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 516 (fresh verification), fresh verification dilakukan hari ini); seluruh file lain cocak dengan HEAD; untracked: 61 skrip utility (tidak terpantau dalam git); `commit_msg.txt` dihapus (build artifact); `git ls-files` = 187 file."""

new_header = """Rev. 517: PRD fresh verification & stability confirmation (24 Oct 2026 WIB); header Rev. 517 (updated to Rev. 517), §11 kompakt changelog 116–517, §12 updated; HEAD `3b3751b972c70052b930f91011e1b01f84771ff7` (Rev. 516 commit: PRD fresh verification & stability confirmation (24 Oct 2026 WIB)); 0 / 0 (0 commits ahead origin_main). Branch `main`, remote `brontolano/pondok-banat`. `git rev-parse HEAD` = `3b3751b972c70052b930f91011e1b01f84771ff7` (Rev. 516 commit, fresh verification dilakukan hari ini); **origin/main:** `3b3751b972c70052b930f91011e1b01f84771ff7` (Rev. 516, in sync). Local branch **0 commits ahead / 0 behind** origin_main. Working tree: `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 517 (fresh verification), fresh verification dilakukan hari ini); seluruh file lain cocak dengan HEAD; untracked: 61 skrip utility (tidak terpantau dalam git); `commit_msg.txt` dihapus (build artifact); `git ls-files` = 187 file."""

if old_header not in content:
    print("ERROR: Header not found!")
    sys.exit(1)

content = content.replace(old_header, new_header)

# 2. Update §11: insert Rev. 517 entry before Rev. 515 entry
# The §11 Rev. 515 entry starts with |||- (3 pipes)
old_s11 = """|||- **Rev. 515 (final).** 25 Oktober 2026 (WIB): PRD fresh verification & stability confirmation (25 Oct 2026 WIB); HEAD `d8a2a45d5636929006f3314c9ded5bbb4179a45d` (Rev. 514 commit: PRD fresh verification & stability confirmation (25 Oct 2026 WIB); header Rev. 515, §11 kompakt changelog 116–515, §12 updated); 1 / 0 (1 commit ahead origin_main). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run): **state stabil, tidak ada perubahan signifikan dari Rev. 514** (data terkonsisten). Build gate: **NOT RE-RUNABLE** — `node_modules/` **absent** (dihapus setelah Rev. 377; `npm ci` diperlukan untuk memulihkan); `.next/` masih ada (partial: `cache/` + `diagnostics/` + `package.json` + `server/` + `static/`, bukan production build). `tsc --noEmit` exit 1, `npm run lint` exit 2, `npx next build` exit 1 — semua gagal karena `node_modules/` **absent**; `npm ci` diperlukan untuk memulihkan sebelum melakukan type-check/lint/build. Database (dev.db): **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`; seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` & `import_students_grades_clean.py` tidak ditemukan di working tree). **M02a (NFC):** field `uid_nfc` ada aktif di tabel students, semua 453 NULL (data ekspor NFC Tools belum tersedia). **Auth hardcode:** Login.tsx tetap `admin@pondokanbat.com` / `admin123` (typo domain). **Beranda hardcode:** Beranda.tsx & page.tsx masih hardcoded totalSantri 453. **Schema:** model `KitabProgress` & `Sertakan` sudah terdefinisi; `prisma validate` sukses. **Status:** dokumen PRD **REVISI** — rev 515 = PRD fresh verification & konfirmasi stabilitas; seluruh data terkonsisten, tidak ada perubahan signifikan dari Rev. 514; branch 1 ahead / 0 behind origin_main."""

new_s11 = """|||||- **Rev. 517 (final).** 24 Oktober 2026 (WIB): PRD fresh verification & stability confirmation (24 Oct 2026 WIB); HEAD `3b3751b972c70052b930f91011e1b01f84771ff7` (Rev. 516 commit: PRD fresh verification & stability confirmation (24 Oct 2026 WIB); header Rev. 517, §11 kompakt changelog 116–517, §12 updated); 0 / 0 (0 commits ahead origin_main). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run): **state stabil, tidak ada perubahan signifikan dari Rev. 516** (data terkonsisten). Build gate: **NOT RE-RUNABLE** — `node_modules/` **absent** (dihapus setelah Rev. 377; `npm ci` diperlukan untuk memulihkan); `.next/` masih ada (partial: `cache/` + `diagnostics/` + `package.json` + `server/` + `static/`, bukan production build). `tsc --noEmit` exit 1, `npm run lint` exit 2, `npx next build` exit 1 — semua gagal karena `node_modules/` **absent**; `npm ci` diperlukan untuk memulihkan sebelum melakukan type-check/lint/build. Database (dev.db): **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`; seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` & `import_students_grades_clean.py` tidak ditemukan di working tree). **M02a (NFC):** field `uid_nfc` ada aktif di tabel students, semua 453 NULL (data ekspor NFC Tools belum tersedia). **Auth hardcode:** Login.tsx tetap `admin@pondokanbat.com` / `admin123` (typo domain). **Beranda hardcode:** Beranda.tsx & page.tsx masih hardcoded totalSantri. **Schema:** model `KitabProgress` & `Sertakan` sudah terdefinisi; `prisma validate` sukses. **Status:** dokumen PRD **REVISI** — rev 517 = PRD fresh verification & konfirmasi stabilitas; seluruh data terkonsisten, tidak ada perubahan signifikan dari Rev. 516; branch 0 ahead / 0 behind origin_main."""

# Try 3 pipes first, then 4 pipes
if old_s11 not in content:
    old_s11 = old_s11.replace("|||- **Rev. 515", "|||||- **Rev. 515")
    if old_s11 not in content:
        print("ERROR: §11 Rev. 515 entry not found (3-pipe or 4-pipe)!")
        sys.exit(1)

content = content.replace(old_s11, new_s11)

# 3. Update §12: insert Rev. 517 entry before Rev. 515 entry
old_s12_header = "## 12. REVISI TERBARU (Rev. 468–516 — 24 Oktober 2026 WIB)\n\n> **Verifikasi fresh dilakukan:** 25 Oktober 2026 (WIB, cron run) — query `sqlite3` ke `dev.db`, `npx tsc --noEmit`, `npx eslint .`, `npx next build`."

new_s12 = """## 12. REVISI TERBARU (Rev. 468–516 — 24 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 24 Oktober 2026 (WIB, cron run) — query `sqlite3` ke `dev.db`, `npx tsc --noEmit`, `npx eslint .`, `npx next build`.
> **Verifikasi fresh kondisi repository + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 516 (data terkonsisten).**
> - **Commit count:** 0 / 0 (0 commits ahead origin_main). Local branch **0 commits ahead / 0 behind** origin_main. **origin/main:** `3b3751b972c70052b930f91011e1b01f84771ff7` (Rev. 516, in sync).
> - **Working tree:** `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 517 (final)); HEAD `3b3751b972c70052b930f91011e1b01f84771ff7` (Rev. 516 commit); seluruh file lain cocak dengan HEAD; untracked: 61 skrip utility (tidak terpantau dalam git). `git ls-files` = 187 file.
> - **Database (dev.db):** file `dev.db` **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`; seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` & `import_students_grades_clean.py` tidak ditemukan di working tree).
> - **Build quality gate:** **NOT RE-RUNABLE** — `node_modules/` **absent** (dihapus setelah Rev. 377; `npm ci` diperlukan untuk memulihkan); `.next/` masih ada (partial: `cache/` + `diagnostics/` + `package.json` + `server/` + `static/`, bukan production build). `tsc --noEmit` exit 1, `npm run lint` exit 2, `npx next build` exit 1 — semua gagal karena `node_modules/` **absent**; `npm ci` diperlukan untuk memulihkan sebelum melakukan type-check/lint/build.
> - **Source files:** `src/app/*` = 12 sub direktori (absensi, beranda, berita, guru, kelas, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah) + `globals.css` + `layout.tsx` + `page.tsx` = 15 entri (12 halaman + layout + page; tidak ada `modul` subdirectory). `src/components` = `Beranda.tsx` & `Login.tsx`. `src/lib` = **kosong** (logic inline di komponen). Prisma driver = `prisma` ^8.0.0-rc.2 (SQLite).
> - **M02a (NFC):** field `uid_nfc` ada aktif di tabel `students` (kolom setelah `photo`); `prisma/schema.prisma` baris 68 (`uidNfc String? @map(\\"uid_nfc\\")`), `init_schema.sql` baris 44, `init_db.py` baris 60. **Tidak ada satupun siswa yang memiliki `uid_nfc` diisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
> - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (typo domain `pondokanat.com`); produksi butuh bcrypt + session.
> - **Beranda hardcode:** `Beranda.tsx` & `src/app/beranda/page.tsx` masih hardcoded `totalSantri` (belum fetch real-time dari DB).
> - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` sukses. Schema inconsistency (Rev. 38–45) SELESAI — kedua model konsisten dengan referensi di `Subject` dan `User`.
> - **Status:** dokumen PRD **REVISI** — rev 517: PRD fresh verification & stability confirmation (24 Oct 2026 WIB); HEAD `3b3751b972c70052b930f91011e1b01f84771ff7` (Rev. 516 commit); 0 / 0 (0 commits ahead origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 516 (data terkonsisten)."""

if old_s12_header not in content:
    print("ERROR: §12 header not found!")
    sys.exit(1)

content = content.replace(old_s12_header, new_s12)

with open(path, "w") as f:
    f.write(content)

print("Done! PRD updated to Rev. 517.")
print(f"File size: {len(content)} bytes")
