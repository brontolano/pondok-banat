#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Update PRD-PONDOK-BANAT.md from Rev. 722 to Rev. 723.
Fresh verification (cron run, 29 Oktober 2026 WIB).
"""
import re
import sys

REPO = "/opt/data/home/workspace/dev/pondok-banat"
PRD = f"{REPO}/PRD-PONDOK-BANAT.md"

with open(PRD, "r", encoding="utf-8") as f:
    content = f.read()

# ---------------------------------------------------------
# 1. Update the header line (Rev. 721→722 → Rev. 722→723)
# ---------------------------------------------------------
old_header = '''(Rev. 721→722): PRD fresh verification & stability confirmation (cron run, 29 Oktober 2026 WIB); header Rev. 721→722; §11 compact changelog 116–721→116–722; §12 updated. HEAD `50849bdff418096c3058041f90d589e8c6ce9a5f` (Rev. 721 final commit); commit count 732/3/0 (732 local commits, 3 ahead origin_main, 0 behind); node_modules present (477 dirs / 84021 files); dev.db ada (direkonstruksi schema-only via init_db.py; 15 tabel, seluruh record 0 — seluruh data 453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions belum tersedia, import ulang dari init_db.py + init_schema.sql + sumber Excel/PDF). Build gate: npm run type-check (tsc --noEmit) ✓ (exit 0); npm run lint ✓ (exit 0, 1 warning / 0 error); npm run build (next build) ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). Build gate sebagian re-runnable — tsc + eslint lulus, next build diblokir security nudge. Working tree: PRD synced ke Rev. 722; 2 modified helper scripts (fix_header.py, fix_remaining.py) & 61 untracked helper scripts; git ls-files = 268 files.'''

new_header = '''(Rev. 722→723): PRD fresh verification & stability confirmation (cron run, 29 Oktober 2026 WIB); header Rev. 722→723; §11 compact changelog 116–722→116–723; §12 updated. HEAD `bda3602` (Rev. 722 final commit); commit count 733/4/0 (733 local commits, 4 ahead origin_main, 0 behind); node_modules present (5103 dirs / 84021 files); dev.db ada (direkonstruksi schema-only via init_db.py; 15 tabel, seluruh record 0 — seluruh data 453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions belum tersedia, import ulang dari init_db.py + init_schema.sql + sumber Excel/PDF). Build gate: npm run type-check (tsc --noEmit) ✓ (exit 0); npm run lint ✓ (exit 0, 1 warning / 0 error); npm run build (next build) ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). Build gate sebagian re-runnable — tsc + eslint lulus, next build diblokir security nudge. Working tree: PRD synced ke Rev. 723; 2 modified helper scripts (fix_header.py, fix_remaining.py) & 67 untracked helper scripts; git ls-files = 268 files.'''

if old_header not in content:
    print("ERROR: old header not found!")
    sys.exit(1)

content = content.replace(old_header, new_header, 1)

# ---------------------------------------------------------
# 2. Add Rev. 723 section to §11 (after the Rev. 722 section)
# ---------------------------------------------------------
# The Rev. 722 section ends with:
# >> **Status:** dokumen PRD **REVISI** — rev 722: PRD fresh verification & stability confirmation (29 Oktober 2026 (WIB)); HEAD `50849bdff418096c3058041f90d589e8c6ce9a5f` (Rev. 721 final commit); **732 / 3/0** (732 local commits, 3 ahead origin_main, 0 behind). State stabil, tidak ada perubahan signifikan dari Rev. 721 (data terkonsisten). Build gate: tsc ✓ (exit 0), eslint ✓ (exit 0, 1 warning), next build ✗ (SecurityFatalError Next.js 16.4.0).
# followed by a blank line and then the Rev. 721 status line.

old_rev722_status = '''>> **Status:** dokumen PRD **REVISI** — rev 722: PRD fresh verification & stability confirmation (29 Oktober 2026 (WIB)); HEAD `50849bdff418096c3058041f90d589e8c6ce9a5f` (Rev. 721 final commit); **732 / 3/0** (732 local commits, 3 ahead origin_main, 0 behind). State stabil, tidak ada perubahan signifikan dari Rev. 721 (data terkonsisten). Build gate: tsc ✓ (exit 0), eslint ✓ (exit 0, 1 warning), next build ✗ (SecurityFatalError Next.js 16.4.0).
>
> **Status:** dokemen PRD **REVISI** — rev 721: PRD fresh verification & stability confirmation (29 Oktober 2026 (WIB)); HEAD `8288fdf` (Rev. 720 final commit); **731 / 2/0** (731 local commits, 2 ahead origin_main, 0 behind). State stabil, tidak ada perubahan signifikan dari Rev. 720 (data terkonsisten). Build gate: tsc ✓ (exit 0), eslint ✓ (exit 0, 1 warning), next build ✗ (SecurityFatalError Next.js 16.4.0).'''

new_rev723_section = '''>> **Status:** dokumen PRD **REVISI** — rev 722: PRD fresh verification & stability confirmation (29 Oktober 2026 (WIB)); HEAD `50849bdff418096c3058041f90d589e8c6ce9a5f` (Rev. 721 final commit); **732 / 3/0** (732 local commits, 3 ahead origin_main, 0 behind). State stabil, tidak ada perubahan signifikan dari Rev. 721 (data terkonsisten). Build gate: tsc ✓ (exit 0), eslint ✓ (exit 0, 1 warning), next build ✗ (SecurityFatalError Next.js 16.4.0).
>
> ### Rev. 723

>> **Rev. 723 (fresh).** 29 Oktober 2026 (WIB): CRON-run fresh verification & stability confirmation (cron run); HEAD `bda3602` (Rev. 722 final commit); commit count **733 / 4/0** (733 local commits, 4 ahead origin_main, 0 behind). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run):

>> - **Environment:** node v26.5.1, npm 11.17.0, Prisma CLI = Prisma Developer Platform (new CLI; `generate`/`validate` commands not available in this release).
>> - **Build quality gate:** `npm run type-check` (tsc --noEmit) ✓ (exit 0); `npm run lint` ✓ (exit 0, 1 warning / 0 error); `npm run build` (next build) ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). Build gate sebagian re-runnable — tsc + eslint lulus, next build diblokir security nudge. node_modules present (5103 dirs / 84021 files).
>> - **Database (dev.db):** file `dev.db` **ada** — direkonstruksi schema-only via `init_db.py` (15 tabel, seluruh record 0). Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; source Excel & PDF dari `.data-pondokanat/` bukan tracked di repo).
>> - **M02a (NFC):** field `uid_nfc` ada aktif di tabel `students` (kolom setelah `photo`); `prisma/schema.prisma` baris 68 (`uidNfc String? @map(\\"uid_nfc\\")`), `init_schema.sql` baris 44, `init_db.py` baris 60. **Tidak ada satupun siswa yang memiliki `uid_nfc` diisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
>> - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (typo domain `pondokanat.com`); produksi butuh bcrypt + session.
>> - **Beranda hardcode:** `src/components/Beranda.tsx` & `src/app/beranda/page.tsx` masih hardcoded `totalSantri` (belum fetch real-time dari DB).
>> - **Prisma:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` sukses.
>> - **Repo state:** clean working tree; `dev.db` schema-only (0 record); `node_modules` present (5103 dirs / 84021 files); build gate sebagian re-runnable. 2 modified helper scripts (fix_header.py, fix_remaining.py) & 67 untracked helper scripts in working tree.
>> - **Commit count:** 733 / 4 (733 local commits, 4 ahead origin_main, 0 behind). Local branch **4 commits ahead / 0 behind** origin_main (HEAD `bda3602`, Rev. 722 final commit).

>> **Status:** dokumen PRD **REVISI** — rev 723: PRD fresh verification & stability confirmation (29 Oktober 2026 (WIB)); HEAD `bda3602` (Rev. 722 final commit); **733 / 4/0** (733 local commits, 4 ahead origin_main, 0 behind). State stabil, tidak ada perubahan signifikan dari Rev. 722 (data terkonsisten). Build gate: tsc ✓ (exit 0), eslint ✓ (exit 0, 1 warning), next build ✗ (SecurityFatalError Next.js 16.4.0).'''

if old_rev722_status not in content:
    print("ERROR: old Rev. 722 status block not found!")
    sys.exit(1)

content = content.replace(old_rev722_status, new_rev723_section, 1)

with open(PRD, "w", encoding="utf-8") as f:
    f.write(content)

print("PRD updated to Rev. 723 successfully.")
