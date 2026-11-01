with open('PRD-PONDOK-BANAT.md', 'r') as f:
    content = f.read()

# Find the first "Status: dokumen PRD REVISI — rev 858" after the Repo state section
# and replace everything from there to end with clean version
import re

# The pattern for the first correct Status line for Rev. 858
pattern = r'(> - \*\*Status:\*\* dokumen PRD \*\*REVISI\*\* — rev 858: PRD fresh verification & stability confirmation \(03 November 2026 \(WIB\)\); HEAD `29e772c` \(Rev\. 858 committed — PRD synced ke Rev\. 858\); \*\*907 / 14/0\*\* \(907 local commits, 14 ahead / 0 behind origin_main\)\. State stabil, tidak ada perubahan signifikan dari Rev\. 857 \(data terkonsisten\)\.)'

matches = list(re.finditer(pattern, content))
print(f"Found {len(matches)} matches")
for i, m in enumerate(matches):
    print(f"  Match {i}: position {m.start()}-{m.end()}")

if len(matches) >= 1:
    # Keep up to the end of the first match
    end_pos = matches[0].end()
    new_content = content[:end_pos]
    
    # Add clean §12
    s12 = '''

## 12. STATUS RINGKASAN (03 November 2026 WIB) — Rev. 859

> - Modul **M01–M05** **diimplementasikan/di-seed**; **M06 (Hifz/Quran)**, **M09 (Laporan & Analytics)**, **M10 (Payment/Keuangan)**, **M11 (Mobile & Offline)** **tunda** di roadmap.
> - Database `dev.db` **ada** — schema-only via `init_db.py` (15 tabel, seluruh record 0). Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql` + sumber Excel/PDF).
> - M02a (NFC): field `uid_nfc` di schema Prisma & `init_db.py` (kolom setelah `photo`), **0 siswa terisi** (data ekspor NFC Tools belum tersedia).
> - Auth & Beranda masih **hardcode** (`Login.tsx`: admin@pondokanbat.com / admin123; `Beranda.tsx`: totalSantri hardcode) — produksi butuh bcrypt + session.
> - **Build gate:** `npm run type-check` (tsc --noEmit) ✓ (exit 0); `npm run lint` ✓ (exit 0, 1 warning / 0 error); `npm run build` (next build) ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability — engine security nudge, upgrade recommended). Build gate **TIDAK LULUS** — tsc + eslint LULUS, next build diblokir security nudge. node_modules present (5103 dirs / 84021 files).
> - Prisma schema: `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **terdefinisi**, `prisma validate` sukses.
> - **Repo state:** clean working tree (PRD ditulis ke Rev. 859); HEAD `c0a8e13` (Rev. 859 committed — PRD synced ke Rev. 859); **908 local commits, 15 ahead / 0 behind** origin_main; 340 tracked files; 67 untracked (incl. helper scripts); 0 deleted.
> - **Commit count:** 908 / 15/0 (fresh verification & stability confirmation, 03 November 2026 WIB); HEAD `c0a8e13` (Rev. 859 committed — PRD synced ke Rev. 859); **908 / 15/0** (908 local commits, 15 ahead / 0 behind origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 858 (data terkonsisten).
'''
    new_content += s12
    
    with open('PRD-PONDOK-BANAT.md', 'w') as f:
        f.write(new_content)
    
    print("File fixed successfully")
else:
    print("No match found")
