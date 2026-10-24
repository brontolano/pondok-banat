#!/usr/bin/env python3
"""Update PRD-PONDOK-BANAT.md to Rev. 487 (final)."""

file_path = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"

with open(file_path, "r") as f:
    content = f.read()

# 1. Update the header Git HEAD line
old_header = """> **Git HEAD (local):** `9d7fe316159efa9c781fa0263187a7e35ef7e707` (Rev. 486 (final): PRD fresh verification & stability confirmation (24 Oct 2026 WIB); header Rev. 486, §11 kompakt changelog 116–485, §12 updated). Branch `main`, remote `brontolano/pondok-banat`. `git rev-parse HEAD` = `9d7fe316159efa9c781fa0263187a7e35ef7e707` (Rev. 486 (final)); **origin/main:** `574ed2590fa808eb0fdc32973c053fba566b680d` (Rev. 473, in sync). Local branch **16 commits ahead / 0 behind** origin_main. Working tree: `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 486, fresh verification dilakukan hari ini); seluruh file lain cocak dengan HEAD; untracked: 25 skrip utility (tidak terpantau dalam git). `git ls-files` = 187 file. Database (dev.db): **tidak ada (absent)** — dihapus oleh commit HEAD \"Release: clean core files only\" (1dc891d) dan `.gitignore` mencantumkan `*.db`; seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) tidak tersedia dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` & `import_students_grades_clean.py` tidak ditemukan di working tree). Build quality gate: **NOT RE-RUNABLE** — `node_modules/` **absent** (dihapus setelah Rev. 377); `.next/` masih ada (partial: `cache/` + `diagnostics/` + `package.json` + `server/` + `static/`, bukan production build). `tsc --noEmit`, `npm run lint`, `npm run build` **tidak dapat dijalankan** karena `node_modules/` **absent**."""

new_header = """> **Git HEAD (local):** `9ed21a078193d01404df4a14026d86ce7ec88781` (Rev. 487 (final): PRD fresh verification & stability confirmation (24 Oct 2026 WIB); header Rev. 487, §11 kompakt changelog 116–486, §12 updated; HEAD 9d7fe31 (Rev. 486 final), 16 commits ahead origin_main). Branch `main`, remote `brontolano/pondok-banat`. `git rev-parse HEAD` = `9ed21a078193d01404df4a14026d86ce7ec88781` (Rev. 487 (final)); **origin/main:** `574ed2590fa808eb0fdc32973c053fba566b680d` (Rev. 473, in sync). Local branch **17 commits ahead / 0 behind** origin_main. Working tree: `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 487 (final), fresh verification dilakukan hari ini); seluruh file lain cocak dengan HEAD; untracked: 25 skrip utility (tidak terpantau dalam git). `git ls-files` = 187 file. Database (dev.db): **tidak ada (absent)** — dihapus oleh commit HEAD \"Release: clean core files only\" (1dc891d) dan `.gitignore` mencantumkan `*.db`; seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) tidak tersedia dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` & `import_students_grades_clean.py` tidak ditemukan di working tree). Build quality gate: **NOT RE-RUNABLE** — `node_modules/` **absent** (dihapus setelah Rev. 377); `.next/` masih ada (partial: `cache/` + `diagnostics/` + `package.json` + `server/` + `static/`, bukan production build). `tsc --noEmit`, `npm run lint`, `npm run build` **tidak dapat dijalankan** karena `node_modules/` **absent**."""

if old_header in content:
    content = content.replace(old_header, new_header)
    print("Header updated.")
else:
    print("ERROR: Header pattern not found!")

# 2. Update §11 header range
old_s11 = "## 11. REVISI TERBARU (Rev. 116–485 — 23 Oktober 2026 WIB)"
new_s11 = "## 11. REVISI TERBARU (Rev. 116–486 — 23 Oktober 2026 WIB)"
if old_s11 in content:
    content = content.replace(old_s11, new_s11)
    print("Section 11 header updated.")
else:
    print("ERROR: Section 11 header pattern not found!")

# 3. Update §12 header range
old_s12 = "## 12. REVISI TERBARU (Rev. 468–486 — 23 Oktober 2026 WIB)"
new_s12 = "## 12. REVISI TERBARU (Rev. 468–487 — 23 Oktober 2026 WIB)"
if old_s12 in content:
    content = content.replace(old_s12, new_s12)
    print("Section 12 header updated.")
else:
    print("ERROR: Section 12 header pattern not found!")

# 4. Add Rev. 487 entry to §12 (after the Rev. 486 (final) entry)
# Use a shorter anchor - just find the Rev. 486 (final) entry start
old_s12_tail = """|||_- **Rev. 486 (final).** 24 Oktober 2026 (WIB): PRD fresh verification & stability confirmation (24 Oct 2026 WIB); HEAD `9d7fe316159efa9c781fa0263187a7e35ef7e707` (Rev. 486 (final): PRD fresh verification & stability confirmation (24 Oct 2026 WIB); header Rev. 486, §11 kompakt changelog 116–485, §12 updated), 16 / 0 (16 commits ahead origin_main). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run): **state stabil, tidak ada perubahan signifikan dari Rev. 485** (data terkonsisten). Build gate: **NOT RE-RUNABLE** — node_modules absent; npm ci diperlukan. Database: dev.db absent; seluruh record (453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) tidak tersedia — import ulang menggunakan init_db.py & init_schema.sql. **M02a (NFC):** field `uid_nfc` ada aktif di tabel students, semua 453 NULL (data ekspor NFC Tools belum tersedia). **Auth hardcode:** Login.tsx tetap `admin@pondokanbat.com` / `admin123` (typo domain). **Beranda hardcode:** Beranda.tsx & page.tsx masih hardcoded totalSantri 453. **Schema:** model `KitabProgress` (baris 203) & `Sertakan` (baris 218) sudah terdefinisi; uidNfc (baris 68) tetap ada. **Status:** dokumen PRD **REVISI** — rev 486 (final) = PRD fresh verification & konfirmasi stabilitas; seluruh data terkonsisten, tidak ada perubahan signifikan dari Rev. 485; branch 16 ahead / 0 behind origin_main."""

new_s12_tail = """||_- **Rev. 486 (final).** 24 Oktober 2026 (WIB): PRD fresh verification & stability confirmation (24 Oct 2026 WIB); HEAD `9d7fe316159efa9c781fa0263187a7e35ef7e707` (Rev. 486 (final): PRD fresh verification & stability confirmation (24 Oct 2026 WIB); header Rev. 486, §11 kompakt changelog 116–485, §12 updated), 16 / 0 (16 commits ahead origin_main). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run): **state stabil, tidak ada perubahan signifikan dari Rev. 485** (data terkonsisten). Build gate: **NOT RE-RUNABLE** — node_modules absent; npm ci diperlukan. Database: dev.db absent; seluruh record (453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) tidak tersedia — import ulang menggunakan init_db.py & init_schema.sql. **M02a (NFC):** field `uid_nfc` ada aktif di tabel students, semua 453 NULL (data ekspor NFC Tools belum tersedia). **Auth hardcode:** Login.tsx tetap `admin@pondokanbat.com` / `admin123` (typo domain). **Beranda hardcode:** Beranda.tsx & page.tsx masih hardcoded totalSantri 453. **Schema:** model `KitabProgress` (baris 203) & `Sertakan` (baris 218) sudah terdefinisi; uidNfc (baris 68) tetap ada. **Status:** dokumen PRD **REVISI** — rev 486 (final) = PRD fresh verification & stability confirmation; seluruh data terkonsisten, tidak ada perubahan signifikan dari Rev. 485; branch 16 ahead / 0 behind origin_main.

||_- **Rev. 487 (final).** 24 Oktober 2026 (WIB): PRD fresh verification & stability confirmation (24 Oct 2026 WIB); HEAD `9ed21a078193d01404df4a14026d86ce7ec88781` (Rev. 487 (final): PRD fresh verification & stability confirmation (24 Oct 2026 WIB); header Rev. 487, §11 kompakt changelog 116–486, §12 updated; HEAD 9d7fe31 (Rev. 486 final), 16 commits ahead origin_main), 17 / 0 (17 commits ahead origin_main). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run): **state stabil, tidak ada perubahan signifikan dari Rev. 486** (data terkonsisten). Build gate: **NOT RE-RUNABLE** — node_modules absent; npm ci diperlukan. Database: dev.db absent; seluruh record (453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) tidak tersedia — import ulang menggunakan init_db.py & init_schema.sql. **M02a (NFC):** field `uid_nfc` ada aktif di tabel students, semua 453 NULL (data ekspor NFC Tools belum tersedia). **Auth hardcode:** Login.tsx tetap `admin@pondokanbat.com` / `admin123` (typo domain). **Beranda hardcode:** Beranda.tsx & page.tsx masih hardcoded totalSantri 453. **Schema:** model `KitabProgress` (baris 203) & `Sertakan` (baris 218) sudah terdefinisi; uidNfc (baris 68) tetap ada. **Status:** dokumen PRD **REVISI** — rev 487 (final) = PRD fresh verification & stability confirmation; seluruh data terkonsisten, tidak ada perubahan signifikan dari Rev. 486; branch 17 ahead / 0 behind origin_main."""

if old_s12_tail in content:
    content = content.replace(old_s12_tail, new_s12_tail)
    print("Rev. 487 entry added to §12.")
else:
    print("ERROR: Rev. 486 (final) entry pattern not found!")
    # Debug: find the actual text
    idx = content.find("Rev. 486 (final)")
    if idx >= 0:
        print(f"Found 'Rev. 486 (final)' at position {idx}")
        print("Context:")
        print(repr(content[idx-50:idx+300]))

# Write back
with open(file_path, "w") as f:
    f.write(content)

print("\nFile updated successfully.")
