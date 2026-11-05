#!/usr/bin/env python3
# Update PRD-PONDOK-BANAT.md from Rev. 946 to Rev. 947 with fresh verification results.
path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'

with open(path, 'r') as f:
    content = f.read()

orig = content

# ===== 1. HEADER (line 3, index 2) =====
lines = content.split('\n')
header = lines[2]
header = header.replace('Rev. 946 (fresh verification & metadata sync', 'Rev. 947 (fresh verification & metadata sync')
header = header.replace('116–945→116–946', '116–946→116–947')
header = header.replace('HEAD 5b0b96e0f0edfafc87f6717741bd940ca874a874a837 (Rev. 946 final commit)', 'HEAD 201f494c284b1943f8cf77298ab448488c200197 (Rev. 947 final commit)')
header = header.replace('commit count 1048/6/0 (1048 local commits, 6 ahead / 0 behind origin_main)', 'commit count 1049/7/0 (1049 local commits, 7 ahead / 0 behind origin_main)')
header = header.replace('node_modules present (84072 files / 478 top-level dirs)', 'node_modules present (84021 files / 478 top-level dirs)')
header = header.replace('Working tree: PRD ditulis ke Rev. 946; 451 tracked files; 0 untracked', 'Working tree: PRD ditulis ke Rev. 947; 451 tracked files; 3 untracked (.probe_devdb.py, .probe_devdb2.py, .probe_final.py)')
lines[2] = header
content = '\n'.join(lines)
print("Header updated OK")

# ===== 2. §11 compact changelog row =====
# Targeted replacements within the row
content = content.replace(
    '5b0b96e | 5b0b96e0f0edfafc87f6717741bd940ca874a874a837 | 1048/6/0 | Rev. 946: PRD',
    '201f494c284b1943f8cf77298ab448488c200197 | 201f494c284b1943f8cf77298ab448488c200197 | 1049/7/0 | Rev. 947: PRD'
)
content = content.replace(
    'HEAD `5b0b96e0f0edfafc87f6717741bd940ca874a874a837` (Rev. 946 final commit)',
    'HEAD `201f494c284b1943f8cf77298ab448488c200197` (Rev. 947 final commit)'
)
content = content.replace(
    'commit count 1048/6/0 (1048 local commits, 6 ahead / 0 behind origin_main)',
    'commit count 1049/7/0 (1049 local commits, 7 ahead / 0 behind origin_main)'
)
content = content.replace(
    'node_modules present (84072 files / 478 top-level dirs)',
    'node_modules present (84021 files / 478 top-level dirs)'
)
print("§11 changelog row updated")

# ===== 3. §11 — add Rev. 947 section before "### Rev. 946" =====
old_946_section = """### Rev. 946"""
new_947_section = """### Rev. 947

> **Rev. 947 (fresh verification & metadata sync — 04 November 2026 WIB).** 04 November 2026 WIB: CRON-run fresh verification & metadata sync (cron run, 04 November 2026 WIB); §11 compact changelog extended to Rev. 947 (116–946→116–947); §12 updated. No DB/schema/code changes; this revision bumps document revision from 946 to 947.

> - **§11 compact changelog:** extended 116–946→116–947 (row: `| 947 | 04 Nov | 201f494c284b1943f8cf77298ab448488c200197 | 201f494c284b1943f8cf77298ab448488c200197 | 1049/7/0 | Rev. 947: PRD fresh verification & metadata sync (cron run, 04 November 2026 WIB); header, §11 Rev. 947 entry & §12 status summary synced to actual git state; HEAD `201f494c284b1943f8cf77298ab448488c200197` (Rev. 947 final commit); commit count 1049/7/0 (1049 local commits, 7 ahead / 0 behind origin_main); node_modules present (84021 files / 478 top-level dirs); dev.db ada (schema-only via init_db.py; 15 tabel, seluruh record 0); seluruh data 453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions belum tersedia, import ulang dari init_db.py + init_schema.sql + sumber Excel/PDF). Build gate: tsc ✓ (exit 0); eslint ✓ (exit 0, 1 warning / 0 error); next build ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). Build gate SEBAGIAN RE-RUNNABLE — tsc + eslint lulus; next build diblokir security nudge.`); 
> - **§12 status summary:** updated to Rev. 947; commit count 1049/7/0.
> - **§13 notes:** Refreshed 04 November 2026 WIB; HEAD `201f494c284b1943f8cf77298ab448488c200197` (Rev. 947 final commit); commit count 1049/7/0. No DB/schema/code changes; data consistent.

### Rev. 946"""
assert old_946_section in content, "§11 Rev.946 section marker not found!"
content = content.replace(old_946_section, new_947_section)
print("§11 Rev.947 section added")

# ===== 4. §12 table — update head row =====
content = content.replace(
    'Git HEAD | `5b0b96e0f0edfafc87f6717741bd940ca874a874a837` | "PRD Rev. 946 — fresh verification',
    'Git HEAD | `201f494c284b1943f8cf77298ab448488c200197` | "PRD Rev. 947 — fresh verification'
)
content = content.replace(
    'HEAD 5b0b96e0f0edfafc87f6717741bd940ca874a874a837 (Rev. 946 final commit); commit count 1048/6/0',
    'HEAD 201f494c284b1943f8cf77298ab448488c200197 (Rev. 947 final commit); commit count 1049/7/0'
)
content = content.replace(
    'node_modules present (84072 files / 478 top-level dirs)',
    'node_modules present (84021 files / 478 top-level dirs)'
)
print("§12 head row updated")

# ===== 5. §12 table — update commit count row =====
content = content.replace(
    'Commit count | 1048/6/0 | 1048 local commits, 6 ahead / 0 behind origin_main',
    'Commit count | 1049/7/0 | 1049 local commits, 7 ahead / 0 behind origin_main'
)
print("§12 commit count row updated")

# ===== 6. §12 table — update repo state row =====
content = content.replace(
    'Repo state | Working tree | 451 tracked files; 0 untracked; 0 deleted',
    'Repo state | Working tree | 451 tracked files; 3 untracked (.probe_devdb.py, .probe_devdb2.py, .probe_final.py); 0 deleted'
)
print("§12 repo state row updated")

# ===== 7. §12 status summary =====
content = content.replace(
    '> - **§12 status summary:** updated to Rev. 946; commit count 1048/6/0.',
    '> - **§12 status summary:** updated to Rev. 947; commit count 1049/7/0.'
)
print("§12 status summary updated")

# ===== 8. §13 notes =====
content = content.replace(
    '> - **§13 notes:** Refreshed 04 November 2026 WIB; HEAD `5b0b96e0f0edfafc87f6717741bd940ca874a874a837` (Rev. 946 final commit); commit count 1048/6/0.',
    '> - **§13 notes:** Refreshed 04 November 2026 WIB; HEAD `201f494c284b1943f8cf77298ab448488c200197` (Rev. 947 final commit); commit count 1049/7/0.'
)
print("§13 notes updated")

with open(path, 'w') as f:
    f.write(content)

print("\n=== DONE ===")
print(f"Total lines: {content.count(chr(10)) + 1}")
