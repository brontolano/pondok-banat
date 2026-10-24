#!/usr/bin/env python3
"""Update PRD-PONDOK-BANAT.md to Rev. 506."""

path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'

with open(path, 'r') as f:
    lines = f.readlines()

# Find and update line 4 (header)
# Find and update §11 header (line 413)
# Find Rev. 504 entry and add Rev. 506 entry after it
# Find and update §12

for i, line in enumerate(lines):
    # Update header (line 4, index 3)
    if i == 3 and 'Rev. 505: PRD fresh verification' in line:
        lines[i] = line.replace('Rev. 505: PRD fresh verification', 'Rev. 506: PRD fresh verification')
        lines[i] = lines[i].replace('header Rev. 505, §11 kompakt changelog 116–505, §12 updated',
                                     'header Rev. 506, §11 kompakt changelog 116–506, §12 updated')
        lines[i] = lines[i].replace('39 commits ahead origin_main', '40 commits ahead origin_main')
        lines[i] = lines[i].replace('revisi terbaru = Rev. 505 (final)', 'revisi terbaru = Rev. 506 (final)')
        print(f"Header updated at line {i+1}")
    
    # Update §11 header (line 413, index 412)
    if i == 412 and '## 11. REVISI TERBARU (Rev. 116–505' in line:
        lines[i] = line.replace('Rev. 116–505', 'Rev. 116–506')
        print(f"§11 header updated at line {i+1}")
    
    # Update §12 (find 'Verifikasi fresh dilakukan')
    if 'Verifikasi fresh dilakukan' in line:
        # Update the verification message
        if 'Tidak ada perubahan signifikan dari Rev. 503' in line:
            lines[i] = line.replace('Rev. 503', 'Rev. 505')
            print(f"§12 updated at line {i+1}")
        # Update HEAD reference
        if 'bae146f4e9c2bc403bb5308ac64e0eee281419e7' in line and 'Rev. 504' in line:
            lines[i] = line.replace('bae146f4e9c2bc403bb5308ac64e0eee281419e7', 'dc9bd27f6be685f176bfed9c08be3674b17cf744')
            lines[i] = lines[i].replace('Rev. 504 (final)', 'Rev. 506 commit')
            lines[i] = lines[i].replace('38 commits ahead', '40 commits ahead')
            print(f"§12 HEAD updated at line {i+1}")
        # Update working tree reference
        if 'Working tree' in line and 'Rev. 504' in line:
            lines[i] = line.replace('bae146f4e9c2bc403bb5308ac64e0eee281419e7', 'dc9bd27f6be685f176bfed9c08be3674b17cf744')
            lines[i] = lines[i].replace('Rev. 504 (final)', 'Rev. 506 (final)')
            lines[i] = lines[i].replace('Rev. 504 (final)', 'Rev. 506 (final)')
            print(f"§12 Working tree updated at line {i+1}")

# Find the Rev. 504 entry and add Rev. 506 entry after it
for i, line in enumerate(lines):
    if 'Rev. 504 (final)' in line and '38 / 0 (38 commits ahead' in line:
        # Add Rev. 506 entry after this line
        rev506_entry = '''|||- **Rev. 506.** 24 Oktober 2026 (WIB): PRD fresh verification & stability confirmation (24 Oct 2026 WIB); HEAD `dc9bd27f6be685f176bfed9c08be3674b17cf744` (Rev. 505 commit), 40 / 0 (40 commits ahead origin_main). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run): **state stabil, tidak ada perubahan signifikan dari Rev. 505** (data terkonsisten). Build gate: **NOT RE-RUNABLE** — node_modules absent; npm ci diperlukan. Database: dev.db absent; seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` & `import_students_grades_clean.py` tidak ditemukan di working tree). **M02a (NFC):** field `uid_nfc` ada aktif di tabel students, semua 453 NULL. **Auth hardcode:** Login.tsx tetap `admin@pondokanbat.com` / `admin123` (typo domain). **Beranda hardcode:** Beranda.tsx & page.tsx masih hardcoded totalSantri 453. **Prisma schema:** model `KitabProgress` & `Sertakan` sudah terdefinisi; `prisma validate` sukses. **Status:** dokumen PRD **REVISI** — rev 506 = PRD fresh verification & konfirmasi stabilitas; seluruh data terkonsisten, tidak ada perubahan signifikan dari Rev. 505; branch 40 ahead / 0 behind origin_main.

'''
        lines.insert(i + 1, rev506_entry)
        print(f"Rev. 506 entry added after line {i+1}")
        break

with open(path, 'w') as f:
    f.writelines(lines)

print("File updated successfully")
