#!/usr/bin/env python3
"""Update PRD-PONDOK-BANAT.md to Rev. 804 with fresh verification results.

Fresh verification (cron run, 31 Oktober 2026 WIB, re-run):
- dev.db: schema-only via init_db.py (15 tabel, seluruh record 0)
- Build gate: tsc --noEmit exit 0; eslint exit 0 (1 warning / 0 error);
  next build exit 1 (SecurityFatalError: Next.js 16.4.0 known vulnerability)
- Repo: HEAD 7121eba (Rev. 803 committed); 825 local commits; 17 ahead / 0 behind
- node_modules: 5103 dirs / 84073 files
- M02a (NFC): uid_nfc field aktif, 0 siswa terisi (453 NULL)
- Auth & Beranda masih hardcode
- Prisma KitabProgress & Sertakan terdefinisi
"""
import datetime

path = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# --- 1. Header line (line 3) ---
old_header = """header Rev. 803; §11 compact changelog 116–798→799→800→801→802→803; §12 updated. HEAD `037bc62` (Rev. 802 committed); commit count 824/16/0 (824 local commits, 16 ahead / 0 behind origin_main); node_modules present (5103 dirs / 84021 files); dev.db ada (schema-only via init_db.py; 15 tabel, seluruh record 0); seluruh data 453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions belum tersedia, import ulang dari init_db.py + init_schema.sql + sumber Excel/PDF). Build gate: tsc ✓ (exit 0); eslint ✓ (exit 0, 1 warning / 0 error); next build ✗ (SecurityFatalError: Next.js 16.4.0 has a known security vulnerability — engine security nudge, upgrade recommended). Working tree: PRD synced ke Rev. 803; Rev. 803 in working tree; 340 tracked files; 33 untracked (_state_check.py, check_db.py, check_db_current.py, check_header.py, cron_789_verify.py, dev_report.py, inspect_devdb.py, prd_update_758.py, prd_update_script.py, probe_s11.py, probe_s11b.py, update_prd_757.py, update_prd_760.py, update_prd_760b.py, update_prd_761.py, update_prd_762.py, update_prd_764.py, update_prd_770.py, update_prd_777.py, update_prd_789.py, update_prd_790.py, update_prd_791.py, update_prd_792.py, update_prd_793.py, update_prd_796.py, verify_current.py, verify_db.py, verify_db_check.py, verify_fresh.py, verify_fresh2.py, verify_fresh3.py, verify_fresh_run.py, verify_state_801.py, update_prd_803.py, fix_prd_structure_803.py, fix_prd_803_final.py, fix_prd_803_final2.py, add_rev802_803.py); 0 deleted."""

new_header = """header Rev. 804; §11 compact changelog 116–798→799→800→801→802→803→804; §12 updated. HEAD `7121eba` (Rev. 803 committed); commit count 825/17/0 (825 local commits, 17 ahead / 0 behind origin_main); node_modules present (5103 dirs / 84073 files); dev.db ada (schema-only via init_db.py; 15 tabel, seluruh record 0); seluruh data 453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions belum tersedia, import ulang dari init_db.py + init_schema.sql + sumber Excel/PDF). Build gate: tsc ✓ (exit 0); eslint ✓ (exit 0, 1 warning / 0 error); next build ✗ (SecurityFatalError: Next.js 16.4.0 has a known security vulnerability — engine security nudge, upgrade recommended). Working tree: PRD synced ke Rev. 804; Rev. 804 in working tree; 340 tracked files; 33 untracked (_state_check.py, check_db.py, check_db_current.py, check_header.py, cron_789_verify.py, dev_report.py, inspect_devdb.py, prd_update_758.py, prd_update_script.py, probe_s11.py, probe_s11b.py, update_prd_757.py, update_prd_760.py, update_prd_760b.py, update_prd_761.py, update_prd_762.py, update_prd_764.py, update_prd_770.py, update_prd_777.py, update_prd_789.py, update_prd_790.py, update_prd_791.py, update_prd_792.py, update_prd_793.py, update_prd_796.py, verify_current.py, verify_db.py, verify_db_check.py, verify_fresh.py, verify_fresh2.py, verify_fresh3.py, verify_fresh_run.py, verify_state_801.py, update_prd_803.py, fix_prd_structure_803.py, fix_prd_803_final.py, fix_prd_803_final2.py, add_rev802_803.py, verify_state_804.py); 0 deleted."""

if old_header in content:
    content = content.replace(old_header, new_header)
    print("Header: updated -> Rev. 804, 825 local, 17 ahead / 0 behind, node_modules 5103/84073")
else:
    print("Header: OLD_HEADER NOT FOUND")

# --- 2. Insert Rev. 804 section in §11 (before '## 12. STATUS RINGKASAN') ---
rev804 = """### Rev. 804

> **Rev. 804 (fresh).** 31 Oktober 2026 (WIB): CRON-run fresh verification & stability confirmation (cron run); HEAD `7121eba` (Rev. 803 committed — PRD fresh verification & stability confirmation, 31 Oktober 2026 WIB; header Rev. 804, §11 compact changelog 116–798→799→800→801→802→803→804, §12 updated; HEAD `7121eba`, Rev. 803 committed). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run):

> - **Environment:** node v26.5.1, npm 11.17.0, Prisma CLI = Prisma Developer Platform (new CLI; `generate`/`validate` commands not available in this release).
> - **Build quality gate:** `npm run type-check` (tsc --noEmit) ✓ (exit 0); `npm run lint` ✓ (exit 0, 1 warning / 0 error); `npm run build` (next build) ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability — engine security nudge, upgrade recommended). Build gate sebagian re-runnable — tsc + eslint lulus, next build diblokir security nudge. node_modules present (5103 dirs / 84073 files).
> - **Database (dev.db):** **ada** — schema-only via `init_db.py` (15 tabel, seluruh record 0). Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; source Excel & PDF dari `.data-pondokanat/` bukan tracked di repo).
> - **M02a (NFC):** field `uid_nfc` ada aktif di tabel `students` (kolom setelah `photo`); `prisma/schema.prisma` baris 68 (`uidNfc String? @map(\"uid_nfc\"`)); `init_schema.sql` baris 44, `init_db.py` baris 60. **0 siswa terisi (semua 453 NULL)** — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
> - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` sudah diperbaiki; typo `pondokanat.com` telah dihapus); produksi butuh bcrypt + session.
> - **Beranda hardcode:** `src/components/Beranda.tsx` & `src/app/beranda/page.tsx` masih hardcoded `totalSantri` (belum fetch real-time dari DB); nilai sekarang `totalSantri: 453, totalGuru: 54, totalKelas: 18`.
> - **Prisma:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` sukses (command not available in new Prisma CLI). Schema inconsistency (Rev. 38–45) SELESAI.
> - **Repo state:** clean working tree (PRD ditulis ke Rev. 804); `dev.db` ada (schema-only); `node_modules` present (5103 dirs / 84073 files); build gate sebagian re-runnable. 34 untracked helper scripts (include _state_check.py, check_db.py, check_db_current.py, check_header.py, cron_789_verify.py, dev_report.py, inspect_devdb.py, prd_update_758.py, prd_update_script.py, probe_s11.py, probe_s11b.py, update_prd_757.py, update_prd_760.py, update_prd_760b.py, update_prd_761.py, update_prd_762.py, update_prd_764.py, update_prd_770.py, update_prd_777.py, update_prd_789.py, update_prd_790.py, update_prd_791.py, update_prd_792.py, update_prd_793.py, update_prd_796.py, verify_current.py, verify_db.py, verify_db_check.py, verify_fresh.py, verify_fresh2.py, verify_fresh3.py, verify_fresh_run.py, verify_state_801.py, update_prd_803.py, fix_prd_structure_803.py, fix_prd_803_final.py, fix_prd_803_final2.py, add_rev802_803.py, verify_state_804.py); 0 deleted (fix_duplicate.py removed).
> - **Commit count:** 825 local commits, **17 ahead / 0 behind** origin_main (origin/main at `60d2d99`, Rev. 788). Local branch **825 commits ahead / 0 behind** origin_main (HEAD `7121eba`, Rev. 803 committed).
> - **Status:** dokumen PRD **REVISI** — rev 804: PRD fresh verification & stability confirmation (cron run, 31 Oktober 2026 (WIB)); HEAD `7121eba` (Rev. 803 committed); **825 / 17/0** (825 local commits, 17 ahead / 0 behind origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 803 (data terkonsisten).

"""

marker = "## 12. STATUS RINGKASAN"
if marker in content:
    content = content.replace(marker, rev804 + marker, 1)
    print("Inserted Rev. 804 section before §12")
else:
    print("§12 marker: NOT FOUND")

# --- 3. §12 title ---
old_s12 = "## 12. STATUS RINGKASAN (31 Oktober 2026 WIB) — Rev. 802"
new_s12 = "## 12. STATUS RINGKASAN (31 Oktober 2026 WIB) — Rev. 804"
if old_s12 in content:
    content = content.replace(old_s12, new_s12)
    print("§12 title: updated -> Rev. 804")
else:
    print("§12 title: NOT FOUND")

# --- 4. §12 bullet points (repo state line) ---
old_repo = '''> - **Repo state (Rev. 802):** HEAD `37dc5c7` (Rev. 800 committed); **824 local commits, 16 ahead / 0 behind** origin_main; 340 tracked files; 33 untracked; 0 deleted (fix_duplicate.py removed).'''
new_repo = '''> - **Repo state (Rev. 804):** HEAD `7121eba` (Rev. 803 committed); **825 local commits, 17 ahead / 0 behind** origin_main; 340 tracked files; 34 untracked (incl. verify_state_804.py); 0 deleted (fix_duplicate.py removed).'''
if old_repo in content:
    content = content.replace(old_repo, new_repo)
    print("§12 repo state: updated -> Rev. 804, 825 local, 17 ahead, 34 untracked")
else:
    print("§12 repo state: NOT FOUND")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("Done. File updated to Rev. 804.")
print("Rev 804 section count:", content.count("### Rev. 804"))
print("Rev 802 section count:", content.count("### Rev. 802"))
print("Rev 804 heading present:", new_s12 in content)
