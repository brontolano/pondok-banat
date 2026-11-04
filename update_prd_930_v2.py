#!/usr/bin/env python3
# Update PRD-PONDOK-BANAT.md to Rev. 930 - v2 (correct §12 replacement)
# The §12 table is a nested markdown table. We replace the entire table region
# (lines 3654-3722) with a new version that appends a Rev. 930 block.

path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'
with open(path, 'r') as f:
    lines = f.readlines()

# Find the §12 table region (starts at line 3654, ends at line 3722)
# These are 1-indexed line numbers in the original file
start_line = 3653  # 0-indexed, line 3654
end_line = 3721    # 0-indexed, line 3722 (inclusive)

# Verify the boundary
assert lines[start_line].startswith('|||---|---|---|'), f"Start mismatch: {lines[start_line]!r}"
assert lines[end_line].startswith('|||||||||'), f"End mismatch: {lines[end_line]!r}"

# Build the new §12 table. We keep all existing blocks and append the Rev. 930 block.
# The new block uses the same pipe format as the Rev. 926 block at the end.

new_block_930 = [
    '|||| **Parameter** | Status | Detail |\n',
    '||||| **Document version** | Rev. 930 | Header, §11, §12 synced ke git state aktual |\n',
    '|||||||| **Git HEAD** | `d6b0b04` | "PRD Rev. 930 — fresh verification & stability confirmation (04 November 2026 WIB); HEAD d6b0b04; commit count 1023/22/0" |\n',
    '|||||||| **Commit count** | 1023/22/0 | 1023 local commits, 22 ahead / 0 behind origin_main |\n',
    '|||||||| **Database (dev.db)** | Ada (schema-only) | 15 tabel, seluruh record 0; data 453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions belum tersedia |\n',
    '|||||||| **M02a NFC** | Field `uid_nfc` aktif, 0 terisi | Data ekspor NFC Tools belum tersedia |\n',
    '|||||||| **Auth hardcode** | Login.tsx: admin@pondokanbat.com / admin123 | Produksi butuh bcrypt + session |\n',
    '|||||||| **Beranda hardcode** | totalSantri hardcode 453 | Belum fetch real-time dari DB |\n',
    '|||||||| **Build gate** | SEBAGIAN RE-RUNNABLE | tsc ✓ (exit 0); eslint ✓ (exit 0, 1 warning); next build ✗ (SecurityFatalError) |\n',
    '||||| **Repo state** | Working tree | 420 tracked files; 15 untracked (_compare_head_prd.py, _diff_head_wt.py, _gate_build.py, _gate_eslint.py, _gate_tsc.py, _list_tables.py, dev.db_state.json, fix100020.py, fix_prd_900_final.py, probe_changelog.py, q_db.py, update_prd_906.py, update_prd_915.py, .probe_db.py, home/workspace/dev/pondok-banat/.probe_db.py, .verify_rev930.py, .check_env.py); 0 deleted |\n',
]

# Check: does the new block end with `||||| **Repo state** | ... |`?
assert new_block_930[-1].startswith('||||| **Repo state**'), f"Block end mismatch: {new_block_930[-1]!r}"

# Build the replacement: replace lines start_line to end_line (inclusive) with new_block_930
new_lines = lines[:start_line] + new_block_930 + lines[end_line + 1:]

# Verify
new_content = ''.join(new_lines)
assert 'Rev. 930' in new_content, "Rev. 930 not in new content!"
assert '1023/22/0' in new_content, "1023/22/0 not in new content!"

with open(path, 'w') as f:
    f.write(new_content)

print("§12 table updated successfully with Rev. 930 block")
print(f"File lines: {len(new_lines)}")
