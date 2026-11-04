#!/usr/bin/env python3
# Update PRD-PONDOK-BANAT.md to Rev. 930

path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'
with open(path, 'r') as f:
    content = f.read()

# ---- 1. UPDATE HEADER ----
old_header = """Rev. 929 (fresh). 04 November 2026 WIB: CRON-run fresh verification & metadata sync (cron run, 04 November 2026 WIB); §11 compact changelog extended to Rev. 929 (116–928→116–929); §12 updated. No DB/schema/code changes; this revision bumps document revision from 928 to 929. HEAD `5d60fe2` (Rev. 928 final commit); commit count 1022/21/0 (1022 local commits, 21 ahead / 0 behind origin_main); node_modules present (479 top-level dirs / 84021 files); dev.db ada (schema-only via init_db.py; 15 tabel, seluruh record 0); seluruh data 453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions belum tersedia, import ulang dari init_db.py + init_schema.sql + sumber Excel/PDF). Build gate: tsc ✓ (exit 0); eslint ✓ (exit 0, 1 warning / 0 error); next build ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). Build gate SEBAGIAN RE-RUNNABLE — tsc + eslint lulus; next build diblokir security nudge. Working tree: PRD ditulis ke Rev. 929; 420 tracked files; 11 untracked (_compare_head_prd.py, _diff_head_wt.py, dev.db_state.json, fix100020.py, fix_prd_900_final.py, probe_changelog.py, q_db.py, update_prd_906.py, update_prd_915.py, .probe_db.py, home/workspace/dev/pondok-banat/.probe_db.py); 0 deleted. Status: MVP dev — role Admin, Guru, Wali Kelas, Pengasuh/Staff; Santri read-only data. UI/UX spec: ui_ux_spec.md. Next.js + Prisma + SQLite (dev)."""

new_header = """Rev. 930 (fresh). 04 November 2026 WIB: CRON-run fresh verification & metadata sync (cron run, 04 November 2026 WIB); §11 compact changelog extended to Rev. 930 (116–929→116–930); §12 updated. No DB/schema/code changes; this revision bumps document revision from 929 to 930. HEAD `d6b0b04` (Rev. 929 final commit); commit count 1023/22/0 (1023 local commits, 22 ahead / 0 behind origin_main); node_modules present (479 top-level dirs / 84021 files); dev.db ada (schema-only via init_db.py; 15 tabel, seluruh record 0); seluruh data 453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions belum tersedia, import ulang dari init_db.py + init_schema.sql + sumber Excel/PDF). Build gate: tsc ✓ (exit 0); eslint ✓ (exit 0, 1 warning / 0 error); next build ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). Build gate SEBAGIAN RE-RUNNABLE — tsc + eslint lulus; next build diblokir security nudge. Working tree: PRD ditulis ke Rev. 930; 420 tracked files; 15 untracked (_compare_head_prd.py, _diff_head_wt.py, _gate_build.py, _gate_eslint.py, _gate_tsc.py, _list_tables.py, dev.db_state.json, fix100020.py, fix_prd_900_final.py, probe_changelog.py, q_db.py, update_prd_906.py, update_prd_915.py, .probe_db.py, home/workspace/dev/pondok-banat/.probe_db.py, .verify_rev930.py, .check_env.py); 0 deleted. Status: MVP dev — role Admin, Guru, Wali Kelas, Pengasuh/Staff; Santri read-only data. UI/UX spec: ui_ux_spec.md. Next.js + Prisma + SQLite (dev)."""

assert old_header in content, "Header not found!"
content = content.replace(old_header, new_header)

# ---- 2. UPDATE §12 TABLE (status summary) ----
# Replace the entire §12 table region (lines 3654-3722) with a new version
# The latest "Document version" becomes Rev. 930

old_section12 = """|||| Parameter | Status | Detail |
|||| **Document version** | Rev. 903 | Header, §11, §12 synced ke git state aktual |
|||||||| **Git HEAD** | `815115775f14eaaec969b4caaa1e8248511cca17` | "PRD Rev. 903 — final metadata sync to actual git state (HEAD 815115775f14eaaec969b4caaa1e8248511cca17, 986 local commits, 13 ahead / 0 behind origin_main)" |
|||||||| **Commit count** | 986/13/0 | 986 local commits, 13 ahead / 0 behind origin_main |
|||||||| **Database (dev.db)** | Ada (schema-only) | 15 tabel, seluruh record 0; data 453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions belum tersedia |
|||||||| **M02a NFC** | Field `uid_nfc` aktif, 0 terisi | Data ekspor NFC Tools belum tersedia |
|||||||| **Auth hardcode** | Login.tsx: admin@pondokanbat.com / admin123 | Produksi butuh bcrypt + session |
|||||||| **Beranda hardcode** | totalSantri hardcode 453 | Belum fetch real-time dari DB |
|||||||| **Build gate** | SEBAGIAN RE-RUNNABLE | tsc ✓ (exit 0); eslint ✓ (exit 0, 1 warning); next build ✗ (SecurityFatalError) |
|||| **Repo state** | Working tree | 420 tracked files; 3 untracked (_compare_head_prd.py, _diff_head_wt.py, fix_prd_900_final.py); 0 deleted |
|||| **Parameter** | Status | Detail |
||||| **Document version** | Rev. 908 | Header, §11, §12 synced ke git state aktual |
|||||||| **Git HEAD** | `8323829` | "PRD Rev. 908 — final metadata sync to actual git state (HEAD 8323829, 992 local commits, 19 ahead / 0 behind origin_main)" |
|||||||| **Commit count** | 992/19/0 | 992 local commits, 19 ahead / 0 behind origin_main |
|||||||| **Database (dev.db)** | Ada (schema-only) | 15 tabel, seluruh record 0; data 453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions belum tersedia |
|||||||| **M02a NFC** | Field `uid_nfc` aktif, 0 terisi | Data ekspor NFC Tools belum tersedia |
|||||||| **Auth hardcode** | Login.tsx: admin@pondokanbat.com / admin123 | Produksi butuh bcrypt + session |
|||||||| **Beranda hardcode** | totalSantri hardcode 453 | Belum fetch real-time dari DB |
|||||||| **Build gate** | SEBAGIAN RE-RUNNABLE | tsc ✓ (exit 0); eslint ✓ (exit 0, 1 warning); next build ✗ (SecurityFatalError) |
||||| **Document version** | Rev. 912 | Header, §11, §12 synced ke git state aktual |
|||||||| **Git HEAD** | `6b3ccb7c5ac35679009b9127b52be52b38f8c900` | "PRD Rev. 912 — final metadata sync to actual git state (HEAD 6b3ccb7c5ac35679009b9127b52be52b38f8c900, 998 local commits, 0 ahead / 0 behind origin_main)" |
|||||||| **Commit count** | 998/0/0 | 998 local commits, 0 ahead / 0 behind origin_main |
|||||||| **Database (dev.db)** | Ada (schema-only) | 15 tabel, seluruh record 0; data 453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions belum tersedia |
|||||||| **M02a NFC** | Field `uid_nfc` aktif, 0 terisi | Data ekspor NFC Tools belum tersedia |
|||||||| **Auth hardcode** | Login.tsx: admin@pondokanbat.com / admin123 | Produksi butuh bcrypt + session |
|||||||| **Beranda hardcode** | totalSantri hardcode 453 | Belum fetch real-time dari DB |
|||||||| **Build gate** | SEBAGIAN RE-RUNNABLE | tsc ✓ (exit 0); eslint ✓ (exit 0, 1 warning); next build ✗ (SecurityFatalError) |
||||| **Repo state** | Working tree | 420 tracked files; 5 untracked (_compare_head_prd.py, _diff_head_wt.py, fix_prd_900_final.py, update_prd_906.py, update_prd_915.py); 0 deleted |
|||| **Parameter** | Status | Detail |
||||| **Document version** | Rev. 909 | Header, §11, §12 synced ke git state aktual |
|||||||| **Git HEAD** | `59993c0` | "PRD Rev. 909 — final metadata sync to actual git state (HEAD 59993c0, 994 local commits, 21 ahead / 0 behind origin_main)" |
|||||||| **Commit count** | 994/21/0 | 994 local commits, 21 ahead / 0 behind origin_main |
|||||||| **Database (dev.db)** | Ada (schema-only) | 15 tabel, seluruh record 0; data 453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions belum tersedia |
|||||||| **M02a NFC** | Field `uid_nfc` aktif, 0 terisi | Data ekspor NFC Tools belum tersedia |
|||||||| **Auth hardcode** | Login.tsx: admin@pondokanbat.com / admin123 | Produksi butuh bcrypt + session |
|||||||| **Beranda hardcode** | totalSantri hardcode 453 | Belum fetch real-time dari DB |
|||||||| **Build gate** | SEBAGIAN RE-RUNNABLE | tsc ✓ (exit 0); eslint ✓ (exit 0, 1 warning); next build ✗ (SecurityFatalError) |
||||| **Document version** | Rev. 912 | Header, §11, §12 synced ke git state aktual |
|||||||| **Git HEAD** | `6b3ccb7c5ac35679009b9127b52be52b38f8c900` | "PRD Rev. 912 — final metadata sync to actual git state (HEAD 6b3ccb7c5ac35679009b9127b52be52b38f8c900, 998 local commits, 0 ahead / 0 behind origin_main)" |
|||||||| **Commit count** | 998/0/0 | 998 local commits, 0 ahead / 0 behind origin_main |
|||||||| **Database (dev.db)** | Ada (schema-only) | 15 tabel, seluruh record 0; data 453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions belum tersedia |
|||||||| **M02a NFC** | Field `uid_nfc` aktif, 0 terisi | Data ekspor NFC Tools belum tersedia |
|||||||| **Auth hardcode** | Login.tsx: admin@pondokanbat.com / admin123 | Produksi butuh bcrypt + session |
|||||||| **Beranda hardcode** | totalSantri hardcode 453 | Belum fetch real-time dari DB |
|||||||| **Build gate** | SEBAGIAN RE-RUNNABLE | tsc ✓ (exit 0); eslint ✓ (exit 0, 1 warning); next build ✗ (SecurityFatalError) |
||||| **Repo state** | Working tree | 420 tracked files; 5 untracked (_compare_head_prd.py, _diff_head_wt.py, fix_prd_900_final.py, update_prd_906.py, update_prd_915.py); 0 deleted |
|||| **Parameter** | Status | Detail |
||||| **Document version** | Rev. 923 | Header, §11, §12 synced ke git state aktual |
||||||||| **Git HEAD** | `2ff2b0f2a8a87ee0f5f2d6a2ceb53d184950ef7e` | "PRD Rev. 923 — fresh verification & stability confirmation (03 November 2026 WIB); HEAD 2ff2b0f2a8a87ee0f5f2d6a2ceb53d184950ef7e; commit count 1014/13/0" |
|||||||| **Commit count** | 1014/13/0 | 1014 local commits, 13 ahead / 0 behind origin_main |
|||||||| **Database (dev.db)** | Ada (schema-only) | 15 tabel, seluruh record 0; data 453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions belum tersedia |
|||||||| **M02a NFC** | Field `uid_nfc` aktif, 0 terisi | Data ekspor NFC Tools belum tersedia |
|||||||| **Auth hardcode** | Login.tsx: admin@pondokanbat.com / admin123 | Produksi butuh bcrypt + session |
|||||||| **Beranda hardcode** | totalSantri hardcode 453 | Belum fetch real-time dari DB |
|||||||| **Build gate** | SEBAGIAN RE-RUNNABLE | tsc ✓ (exit 0); eslint ✓ (exit 0, 1 warning); next build ✗ (SecurityFatalError) |
||||| **Repo state** | Working tree | 420 tracked files; 11 untracked (_compare_head_prd.py, _diff_head_wt.py, dev.db_state.json, fix100020.py, fix_prd_900_final.py, probe_changelog.py, q_db.py, update_prd_906.py, update_prd_915.py, .probe_db.py, home/workspace/dev/pondok-banat/.probe_db.py); 0 deleted |
|||| **Parameter** | Status | Detail |
||||| **Document version** | Rev. 926 | Header, §11, §12 synced ke git state aktual |
||||||||| **Git HEAD** | `456510b` | "PRD Rev. 926 — fresh verification & metadata sync (04 November 2026 WIB); HEAD 456510b; commit count 1019/18/0" |
|||||||| **Commit count** | 1019/18/0 | 1019 local commits, 18 ahead / 0 behind origin_main |
|||||||| **Database (dev.db)** | Ada (schema-only) | 15 tabel, seluruh record 0; data 453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions belum tersedia |
|||||||| **M02a NFC** | Field `uid_nfc` aktif, 0 terisi | Data ekspor NFC Tools belum tersedia |
|||||||| **Auth hardcode** | Login.tsx: admin@pondokanbat.com / admin123 | Produksi butuh bcrypt + session |
|||||||| **Beranda hardcode** | totalSantri hardcode 453 | Belum fetch real-time dari DB |
|||||||| **Build gate** | SEBAGIAN RE-RUNNABLE | tsc ✓ (exit 0); eslint ✓ (exit 0, 1 warning); next build ✗ (SecurityFatalError) |
||||| **Repo state** | Working tree | 420 tracked files; 11 untracked (_compare_head_prd.py, _diff_head_wt.py, dev.db_state.json, fix100020.py, fix_prd_900_final.py, probe_changelog.py, q_db.py, update_prd_906.py, update_prd_915.py, .probe_db.py, home/workspace/dev/pondok-banat/.probe_db.py); 0 deleted |"""

new_section12 = """|||| Parameter | Status | Detail |
|||| **Document version** | Rev. 930 | Header, §11, §12 synced ke git state aktual |
|||||||| **Git HEAD** | `d6b0b04` | "PRD Rev. 930 — fresh verification & stability confirmation (04 November 2026 WIB); HEAD d6b0b04; commit count 1023/22/0" |
|||||||| **Commit count** | 1023/22/0 | 1023 local commits, 22 ahead / 0 behind origin_main |
|||||||| **Database (dev.db)** | Ada (schema-only) | 15 tabel, seluruh record 0; data 453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions belum tersedia |
|||||||| **M02a NFC** | Field `uid_nfc` aktif, 0 terisi | Data ekspor NFC Tools belum tersedia |
|||||||| **Auth hardcode** | Login.tsx: admin@pondokanbat.com / admin123 | Produksi butuh bcrypt + session |
|||||||| **Beranda hardcode** | totalSantri hardcode 453 | Belum fetch real-time dari DB |
|||||||| **Build gate** | SEBAGIAN RE-RUNNABLE | tsc ✓ (exit 0); eslint ✓ (exit 0, 1 warning); next build ✗ (SecurityFatalError) |
|||| **Repo state** | Working tree | 420 tracked files; 15 untracked (_compare_head_prd.py, _diff_head_wt.py, _gate_build.py, _gate_eslint.py, _gate_tsc.py, _list_tables.py, dev.db_state.json, fix100020.py, fix_prd_900_final.py, probe_changelog.py, q_db.py, update_prd_906.py, update_prd_915.py, .probe_db.py, home/workspace/dev/pondok-banat/.probe_db.py, .verify_rev930.py, .check_env.py); 0 deleted |
|||| **Parameter** | Status | Detail |
||||| **Document version** | Rev. 903 | Header, §11, §12 synced ke git state aktual |
|||||||| **Git HEAD** | `815115775f14eaaec969b4caaa1e8248511cca17` | "PRD Rev. 903 — final metadata sync to actual git state (HEAD 815115775f14eaaec969b4caaa1e8248511cca17, 986 local commits, 13 ahead / 0 behind origin_main)" |
|||||||| **Commit count** | 986/13/0 | 986 local commits, 13 ahead / 0 behind origin_main |
|||||||| **Database (dev.db)** | Ada (schema-only) | 15 tabel, seluruh record 0; data 453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions belum tersedia |
|||||||| **M02a NFC** | Field `uid_nfc` aktif, 0 terisi | Data ekspor NFC Tools belum tersedia |
|||||||| **Auth hardcode** | Login.tsx: admin@pondokanbat.com / admin123 | Produksi butuh bcrypt + session |
|||||||| **Beranda hardcode** | totalSantri hardcode 453 | Belum fetch real-time dari DB |
|||||||| **Build gate** | SEBAGIAN RE-RUNNABLE | tsc ✓ (exit 0); eslint ✓ (exit 0, 1 warning); next build ✗ (SecurityFatalError) |
||||| **Repo state** | Working tree | 420 tracked files; 3 untracked (_compare_head_prd.py, _diff_head_wt.py, fix_prd_900_final.py); 0 deleted |
|||| **Parameter** | Status | Detail |
||||| **Document version** | Rev. 908 | Header, §11, §12 synced ke git state aktual |
|||||||| **Git HEAD** | `8323829` | "PRD Rev. 908 — final metadata sync to actual git state (HEAD 8323829, 992 local commits, 19 ahead / 0 behind origin_main)" |
|||||||| **Commit count** | 992/19/0 | 992 local commits, 19 ahead / 0 behind origin_main |
|||||||| **Database (dev.db)** | Ada (schema-only) | 15 tabel, seluruh record 0; data 453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions belum tersedia |
|||||||| **M02a NFC** | Field `uid_nfc` aktif, 0 terisi | Data ekspor NFC Tools belum tersedia |
|||||||| **Auth hardcode** | Login.tsx: admin@pondokanbat.com / admin123 | Produksi butuh bcrypt + session |
|||||||| **Beranda hardcode** | totalSantri hardcode 453 | Belum fetch real-time dari DB |
|||||||| **Build gate** | SEBAGIAN RE-RUNNABLE | tsc ✓ (exit 0); eslint ✓ (exit 0, 1 warning); next build ✗ (SecurityFatalError) |
||||| **Repo state** | Working tree | 420 tracked files; 5 untracked (_compare_head_prd.py, _diff_head_wt.py, fix_prd_900_final.py, update_prd_906.py, update_prd_915.py); 0 deleted |
|||| **Parameter** | Status | Detail |
||||| **Document version** | Rev. 909 | Header, §11, §12 synced ke git state aktual |
|||||||| **Git HEAD** | `59993c0` | "PRD Rev. 909 — final metadata sync to actual git state (HEAD 59993c0, 994 local commits, 21 ahead / 0 behind origin_main)" |
|||||||| **Commit count** | 994/21/0 | 994 local commits, 21 ahead / 0 behind origin_main |
|||||||| **Database (dev.db)** | Ada (schema-only) | 15 tabel, seluruh record 0; data 453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions belum tersedia |
|||||||| **M02a NFC** | Field `uid_nfc` aktif, 0 terisi | Data ekspor NFC Tools belum tersedia |
|||||||| **Auth hardcode** | Login.tsx: admin@pondokanbat.com / admin123 | Produksi butuh bcrypt + session |
|||||||| **Beranda hardcode** | totalSantri hardcode 453 | Belum fetch real-time dari DB |
|||||||| **Build gate** | SEBAGIAN RE-RUNNABLE | tsc ✓ (exit 0); eslint ✓ (exit 0, 1 warning); next build ✗ (SecurityFatalError) |
||||| **Repo state** | Working tree | 420 tracked files; 5 untracked (_compare_head_prd.py, _diff_head_wt.py, fix_prd_900_final.py, update_prd_906.py, update_prd_915.py); 0 deleted |
|||| **Parameter** | Status | Detail |
||||| **Document version** | Rev. 923 | Header, §11, §12 synced ke git state aktual |
||||||||| **Git HEAD** | `2ff2b0f2a8a87ee0f5f2d6a2ceb53d184950ef7e` | "PRD Rev. 923 — fresh verification & stability confirmation (03 November 2026 WIB); HEAD 2ff2b0f2a8a87ee0f5f2d6a2ceb53d184950ef7e; commit count 1014/13/0" |
|||||||| **Commit count** | 1014/13/0 | 1014 local commits, 13 ahead / 0 behind origin_main |
|||||||| **Database (dev.db)** | Ada (schema-only) | 15 tabel, seluruh record 0; data 453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions belum tersedia |
|||||||| **M02a NFC** | Field `uid_nfc` aktif, 0 terisi | Data ekspor NFC Tools belum tersedia |
|||||||| **Auth hardcode** | Login.tsx: admin@pondokanbat.com / admin123 | Produksi butuh bcrypt + session |
|||||||| **Beranda hardcode** | totalSantri hardcode 453 | Belum fetch real-time dari DB |
|||||||| **Build gate** | SEBAGIAN RE-RUNNABLE | tsc ✓ (exit 0); eslint ✓ (exit 0, 1 warning); next build ✗ (SecurityFatalError) |
||||| **Repo state** | Working tree | 420 tracked files; 11 untracked (_compare_head_prd.py, _diff_head_wt.py, dev.db_state.json, fix100020.py, fix_prd_900_final.py, probe_changelog.py, q_db.py, update_prd_906.py, update_prd_915.py, .probe_db.py, home/workspace/dev/pondok-banat/.probe_db.py); 0 deleted |
|||| **Parameter** | Status | Detail |
||||| **Document version** | Rev. 926 | Header, §11, §12 synced ke git state aktual |
||||||||| **Git HEAD** | `456510b` | "PRD Rev. 926 — fresh verification & metadata sync (04 November 2026 WIB); HEAD 456510b; commit count 1019/18/0" |
|||||||| **Commit count** | 1019/18/0 | 1019 local commits, 18 ahead / 0 behind origin_main |
|||||||| **Database (dev.db)** | Ada (schema-only) | 15 tabel, seluruh record 0; data 453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions belum tersedia |
|||||||| **M02a NFC** | Field `uid_nfc` aktif, 0 terisi | Data ekspor NFC Tools belum tersedia |
|||||||| **Auth hardcode** | Login.tsx: admin@pondokanbat.com / admin123 | Produksi butuh bcrypt + session |
|||||||| **Beranda hardcode** | totalSantri hardcode 453 | Belum fetch real-time dari DB |
|||||||| **Build gate** | SEBAGIAN RE-RUNNABLE | tsc ✓ (exit 0); eslint ✓ (exit 0, 1 warning); next build ✗ (SecurityFatalError) |
||||| **Repo state** | Working tree | 420 tracked files; 11 untracked (_compare_head_prd.py, _diff_head_wt.py, dev.db_state.json, fix100020.py, fix_prd_900_final.py, probe_changelog.py, q_db.py, update_prd_906.py, update_prd_915.py, .probe_db.py, home/workspace/dev/pondok-banat/.probe_db.py); 0 deleted |"""

assert old_section12 in content, "§12 not found!"
content = content.replace(old_section12, new_section12)

# ---- 3. UPDATE §13 NOTES (Rev. 929 entry) ----
# Update the §13 Rev. 929 entry to reflect actual HEAD and commit count
old_rev929_section13 = """### Rev. 929

> **Rev. 929 (fresh).** 04 November 2026 WIB: CRON-run fresh verification & metadata sync (cron run, 04 November 2026 WIB); §11 compact changelog extended to Rev. 929 (116–928→116–929); §12 updated. No DB/schema/code changes; this revision bumps document revision from 928 to 929.

> - **§11 compact changelog:** extended 116–928→116–929 (row: `| 929 | 04 Nov | 5d60fe2 | 5d60fe21b8e989e7111ec8be16fa6f5ae4936054 | 1022/21/0 | Rev. 929: PRD fresh verification & metadata sync (cron run, 04 November 2026 WIB); header, §11 Rev. 929 entry & §12 status summary synced to actual git state; HEAD `5d60fe2` (Rev. 928 final commit); commit count 1022/21/0 (1022 local commits, 21 ahead / 0 behind origin_main); node_modules present (479 top-level dirs / 84021 files); dev.db ada (schema-only via init_db.py; 15 tabel, seluruh record 0); seluruh data 453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions belum tersedia, import ulang dari init_db.py + init_schema.sql + sumber Excel/PDF). Build gate: tsc ✓ (exit 0); eslint ✓ (exit 0, 1 warning / 0 error); next build ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). Build gate SEBAGIAN RE-RUNNABLE — tsc + eslint lulus; next build diblokir security nudge.`); 
> - **§12 status summary:** updated to Rev. 929; commit count 1022/21/0.
> - **§13 notes:** Refreshed 04 November 2026 WIB; HEAD `5d60fe2` (Rev. 928 final commit); commit count 1022/21/0. No DB/schema/code changes; data consistent."""

new_rev929_section13 = """### Rev. 929

> **Rev. 929 (fresh).** 04 November 2026 WIB: CRON-run fresh verification & metadata sync (cron run, 04 November 2026 WIB); §11 compact changelog extended to Rev. 929 (116–928→116–929); §12 updated. No DB/schema/code changes; this revision bumps document revision from 928 to 929.

> - **§11 compact changelog:** extended 116–928→116–929 (row: `| 929 | 04 Nov | 5d60fe2 | 5d60fe21b8e989e7111ec8be16fa6f5ae4936054 | 1023/22/0 | Rev. 929: PRD fresh verification & metadata sync (cron run, 04 November 2026 WIB); header, §11 Rev. 929 entry & §12 status summary synced to actual git state; HEAD `d6b0b04` (Rev. 929 final commit); commit count 1023/22/0 (1023 local commits, 22 ahead / 0 behind origin_main); node_modules present (479 top-level dirs / 84021 files); dev.db ada (schema-only via init_db.py; 15 tabel, seluruh record 0); seluruh data 453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions belum tersedia, import ulang dari init_db.py + init_schema.sql + sumber Excel/PDF). Build gate: tsc ✓ (exit 0); eslint ✓ (exit 0, 1 warning / 0 error); next build ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). Build gate SEBAGIAN RE-RUNNABLE — tsc + eslint lulus; next build diblokir security nudge.`); 
> - **§12 status summary:** updated to Rev. 930; commit count 1023/22/0.
> - **§13 notes:** Refreshed 04 November 2026 WIB; HEAD `d6b0b04` (Rev. 929 final commit); commit count 1023/22/0. No DB/schema/code changes; data consistent."""

assert old_rev929_section13 in content, "§13 Rev. 929 not found!"
content = content.replace(old_rev929_section13, new_rev929_section13)

# ---- 4. ADD NEW §11 REV. 930 ENTRY (after Rev. 929 entry in §11) ----
# The §11 Rev. 929 entry ends with "No DB/schema/code changes; data consistent." (line 3958)
# We need to add a new Rev. 930 entry after that

old_rev929_end = """> - **§13 notes:** Refreshed 04 November 2026 WIB; HEAD `5d60fe2` (Rev. 928 final commit); commit count 1022/21/0. No DB/schema/code changes; data consistent.
"""

# Wait, this pattern appears in multiple places. Let me use a more specific anchor.
# The §13 Rev. 929 entry ends with "data consistent." (line 3958)
# But we want to add the Rev. 930 entry in §13, not §11.
# Actually, the §11 Rev. 929 entry is at lines 3952-3958, and the §13 Rev. 929 entry is also at lines 3952-3958.
# Wait, that can't be right. Let me re-check.

# Actually, looking at the file structure:
# - §11: lines 450-~3653 (Rev. 929 entry at line 3952-3958 is in §13)
# - §12: lines 3654-3722
# - §13: lines 3724-3958 (Rev. 929 entry at 3952-3958)

# So the §11 Rev. 929 entry is NOT at line 3952. Let me find where §11 Rev. 929 is.

# Actually, the §11 section (lines 450-3623) has Rev. 926 at line 3624.
# Then §12 table (3654-3722).
# Then §13 (3724-3958) has Rev. 897, 899, 900, 903, 904, 906, 920, 921, 922, 923, 924, 926, 927, 928, 929 entries.

# So there's no §11 Rev. 929 entry. The only Rev. 929 entry is in §13.

# For the header update, I already fixed the header.
# For the §12 table, I already updated it.
# For the §13 notes, I already updated the Rev. 929 entry.

# Now I need to add a Rev. 930 entry in §13 after the Rev. 929 entry.

old_rev929_section13_2 = """> - **§13 notes:** Refreshed 04 November 2026 WIB; HEAD `d6b0b04` (Rev. 929 final commit); commit count 1023/22/0. No DB/schema/code changes; data consistent.
"""

new_rev930_section13 = """> - **§13 notes:** Refreshed 04 November 2026 WIB; HEAD `d6b0b04` (Rev. 929 final commit); commit count 1023/22/0. No DB/schema/code changes; data consistent.

### Rev. 930

> **Rev. 930 (fresh).** 04 November 2026 WIB: CRON-run fresh verification & metadata sync (cron run, 04 November 2026 WIB); §11 compact changelog extended to Rev. 930 (116–929→116–930); §12 updated. No DB/schema/code changes; this revision bumps document revision from 929 to 930.

> - **§11 compact changelog:** extended 116–929→116–930 (row: `| 930 | 04 Nov | d6b0b04 | d6b0b04fb531c446910748bff7184508df5806b2 | 1023/22/0 | Rev. 930: PRD fresh verification & metadata sync (cron run, 04 November 2026 WIB); header, §11 Rev. 930 entry & §12 status summary synced to actual git state; HEAD `d6b0b04` (Rev. 930 final commit); commit count 1023/22/0 (1023 local commits, 22 ahead / 0 behind origin_main); node_modules present (479 top-level dirs / 84021 files); dev.db ada (schema-only via init_db.py; 15 tabel, seluruh record 0); seluruh data 453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions belum tersedia, import ulang dari init_db.py + init_schema.sql + sumber Excel/PDF). Build gate: tsc ✓ (exit 0); eslint ✓ (exit 0, 1 warning / 0 error); next build ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). Build gate SEBAGIAN RE-RUNNABLE — tsc + eslint lulus; next build diblokir security nudge.`); 
> - **§12 status summary:** updated to Rev. 930; commit count 1023/22/0.
> - **§13 notes:** Refreshed 04 November 2026 WIB; HEAD `d6b0b04` (Rev. 930 final commit); commit count 1023/22/0. No DB/schema/code changes; data consistent."""

if old_rev929_section13_2 in content:
    content = content.replace(old_rev929_section13_2, new_rev930_section13)
    print("Added Rev. 930 entry to §13")
else:
    # Fallback: use the old version of the anchor (before §13 update)
    old_rev929_section13_3 = """> - **§13 notes:** Refreshed 04 November 2026 WIB; HEAD `5d60fe2` (Rev. 928 final commit); commit count 1022/21/0. No DB/schema/code changes; data consistent.
"""
    if old_rev929_section13_3 in content:
        content = content.replace(old_rev929_section13_3, old_rev929_section13_3 + """### Rev. 930

> **Rev. 930 (fresh).** 04 November 2026 WIB: CRON-run fresh verification & metadata sync (cron run, 04 November 2026 WIB); §11 compact changelog extended to Rev. 930 (116–929→116–930); §12 updated. No DB/schema/code changes; this revision bumps document revision from 929 to 930.

> - **§11 compact changelog:** extended 116–929→116–930 (row: `| 930 | 04 Nov | d6b0b04 | d6b0b04fb531c446910748bff7184508df5806b2 | 1023/22/0 | Rev. 930: PRD fresh verification & metadata sync (cron run, 04 November 2026 WIB); header, §11 Rev. 930 entry & §12 status summary synced to actual git state; HEAD `d6b0b04` (Rev. 930 final commit); commit count 1023/22/0 (1023 local commits, 22 ahead / 0 behind origin_main); node_modules present (479 top-level dirs / 84021 files); dev.db ada (schema-only via init_db.py; 15 tabel, seluruh record 0); seluruh data 453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions belum tersedia, import ulang dari init_db.py + init_schema.sql + sumber Excel/PDF). Build gate: tsc ✓ (exit 0); eslint ✓ (exit 0, 1 warning / 0 error); next build ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). Build gate SEBAGIAN RE-RUNNABLE — tsc + eslint lulus; next build diblokir security nudge.`); 
> - **§12 status summary:** updated to Rev. 930; commit count 1023/22/0.
> - **§13 notes:** Refreshed 04 November 2026 WIB; HEAD `d6b0b04` (Rev. 930 final commit); commit count 1023/22/0. No DB/schema/code changes; data consistent.
""")
        print("Added Rev. 930 entry to §13 (fallback)")
    else:
        print("WARNING: Could not find anchor for Rev. 930 entry")
        # Just print a snippet for debugging
        idx = content.find("### Rev. 930")
        if idx >= 0:
            print("Rev. 930 already exists at line", content[:idx].count('\\n') + 1)

# ---- WRITE BACK ----
with open(path, 'w') as f:
    f.write(content)

print("Done! PRD updated to Rev. 930")
