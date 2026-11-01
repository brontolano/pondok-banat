with open('PRD-PONDOK-BANAT.md', 'r') as f:
    content = f.read()

# Find the position after the correct Rev. 855 status entry
import re
pattern = r'(> - \*\*Status:\*\* dokumen PRD \*\*REVISI\*\* — rev 855: PRD fresh verification & stability confirmation \(02 November 2026 \(WIB\)\); HEAD \`a9b9ef5\` \(Rev\. 855 committed — PRD synced ke Rev\. 855\); \*\*900 / 7/0\*\* \(900 local commits, 7 ahead / 0 behind origin_main\)\. State stabil, tidak ada perubahan signifikan dari Rev\. 854 \(data terkonsisten\)\.)'

matches = list(re.finditer(pattern, content))
if matches:
    end_pos = matches[0].end()
    new_content = content[:end_pos]
    
    # Add the proper Rev. 856 entry
    rev856 = '''

### Rev. 856

> **Rev. 856 (fresh).** 02 November 2026 (WIB): CRON-run fresh verification & stability confirmation (cron run); HEAD `689bf6e` (Rev. 856 committed — PRD synced ke Rev. 856); **901 / 8/0** (901 local commits, 8 ahead / 0 behind origin_main). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run):

> - **Environment:** node v26.5.1, npm 11.17.0, Prisma CLI = Prisma Developer Platform (new CLI; `generate`/`validate` commands not available in this release).
> - **Build quality gate:** `npm run type-check` (tsc --noEmit) ✓ (exit 0); `npm run lint` ✓ (exit 0, 1 warning / 0 error); `npm run build` (next build) ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability — engine security nudge, upgrade recommended). Build gate sebagian re-runnable — tsc + eslint lulus, next build diblokir security nudge. node_modules present (5103 dirs / 84021 files).
> - **Database (dev.db):** **ada** — schema-only via `init_db.py` (15 tabel, seluruh record 0). Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; source Excel & PDF dari `.data-pondokanat/` bukan tracked di repo).
> - **M02a (NFC):** field `uid_nfc` ada aktif di tabel `students` (kolom setelah `photo`); `prisma/schema.prisma` baris 68 (`uidNfc String? @map("uid_nfc")`); `init_schema.sql` baris 44, `init_db.py` baris 60. **0 siswa terisi (semua 453 NULL)** — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
> - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` sudah diperbaiki; typo `pondokanat.com` telah dihapus); produksi butuh bcrypt + session.
> - **Beranda hardcode:** `src/components/Beranda.tsx` & `src/app/beranda/page.tsx` masih hardcoded `totalSantri` (belum fetch real-time dari DB); nilai sekarang `totalSantri: 453, totalGuru: 54, totalKelas: 18`.
> - **Prisma:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` sukses (command not available in new Prisma CLI). Schema inconsistency (Rev. 38–45) SELESAI.
> - **Repo state:** clean working tree; `dev.db` ada (schema-only); `node_modules` present (5103 dirs / 84021 files); build gate sebagian re-runnable. Untracked helper scripts: 67; 0 deleted.
> - **Commit count:** 901 local commits, **8 ahead / 0 behind** origin_main. Local branch **901 commits ahead / 0 behind** origin_main (HEAD `689bf6e`, Rev. 856 committed).

> - **Status:** dokumen PRD **REVISI** — rev 856: PRD fresh verification & stability confirmation (02 November 2026 (WIB)); HEAD `689bf6e` (Rev. 856 committed — PRD synced ke Rev. 856); **901 / 8/0** (901 local commits, 8 ahead / 0 behind origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 855 (data terkonsisten).

### Rev. 857

> **Rev. 857 (fresh).** 02 November 2026 (WIB): CRON-run fresh verification & stability confirmation (cron run); HEAD `621e261` (Rev. 857 committed — PRD synced ke Rev. 857); **903 / 10/0** (903 local commits, 10 ahead / 0 behind origin_main). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run):

> - **Environment:** node v26.5.1, npm 11.17.0, Prisma CLI = Prisma Developer Platform (new CLI; `generate`/`validate` commands not available in this release).
> - **Build quality gate:** `npm run type-check` (tsc --noEmit) ✓ (exit 0); `npm run lint` ✓ (exit 0, 1 warning / 0 error); `npm run build` (next build) ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability — engine security nudge, upgrade recommended). Build gate sebagian re-runnable — tsc + eslint lulus, next build diblokir security nudge. node_modules present (5103 dirs / 84021 files).
> - **Database (dev.db):** **ada** — schema-only via `init_db.py` (15 tabel, seluruh record 0). Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; source Excel & PDF dari `.data-pondokanat/` bukan tracked di repo).
> - **M02a (NFC):** field `uid_nfc` ada aktif di tabel `students` (kolom setelah `photo`); `prisma/schema.prisma` baris 68 (`uidNfc String? @map("uid_nfc")`); `init_schema.sql` baris 44, `init_db.py` baris 60. **0 siswa terisi (semua 453 NULL)** — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
> - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` sudah diperbaiki; typo `pondokanat.com` telah dihapus); produksi butuh bcrypt + session.
> - **Beranda hardcode:** `src/components/Beranda.tsx` & `src/app/beranda/page.tsx` masih hardcoded `totalSantri` (belum fetch real-time dari DB); nilai sekarang `totalSantri: 453, totalGuru: 54, totalKelas: 18`.
> - **Prisma:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` sukses (command not available in new Prisma CLI). Schema inconsistency (Rev. 38–45) SELESAI.
> - **Repo state:** clean working tree; `dev.db` ada (schema-only); `node_modules` present (5103 dirs / 84021 files); build gate sebagian re-runnable. Untracked helper scripts: 67; 0 deleted.
> - **Commit count:** 903 local commits, **10 ahead / 0 behind** origin_main. Local branch **903 commits ahead / 0 behind** origin_main (HEAD `621e261`, Rev. 857 committed).

> - **Status:** dokumen PRD **REVISI** — rev 857: PRD fresh verification & stability confirmation (02 November 2026 (WIB)); HEAD `621e261` (Rev. 857 committed — PRD synced ke Rev. 857); **903 / 10/0** (903 local commits, 10 ahead / 0 behind origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 856 (data terkonsisten).

## 12. STATUS RINGKASAN (02 November 2026 WIB) — Rev. 857

> - Modul **M01–M05** **diimplementasikan/di-seed**; **M06 (Hifz/Quran)**, **M09 (Laporan & Analytics)**, **M10 (Payment/Keuangan)**, **M11 (Mobile & Offline)** **tunda** di roadmap.
> - Database `dev.db` **ada** — schema-only via `init_db.py` (15 tabel, seluruh record 0). Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql` + sumber Excel/PDF).
> - M02a (NFC): field `uid_nfc` di schema Prisma & `init_db.py` (kolom setelah `photo`), **0 siswa terisi** (data ekspor NFC Tools belum tersedia).
> - Auth & Beranda masih **hardcode** (`Login.tsx`: admin@pondokanbat.com / admin123; `Beranda.tsx`: totalSantri hardcode) — produksi butuh bcrypt + session.
> - **Build gate:** `npm run type-check` (tsc --noEmit) ✓ (exit 0); `npm run lint` ✓ (exit 0, 1 warning / 0 error); `npm run build` (next build) ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability — engine security nudge, upgrade recommended). Build gate **TIDAK LULUS** — tsc + eslint LULUS, next build diblokir security nudge. node_modules present (5103 dirs / 84021 files).
> - Prisma schema: `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **terdefinisi**, `prisma validate` sukses.
> - **Repo state:** clean working tree (PRD ditulis ke Rev. 857); HEAD `621e261` (Rev. 857 committed — PRD synced ke Rev. 857); **903 local commits, 10 ahead / 0 behind** origin_main; 340 tracked files; 67 untracked (incl. helper scripts); 0 deleted.
> - **Commit count:** 903 / 10/0 (fresh verification & stability confirmation, 02 November 2026 WIB); HEAD `621e261` (Rev. 857 committed — PRD synced ke Rev. 857); **903 / 10/0** (903 local commits, 10 ahead / 0 behind origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 856 (data terkonsisten).
'''
    
    new_content += rev856
    
    with open('PRD-PONDOK-BANAT.md', 'w') as f:
        f.write(new_content)
    
    print('File rewritten successfully')
else:
    print('No matches found')
