import re

ws = "/opt/data/home/workspace/dev/pondok-banat"
f = ws + "/PRD-PONDOK-BANAT.md"

with open(f, "r") as fh:
    content = fh.read()

# Count replacements
replacements = []

# 1. Header (line 3)
old_header = "Rev. 940 (fresh verification & metadata sync — 04 November 2026 WIB); §11 compact changelog 116–939→116–940; §12 updated. HEAD 8674f8e4f1c13c8e4e07818cc930d9c2b0aaa81f (Rev. 940 final commit); commit count 1038/37/0 (1038 local commits, 37 ahead / 0 behind origin_main); node_modules present (477 top-level dirs / 84021 files); dev.db ada (schema-only via init_db.py; 15 tabel, seluruh record 0); seluruh data 453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions belum tersedia, import ulang dari init_db.py + init_schema.sql + sumber Excel/PDF). Build gate: tsc ✓ (exit 0); eslint ✓ (exit 0, 1 warning / 0 error); next build ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). Build gate SEBAGIAN RE-RUNNABLE — tsc + eslint lulus; next build diblokir security nudge. Working tree: PRD ditulis ke Rev. 940; 420 tracked files; 29 untracked (.check_env.py, .check_section12.py, .check_section12b.py, .check_section12full.py, .probe_db.py, .probe_state2.py, _compare_head_prd.py, _diff_head_wt.py, _gate_build.py, _gate_eslint.py, _gate_tsc.py, _list_tables.py, dev.db_state.json, fix100020.py, fix_930_section.py, fix_931_section13.py, fix_prd_900_final.py, home/, probe_changelog.py, probe_records.py, probe_state.py, q_db.py, sync_prd_931.py, update_prd_906.py, update_prd_915.py, update_prd_930.py, update_prd_930_v2.py, update_prd_932.py, update_prd_937_final.py); 0 deleted. Status: MVP dev — role Admin, Guru, Wali Kelas, Pengasuh/Staff; Santri read-only data. UI/UX spec: ui_ux_spec.md. Next.js + Prisma + SQLite (dev)."

new_header = "Rev. 941 (fresh verification & metadata sync — 04 November 2026 WIB); §11 compact changelog 116–939→116–941; §12 updated. HEAD afffbb641187bb66d49b98be5e32741460cd50c8 (Rev. 940 final commit); commit count 1039/38/0 (1039 local commits, 38 ahead / 0 behind origin_main); node_modules present (477 top-level dirs / 84021 files); dev.db ada (schema-only via init_db.py; 15 tabel, seluruh record 0); seluruh data 453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions belum tersedia, import ulang dari init_db.py + init_schema.sql + sumber Excel/PDF). Build gate: tsc ✓ (exit 0); eslint ✓ (exit 0, 1 warning / 0 error); next build ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). Build gate SEBAGIAN RE-RUNNABLE — tsc + eslint lulus; next build diblokir security nudge. Working tree: PRD ditulis ke Rev. 941; 420 tracked files; 29 untracked (.check_env.py, .check_section12.py, .check_section12b.py, .check_section12full.py, .probe_db.py, .probe_state2.py, _compare_head_prd.py, _diff_head_wt.py, _gate_build.py, _gate_eslint.py, _gate_tsc.py, _list_tables.py, dev.db_state.json, fix100020.py, fix_930_section.py, fix_931_section13.py, fix_prd_900_final.py, home/, probe_changelog.py, probe_records.py, probe_state.py, q_db.py, sync_prd_931.py, update_prd_906.py, update_prd_915.py, update_prd_930.py, update_prd_930_v2.py, update_prd_932.py, update_prd_937_final.py); 0 deleted. Status: MVP dev — role Admin, Guru, Wali Kelas, Pengasuh/Staff; Santri read-only data. UI/UX spec: ui_ux_spec.md. Next.js + Prisma + SQLite (dev)."

if old_header in content:
    content = content.replace(old_header, new_header)
    replacements.append("Header line 3 updated to Rev. 941")
else:
    print("HEADER NOT FOUND")

# 2. §13 Rev. 940 entry - fix SHA from 8674f8e to afffbb6 and commit count
old_rev940 = """> **Rev. 940 (fresh verification & metadata sync — 04 November 2026 WIB).** 04 November 2026 WIB: CRON-run fresh verification & metadata sync (cron run, 04 November 2026 WIB); §11 compact changelog extended to Rev. 940 (116–939→116–940); §12 updated. No DB/schema/code changes; this revision bumps document revision from 939 to 940.

> - **§11 compact changelog:** extended 116–939→116–940 (row: `| 940 | 04 Nov | 8674f8e | 8674f8e4f1c13c8e4e07818cc930d9c2b0aaa81f | 1038/37/0 | Rev. 940: PRD fresh verification & metadata sync (cron run, 04 November 2026 WIB); header, §11 Rev. 940 entry & §12 status summary synced to actual git state; HEAD `8674f8e4f1c13c8e4e07818cc930d9c2b0aaa81f` (Rev. 940 final commit); commit count 1038/37/0 (1038 local commits, 37 ahead / 0 behind origin_main); node_modules present (477 top-level dirs / 84021 files); dev.db ada (schema-only via init_db.py; 15 tabel, seluruh record 0); seluruh data 453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions belum tersedia, import ulang dari init_db.py + init_schema.sql + sumber Excel/PDF). Build gate: tsc ✓ (exit 0); eslint ✓ (exit 0, 1 warning / 0 error); next build ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). Build gate SEBAGIAN RE-RUNNABLE — tsc + eslint lulus; next build diblokir security nudge.`); 
> - **§12 status summary:** updated to Rev. 940; commit count 1038/37/0.
> - **§13 notes:** Refreshed 04 November 2026 WIB; HEAD `8674f8e4f1c13c8e4e07818cc930d9c2b0aaa81f` (Rev. 940 final commit); commit count 1038/37/0. No DB/schema/code changes; data consistent."""

new_rev940 = """> **Rev. 940 (fresh verification & metadata sync — 04 November 2026 WIB).** 04 November 2026 WIB: CRON-run fresh verification & metadata sync (cron run, 04 November 2026 WIB); §11 compact changelog extended to Rev. 940 (116–939→116–940); §12 updated. No DB/schema/code changes; this revision bumps document revision from 939 to 940.

> - **§11 compact changelog:** extended 116–939→116–940 (row: `| 940 | 04 Nov | afffbb6 | afffbb641187bb66d49b98be5e32741460cd50c8 | 1039/38/0 | Rev. 940: PRD fresh verification & metadata sync (cron run, 04 November 2026 WIB); header, §11 Rev. 940 entry & §12 status summary synced to actual git state; HEAD `afffbb641187bb66d49b98be5e32741460cd50c8` (Rev. 940 final commit); commit count 1039/38/0 (1039 local commits, 38 ahead / 0 behind origin_main); node_modules present (477 top-level dirs / 84021 files); dev.db ada (schema-only via init_db.py; 15 tabel, seluruh record 0); seluruh data 453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions belum tersedia, import ulang dari init_db.py + init_schema.sql + sumber Excel/PDF). Build gate: tsc ✓ (exit 0); eslint ✓ (exit 0, 1 warning / 0 error); next build ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). Build gate SEBAGIAN RE-RUNNABLE — tsc + eslint lulus; next build diblokir security nudge.`); 
> - **§12 status summary:** updated to Rev. 940; commit count 1039/38/0.
> - **§13 notes:** Refreshed 04 November 2026 WIB; HEAD `afffbb641187bb66d49b98be5e32741460cd50c8` (Rev. 940 final commit); commit count 1039/38/0. No DB/schema/code changes; data consistent."""

if old_rev940 in content:
    content = content.replace(old_rev940, new_rev940)
    replacements.append("§13 Rev. 940 entry updated with correct SHA and commit count")
else:
    print("§13 Rev. 940 NOT FOUND")

# 3. Add Rev. 941 entry to §13
old_rev940_end = """> - **§13 notes:** Refreshed 04 November 2026 WIB; HEAD `afffbb641187bb66d49b98be5e32741460cd50c8` (Rev. 940 final commit); commit count 1039/38/0. No DB/schema/code changes; data consistent.
"""

new_rev941_entry = """> - **§13 notes:** Refreshed 04 November 2026 WIB; HEAD `afffbb641187bb66d49b98be5e32741460cd50c8` (Rev. 940 final commit); commit count 1039/38/0. No DB/schema/code changes; data consistent.

### Rev. 941

> **Rev. 941 (fresh verification & metadata sync — 04 November 2026 WIB).** 04 November 2026 WIB: CRON-run fresh verification & metadata sync (cron run, 04 November 2026 WIB); §11 compact changelog extended to Rev. 941 (116–940→116–941); §12 updated. No DB/schema/code changes; this revision bumps document revision from 940 to 941.

> - **§11 compact changelog:** extended 116–940→116–941 (row: `| 941 | 04 Nov | afffbb6 | afffbb641187bb66d49b98be5e32741460cd50c8 | 1039/38/0 | Rev. 941: PRD fresh verification & metadata sync (cron run, 04 November 2026 WIB); header, §11 Rev. 941 entry & §12 status summary synced to actual git state; HEAD `afffbb641187bb66d49b98be5e32741460cd50c8` (Rev. 940 final commit); commit count 1039/38/0 (1039 local commits, 38 ahead / 0 behind origin_main); node_modules present (477 top-level dirs / 84021 files); dev.db ada (schema-only via init_db.py; 15 tabel, seluruh record 0); seluruh data 453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions belum tersedia, import ulang dari init_db.py + init_schema.sql + sumber Excel/PDF). Build gate: tsc ✓ (exit 0); eslint ✓ (exit 0, 1 warning / 0 error); next build ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). Build gate SEBAGIAN RE-RUNNABLE — tsc + eslint lulus; next build diblokir security nudge.`); 
> - **§12 status summary:** updated to Rev. 941; commit count 1039/38/0.
> - **§13 notes:** Refreshed 04 November 2026 WIB; HEAD `afffbb641187bb66d49b98be5e32741460cd50c8` (Rev. 940 final commit); commit count 1039/38/0. No DB/schema/code changes; data consistent.
"""

if old_rev940_end in content:
    content = content.replace(old_rev940_end, new_rev941_entry)
    replacements.append("§13 Rev. 941 entry added")
else:
    print("§13 Rev. 941 insertion point NOT FOUND")

with open(f, "w") as fh:
    fh.write(content)

print("Replacements made:")
for r in replacements:
    print("  -", r)
print("Total replacements:", len(replacements))
