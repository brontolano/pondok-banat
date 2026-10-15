#!/usr/bin/env python3
"""Final cleanup and verification."""
import os

BASE = "/opt/data/home/workspace/dev/pondok-banat"

# Clean up temp scripts
for f in ['.verify_fresh61.py', '.update_prd61.py', '.fix_header61.py',
          '.fix_header61b.py', '.fix_header61c.py', '.fix_header61d.py']:
    p = os.path.join(BASE, f)
    if os.path.exists(p):
        os.remove(p)
        print('Removed:', f)

print()
print('Final file state:')
with open(os.path.join(BASE, 'PRD-PONDOK-BANAT.md')) as f:
    lines = f.readlines()
print('  PRD lines:', len(lines))
print('  PRD size:', os.path.getsize(os.path.join(BASE, 'PRD-PONDOK-BANAT.md')))
print('  PRD backup size:', os.path.getsize(os.path.join(BASE, 'PRD-PONDOK-BANAT.md.bak')))
print()
print('Header (line 4):', lines[3][:170])
print()
# Find Rev. 61 section
for i, line in enumerate(lines, 1):
    if line.startswith('## 20.'):
        print('Rev. 61 section at line', i)
        break
print()
print('Done.')
