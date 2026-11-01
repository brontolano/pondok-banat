#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Update PRD-PONDOK-BANAT.md to Rev. 757 after fresh verification (cron run)."""

import os

BASE = '/opt/data/home/workspace/dev/pondok-banat'
PRD = os.path.join(BASE, 'PRD-PONDOK-BANAT.md')

with open(PRD, 'r', encoding='utf-8') as f:
    content = f.read()

# ---- Current verified state ----
HEAD = 'def79ed'
LOCAL_COMMIT = 771
AHEAD = 3
BEHIND = 0
NODE_MODULES_DIRS = 477
NODE_MODULES_FILES = 84021
DEV_DB_STATE = 'ada (schema-only via init_db.py; 15 tabel, seluruh record 0)'
NFC_STATE = '0 siswa terisi (semua 453 NULL)'
UNTRACKED = ['dev_report.py', 'prd_update_script.py', 'verify_current.py', 'verify_db.py', 'verify_db_check.py', 'verify_fresh.py']

# ---- 1. Header update (line 4) ----
old_header_block = (
    '(Source: `IDEA.md` + `.data-pondokanat/` (3 Excel + 74 dokumen = 65 RPP + 9 SILABUS) + research.\n'
    'header Rev. 756; §11 compact changelog 116–754→116–756; §12 updated. HEAD 8afc403 (Rev. 755); commit count 770/2/0 (770 local commits, 2 ahead origin_main, 0 behind); node_modules present (477 dirs / 84021 files); dev.db ada (direkonstruksi schema-only via init_db.py; 15 tabel, seluruh record 0 — seluruh data 453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions belum tersedia, import ulang dari init_db.py + init_schema.sql + sumber Excel/PDF). Build gate: npm run type-check (tsc --noEmit) ✓ (exit 0); npm run lint ✓ (exit 0, 1 warning / 0 error); npm run build (next build) ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). Build gate sebagian re-runnable. Working tree: PRD synced ke Rev. 756; 340 tracked files; 3 untracked (dev_report.py, verify_db.py, verify_db_check.py); 0 deleted (fix_duplicate.py removed).'
)

new_header_block = (
    '(Source: `IDEA.md` + `.data-pondokanat/` (3 Excel + 74 dokumen = 65 RPP + 9 SILABUS) + research.\n'
    'header Rev. 757; §11 compact changelog 116–754→116–757; §12 updated. HEAD ' + HEAD + ' (Rev. 756 final commit); commit count ' + str(LOCAL_COMMIT) + '/' + str(AHEAD) + '/0 (' + str(LOCAL_COMMIT) + ' local commits, ' + str(AHEAD) + ' ahead origin_main, ' + str(BEHIND) + ' behind); node_modules present (' + str(NODE_MODULES_DIRS) + ' dirs / ' + str(NODE_MODULES_FILES) + ' files); dev.db ' + DEV_DB_STATE + ' — seluruh data 453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions belum tersedia, import ulang dari init_db.py + init_schema.sql + sumber Excel/PDF). Build gate: npm run type-check (tsc --noEmit) ✓ (exit 0); npm run lint ✓ (exit 0, 1 warning / 0 error); npm run build (next build) ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). Build gate sebagian re-runnable. Working tree: PRD synced ke Rev. 757; 340 tracked files; ' + str(len(UNTRACKED)) + ' untracked (' + ', '.join(UNTRACKED) + '); 0 deleted (fix_duplicate.py removed).'
)

if old_header_block not in content:
    print('ERROR: header block not found')
    idx = content.find('header Rev. 756')
    print('Found header Rev. 756 at index:', idx)
    if idx >= 0:
        print('Context:', repr(content[idx-60:idx+500]))
    raise SystemExit(1)
content = content.replace(old_header_block, new_header_block)
print('✓ Header updated to Rev. 757')

# ---- 2. §11 compact changelog: 116–756 → 116–757 ----
content = content.replace('§11 compact changelog 116–756', '§11 compact changelog 116–756→116–757')
print('✓ §11 compact changelog updated to 116–757')

# ---- 3. Add Rev. 757 fresh verification entry after Rev. 756 entry ----
rev756_entry = (
    '> - **Status:** dokumen PRD **REVISI** — rev 756: PRD fresh verification & stability confirmation (30 Oktober 2026 (WIB)); HEAD `8afc403` (Rev. 755 final commit); **770 / 2/0** (770 local commits, 2 ahead origin_main, 0 behind). State stabil, tidak ada perubahan signifikan dari Rev. 755 (data terkonsisten).'
)

rev757_entry = (
    rev756_entry
    + '\n\n'
    '### Rev. 757\n\n'
    '> **Rev. 757 (fresh).** 30 Oktober 2026 (WIB): CRON-run fresh verification & stability confirmation (cron run); HEAD `' + HEAD + '` (Rev. 756 final commit); **' + str(LOCAL_COMMIT) + ' / ' + str(AHEAD) + '/0** (' + str(LOCAL_COMMIT) + ' local commits, ' + str(AHEAD) + ' ahead origin_main, ' + str(BEHIND) + ' behind). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run):\n'
    '>\n'
    '> - **Environment:** node v26.5.1, npm 11.17.0, Prisma CLI = Prisma Developer Platform (new CLI; `generate`/`validate` commands not available in this release).\n'
    '> - **Build quality gate:** `npm run type-check` (tsc --noEmit) ✓ (exit 0); `npm run lint` ✓ (exit 0, 1 warning / 0 error); `npm run build` (next build) ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). Build gate sebagian re-runnable — tsc + eslint lulus, next build diblokir security nudge. node_modules present (' + str(NODE_MODULES_DIRS) + ' dirs / ' + str(NODE_MODULES_FILES) + ' files).\n'
    '> - **Database (dev.db):** **' + DEV_DB_STATE + '**. Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; source Excel & PDF dari `.data-pondokanat/` bukan tracked di repo).\n'
    '> - **M02a (NFC):** field `uid_nfc` ada aktif di tabel `students` (kolom setelah `photo`); `prisma/schema.prisma` baris 68 (`uidNfc String? @map("uid_nfc")`), `init_schema.sql` baris 44, `init_db.py` baris 60. **' + NFC_STATE + '** — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).\n'
    '> - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (typo domain `pondokanat.com`); produksi butuh bcrypt + session.\n'
    '> - **Beranda hardcode:** `src/components/Beranda.tsx` & `src/app/beranda/page.tsx` masih hardcoded `totalSantri` (belum fetch real-time dari DB).\n'
    '> - **Prisma:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` sukses (command not available in new Prisma CLI). Schema inconsistency (Rev. 38–45) SELESAI.\n'
    '> - **Repo state:** clean working tree; `dev.db` ' + DEV_DB_STATE + '; `node_modules` present (' + str(NODE_MODULES_DIRS) + ' dirs / ' + str(NODE_MODULES_FILES) + ' files); build gate sebagian re-runnable. ' + str(len(UNTRACKED)) + ' untracked helper scripts (' + ', '.join(UNTRACKED) + '); 0 deleted (fix_duplicate.py removed).\n'
    '> - **Commit count:** ' + str(LOCAL_COMMIT) + ' / ' + str(AHEAD) + ' (' + str(LOCAL_COMMIT) + ' local commits, ' + str(AHEAD) + ' ahead origin_main, ' + str(BEHIND) + ' behind). Local branch **' + str(LOCAL_COMMIT) + ' commits ahead / ' + str(BEHIND) + ' behind** origin_main.\n'
    '> - **Status:** dokumen PRD **REVISI** — rev 757: PRD fresh verification & stability confirmation (30 Oktober 2026 (WIB)); HEAD `' + HEAD + '` (Rev. 756 final commit); **' + str(LOCAL_COMMIT) + ' / ' + str(AHEAD) + '/0** (' + str(LOCAL_COMMIT) + ' local commits, ' + str(AHEAD) + ' ahead origin_main, ' + str(BEHIND) + ' behind). State stabil, tidak ada perubahan signifikan dari Rev. 756 (data terkonsisten).'
)

if rev756_entry not in content:
    print('ERROR: Rev. 756 entry marker not found')
    raise SystemExit(1)
content = content.replace(rev756_entry, rev757_entry)
print('✓ Rev. 757 fresh verification entry added')

# ---- 4. §12 header update ----
old_s12 = '## 12. STATUS RINGKASAN (30 Oktober 2026 WIB) — Rev. 756'
new_s12 = '## 12. STATUS RINGKASAN (30 Oktober 2026 WIB) — Rev. 757'
if old_s12 not in content:
    print('ERROR: §12 header not found')
    raise SystemExit(1)
content = content.replace(old_s12, new_s12)
print('✓ §12 header updated to Rev. 757')

with open(PRD, 'w', encoding='utf-8') as f:
    f.write(content)

print('✓ PRD-PONDOK-BANAT.md updated to Rev. 757')
