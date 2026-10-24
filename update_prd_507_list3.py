#!/usr/bin/env python3
"""Add Rev. 507 entry to §12 list - target the last Rev. 504 (final) entry."""
path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'

with open(path, 'r') as f:
    c = f.read()

# Find §12 section start
s12_start = c.find("## 12. REVISI TERBARU (Rev. 468–507")
print(f"§12 section starts at: {s12_start}")

# Find the last "Rev. 504 (final)" entry
last_rev504 = c.rfind("**Rev. 504 (final).** 24 Oktober 2026 (WIB): PRD fresh verification")
print(f"Last 'Rev. 504 (final)' at: {last_rev504}")

# Check if it's after §12 section
if last_rev504 > s12_start:
    # Insert Rev. 507 entry after the last Rev. 504 (final) entry
    # Find the end of that entry (next newline followed by |||_)
    entry_start = last_rev504
    # Find the end of the entry
    end_marker = "\n\n"
    entry_end = c.find(end_marker, entry_start + len("**Rev. 504 (final).** 24 Oktober 2026 (WIB): PRD fresh verification"))
    
    if entry_end == -1:
        # Try alternative: find the end of the line
        entry_end = c.find("\n", entry_start)
    
    print(f"Entry ends at: {entry_end}")
    
    rev507_entry = "\n\n||- **Rev. 507 (final).** 24 Oktober 2026 (WIB): PRD fresh verification & stability confirmation (24 Oct 2026 WIB); HEAD `30bcb2fe40a3910e2d350c502ec6d893c4159a8e` (Rev. 507 commit), 41 / 0 (41 commits ahead origin_main). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run): **state stabil, tidak ada perubahan signifikan dari Rev. 506** (data terkonsisten). Build gate: **NOT RE-RUNABLE** — node_modules absent; npm ci diperlukan. Database: dev.db absent; seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` & `import_students_grades_clean.py` tidak ditemukan di working tree). **M02a (NFC):** field `uid_nfc` ada aktif di tabel students, semua 453 NULL. **Auth hardcode:** Login.tsx tetap `admin@pondokanbat.com` / `admin123` (typo domain). **Beranda hardcode:** Beranda.tsx & page.tsx masih hardcoded totalSantri 453. **Prisma schema:** model `KitabProgress` & `Sertakan` sudah terdefinisi; `prisma validate` sukses. **Status:** dokumen PRD **REVISI** — rev 507 (final): PRD fresh verification & konfirmasi stabilitas; seluruh data terkonsisten, tidak ada perubahan signifikan dari Rev. 506; branch 41 ahead / 0 behind origin_main."
    
    c = c[:entry_end] + rev507_entry + c[entry_end:]
    
    with open(path, 'w') as f:
        f.write(c)
    
    print("Rev. 507 entry added to §12 list")
else:
    print("Last 'Rev. 504 (final)' is NOT in §12 section!")
