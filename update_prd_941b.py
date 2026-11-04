import re

ws = "/opt/data/home/workspace/dev/pondok-banat"
f = ws + "/PRD-PONDOK-BANAT.md"

with open(f, "r") as fh:
    content = fh.read()

# Find the §12 status summary table for Rev. 934 (latest table in §12 section)
# It starts at line 3729 with "Document version | Rev. 934"
old_table = """||||||| **Document version** | Rev. 934 | Header, §11, §12 synced ke git state aktual |
||||||||| **Git HEAD** | `85f7f81a0fa51f5c7439d783cb1daaf9878bb311` | "PRD Rev. 934 — fresh verification & metadata sync (04 November 2026 WIB); header, §11 Rev. 934 entry & §12 status summary synced to actual git state; HEAD 85f7f81a0fa51f5c7439d783cb1daaf9878bb311 (Rev. 934 final commit); commit count 1029/28/0 (1029 local commits, 28 ahead / 0 behind origin_main); node_modules present (477 top-level dirs / 84021 files); dev.db ada (schema-only via init_db.py; 15 tabel, seluruh record 0); seluruh data 453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions belum tersedia, import ulang dari init_db.py + init_schema.sql + sumber Excel/PDF). Build gate: tsc ✓ (exit 0); eslint ✓ (exit 0, 1 warning / 0 error); next build ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). Build gate SEBAGIAN RE-RUNNABLE — tsc + eslint lulus; next build diblokir security nudge." |
||||||||| **Commit count** | 1029/28/0 | 1029 local commits, 28 ahead / 0 behind origin_main |
||||||||| **Database (dev.db)** | Ada (schema-only) | 15 tabel, seluruh record 0; data 453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions belum tersedia, import ulang dari init_db.py + init_schema.sql + sumber Excel/PDF |
||||||||| **M02a NFC** | Field `uid_nfc` aktif, 0 terisi | Data ekspor NFC Tools belum tersedia |
||||||||| **Auth hardcoded** | Login.tsx: admin@pondokanbat.com / admin123 | Produksi butuh bcrypt + session |
||||||||| **Beranda hardcode** | totalSantri hardcode 453 | Belum fetch real-time dari DB |
||||||||| **Build gate** | SEBAGIAN RE-RUNNABLE | tsc ✓ (exit 0); eslint ✓ (exit 0, 1 warning); next build ✗ (SecurityFatalError) |
||||||||| **Repo state** | Working tree | 420 tracked files; 25 untracked (.check_env.py, .check_section12.py, .check_section12b.py, .check_section12full.py, .probe_db.py, _compare_head_prd.py, _diff_head_wt.py, _gate_build.py, _gate_eslint.py, _gate_tsc.py, _list_tables.py, dev.db_state.json, fix100020.py, fix_prd_900_final.py, home/workspace/dev/pondok-banat/.probe_db.py, probe_changelog.py, q_db.py, update_prd_906.py, update_prd_915.py, update_prd_930.py, update_prd_930_v2.py, update_prd_932.py); 0 deleted |"""

new_table = """||||||| **Document version** | Rev. 941 | Header, §11, §12 synced ke git state aktual |
||||||||| **Git HEAD** | `afffbb641187bb66d49b98be5e32741460cd50c8` | "PRD Rev. 941 — fresh verification & metadata sync (04 November 2026 WIB); header, §11 Rev. 941 entry & §12 status summary synced to actual git state; HEAD afffbb641187bb66d49b98be5e32741460cd50c8 (Rev. 940 final commit); commit count 1039/38/0 (1039 local commits, 38 ahead / 0 behind origin_main); node_modules present (477 top-level dirs / 84021 files); dev.db ada (schema-only via init_db.py; 15 tabel, seluruh record 0); seluruh data 453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions belum tersedia, import ulang dari init_db.py + init_schema.sql + sumber Excel/PDF). Build gate: tsc ✓ (exit 0); eslint ✓ (exit 0, 1 warning / 0 error); next build ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). Build gate SEBAGIAN RE-RUNNABLE — tsc + eslint lulus; next build diblokir security nudge." |
||||||||| **Commit count** | 1039/38/0 | 1039 local commits, 38 ahead / 0 behind origin_main |
||||||||| **Database (dev.db)** | Ada (schema-only) | 15 tabel, seluruh record 0; data 453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions belum tersedia, import ulang dari init_db.py + init_schema.sql + sumber Excel/PDF |
||||||||| **M02a NFC** | Field `uid_nfc` aktif, 0 terisi | Data ekspor NFC Tools belum tersedia |
||||||||| **Auth hardcoded** | Login.tsx: admin@pondokanbat.com / admin123 | Produksi butuh bcrypt + session |
||||||||| **Beranda hardcode** | totalSantri hardcode 453 | Belum fetch real-time dari DB |
||||||||| **Build gate** | SEBAGIAN RE-RUNNABLE | tsc ✓ (exit 0); eslint ✓ (exit 0, 1 warning); next build ✗ (SecurityFatalError) |
||||||||| **Repo state** | Working tree | 420 tracked files; 29 untracked (.check_env.py, .check_section12.py, .check_section12b.py, .check_section12full.py, .probe_db.py, .probe_state2.py, _compare_head_prd.py, _diff_head_wt.py, _gate_build.py, _gate_eslint.py, _gate_tsc.py, _list_tables.py, dev.db_state.json, fix100020.py, fix_930_section.py, fix_931_section13.py, fix_prd_900_final.py, home/, probe_changelog.py, probe_records.py, probe_state.py, q_db.py, sync_prd_931.py, update_prd_906.py, update_prd_915.py, update_prd_930.py, update_prd_930_v2.py, update_prd_932.py, update_prd_937_final.py); 0 deleted |"""

if old_table in content:
    content = content.replace(old_table, new_table)
    print("§12 status summary table updated to Rev. 941")
else:
    print("§12 table NOT FOUND")
    # Try to find it differently
    if "Document version** | Rev. 934" in content:
        print("  Found 'Document version | Rev. 934' but exact table not matched")
    else:
        print("  'Document version | Rev. 934' not found either")

with open(f, "w") as fh:
    fh.write(content)

print("Done")
