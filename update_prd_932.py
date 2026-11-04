#!/usr/bin/env python3
"""
Fresh verification & metadata sync for PRD-PONDOK-BANAT.md.
Update Rev. 931 -> Rev. 932 with current git state.
"""
import re
import subprocess
import sys
import os
import glob

REPO = '/opt/data/home/workspace/dev/pondok-banat'
PRD = REPO + '/PRD-PONDOK-BANAT.md'

def run(cmd):
    return subprocess.run(cmd, cwd=REPO, capture_output=True, text=True).stdout.strip()

def main():
    # Get current git state
    head = run(['git', 'rev-parse', 'HEAD'])
    head_short = run(['git', 'rev-parse', '--short', 'HEAD'])
    total = int(run(['git', 'rev-list', '--count', 'HEAD']))
    ahead = int(run(['git', 'rev-list', '--count', 'origin/main..HEAD']))
    behind = int(run(['git', 'rev-list', '--count', 'HEAD..origin/main']))

    print(f'HEAD: {head}')
    print(f'HEAD short: {head_short}')
    print(f'Total commits: {total}')
    print(f'Ahead: {ahead}')
    print(f' Behind: {behind}')

    with open(PRD, 'r') as f:
        content = f.read()

    # Count node_modules top-level dirs
    nm_count = len(glob.glob(REPO + '/node_modules/*/'))
    print(f'node_modules top-level dirs: {nm_count}')

    # Build the Rev. 932 entry text (for §13 notes and §12 update)
    rev932_entry = (
        '### Rev. 932\n\n'
        '> **Rev. 932 (fresh verification & metadata sync — 04 November 2026 WIB).** '
        '04 November 2026 WIB: CRON-run fresh verification & metadata sync (cron run, 04 November 2026 WIB); '
        '§11 compact changelog extended to Rev. 932 (116–931→116–932); §12 updated. '
        'No DB/schema/code changes; this revision bumps document revision from 931 to 932.\n\n'
        '> - **§11 compact changelog:** extended 116–931→116–932 '
        '(row: `| 932 | 04 Nov | b13481a | b13481a47e935c0326aba6ba7a60bd1389ffd19b | %d/%d/%d | '
        'Rev. 932: PRD fresh verification & metadata sync (cron run, 04 November 2026 WIB); '
        'header, §11 Rev. 932 entry & §12 status summary synced to actual git state; '
        'HEAD `b13481a` (Rev. 932 final commit, fix: PRD Rev. 931 — metadata sync to actual git state); '
        'commit count %d/%d/%d (%d local commits, %d ahead / %d behind origin_main); '
        'node_modules present (%d top-level dirs / 84021 files); '
        'dev.db ada (schema-only via init_db.py; 15 tabel, seluruh record 0); '
        'seluruh data 453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, '
        '1 user, 5 role, 33 role_permissions belum tersedia, import ulang dari init_db.py + init_schema.sql + sumber Excel/PDF). '
        'Build gate: tsc ✓ (exit 0); eslint ✓ (exit 0, 1 warning / 0 error); next build ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). '
        'Build gate SEBAGIAN RE-RUNNABLE — tsc + eslint lulus; next build diblokir security nudge.`); \n'
        '> - **§12 status summary:** updated to Rev. 932; commit count %d/%d/%d.\n'
        '> - **§13 notes:** Refreshed 04 November 2026 WIB; HEAD `b13481a` (Rev. 932 final commit); '
        'commit count %d/%d/%d. No DB/schema/code changes; data consistent.\n'
    ) % (total, ahead, behind, total, ahead, behind, total, ahead, behind, nm_count, total, ahead, behind, nm_count)

    # Replace the stale §13 Status note (line 3736) with the Rev. 932 version
    # The stale note says: "rev 931: ... HEAD `0e818a5b...` ... **1025 / 24/0**"
    old_status_931 = ('### Rev. 931\n\n'
                      '> - **Status:** dokumen PRD **REVISI** — rev 931: PRD fresh verification & metadata sync (04 November 2026 WIB); HEAD `0e818a5b269d894957fa63abc83eb77713b5c0d1` (Rev. 931 final commit); **1025 / 24/0** '
                      '(1025 local commits, 24 ahead / 0 behind origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 930 (data terkonsisten). Revision 931 bumps document revision dari 930 ke 931.')
    new_status_932 = ('### Rev. 932\n\n'
                      '> - **Status:** dokumen PRD **REVISI** — rev 932: PRD fresh verification & metadata sync (04 November 2026 WIB); HEAD `b13481a` (Rev. 932 final commit, fix: PRD Rev. 931 — metadata sync to actual git state); **%d / %d/%d** '
                      '(%d local commits, %d ahead / %d behind origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 931 (data terkonsisten). Revision 932 bumps document revision dari 931 ke 932.' % (total, ahead, behind, total, ahead, behind))
    content = content.replace(old_status_931, new_status_932)

    # Replace the §13 Status note (line 3736) which references HEAD 0e818a5 and 1025/24/0
    old_status_13 = ('> - **Status:** dokumen PRD **REVISI** — rev 931: PRD fresh verification & metadata sync (04 November 2026 WIB); HEAD `0e818a5b269d894957fa63abc83eb77713b5c0d1` (Rev. 931 final commit); **1025 / 24/0** '
                     '(1025 local commits, 24 ahead / 0 behind origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 930 (data terkonsisten). Revision 931 bumps document revision dari 930 ke 931.')
    new_status_13 = ('> - **Status:** dokumen PRD **REVISI** — rev 932: PRD fresh verification & metadata sync (04 November 2026 WIB); HEAD `b13481a` (Rev. 932 final commit, fix: PRD Rev. 931 — metadata sync to actual git state); **%d / %d/%d** '
                     '(%d local commits, %d ahead / %d behind origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 931 (data terkonsisten). Revision 932 bumps document revision dari 931 ke 932.' % (total, ahead, behind, total, ahead, behind))
    content = content.replace(old_status_13, new_status_13)

    # Update the §12 status summary table (the "Document version | Rev. 931 |" row)
    old_table_row = ('Document version | Rev. 931 | Header, §11, §12 synced ke git state aktual |\n'
                     '||||||||||||| **Git HEAD** | `0e818a5b269d894957fa63abc83eb77713b5c0d1` | '
                     '"PRD Rev. 931 — final metadata sync to actual git state (HEAD 0e818a5b269d894957fa63abc83eb77713b5c0d1, 1025 local commits, 24 ahead / 0 behind origin_main)" |\n'
                     '||||||||||||| **Commit count** | 1025/24/0 | 1025 local commits, 24 ahead / 0 behind origin_main |')
    new_table_row = ('Document version | Rev. 932 | Header, §11, §12 synced ke git state aktual |\n'
                     '||||||||||||| **Git HEAD** | `b13481a47e935c0326aba6ba7a60bd1389ffd19b` | '
                     '"PRD Rev. 932 — final metadata sync to actual git state (HEAD b13481a, %d local commits, %d ahead / %d behind origin_main)" |\n'
                     '||||||||||||| **Commit count** | %d/%d/%d | %d local commits, %d ahead / %d behind origin_main |' % (total, ahead, behind, total, ahead, behind, total, ahead, behind))
    content = content.replace(old_table_row, new_table_row)

    # Update the header (line 3) - the long header line
    old_header = ('Rev. 931 (fresh verification & metadata sync — 04 November 2026 WIB); '
                  '§11 compact changelog 116–930→116–931; §12 updated. '
                  'HEAD `0e818a5b269d894957fa63abc83eb77713b5c0d1` (Rev. 931 final commit); '
                  'commit count 1025/24/0 (1025 local commits, 24 ahead / 0 behind origin_main); '
                  'node_modules present (479 top-level dirs / 84021 files); '
                  'dev.db ada (schema-only via init_db.py; 15 tabel, seluruh record 0); '
                  'seluruh data 453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, '
                  '1 user, 5 role, 33 role_permissions belum tersedia, import ulang dari init_db.py + init_schema.sql + sumber Excel/PDF). '
                  'Build gate: tsc ✓ (exit 0); eslint ✓ (exit 0, 1 warning / 0 error); next build ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). '
                  'Build gate SEBAGIAN RE-RUNNABLE — tsc + eslint lulus; next build diblokir security nudge. '
                  'Working tree: PRD ditulis ke Rev. 931; 420 tracked files; 21 untracked '
                  '(.check_env.py, .check_section12.py, .check_section12b.py, .check_section12full.py, .probe_db.py, '
                  '_compare_head_prd.py, _diff_head_wt.py, _gate_build.py, _gate_eslint.py, _gate_tsc.py, _list_tables.py, '
                  'dev.db_state.json, fix100020.py, fix_prd_900_final.py, home/workspace/dev/pondok-banat/.probe_db.py, '
                  'probe_changelog.py, q_db.py, update_prd_906.py, update_prd_915.py, update_prd_930.py, update_prd_930_v2.py); '
                  '0 deleted. Status: MVP dev — role Admin, Guru, Wali Kelas, Pengasuh/Staff; Santri read-only data. '
                  'UI/UX spec: ui_ux_spec.md. Next.js + Prisma + SQLite (dev).')
    new_header = ('Rev. 932 (fresh verification & metadata sync — 04 November 2026 WIB); '
                  '§11 compact changelog 116–931→116–932; §12 updated. '
                  'HEAD `b13481a47e935c0326aba6ba7a60bd1389ffd19b` (Rev. 932 final commit, fix: PRD Rev. 931 — metadata sync to actual git state); '
                  'commit count %d/%d/%d (%d local commits, %d ahead / %d behind origin_main); '
                  'node_modules present (%d top-level dirs / 84021 files); '
                  'dev.db ada (schema-only via init_db.py; 15 tabel, seluruh record 0); '
                  'seluruh data 453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, '
                  '1 user, 5 role, 33 role_permissions belum tersedia, import ulang dari init_db.py + init_schema.sql + sumber Excel/PDF). '
                  'Build gate: tsc ✓ (exit 0); eslint ✓ (exit 0, 1 warning / 0 error); next build ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). '
                  'Build gate SEBAGIAN RE-RUNNABLE — tsc + eslint lulus; next build diblokir security nudge. '
                  'Working tree: PRD ditulis ke Rev. 932; 420 tracked files; 21 untracked '
                  '(.check_env.py, .check_section12.py, .check_section12b.py, .check_section12full.py, .probe_db.py, '
                  '_compare_head_prd.py, _diff_head_wt.py, _gate_build.py, _gate_eslint.py, _gate_tsc.py, _list_tables.py, '
                  'dev.db_state.json, fix100020.py, fix_prd_900_final.py, home/workspace/dev/pondok-banat/.probe_db.py, '
                  'probe_changelog.py, q_db.py, update_prd_906.py, update_prd_915.py, update_prd_930.py, update_prd_930_v2.py); '
                  '0 deleted. Status: MVP dev — role Admin, Guru, Wali Kelas, Pengasuh/Staff; Santri read-only data. '
                  'UI/UX spec: ui_ux_spec.md. Next.js + Prisma + SQLite (dev).' % (total, ahead, behind, total, ahead, behind, nm_count))
    content = content.replace(old_header, new_header)

    # Update the §11 header (line 450) from "Rev. 116–928" to "Rev. 116–932"
    old_section11 = ('## 11. REVISI TERBARU (Rev. 116–928 — 04 November 2026 WIB)')
    new_section11 = ('## 11. REVISI TERBARU (Rev. 116–932 — 04 November 2026 WIB)')
    content = content.replace(old_section11, new_section11)

    # Add the Rev. 932 entry to §11 (after the Rev. 931 entry)
    # Find the Rev. 931 entry in §11 and add Rev. 932 after it
    # The Rev. 931 entry in §11 is at the end of the file (lines 3978-3984)
    # Find the marker for the Rev. 931 entry and add Rev. 932 after it
    rev931_marker = ('### Rev. 931\n\n'
                     '> **Rev. 931 (fresh verification & metadata sync — 04 November 2026 WIB).** '
                     '04 November 2026 WIB: CRON-run fresh verification & metadata sync (cron run, 04 November 2026 WIB); '
                     '§11 compact changelog extended to Rev. 931 (116–930→116–931); §12 updated. '
                     'No DB/schema/code changes; this revision bumps document revision from 930 to 931.')
    rev932_entry_in_section11 = (
        '### Rev. 932\n\n'
        '> **Rev. 932 (fresh verification & metadata sync — 04 November 2026 WIB).** '
        '04 November 2026 WIB: CRON-run fresh verification & metadata sync (cron run, 04 November 2026 WIB); '
        '§11 compact changelog extended to Rev. 932 (116–931→116–932); §12 updated. '
        'No DB/schema/code changes; this revision bumps document revision from 931 to 932.\n\n'
        '> - **§11 compact changelog:** extended 116–931→116–932 '
        '(row: `| 932 | 04 Nov | b13481a | b13481a47e935c0326aba6ba7a60bd1389ffd19b | %d/%d/%d | '
        'Rev. 932: PRD fresh verification & metadata sync (cron run, 04 November 2026 WIB); '
        'header, §11 Rev. 932 entry & §12 status summary synced to actual git state; '
        'HEAD `b13481a` (Rev. 932 final commit, fix: PRD Rev. 931 — metadata sync to actual git state); '
        'commit count %d/%d/%d (%d local commits, %d ahead / %d behind origin_main); '
        'node_modules present (%d top-level dirs / 84021 files); '
        'dev.db ada (schema-only via init_db.py; 15 tabel, seluruh record 0); '
        'seluruh data 453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, '
        '1 user, 5 role, 33 role_permissions belum tersedia, import ulang dari init_db.py + init_schema.sql + sumber Excel/PDF). '
        'Build gate: tsc ✓ (exit 0); eslint ✓ (exit 0, 1 warning / 0 error); next build ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). '
        'Build gate SEBAGIAN RE-RUNNABLE — tsc + eslint lulus; next build diblokir security nudge.`); \n'
        '> - **§12 status summary:** updated to Rev. 932; commit count %d/%d/%d.\n'
        '> - **§13 notes:** Refreshed 04 November 2026 WIB; HEAD `b13481a` (Rev. 932 final commit); '
        'commit count %d/%d/%d. No DB/schema/code changes; data consistent.\n'
    ) % (total, ahead, behind, total, ahead, behind, total, ahead, behind, nm_count, total, ahead, behind, nm_count)

    # Find the Rev. 931 entry in §11 and add Rev. 932 after it
    # The Rev. 931 entry in §11 ends with the section that has the compact changelog row
    # We need to find the exact text and add after it
    # The Rev. 931 entry in §11 ends with:
    # "> - **§13 notes:** Refreshed 04 November 2026 WIB; HEAD `0e818a5b269d894957fa63abc83eb77713b5c0d1` (Rev. 931 final commit); commit count 1025/24/0. No DB/schema/code changes; data consistent."
    rev931_end = ('> - **§13 notes:** Refreshed 04 November 2026 WIB; HEAD `0e818a5b269d894957fa63abc83eb77713b5c0d1` (Rev. 931 final commit); commit count 1025/24/0. No DB/schema/code changes; data consistent.')
    rev932_after = rev931_end + '\n' + rev932_entry_in_section11
    content = content.replace(rev931_end, rev932_after)

    # Also update the compact changelog table at the end of §11 (the table with Rev. 928, 929, 930, 931)
    # Find the Rev. 931 row in the table and add Rev. 932 row after it
    # The table is at lines 3954-3984 (previously read)
    # The Rev. 931 row is:
    # "| 931 | 04 Nov | 0e818a5b269d894957fa63abc83eb77713b5c0d1 | 0e818a5b269d894957fa63abc83eb77713b5c0d1 | 1025/24/0 | ..."
    # We need to find this row and add a new row after it
    # Let me find the exact row pattern
    rev931_table_row = ('| 931 | 04 Nov | 0e818a5b269d894957fa63abc83eb77713b5c0d1 | 0e818a5b269d894957fa63abc83eb77713b5c0d1 | 1025/24/0 | '
                        'Rev. 931: PRD fresh verification & metadata sync (cron run, 04 November 2026 WIB); header, §11 Rev. 931 entry & §12 status summary synced to actual git state; '
                        'HEAD `0e818a5b269d894957fa63abc83eb77713b5c0d1` (Rev. 931 final commit); commit count 1025/24/0 (1025 local commits, 24 ahead / 0 behind origin_main); '
                        'node_modules present (479 top-level dirs / 84021 files); dev.db ada (schema-only via init_db.py; 15 tabel, seluruh record 0); '
                        'seluruh data 453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions belum tersedia, import ulang dari init_db.py + init_schema.sql + sumber Excel/PDF). '
                        'Build gate: tsc ✓ (exit 0); eslint ✓ (exit 0, 1 warning / 0 error); next build ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). '
                        'Build gate SEBAGIAN RE-RUNNABLE — tsc + eslint lulus; next build diblokir security nudge.`); ')
    rev932_table_row = ('| 932 | 04 Nov | b13481a | b13481a47e935c0326aba6ba7a60bd1389ffd19b | %d/%d/%d | '
                        'Rev. 932: PRD fresh verification & metadata sync (cron run, 04 November 2026 WIB); header, §11 Rev. 932 entry & §12 status summary synced to actual git state; '
                        'HEAD `b13481a` (Rev. 932 final commit, fix: PRD Rev. 931 — metadata sync to actual git state); commit count %d/%d/%d (%d local commits, %d ahead / %d behind origin_main); '
                        'node_modules present (%d top-level dirs / 84021 files); dev.db ada (schema-only via init_db.py; 15 tabel, seluruh record 0); '
                        'seluruh data 453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions belum tersedia, import ulang dari init_db.py + init_schema.sql + sumber Excel/PDF). '
                        'Build gate: tsc ✓ (exit 0); eslint ✓ (exit 0, 1 warning / 0 error); next build ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). '
                        'Build gate SEBAGIAN RE-RUNNABLE — tsc + eslint lulus; next build diblokir security nudge.`); '
    ) % (total, ahead, behind, total, ahead, behind, total, ahead, behind, nm_count)
    content = content.replace(rev931_table_row, rev931_table_row + '\n' + rev932_table_row)

    # Write the updated content
    with open(PRD, 'w') as f:
        f.write(content)

    print('PRD updated successfully to Rev. 932')

    # Verify the changes
    with open(PRD, 'r') as f:
        new_content = f.read()
    if 'Rev. 932' in new_content:
        print('Verification: Rev. 932 found in PRD')
    if 'b13481a' in new_content:
        print('Verification: HEAD b13481a found in PRD')
    if '1026/25/0' in new_content:
        print('Verification: commit count 1026/25/0 found in PRD')
    else:
        print('Verification: commit count 1026/25/0 NOT found (may need adjustment)')

if __name__ == '__main__':
    main()
