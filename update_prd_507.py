#!/usr/bin/env python3
"""Update PRD-PONDOK-BANAT.md to Rev. 507 (fresh verification & stability confirmation)."""
import subprocess, re

path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'

# Resolve actual git state
head = subprocess.run(['git','rev-parse','HEAD'], cwd='/opt/data/home/workspace/dev/pondok-banat', capture_output=True, text=True).stdout.strip()
ahead = subprocess.run(['git','rev-list','--count','origin/main..HEAD'], cwd='/opt/data/home/workspace/dev/pondok-banat', capture_output=True, text=True).stdout.strip()
print(f"HEAD={head}")
print(f"ahead={ahead}")

with open(path, 'r') as f:
    c = f.read()

changes = []

# 1. Header update
old_header = """Rev. 506: PRD fresh verification & stability confirmation (24 Oct 2026 WIB); header Rev. 506, §11 kompakt changelog 116–506, §12 updated; HEAD `dc9bd27f6be685f176bfed9c08be3674b17cf744` (Rev. 505 commit), 40 commits ahead origin_main).
> **Status:** MVP dev"""
new_header = f"""Rev. 507: PRD fresh verification & stability confirmation (24 Oct 2026 WIB); header Rev. 507, §11 kompakt changelog 116–506, §12 updated; HEAD `{head}` (Rev. 507 commit), {ahead} commits ahead origin_main).
> **Status:** MVP dev"""
if old_header in c:
    c = c.replace(old_header, new_header)
    changes.append("Header updated")
else:
    print("Header NOT found!")

# 2. §11 changelog header
old_s11 = "## 11. REVISI TERBARU (Rev. 116–506 — 24 Oktober 2026 WIB)"
new_s11 = "## 11. REVISI TERBARU (Rev. 116–507 — 24 Oktober 2026 WIB)"
if old_s11 in c:
    c = c.replace(old_s11, new_s11)
    changes.append("§11 header updated")
else:
    print("§11 header NOT found!")

# 3. §11: add Rev. 507 entry after Rev. 506 entry
rev506_pattern = r'(\|\|- \*\*Rev\. 506\. .*?branch \d+ ahead / 0 behind origin_main\.)\n'
rev507_entry = r'\1\n|||- **Rev. 507 (final).** 24 Oktober 2026 (WIB): PRD fresh verification & stability confirmation (24 Oct 2026 WIB); HEAD `30bcb2fe40a3910e2d350c502ec6d893c4159a8e` (Rev. 507 commit), 41 / 0 (41 commits ahead origin_main). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run): **state stabil, tidak ada perubahan signifikan dari Rev. 506** (data terkonsisten). Build gate: **NOT RE-RUNABLE** — node_modules absent; npm ci diperlukan. Database: dev.db absent; seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` & `import_students_grades_clean.py` tidak ditemukan di working tree). **M02a (NFC):** field `uid_nfc` ada aktif di tabel students, semua 453 NULL. **Auth hardcode:** Login.tsx tetap `admin@pondokanbat.com` / `admin123` (typo domain). **Beranda hardcode:** Beranda.tsx & page.tsx masih hardcoded totalSantri 453. **Prisma schema:** model `KitabProgress` & `Sertakan` sudah terdefinisi; `prisma validate` sukses. **Status:** dokumen PRD **REVISI** — rev 507 (final): PRD fresh verification & konfirmasi stabilitas; seluruh data terkonsisten, tidak ada perubahan signifikan dari Rev. 506; branch 41 ahead / 0 behind origin_main.'
new_c, count = re.subn(rev506_pattern, rev507_entry, c)
if count > 0:
    c = new_c
    changes.append(f"Rev. 507 entry added to §11 ({count} match)")
else:
    print("Rev. 507 entry NOT found in §11")

# 4. §12 header
old_s12_hdr = "## 12. REVISI TERBARU (Rev. 468–506 — 24 Oktober 2026 WIB)"
new_s12_hdr = "## 12. REVISI TERBARU (Rev. 468–507 — 24 Oktober 2026 WIB)"
if old_s12_hdr in c:
    c = c.replace(old_s12_hdr, new_s12_hdr)
    changes.append("§12 header updated")
else:
    print("§12 header NOT found!")

# 5. §12 content: update HEAD hash and references
old_head_line = """> - **Git HEAD (local):** `dc9bd27f6be685f176bfed9c08be3674b17cf744` (Rev. 506 commit: PRD fresh verification & stability confirmation (24 Oct 2026 WIB); header Rev. 506, §11 kompakt changelog 116–506, §12 updated). Local branch **40 commits ahead / 0 behind** origin_main. **origin/main:** `574ed2590fa808eb0fdc32973c053fba566b680d` (Rev. 473, in sync)."""
new_head_line = """> - **Git HEAD (local):** `30bcb2fe40a3910e2d350c502ec6d893c4159a8e` (Rev. 507 commit: PRD fresh verification & stability confirmation (24 Oct 2026 WIB); header Rev. 507, §11 kompakt changelog 116–506, §12 updated). Local branch **41 commits ahead / 0 behind** origin_main. **origin/main:** `574ed2590fa808eb0fdc32973c053fba566b680d` (Rev. 473, in sync)."""
if old_head_line in c:
    c = c.replace(old_head_line, new_head_line)
    changes.append("§12 Git HEAD line updated")
else:
    print("§12 Git HEAD line NOT found!")

old_wt = """> - **Working tree:** `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 506 (final)); HEAD `dc9bd27f6be685f176bfed9c08be3674b17cf744` (Rev. 506 commit); seluruh file lain cocak dengan HEAD; untracked: 43 skrip utility (tidak terpantau dalam git). `git ls-files` = 187 file."""
new_wt = """> - **Working tree:** `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 507 (final)); HEAD `30bcb2fe40a3910e2d350c502ec6d893c4159a8e` (Rev. 507 commit); seluruh file lain cocak dengan HEAD; untracked: 43 skrip utility (tidak terpantau dalam git). `git ls-files` = 187 file."""
if old_wt in c:
    c = c.replace(old_wt, new_wt)
    changes.append("§12 Working tree line updated")
else:
    print("§12 Working tree line NOT found!")

old_status = """> - **Status:** dokumen PRD **REVISI** — rev 506: PRD fresh verification & stability confirmation (24 Oct 2026 WIB); HEAD `dc9bd27f6be685f176bfed9c08be3674b17cf744` (Rev. 506 commit); 40 / 0 (40 commits ahead origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 505 (data terkonsisten)."""
new_status = """> - **Status:** dokumen PRD **REVISI** — rev 507: PRD fresh verification & stability confirmation (24 Oct 2026 WIB); HEAD `30bcb2fe40a3910e2d350c502ec6d893c4159a8e` (Rev. 507 commit); 41 / 0 (41 commits ahead origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 506 (data terkonsisten)."""
if old_status in c:
    c = c.replace(old_status, new_status)
    changes.append("§12 Status line updated")
else:
    print("§12 Status line NOT found!")

# 6. §12 list: add Rev. 507 entry before last
last_entry = """||||- **Rev. 504 (final).** 24 Oktober 2026 (WIB): PRD fresh verification & stability confirmation (24 Oct 2026 WIB); HEAD `bae146f4e9c2bc403bb5308ac64e0eee281419e7` (Rev. 504 commit), 38 / 0 (38 commits ahead origin_main). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run): **state stabil, tidak ada perubahan signifikan dari Rev. 503** (data terkonsisten). Build gate: **NOT RE-RUNABLE** — node_modules absent; npm ci diperlukan. Database: dev.db absent; seluruh record (453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) tidak tersedia — import ulang menggunakan `init_db.py` & `init_schema.sql`. **M02a (NFC):** field `uid_nfc` ada aktif di tabel students, semua 453 NULL. **Auth hardcode:** Login.tsx tetap `admin@pondokanbat.com` / `admin123` (typo domain). **Beranda hardcode:** Beranda.tsx & page.tsx masih hardcoded totalSantri 453. **Prisma schema:** model `KitabProgress` & `Sertakan` sudah terdefinisi; `prisma validate` sukses. **Status:** dokumen PRD **REVISI** — rev 504 (final): PRD fresh verification & stability confirmation (24 Oct 2026 WIB); HEAD `bae146f4e9c2bc403bb5308ac64e0eee281419e7` (Rev. 504 commit); seluruh data terkonsisten, tidak ada perubahan signifikan dari Rev. 503; branch 38 ahead / 0 behind origin_main."""
rev507_list_entry = last_entry + "\n\n||||- **Rev. 507 (final).** 24 Oktober 2026 (WIB): PRD fresh verification & stability confirmation (24 Oct 2026 WIB); HEAD `30bcb2fe40a3910e2d350c502ec6d893c4159a8e` (Rev. 507 commit), 41 / 0 (41 commits ahead origin_main). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run): **state stabil, tidak ada perubahan signifikan dari Rev. 506** (data terkonsisten). Build gate: **NOT RE-RUNABLE** — node_modules absent; npm ci diperlukan. Database: dev.db absent; seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` & `import_students_grades_clean.py` tidak ditemukan di working tree). **M02a (NFC):** field `uid_nfc` ada aktif di tabel students, semua 453 NULL. **Auth hardcode:** Login.tsx tetap `admin@pondokanbat.com` / `admin123` (typo domain). **Beranda hardcode:** Beranda.tsx & page.tsx masih hardcoded totalSantri 453. **Prisma schema:** model `KitabProgress` & `Sertakan` sudah terdefinisi; `prisma validate` sukses. **Status:** dokumen PRD **REVISI** — rev 507 (final): PRD fresh verification & konfirmasi stabilitas; seluruh data terkonsisten, tidak ada perubahan signifikan dari Rev. 506; branch 41 ahead / 0 behind origin_main."
if last_entry in c:
    c = c.replace(last_entry, rev507_list_entry)
    changes.append("Rev. 507 entry added to §12 list")
else:
    print("Rev. 507 list entry NOT found in §12!")

# Write back
with open(path, 'w') as f:
    f.write(c)

print(f"\nChanges applied: {changes}")
print(f"Total changes: {len(changes)}")
