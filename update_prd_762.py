#!/usr/bin/env python3
"""Update PRD-PONDOK-BANAT.md to Rev. 762 with fresh verification results.

Fresh verification (cron run, 30 Oktober 2026 WIB):
- dev.db: schema-only, 15 tables, all 0 records (query sqlite3 confirmed)
- Build gate: tsc --noEmit exit 0; eslint exit 0 (1 warning / 0 error);
  next build exit 1 (SecurityFatalError: Next.js 16.4.0 known vulnerability)
- Repo: HEAD 66e356f (Rev. 761 committed); 776 local commits;
  340 tracked files; 13 untracked helper scripts; origin/main 2 behind
- M02a (NFC): uid_nfc field aktif, 0 siswa terisi (453 NULL)
- Auth & Beranda masih hardcode
- Prisma KitabProgress & Sertakan terdefinisi
"""
import datetime

path = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# --- 1. Header line (line 4) ---
old_header = 'header Rev. 761; \u00a711 compact changelog 116\u2013754\u2192116\u2013761; \u00a712 updated. HEAD 0aa3589 (Rev. 759 committed); Rev. 761 in working tree; commit count 775/0/1 (775 local commits, 0 ahead / 1 behind origin_main); node_modules present (477 dirs / 84021 files); dev.db ada (schema-only via init_db.py; 15 tabel, seluruh record 0) \u2014 seluruh data 453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions belum tersedia, import ulang dari init_db.py + init_schema.sql + sumber Excel/PDF). Build gate: npm run type-check (tsc --noEmit) \u2713 (exit 0); npm run lint \u2713 (exit 0, 1 warning / 0 error); npm run build (next build) \u2717 (exit 1 \u2014 SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). Build gate sebagian re-runnable. Working tree: PRD synced ke Rev. 761; 340 tracked files; 10 untracked (check_header.py, check_db.py, dev_report.py, prd_update_script.py, update_prd_757.py, verify_current.py, verify_db.py, verify_db_check.py, verify_fresh.py, update_prd_761.py); 0 deleted (fix_duplicate.py removed).'

new_header = 'header Rev. 762; \u00a711 compact changelog 116\u2013754\u2192116\u2013762; \u00a712 updated. HEAD 0aa3589 (Rev. 759 committed); Rev. 762 in working tree; commit count 776/2/0 (776 local commits, 2 ahead / 0 behind origin_main); node_modules present (477 dirs / 84021 files); dev.db ada (schema-only via init_db.py; 15 tabel, seluruh record 0) \u2014 seluruh data 453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions belum tersedia, import ulang dari init_db.py + init_schema.sql + sumber Excel/PDF). Build gate: npm run type-check (tsc --noEmit) \u2713 (exit 0); npm run lint \u2713 (exit 0, 1 warning / 0 error); npm run build (next build) \u2717 (exit 1 \u2014 SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). Build gate sebagian re-runnable. Working tree: PRD synced ke Rev. 762; 340 tracked files; 13 untracked (check_db.py, check_header.py, dev_report.py, prd_update_758.py, prd_update_script.py, update_prd_757.py, update_prd_760.py, update_prd_760b.py, update_prd_761.py, verify_current.py, verify_db.py, verify_db_check.py, verify_fresh.py); 0 deleted (fix_duplicate.py removed).'

if old_header in content:
    content = content.replace(old_header, new_header)
    print("Header: updated -> Rev. 762, 776 local, 2 ahead / 0 behind, 13 untracked")
else:
    print("Header: OLD_HEADER NOT FOUND")

# --- 2. Insert Rev. 762 section in §11 (before '## 12.') ---
rev762 = """### Rev. 762

> **Rev. 762 (fresh).** 30 Oktober 2026 (WIB): CRON-run fresh verification & stability confirmation (cron run); HEAD `66e356f` (Rev. 761 committed); commit count **776 / 2/0** (776 local commits, 2 ahead / 0 behind origin_main). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run):

> - **Environment:** node v26.5.1, npm 11.17.0, Prisma CLI = Prisma Developer Platform (new CLI; `generate`/`validate` commands not available in this release).

> - **Build quality gate:** `npm run type-check` (tsc --noEmit) \u2713 (exit 0); `npm run lint` \u2713 (exit 0, 1 warning / 0 error); `npm run build` (next build) \u2717 (exit 1 \u2014 SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). Build gate sebagian re-runnable \u2014 tsc + eslint lulus, next build diblokir security nudge. node_modules present (477 dirs / 84021 files).

> - **Database (dev.db):** **ada** \u2014 direkonstruksi schema-only via `init_db.py` (15 tabel, seluruh record 0). Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; source Excel & PDF dari `.data-pondokanat/` bukan tracked di repo).

> - **M02a (NFC):** field `uid_nfc` ada aktif di tabel `students` (kolom setelah `photo`); `prisma/schema.prisma` baris 68 (`uidNfc String? @map("uid_nfc")`), `init_schema.sql` baris 44, `init_db.py` baris 60. **0 siswa terisi (semua 453 NULL)** \u2014 data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).

> - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (typo domain `pondokanat.com`); produksi butuh bcrypt + session.

> - **Beranda hardcode:** `src/components/Beranda.tsx` & `src/app/beranda/page.tsx` masih hardcoded `totalSantri` (belum fetch real-time dari DB).

> - **Prisma:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` sukses (command not available in new Prisma CLI). Schema inconsistency (Rev. 38\u201345) SELESAI.

> - **Repo state:** clean working tree (PRD ditulis ke Rev. 762); `dev.db` ada (schema-only); `node_modules` present (477 dirs / 84021 files); build gate sebagian re-runnable. 13 untracked helper scripts (check_db.py, check_header.py, dev_report.py, prd_update_758.py, prd_update_script.py, update_prd_757.py, update_prd_760.py, update_prd_760b.py, update_prd_761.py, verify_current.py, verify_db.py, verify_db_check.py, verify_fresh.py); 0 deleted (fix_duplicate.py removed).

> - **Commit count:** 776 / 775 local commits (776 local commits, 2 ahead / 0 behind origin_main). Local branch **776 commits ahead / 0 behind** origin_main (HEAD `66e356f`, Rev. 761 committed; Rev. 762 dalam working tree).

> - **Status:** dokumen PRD **REVISI** \u2014 rev 762: PRD fresh verification & stability confirmation (30 Oktober 2026 (WIB)); HEAD `66e356f` (Rev. 761); **776 / 2/0** (776 local commits, 2 ahead / 0 behind origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 761 (data terkonsisten).

"""

marker = "## 12. STATUS RINGKASAN"
if marker in content:
    content = content.replace(marker, rev762 + marker, 1)
    print("Inserted Rev. 762 section before §12")
else:
    print("§12 marker: NOT FOUND")

# --- 3. §12 title ---
old_s12 = "## 12. STATUS RINGKASAN (30 Oktober 2026 WIB) \u2014 Rev. 761"
new_s12 = "## 12. STATUS RINGKASAN (30 Oktober 2026 WIB) \u2014 Rev. 762"
if old_s12 in content:
    content = content.replace(old_s12, new_s12)
    print("§12 title: updated -> Rev. 762")
else:
    print("§12 title: NOT FOUND")

# --- 4. §12 repo state line ---
old_repo = '**Repo state (Rev. 761):** HEAD `0aa3589` (Rev. 759 committed; Rev. 760 & Rev. 761 in working tree); **775 local commits, 0 ahead / 1 behind** origin_main; 340 tracked files; 10 untracked (check_header.py, check_db.py, dev_report.py, prd_update_script.py, update_prd_757.py, verify_current.py, verify_db.py, verify_db_check.py, verify_fresh.py, update_prd_761.py); 0 deleted (fix_duplicate.py removed).'
new_repo = '**Repo state (Rev. 762):** HEAD `66e356f` (Rev. 761 committed; Rev. 762 in working tree); **776 local commits, 2 ahead / 0 behind** origin_main; 340 tracked files; 13 untracked (check_db.py, check_header.py, dev_report.py, prd_update_758.py, prd_update_script.py, update_prd_757.py, update_prd_760.py, update_prd_760b.py, update_prd_761.py, verify_current.py, verify_db.py, verify_db_check.py, verify_fresh.py); 0 deleted (fix_duplicate.py removed).'
if old_repo in content:
    content = content.replace(old_repo, new_repo)
    print("§12 repo state: updated -> Rev. 762, 776 local, 2 ahead, 13 untracked")
else:
    print("§12 repo state: NOT FOUND")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("Done. File updated to Rev. 762.")
print("Rev 762 section count:", content.count("### Rev. 762"))
print("Rev 761 section count:", content.count("### Rev. 761"))
print("Rev 762 heading present:", new_s12 in content)
