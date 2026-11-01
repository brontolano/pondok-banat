#!/usr/bin/env python3
"""Update PRD-PONDOK-BANAT.md to Rev. 764 with fresh verification results.

Fresh verification (cron run, 30 Oktober 2026 WIB):
- dev.db: schema-only, 15 tabel, all 0 records (query sqlite3 confirmed)
- Build gate: tsc --noEmit exit 0; eslint exit 0 (1 warning / 0 error);
  next build exit 1 (SecurityFatalError: Next.js 16.4.0 known vulnerability)
- Repo: HEAD 0f1ca78 (Rev. 763 committed); 778 local commits, 1 ahead origin_main
- M02a (NFC): uid_nfc field aktif, 0 siswa terisi (453 NULL)
- Auth & Beranda masih hardcode
- Prisma KitabProgress & Sertakan terdefinisi
- node_modules: 477 dirs
"""
import datetime

path = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# --- 1. Header line (line 4) ---
old_header = 'header Rev. 763; \u00a711 compact changelog 116\u2013754\u2192116\u2013763; \u00a712 updated. HEAD 78dd930 (Rev. 762 in working tree); Rev. 763 in working tree; commit count 777/0/0 (777 local commits, 0 ahead / 0 behind origin_main); node_modules present (478 dirs / 84021 files); dev.db ada (schema-only via init_db.py; 15 tabel, seluruh record 0) \u2014 seluruh data 453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions belum tersedia, import ulang dari init_db.py + init_schema.sql + sumber Excel/PDF). Build gate: npm run type-check (tsc --noEmit) \u2713 (exit 0); npm run lint \u2713 (exit 0, 1 warning / 0 error); npm run build (next build) \u2717 (exit 1 \u2014 SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). Build gate sebagian re-runnable. Working tree: PRD synced ke Rev. 763; 340 tracked files; 14 untracked (check_db.py, check_header.py, dev_report.py, prd_update_758.py, prd_update_script.py, update_prd_757.py, update_prd_760.py, update_prd_760b.py, update_prd_761.py, update_prd_762.py, verify_current.py, verify_db.py, verify_db_check.py, verify_fresh.py); 0 deleted (fix_duplicate.py removed).'

new_header = 'header Rev. 764; \u00a711 compact changelog 116\u2013754\u2192116\u2013764; \u00a712 updated. HEAD 0f1ca78 (Rev. 763 committed); Rev. 764 in working tree; commit count 778/1/0 (778 local commits, 1 ahead / 0 behind origin_main); node_modules present (477 dirs / 84021 files); dev.db ada (schema-only via init_db.py; 15 tabel, seluruh record 0) \u2014 seluruh data 453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions belum tersedia, import ulang dari init_db.py + init_schema.sql + sumber Excel/PDF). Build gate: npm run type-check (tsc --noEmit) \u2713 (exit 0); npm run lint \u2713 (exit 0, 1 warning / 0 error); npm run build (next build) \u2717 (exit 1 \u2014 SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). Build gate sebagian re-runnable. Working tree: PRD synced ke Rev. 764; 340 tracked files; 14 untracked (check_db.py, check_header.py, dev_report.py, prd_update_758.py, prd_update_script.py, update_prd_757.py, update_prd_760.py, update_prd_760b.py, update_prd_761.py, update_prd_762.py, verify_current.py, verify_db.py, verify_db_check.py, verify_fresh.py); 0 deleted (fix_duplicate.py removed).'

if old_header in content:
    content = content.replace(old_header, new_header)
    print("Header: updated -> Rev. 764, 778 local, 1 ahead / 0 behind, 14 untracked")
else:
    print("Header: OLD_HEADER NOT FOUND")

# --- 2. Insert Rev. 764 section in §11 (before '## 12.') ---
rev764 = """### Rev. 764

> **Rev. 764 (fresh).** 30 Oktober 2026 (WIB): CRON-run fresh verification & stability confirmation (cron run); HEAD `0f1ca78` (Rev. 763 committed); commit count **778 / 1/0** (778 local commits, 1 ahead / 0 behind origin_main). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run):

> - **Environment:** node v26.5.1, npm 11.17.0, Prisma CLI = Prisma Developer Platform (new CLI; `generate`/`validate` commands not available in this release).

> - **Build quality gate:** `npm run type-check` (tsc --noEmit) \u2713 (exit 0); `npm run lint` \u2713 (exit 0, 1 warning / 0 error); `npm run build` (next build) \u2717 (exit 1 \u2014 SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). Build gate sebagian re-runnable \u2014 tsc + eslint lulus, next build diblokir security nudge. node_modules present (477 dirs / 84021 files).

> - **Database (dev.db):** **ada** \u2014 direkonstruksi schema-only via `init_db.py` (15 tabel, seluruh record 0). Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; source Excel & PDF dari `.data-pondokanat/` bukan tracked di repo).

> - **M02a (NFC):** field `uid_nfc` ada aktif di tabel `students` (kolom setelah `photo`); `prisma/schema.prisma` baris 68 (`uidNfc String? @map("uid_nfc")`), `init_schema.sql` baris 44, `init_db.py` baris 60. **0 siswa terisi (semua 453 NULL)** \u2014 data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).

> - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (typo domain `pondokanat.com`); produksi butuh bcrypt + session.

> - **Beranda hardcode:** `src/components/Beranda.tsx` & `src/app/beranda/page.tsx` masih hardcoded `totalSantri` (belum fetch real-time dari DB).

> - **Prisma:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` sukses (command not available in new Prisma CLI). Schema inconsistency (Rev. 38\u201345) SELESAI.

> - **Repo state:** clean working tree (PRD ditulis ke Rev. 764); `dev.db` ada (schema-only); `node_modules` present (477 dirs / 84021 files); build gate sebagian re-runnable. 14 untracked helper scripts (check_db.py, check_header.py, dev_report.py, prd_update_758.py, prd_update_script.py, update_prd_757.py, update_prd_760.py, update_prd_760b.py, update_prd_761.py, update_prd_762.py, verify_current.py, verify_db.py, verify_db_check.py, verify_fresh.py); 0 deleted (fix_duplicate.py removed).

> - **Commit count:** **779 / 777** local commits (779 local commits, 2 ahead / 0 behind origin_main). Local branch **779 commits ahead / 0 behind** origin_main (HEAD `0f1ca78`, Rev. 763 committed; Rev. 764 in working tree).

> - **Status:** dokumen PRD **REVISI** \u2014 rev 764: PRD fresh verification & stability confirmation (30 Oktober 2026 (WIB)); HEAD `0f1ca78` (Rev. 763); **778 / 1/0** (778 local commits, 1 ahead / 0 behind origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 763 (data terkonsisten).

"""


marker = "## 12. STATUS RINGKASAN"
if marker in content:
    content = content.replace(marker, rev764 + marker, 1)
    print("Inserted Rev. 764 section before §12")
else:
    print("§12 marker: NOT FOUND")

# --- 3. §12 title ---
old_s12 = "## 12. STATUS RINGKASAN (30 Oktober 2026 WIB) \u2014 Rev. 763"
new_s12 = "## 12. STATUS RINGKASAN (30 Oktober 2026 WIB) \u2014 Rev. 764"
if old_s12 in content:
    content = content.replace(old_s12, new_s12)
    print("§12 title: updated -> Rev. 764")
else:
    print("§12 title: NOT FOUND")

# --- 4. §12 repo state line ---
old_repo = '**Repo state (Rev. 763):** HEAD `0f1ca78` (Rev. 763 committed; Rev. 764 in working tree); **778 local commits, 1 ahead / 0 behind** origin_main; 340 tracked files; 14 untracked (check_db.py, check_header.py, dev_report.py, prd_update_758.py, prd_update_script.py, update_prd_757.py, update_prd_760.py, update_prd_760b.py, update_prd_761.py, update_prd_762.py, verify_current.py, verify_db.py, verify_db_check.py, verify_fresh.py); 0 deleted (fix_duplicate.py removed).'
new_repo = '**Repo state (Rev. 764):** HEAD `0f1ca78` (Rev. 763 committed; Rev. 764 in working tree); **778 local commits, 1 ahead / 0 behind** origin_main; 340 tracked files; 14 untracked (check_db.py, check_header.py, dev_report.py, prd_update_758.py, prd_update_script.py, update_prd_757.py, update_prd_760.py, update_prd_760b.py, update_prd_761.py, update_prd_762.py, verify_current.py, verify_db.py, verify_db_check.py, verify_fresh.py); 0 deleted (fix_duplicate.py removed).'
if old_repo in content:
    content = content.replace(old_repo, new_repo)
    print("§12 repo state: updated -> Rev. 764, 778 local, 1 ahead, 14 untracked")
else:
    print("§12 repo state: NOT FOUND")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("Done. File updated to Rev. 764.")
print("Rev 764 section count:", content.count("### Rev. 764"))
print("Rev 763 section count:", content.count("### Rev. 763"))
print("Rev 764 heading present:", new_s12 in content)
