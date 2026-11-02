with open('PRD-PONDOK-BANAT.md', 'r') as f:
    content = f.read()

# Remove the old §12 for Rev. 865 (duplicated)
old_s12_dup = '''> - Modul **M01–M05** **diimplementasikan/di-seed**; **M06 (Hifz/Quran)**, **M09 (Laporan & Analytics)**, **M10 (Payment/Keuangan)**, **M11 (Mobile & Offline)** **tunda** di roadmap.
> - Database `dev.db` **ada** — schema-only via `init_db.py` (15 tabel, seluruh record 0). Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql` + sumber Excel/PDF).
> - M02a (NFC): field `uid_nfc` di schema Prisma & `init_db.py` (kolom setelah `photo`), **0 siswa terisi** (data ekspor NFC Tools belum tersedia).
> - Auth & Beranda masih **hardcode** (`Login.tsx`: admin@pondokanbat.com / admin123; `Beranda.tsx`: totalSantri hardcode) — produksi butuh bcrypt + session.
> - **Build gate:** `npm run type-check` (tsc --noEmit) ✓ (exit 0); `npm run lint` ✓ (exit 0, 1 warning / 0 error); `npm run build` (next build) ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability — engine security nudge, upgrade recommended). Build gate **TIDAK LULUS** — tsc + eslint LULUS, next build diblokir security nudge. node_modules present (479 dirs / 84021 files).
> - Prisma schema: `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **terdefinisi**, `prisma validate` sukses.
> - **Repo state:** clean working tree (PRD ditulis ke Rev. 865); HEAD `60f2c9e` (Rev. 865 final sync — PRD synced ke Rev. 865); **923 local commits, 11 ahead / 0 behind** origin_main; 412 tracked files; 1 untracked (incl. helper scripts); 0 deleted.
> - **Commit count:** 922 / 10/0 (fresh verification & stability confirmation, 01 November 2026 WIB); HEAD `60f2c9e` (Rev. 865 final sync — PRD synced ke Rev. 865); **923 / 11/0** (923 local commits, 11 ahead / 0 behind origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 864 (data terkonsisten).

### Rev. 866'''

new_s12_dup = '''### Rev. 866'''

if old_s12_dup in content:
    content = content.replace(old_s12_dup, new_s12_dup)
    print("Removed duplicate §12 for Rev. 865")
else:
    print("Duplicate §12 pattern not found")

# Also fix the header in §12 - it shows 01 November but should be 02 November
content = content.replace('## 12. STATUS RINGKASAN (01 November 2026 WIB) — Rev. 866', '## 12. STATUS RINGKASAN (02 November 2026 WIB) — Rev. 866')

# Fix the §12 that still has old HEAD/commit count
old_s12_repo = '''HEAD `affd66e` (Rev. 866 final sync — PRD synced ke Rev. 866); **924 local commits, 12 ahead / 0 behind** origin_main'''
new_s12_repo = '''HEAD `99d1fb2` (Rev. 866 final sync — PRD synced ke Rev. 866); **925 local commits, 13 ahead / 0 behind** origin_main'''
content = content.replace(old_s12_repo, new_s12_repo)

old_s12_count = '''923 / 12/0 (fresh verification & stability confirmation, 02 November 2026 WIB); HEAD `affd66e` (Rev. 866 final sync — PRD synced ke Rev. 866); **924 / 12/0**'''
new_s12_count = '''925 / 13/0 (fresh verification & stability confirmation, 02 November 2026 WIB); HEAD `99d1fb2` (Rev. 866 final sync — PRD synced ke Rev. 866); **925 / 13/0**'''
content = content.replace(old_s12_count, new_s12_count)

with open('PRD-PONDOK-BANAT.md', 'w') as f:
    f.write(content)

print("Done")
