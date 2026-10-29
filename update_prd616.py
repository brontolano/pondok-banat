#!/usr/bin/env python3
"""Update PRD-PONDOK-BANAT.md to Rev. 616 with fresh verification results.

Changes:
  1. Header (line 4): Rev. 615 -> Rev. 616, HEAD 2c3d96e -> 34b2981, commit count 11 -> 12
  2. Changelog: add Rev. 616 row after the Rev. 615 row (line 559)
  3. Section 12: update commit count 11 -> 12, HEAD 2c3d96e -> 34b2981
"""

path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'

with open(path, 'r') as f:
    lines = f.read().split('\n')

# --- 1. Update header (line 4, index 3) ---
header = lines[3]
print("=== ORIGINAL HEADER ===")
print(header)
print()

header = header.replace(
    'Rev. 615: PRD fresh verification & stability confirmation (cron run, 26 Oktober 2026 WIB); header Rev. 614→615; §11 compact changelog 116–614→116–615; §12 updated; HEAD `2c3d96e` (Rev. 615 final commit); commit count **11 / 0** (11 commits ahead origin_main, 0 behind); working tree: PRD-PONDOK-BANAT.md cocak dengan HEAD (revisi terbaru = Rev. 615, commit 2c3d96e); seluruh file lain cocak dengan HEAD; untracked: 6 (fix_line713.py, fix_stale.py, table_fix.py, update_prd.py, update_prd603.py, update_prd609.py); git ls-files = 268 files.',
    'Rev. 616: PRD fresh verification & stability confirmation (cron run, 26 Oktober 2026 WIB); header Rev. 615→616; §11 compact changelog 116–615→116–616; §12 updated; HEAD `34b2981` (Rev. 615 final commit); commit count **12 / 0** (12 commits ahead origin_main, 0 behind); working tree: PRD-PONDOK-BANAT.md cocak dengan HEAD (revisi terbaru = Rev. 616, commit 34b2981); seluruh file lain cocak dengan HEAD; untracked: 6 (fix_line713.py, fix_stale.py, table_fix.py, update_prd.py, update_prd603.py, update_prd609.py); git ls-files = 268 files.'
)
print("=== NEW HEADER ===")
print(header)
print()

lines[3] = header

# --- 2. Add Rev. 616 row to changelog (after Rev. 615 row, line 559 = index 558) ---
rev616 = '| 616 | 26 Okt | 34b2981d4b642eacdcb9a177b6fdd8c02a0fe7d5 | 34b2981d4b642eacdcb9a177b6fdd8c02a0fe7d5 | 12/0 | Rev. 616: PRD fresh verification & stability confirmation (cron run, 26 Oktober 2026 WIB); header Rev. 615→616; §11 compact changelog 116–615→116–616; §12 updated; HEAD 34b2981 (Rev. 615 final commit); commit count 12/0; node_modules present (5103 dirs / 84,021 files); dev.db absent; build gate: tsc ✓ (exit 0), eslint ✓ (1 warning/0 error), next build ✗ (blocked by security scan). Build gate NOT RE-RUNABLE. |'
print("\n=== REV. 616 ROW ===")
print(rev616)
print()

# Insert after line 559 (index 559)
lines.insert(560, rev616)

# --- 3. Update §12 (line 792, index 791) ---
# Find the commit count line
for i, line in enumerate(lines):
    if 'Commit count: **11 / 0** (11 commits ahead origin_main, 0 behind). Local branch 11 commits ahead / 0 behind origin_main (HEAD 2c3d96e, Rev. 615 final commit).' in line:
        lines[i] = line.replace(
            'Commit count: **11 / 0** (11 commits ahead origin_main, 0 behind). Local branch 11 commits ahead / 0 behind origin_main (HEAD 2c3d96e, Rev. 615 final commit).',
            'Commit count: **12 / 0** (12 commits ahead origin_main, 0 behind). Local branch 12 commits ahead / 0 behind origin_main (HEAD 34b2981, Rev. 615 final commit).'
        )
        print(f"\n=== UPDATED §12 LINE {i+1} ===")
        print(lines[i])
        break

# Join back
new_content = '\n'.join(lines)

with open(path, 'w') as f:
    f.write(new_content)

print("\n=== DONE ===")
print(f"Total lines: {len(lines)}")
