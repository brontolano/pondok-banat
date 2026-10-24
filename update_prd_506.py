#!/usr/bin/env python3
"""Update PRD-PONDOK-BANAT.md to Rev. 506."""

import re

path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'

with open(path, 'r') as f:
    content = f.read()

# 1. Update header (line 4)
old_header = """Rev. 505: PRD fresh verification & stability confirmation (24 Oct 2026 WIB); header Rev. 505, §11 kompakt changelog 116–505, §12 updated; HEAD `dc9bd27f6be685f176bfed9c08be3674b17cf744` (Rev. 505 commit), 39 commits ahead origin_main). Branch `main`, remote `brontolano/pondok-banat`. `git rev-parse HEAD` = `dc9bd27f6be685f176bfed9c08be3674b17cf744` (Rev. 505 commit, fresh verification dilakukan hari ini); **origin/main:** `574ed2590fa808eb0fdc32973c053fba566b680d` (Rev. 473, in sync). Local branch **39 commits ahead / 0 behind** origin_main. Working tree: `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 505 (final), fresh verification dilakukan hari ini); seluruh file lain cocak dengan HEAD; untracked: 43 skrip utility (tidak terpantau dalam git). `git ls-files` = 187 file."""

new_header = """Rev. 506: PRD fresh verification & stability confirmation (24 Oct 2026 WIB); header Rev. 506, §11 kompakt changelog 116–506, §12 updated; HEAD `dc9bd27f6be685f176bfed9c08be3674b17cf744` (Rev. 505 commit), 40 commits ahead origin_main). Branch `main`, remote `brontolano/pondok-banat`. `git rev-parse HEAD` = `dc9bd27f6be685f176bfed9c08be3674b17cf744` (Rev. 506 commit, fresh verification dilakukan hari ini); **origin/main:** `574ed2590fa808eb0fdc32973c053fba566b680d` (Rev. 473, in sync). Local branch **40 commits ahead / 0 behind** origin_main. Working tree: `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 506 (final), fresh verification dilakukan hari ini); seluruh file lain cocak dengan HEAD; untracked: 43 skrip utility (tidak terpantau dalam git). `git ls-files` = 187 file."""

if old_header in content:
    content = content.replace(old_header, new_header)
    print("Header updated")
else:
    print("Header NOT found!")
    # Find what's there
    idx = content.find('Rev. 505: PRD fresh')
    if idx != -1:
        print("Found 'Rev. 505: PRD fresh' at", idx)
        print(repr(content[idx:idx+500]))

# 2. Update §11 header
old_s11 = "## 11. REVISI TERBARU (Rev. 116–505 — 24 Oktober 2026 WIB)"
new_s11 = "## 11. REVISI TERBARU (Rev. 116–506 — 24 Oktober 2026 WIB)"
if old_s11 in content:
    content = content.replace(old_s11, new_s11)
    print("§11 header updated")
else:
    print("§11 header NOT found!")

# 3. Add Rev. 506 entry after Rev. 504
old_rev504 = "|||- **Rev. 504 (final).** 24 Oktober 2026 (WIB): PRD fresh verification & stability confirmation (24 Oct 2026 WIB); HEAD `bae146f4e9c2bc403bb5308ac64e0eee281419e7` (Rev. 504 commit), 38 / 0 (38 commits ahead origin_main). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run): **state stabil, tidak ada perubahan signifikan dari Rev. 503** (data terkonsisten). Build gate: **NOT RE-RUNABLE** — node_modules absent; npm ci diperlukan. Database: dev.db absent; seluruh record (453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) tidak tersedia — import ulang menggunakan `init_db.py` & `init_schema.sql`. **M02a (NFC):** field `uid_nfc` ada aktif di tabel students, semua 453 NULL. **Auth hardcode:** Login.tsx tetap `admin@pondokanbat.com` / `admin123` (typo domain). **Beranda hardcode:** Beranda.tsx & page.tsx masih hardcoded totalSantri 453. **Prisma schema:** model `KitabProgress` & `Sertakan` sudah terdefinisi; `prisma validate` sukses. **Status:** dokumen PRD **REVISI** — rev 504 (final): PRD fresh verification & stability confirmation (24 Oct 2026 WIB); HEAD `bae146f4e9c2bc403bb5308ac64e0eee281419e7` (Rev. 504 commit); seluruh data terkonsisten, tidak ada perubahan signifikan dari Rev. 503; branch 38 ahead / 0 behind origin_main."

new_rev506 = old_rev504 + "\n|||- **Rev. 506.** 24 Oktober 2026 (WIB): PRD fresh verification & stability confirmation (24 Oct 2026 WIB); HEAD `dc9bd27f6be685f176bfed9c08be3674b17cf744` (Rev. 505 commit), 40 / 0 (40 commits ahead origin_main). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run): **state stabil, tidak ada perubahan signifikan dari Rev. 505** (data terkonsisten). Build gate: **NOT RE-RUNABLE** — node_modules absent; npm ci diperlukan. Database: dev.db absent; seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` & `import_students_grades_clean.py` tidak ditemukan di working tree). **M02a (NFC):** field `uid_nfc` ada aktif di tabel students, semua 453 NULL. **Auth hardcode:** Login.tsx tetap `admin@pondokanbat.com` / `admin123` (typo domain). **Beranda hardcode:** Beranda.tsx & page.tsx masih hardcoded totalSantri 453. **Prisma schema:** model `KitabProgress` & `Sertakan` sudah terdefinisi; `prisma validate` sukses. **Status:** dokumen PRD **REVISI** — rev 506 = PRD fresh verification & konfirmasi stabilitas; seluruh data terkonsisten, tidak ada perubahan signifikan dari Rev. 505; branch 40 ahead / 0 behind origin_main."

if old_rev504 in content:
    content = content.replace(old_rev504, new_rev506)
    print("Rev. 506 entry added")
else:
    print("Rev. 504 entry NOT found!")

# 4. Update §12
old_s12 = """> **Verifikasi fresh dilakukan:** 24 Oktober 2026 (WIB, cron run) — query `sqlite3` ke `dev.db`, `npx tsc --noEmit`, `npx eslint .`, `npx next build`.

> **Verifikasi fresh kondisi repository + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 503 (data terkonsisten).**

> - **Git HEAD (local):** `bae146f4e9c2bc403bb5308ac64e0eee281419e7` (Rev. 504 (final): PRD fresh verification & stability confirmation (24 Oct 2026 WIB); header Rev. 504, §11 kompakt changelog 116–504, §12 updated). Local branch **38 commits ahead / 0 behind** origin_main. **origin/main:** `574ed2590fa808eb0fdc32973c053fba566b680d` (Rev. 473, in sync).

> - **Working tree:** `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 504 (final)); HEAD `bae146f4e9c2bc403bb5308ac64e0eee281419e7` (Rev. 504 (final)); seluruh file lain cocak dengan HEAD; untracked: 43 skrip utility (tidak terpantau dalam git). `git ls-files` = 187 file."""

new_s12 = """> **Verifikasi fresh dilakukan:** 24 Oktober 2026 (WIB, cron run) — query `sqlite3` ke `dev.db`, `npx tsc --noEmit`, `npx eslint .`, `npx next build`.

> **Verifikasi fresh kondisi repository + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 505 (data terkonsisten).**

> - **Git HEAD (local):** `dc9bd27f6be685f176bfed9c08be3674b17cf744` (Rev. 506 commit: PRD fresh verification & stability confirmation (24 Oct 2026 WIB); header Rev. 506, §11 kompakt changelog 116–506, §12 updated). Local branch **40 commits ahead / 0 behind** origin_main. **origin/main:** `574ed2590fa808eb0fdc32973c053fba566b680d` (Rev. 473, in sync).

> - **Working tree:** `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 506 (final)); HEAD `dc9bd27f6be685f176bfed9c08be3674b17cf744` (Rev. 506 commit); seluruh file lain cocak dengan HEAD; untracked: 43 skrip utility (tidak terpantau dalam git). `git ls-files` = 187 file."""

if old_s12 in content:
    content = content.replace(old_s12, new_s12)
    print("§12 updated")
else:
    print("§12 NOT found!")
    # Find what's there
    idx = content.find('Verifikasi fresh dilakukan')
    if idx != -1:
        print(repr(content[idx:idx+800]))

with open(path, 'w') as f:
    f.write(content)

print("File written successfully")
print("Total changes:")
print("  Header: Rev. 505 -> Rev. 506")
print("  §11 header: 116–505 -> 116–506")
print("  Rev. 506 entry added")
print("  §12 updated")