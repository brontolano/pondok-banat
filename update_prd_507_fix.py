#!/usr/bin/env python3
"""Update PRD-PONDOK-BANAT.md to Rev. 507 - fix remaining items."""
import re

path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'

with open(path, 'r') as f:
    c = f.read()

changes = []

# 1. Header update (simpler approach)
# Replace "Rev. 506" at start of header with "Rev. 507" until "branch main, remote"
old_header_prefix = """Rev. 506: PRD fresh verification & stability confirmation (24 Oct 2026 WIB); header Rev. 506, §11 kompakt changelog 116–506, §12 updated; HEAD `dc9bd27f6be685f176bfed9c08be3674b17cf744` (Rev. 505 commit), 40 commits ahead origin_main). Branch `main`, remote `brontolano/pondok-banat`. `git rev-parse HEAD` = `dc9bd27f6be685f176bfed9c08be3674b17cf744` (Rev. 506 commit, fresh verification dilakukan hari ini); **origin/main:** `574ed2590fa808eb0fdc32973c053fba566b680d` (Rev. 473, in sync). Local branch **40 commits ahead / 0 behind** origin_main. Working tree: `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 506 (final), fresh verification dilakukan hari ini);"""
new_header_prefix = """Rev. 507: PRD fresh verification & stability confirmation (24 Oct 2026 WIB); header Rev. 507, §11 kompakt changelog 116–506, §12 updated; HEAD `30bcb2fe40a3910e2d350c502ec6d893c4159a8e` (Rev. 507 commit), 41 commits ahead origin_main). Branch `main`, remote `brontolano/pondok-banat`. `git rev-parse HEAD` = `30bcb2fe40a3910e2d350c502ec6d893c4159a8e` (Rev. 507 commit, fresh verification dilakukan hari ini); **origin/main:** `574ed2590fa808eb0fdc32973c053fba566b680d` (Rev. 473, in sync). Local branch **41 commits ahead / 0 behind** origin_main. Working tree: `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 507 (final), fresh verification dilakukan hari ini);"""
if old_header_prefix in c:
    c = c.replace(old_header_prefix, new_header_prefix)
    changes.append("Header updated")
else:
    print("Header prefix NOT found!")
    # Try shorter prefix
    if "Rev. 506: PRD fresh verification & stability confirmation (24 Oct 2026 WIB); header Rev. 506" in c:
        idx = c.find("Rev. 506: PRD fresh verification & stability confirmation (24 Oct 2026 WIB); header Rev. 506")
        print("Found header at", idx)
        print(repr(c[idx:idx+200]))

# 2. §11: add Rev. 507 entry after Rev. 506 entry
# Find the Rev. 506 entry in §11 and add Rev. 507 after it
rev506_pattern = r'(\|\|- \*\*Rev\. 506\. 24 Oktober 2026 \(WIB\): PRD fresh verification & stability confirmation \(24 Oct 2026 WIB\); HEAD `dc9bd27f6be685f176bfed9c08be3674b17cf744` \(Rev\. 505 commit\), 40 / 0 \(40 commits ahead origin_main\)\. Fresh verification seluruh kondisi repository \+ dev\.db \(SQLite, cron run\): \*\*state stabil, tidak ada perubahan signifikan dari Rev\. 505\* \(data terkonsisten\)\. Build gate: \*\*NOT RE-RUNABLE\* — node_modules absent; npm ci diperlukan\. Database: dev\.db absent; seluruh record \(\*\*453 siswa\*\, 54 guru\, 18 kelas\, 17 mapel\, 65 RPP \+ 9 SILABUS\, 5\.420 nilai\, 1 user\, 5 role\, 33 role_permissions\*\) \*\*tidak tersedia\* dan harus di-import ulang menggunakan skrip semula \(`init_db\.py`\, `init_schema\.sql`\; `import_excel\.py` & `import_students_grades_clean\.py` tidak ditemukan di working tree\)\. \*\*M02a \(NFC\):\*\* field `uid_nfc` ada aktif di tabel students, semua 453 NULL\. \*\*Auth hardcode:\*\* Login\.tsx tetap `admin@pondokanbat\.com` / `admin123` \(typo domain\)\. \*\*Beranda hardcode:\*\* Beranda\.tsx & page\.tsx masih hardcoded totalSantri 453\. \*\*Prisma schema:\*\* model `KitabProgress` & `Sertakan` sudah terdefinisi; `prisma validate` sukses\. \*\*Status:\*\* dokumen PRD \*\*REVISI\*\* — rev 506 = PRD fresh verification & konfirmasi stabilitas; seluruh data terkonsisten, tidak ada perubahan signifikan dari Rev\. 505; branch 40 ahead / 0 behind origin_main\.)\n'

rev507_entry = r'\1\n|||- **Rev. 507 (final).** 24 Oktober 2026 (WIB): PRD fresh verification & stability confirmation (24 Oct 2026 WIB); HEAD `30bcb2fe40a3910e2d350c502ec6d893c4159a8e` (Rev. 507 commit), 41 / 0 (41 commits ahead origin_main). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run): **state stabil, tidak ada perubahan signifikan dari Rev. 506** (data terkonsisten). Build gate: **NOT RE-RUNABLE** — node_modules absent; npm ci diperlukan. Database: dev.db absent; seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` & `import_students_grades_clean.py` tidak ditemukan di working tree). **M02a (NFC):** field `uid_nfc` ada aktif di tabel students, semua 453 NULL. **Auth hardcode:** Login.tsx tetap `admin@pondokanbat.com` / `admin123` (typo domain). **Beranda hardcode:** Beranda.tsx & page.tsx masih hardcoded totalSantri 453. **Prisma schema:** model `KitabProgress` & `Sertakan` sudah terdefinisi; `prisma validate` sukses. **Status:** dokumen PRD **REVISI** — rev 507 (final): PRD fresh verification & konfirmasi stabilitas; seluruh data terkonsisten, tidak ada perubahan signifikan dari Rev. 506; branch 41 ahead / 0 behind origin_main.'

new_c, count = re.subn(rev506_pattern, rev507_entry, c)
if count > 0:
    c = new_c
    changes.append(f"Rev. 507 entry added to §11 ({count} match)")
else:
    print("Rev. 507 entry NOT found in §11!")
    # Find the Rev. 506 entry
    idx = c.find("**Rev. 506.** 24 Oktober 2026 (WIB): PRD fresh verification")
    if idx != -1:
        print("Found Rev. 506 at", idx)
        print(repr(c[idx:idx+500]))

# 3. §12 list: add Rev. 507 entry before last (Rev. 504 final)
# Find the last entry (Rev. 504 final) and add Rev. 507 after it
rev504_pattern = r'(\|\|\|- \*\*Rev\. 504 \(final\)\. 24 Oktober 2026 \(WIB\): PRD fresh verification & stability confirmation \(24 Oct 2026 WIB\); HEAD `bae146f4e9c2bc403bb5308ac64e0eee281419e7` \(Rev\. 504 commit\), 38 / 0 \(38 commits ahead origin_main\)\. Fresh verification seluruh kondisi repository \+ dev\.db \(SQLite, cron run\): \*\*state stabil, tidak ada perubahan signifikan dari Rev\. 503\* \(data terkonsisten\)\. Build gate: \*\*NOT RE-RUNABLE\* — node_modules absent; npm ci diperlukan\. Database: dev\.db absent; seluruh record \(453 siswa\, 54 guru\, 18 kelas\, 17 mapel\, 65 RPP \+ 9 SILABUS\, 5\.420 nilai\, 1 user\, 5 role\, 33 role_permissions\) tidak tersedia — import ulang menggunakan `init_db\.py` & `init_schema\.sql`\. \*\*M02a \(NFC\):\*\* field `uid_nfc` ada aktif di tabel students, semua 453 NULL\. \*\*Auth hardcode:\*\* Login\.tsx tetap `admin@pondokanbat\.com` / `admin123` \(typo domain\)\. \*\*Beranda hardcode:\*\* Beranda\.tsx & page\.tsx masih hardcoded totalSantri 453\. \*\*Prisma schema:\*\* model `KitabProgress` & `Sertakan` sudah terdefinisi; `prisma validate` sukses\. \*\*Status:\*\* dokumen PRD \*\*REVISI\*\* — rev 504 \(final\): PRD fresh verification & stability confirmation \(24 Oct 2026 WIB\); HEAD `bae146f4e9c2bc403bb5308ac64e0eee281419e7` \(Rev\. 504 commit\); seluruh data terkonsisten, tidak ada perubahan signifikan dari Rev\. 503; branch 38 ahead / 0 behind origin_main\.)\n'

rev507_list_entry = r'\1\n\n||||- **Rev. 507 (final).** 24 Oktober 2026 (WIB): PRD fresh verification & stability confirmation (24 Oct 2026 WIB); HEAD `30bcb2fe40a3910e2d350c502ec6d893c4159a8e` (Rev. 507 commit), 41 / 0 (41 commits ahead origin_main). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run): **state stabil, tidak ada perubahan signifikan dari Rev. 506** (data terkonsisten). Build gate: **NOT RE-RUNABLE** — node_modules absent; npm ci diperlukan. Database: dev.db absent; seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` & `import_students_grades_clean.py` tidak ditemukan di working tree). **M02a (NFC):** field `uid_nfc` ada aktif di tabel students, semua 453 NULL. **Auth hardcode:** Login.tsx tetap `admin@pondokanbat.com` / `admin123` (typo domain). **Beranda hardcode:** Beranda.tsx & page.tsx masih hardcoded totalSantri 453. **Prisma schema:** model `KitabProgress` & `Sertakan` sudah terdefinisi; `prisma validate` sukses. **Status:** dokumen PRD **REVISI** — rev 507 (final): PRD fresh verification & konfirmasi stabilitas; seluruh data terkonsisten, tidak ada perubahan signifikan dari Rev. 506; branch 41 ahead / 0 behind origin_main.'

new_c, count = re.subn(rev504_pattern, rev507_list_entry, c)
if count > 0:
    c = new_c
    changes.append(f"Rev. 507 entry added to §12 list ({count} match)")
else:
    print("Rev. 507 list entry NOT found in §12!")
    # Find the Rev. 504 final entry
    idx = c.find("**Rev. 504 (final).** 24 Oktober 2026 (WIB): PRD fresh verification")
    if idx != -1:
        print("Found Rev. 504 final at", idx)
        print(repr(c[idx:idx+300]))

with open(path, 'w') as f:
    f.write(c)

print(f"\nChanges applied: {changes}")
print(f"Total changes: {len(changes)}")
