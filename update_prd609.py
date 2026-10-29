#!/usr/bin/env python3
"""Update PRD-PONDOK-BANAT.md with fresh verification results."""

path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'

with open(path, 'r') as f:
    lines = f.read().split('\n')

# --- 1. Update header (line 4, index 3) ---
header = lines[3]
print("=== ORIGINAL HEADER ===")
print(header)
print()

# Apply header replacements
header = header.replace(
    '> Rev. 607: PRD fresh verification & stability confirmation (cron run, 26 Oktober 2026 WIB); header Rev. 606→607; §11 compact changelog 116–606→116–607; §12 updated; HEAD `0b0bc902e0bc016db469812094b0c73b1969825c` (Rev. 607 final commit); commit count **38 / 0** (38 commits ahead origin_main, 0 behind); working tree: PRD-PONDOK-BANAT.md cocak dengan HEAD (revisi terbaru = Rev. 607, commit 0b0bc902e0bc016db469812094b0c73b1969825c); seluruh file lain cocak dengan HEAD; untracked: 5 (fix_line713.py, fix_stale.py, table_fix.py, update_prd.py, update_prd603.py); git ls-files = 268 files.',
    '> Rev. 609: PRD fresh verification & stability confirmation (cron run, 26 Oktober 2026 WIB); header Rev. 608→609; §11 compact changelog 116–608→116–609; §12 updated; HEAD `afaa46a` (Rev. 608 final commit); commit count **39 / 0** (39 commits ahead origin_main, 0 behind); working tree: PRD-PONDOK-BANAT.md cocak dengan HEAD (revisi terbaru = Rev. 609, commit afaa46a); seluruh file lain cocak dengan HEAD; untracked: 5 (fix_line713.py, fix_stale.py, table_fix.py, update_prd.py, update_prd603.py); git ls-files = 268 files.'
)
print("=== NEW HEADER ===")
print(header)
print()

lines[3] = header

# --- 2. Add Rev. 608 and Rev. 609 rows to the table ---
# Find the Rev. 607 row (index 548, line 550)
print("\n=== TABLE ROW 550 (index 549) ===")
print(repr(lines[549]))
print()

rev608 = '| 608 | 26 Okt | afaa46a | afaa46a | 39/0 | Rev. 608: PRD fresh verification & stability confirmation (cron run, 26 Oktober 2026 WIB); header Rev. 607→608; §11 compact changelog 116–607→116–608; §12 updated; HEAD afaa46a (Rev. 607 final commit); commit count 39/0; node_modules present (477 dirs / 84,021 files); dev.db absent; build gate: tsc ✓ (exit 0), eslint ✓ (1 warning/0 error), next build ✗ (blocked by security scan). Build gate NOT RE-RUNABLE. |'
rev609 = '| 609 | 26 Okt | afaa46a94a8fd45750505800f382bd042493387f | afaa46a94a8fd45750505800f382bd042493387f | 39/0 | Rev. 609: PRD fresh verification & stability confirmation (cron run, 26 Oktober 2026 WIB); header Rev. 608→609; §11 compact changelog 116–608→116–609; §12 updated; HEAD afaa46a94a8fd45750505800f382bd042493387f (Rev. 609 final commit); commit count 39/0; node_modules present (477 dirs / 84,021 files); dev.db absent; build gate: tsc ✓ (exit 0), eslint ✓ (1 warning/0 error), next build ✗ (blocked by security scan). Build gate NOT RE-RUNABLE. |'

# Insert after the Rev. 607 row (index 549)
lines.insert(550, rev609)
lines.insert(549, rev608)

# --- 3. Update §12 (line 783, index 782) ---
# Find the commit count line
for i, line in enumerate(lines):
    if 'Commit count: **38 / 0**' in line:
        lines[i] = line.replace('Commit count: **38 / 0** (38 commits ahead origin_main, 0 behind). Branch 38 commits ahead of origin/main (ed6551d, Rev. 583).',
                                 'Commit count: **39 / 0** (39 commits ahead origin_main, 0 behind). Branch 39 commits ahead of origin/main (ed6551d, Rev. 583).')
        print(f"\n=== UPDATED §12 LINE {i+1} ===")
        print(lines[i])
        break

# Join back
new_content = '\n'.join(lines)

with open(path, 'w') as f:
    f.write(new_content)

print("\n=== DONE ===")
print(f"Total lines: {len(lines)}")
