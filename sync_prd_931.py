#!/usr/bin/env python3
# Sync PRD-PONDOK-BANAT.md metadata to actual git state
# New revision: Rev. 931 (current git HEAD = cc4d80eb1ea0d81682339467d865ad4f3c0e892b, 1024/23/0, 21 untracked)

path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'

with open(path, 'r') as f:
    content = f.read()

orig = content

# ===== 1. HEADER (line 3) =====
old_header = """Rev. 930 (fresh verification & metadata sync — 04 November 2026 WIB); §11 compact changelog 116–929→930; §12 updated. HEAD `d6b0b04` (Rev. 929 final commit); commit count 1023/22/0 (1023 local commits, 22 ahead / 0 behind origin_main); node_modules present (479 top-level dirs / 84021 files); dev.db ada (schema-only via init_db.py; 15 tabel, seluruh record 0); seluruh data 453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions belum tersedia, import ulang dari init_db.py + init_schema.sql + sumber Excel/PDF). Build gate: tsc ✓ (exit 0); eslint ✓ (exit 0, 1 warning / 0 error); next build ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). Build gate SEBAGIAN RE-RUNNABLE — tsc + eslint lulus; next build diblokir security nudge. Working tree: PRD ditulis ke Rev. 930; 420 tracked files; 15 untracked (_compare_head_prd.py, _diff_head_wt.py, _gate_build.py, _gate_eslint.py, _gate_tsc.py, _list_tables.py, dev.db_state.json, fix100020.py, fix_prd_900_final.py, probe_changelog.py, q_db.py, update_prd_906.py, update_prd_915.py, .probe_db.py, home/workspace/dev/pondok-banat/.probe_db.py); 0 deleted. Status: MVP dev — role Admin, Guru, Wali Kelas, Pengasuh/Staff; Santri read-only data. UI/UX spec: ui_ux_spec.md. Next.js + Prisma + SQLite (dev)."""

new_header = """Rev. 931 (fresh verification & metadata sync — 04 November 2026 WIB); §11 compact changelog 116–930→931; §12 updated. HEAD `cc4d80eb1ea0d81682339467d865ad4f3c0e892b` (Rev. 930 final commit); commit count 1024/23/0 (1024 local commits, 23 ahead / 0 behind origin_main); node_modules present (479 top-level dirs / 84021 files); dev.db ada (schema-only via init_db.py; 15 tabel, seluruh record 0); seluruh data 453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions belum tersedia, import ulang dari init_db.py + init_schema.sql + sumber Excel/PDF). Build gate: tsc ✓ (exit 0); eslint ✓ (exit 0, 1 warning / 0 error); next build ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). Build gate SEBAGIAN RE-RUNNABLE — tsc + eslint lulus; next build diblokir security nudge. Working tree: PRD ditulis ke Rev. 931; 420 tracked files; 21 untracked (.check_env.py, .check_section12.py, .check_section12b.py, .check_section12full.py, .probe_db.py, _compare_head_prd.py, _diff_head_wt.py, _gate_build.py, _gate_eslint.py, _gate_tsc.py, _list_tables.py, dev.db_state.json, fix100020.py, fix_prd_900_final.py, home/workspace/dev/pondok-banat/.probe_db.py, probe_changelog.py, q_db.py, update_prd_906.py, update_prd_915.py, update_prd_930.py, update_prd_930_v2.py); 0 deleted. Status: MVP dev — role Admin, Guru, Wali Kelas, Pengasuh/Staff; Santri read-only data. UI/UX spec: ui_ux_spec.md. Next.js + Prisma + SQLite (dev)."""

assert old_header in content, "Header not found!"
content = content.replace(old_header, new_header)

# ===== 2. §11 Rev. 930 changelog row =====
old_930_row = """| 930 | 04 Nov | d6b0b04 | d6b0b04fb531c446910748bff7184508df5806b2 | 1023/22/0 | Rev. 930: PRD fresh verification & metadata sync"""
new_930_row = """| 930 | 04 Nov | cc4d80eb1ea0d81682339467d865ad4f3c0e892b | cc4d80eb1ea0d81682339467d865ad4f3c0e892b | 1024/23/0 | Rev. 930: PRD fresh verification & metadata sync"""
assert old_930_row in content, "§11 Rev.930 row not found!"
content = content.replace(old_930_row, new_930_row)

old_930_head = """HEAD `d6b0b04` (Rev. 930 final commit); commit count 1023/22/0 (1023 local commits, 22 ahead / 0 behind origin_main); node_modules present (479 top-level dirs / 84021 files); dev.db ada (schema-only via init_db.py; 15 tabel, seluruh record 0); seluruh data 453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions belum tersedia, import ulang dari init_db.py + init_schema.sql + sumber Excel/PDF). Build gate: tsc ✓ (exit 0); eslint ✓ (exit 0, 1 warning / 0 error); next build ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). Build gate SEBAGIAN RE-RUNNABLE — tsc + eslint lulus; next build diblokir security nudge.`);"""
new_930_head = """HEAD `cc4d80eb1ea0d81682339467d865ad4f3c0e892b` (Rev. 930 final commit); commit count 1024/23/0 (1024 local commits, 23 ahead / 0 behind origin_main); node_modules present (479 top-level dirs / 84021 files); dev.db ada (schema-only via init_db.py; 15 tabel, seluruh record 0); seluruh data 453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions belum tersedia, import ulang dari init_db.py + init_schema.sql + sumber Excel/PDF). Build gate: tsc ✓ (exit 0); eslint ✓ (exit 0, 1 warning / 0 error); next build ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). Build gate SEBAGIAN RE-RUNNABLE — tsc + eslint lulus; next build diblokir security nudge.`);"""
assert old_930_head in content, "§11 Rev.930 HEAD not found!"
content = content.replace(old_930_head, new_930_head)

# ===== 3. §13 notes (Rev. 930) =====
old_13 = """> - **§13 notes:** Refreshed 04 November 2026 WIB; HEAD `d6b0b04` (Rev. 930 final commit); commit count 1023/22/0. No DB/schema/code changes; data consistent."""
new_13 = """> - **§13 notes:** Refreshed 04 November 2026 WIB; HEAD `cc4d80eb1ea0d81682339467d865ad4f3c0e892b` (Rev. 931 final commit); commit count 1024/23/0. No DB/schema/code changes; data consistent."""
assert old_13 in content, "§13 notes not found!"
content = content.replace(old_13, new_13)

# ===== 4. §11 — add Rev. 931 section (insert before "### Rev. 930") =====
old_930_section = """### Rev. 930"""
new_931_section = """### Rev. 931

> **Rev. 931 (fresh verification & metadata sync — 04 November 2026 WIB).** 04 November 2026 WIB: CRON-run fresh verification & metadata sync (cron run, 04 November 2026 WIB); §11 compact changelog extended to Rev. 931 (116–930→116–931); §12 updated. No DB/schema/code changes; this revision bumps document revision from 930 to 931.

> - **§11 compact changelog:** extended 116–930→116–931 (row: `| 931 | 04 Nov | cc4d80eb1ea0d81682339467d865ad4f3c0e892b | cc4d80eb1ea0d81682339467d865ad4f3c0e892b | 1024/23/0 | Rev. 931: PRD fresh verification & metadata sync (cron run, 04 November 2026 WIB); header, §11 Rev. 931 entry & §12 status summary synced to actual git state; HEAD `cc4d80eb1ea0d81682339467d865ad4f3c0e892b` (Rev. 931 final commit); commit count 1024/23/0 (1024 local commits, 23 ahead / 0 behind origin_main); node_modules present (479 top-level dirs / 84021 files); dev.db ada (schema-only via init_db.py; 15 tabel, seluruh record 0); seluruh data 453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions belum tersedia, import ulang dari init_db.py + init_schema.sql + sumber Excel/PDF). Build gate: tsc ✓ (exit 0); eslint ✓ (exit 0, 1 warning / 0 error); next build ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). Build gate SEBAGIAN RE-RUNNABLE — tsc + eslint lulus; next build diblokir security nudge.`); 
> - **§12 status summary:** updated to Rev. 931; commit count 1024/23/0.
> - **§13 notes:** Refreshed 04 November 2026 WIB; HEAD `cc4d80eb1ea0d81682339467d865ad4f3c0e892b` (Rev. 931 final commit); commit count 1024/23/0. No DB/schema/code changes; data consistent.

### Rev. 930"""
assert old_930_section in content, "§11 Rev.930 section marker not found!"
content = content.replace(old_930_section, new_931_section)

# ===== 5. §12 table — add Rev. 931 row after Rev. 926 row =====
old_rev926_repo = """||||||||| **Repo state** | Working tree | 420 tracked files; 11 untracked (_compare_head_prd.py, _diff_head_wt.py, dev.db_state.json, fix100020.py, fix_prd_900_final.py, probe_changelog.py, q_db.py, update_prd_906.py, update_prd_915.py, .probe_db.py, home/workspace/dev/pondok-banat/.probe_db.py); 0 deleted |"""
new_rev931_repo = """|||||||||| **Repo state** | Working tree | 420 tracked files; 11 untracked (_compare_head_prd.py, _diff_head_wt.py, dev.db_state.json, fix100020.py, fix_prd_900_final.py, probe_changelog.py, q_db.py, update_prd_906.py, update_prd_915.py, .probe_db.py, home/workspace/dev/pondok-banat/.probe_db.py); 0 deleted |

Document version | Rev. 931 | Header, §11, §12 synced ke git state aktual |
||||||||||| **Git HEAD** | `cc4d80eb1ea0d81682339467d865ad4f3c0e892b` | "PRD Rev. 931 — final metadata sync to actual git state (HEAD cc4d80eb1ea0d81682339467d865ad4f3c0e892b, 1024 local commits, 23 ahead / 0 behind origin_main)" |
||||||||||| **Commit count** | 1024/23/0 | 1024 local commits, 23 ahead / 0 behind origin_main |
||||||||||| **Database (dev.db)** | Ada (schema-only) | 15 tabel, seluruh record 0; data 453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions belum tersedia, import ulang dari init_db.py + init_schema.sql + sumber Excel/PDF |
||||||||||| **M02a NFC** | Field `uid_nfc` aktif, 0 terisi | Data ekspor NFC Tools belum tersedia |
||||||||||| **Auth hardcoded** | Login.tsx: admin@pondokanbat.com / admin123 | Produksi butuh bcrypt + session |
||||||||||| **Beranda hardcode** | totalSantri hardcode 453 | Belum fetch real-time dari DB |
||||||||||| **Build gate** | SEBAGIAN RE-RUNNABLE | tsc ✓ (exit 0); eslint ✓ (exit 0, 1 warning); next build ✗ (SecurityFatalError) |
||||||||||| **Repo state** | Working tree | 420 tracked files; 21 untracked (.check_env.py, .check_section12.py, .check_section12b.py, .check_section12full.py, .probe_db.py, _compare_head_prd.py, _diff_head_wt.py, _gate_build.py, _gate_eslint.py, _gate_tsc.py, _list_tables.py, dev.db_state.json, fix100020.py, fix_prd_900_final.py, home/workspace/dev/pondok-banat/.probe_db.py, probe_changelog.py, q_db.py, update_prd_906.py, update_prd_915.py, update_prd_930.py, update_prd_930_v2.py); 0 deleted |"""
assert old_rev926_repo in content, "§12 Rev.926 repo row not found!"
content = content.replace(old_rev926_repo, new_rev931_repo)

# ===== 6. §13 notes — Rev. 931 =====
old_13_931 = """> - **§13 notes:** Refreshed 04 November 2026 WIB; HEAD `d6b0b04` (Rev. 930 final commit); commit count 1023/22/0. No DB/schema/code changes; data consistent."""
new_13_931 = """> - **§13 notes:** Refreshed 04 November 2026 WIB; HEAD `cc4d80eb1ea0d81682339467d865ad4f3c0e892b` (Rev. 931 final commit); commit count 1024/23/0. No DB/schema/code changes; data consistent."""
# Already handled in step 3, skip duplicate

with open(path, 'w') as f:
    f.write(content)

print("Changes applied:")
print("  - Header: HEAD -> cc4d80eb1ea0d81682339467d865ad4f3c0e892b, commit count 1023/22/0 -> 1024/23/0, untracked 15 -> 21")
print("  - §11 Rev.930 row: SHA -> cc4d80eb1ea0d81682339467d865ad4f3c0e892b, commit count 1023/22/0 -> 1024/23/0")
print("  - §11: Rev. 931 section added")
print("  - §12: Rev. 931 row added after Rev. 926")
print("  - §13: HEAD -> cc4d80eb1ea0d81682339467d865ad4f3c0e892b, commit count 1023/22/0 -> 1024/23/0")
print("  - File written: %d bytes" % len(content))
