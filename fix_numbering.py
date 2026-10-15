#!/usr/bin/env python3
"""Fix numbering in PRD after Rev 19/20 updates."""
path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find and fix the problematic lines
for i, line in enumerate(lines):
    if '7. **Build quality gate:**' in line and '5. **Rev. 19' in lines[i-2]:
        # This is Rev. 19's build quality gate - should be 8.
        lines[i] = line.replace('7. **Build quality gate:**', '8. **Build quality gate:**')
        print(f'Fixed line {i+1}: Rev. 19 build quality gate -> 8.')
    if '5. **Rev. 20 — 14 Oktober 2026' in line:
        # This is Rev. 20 heading - should be 6.
        lines[i] = line.replace('5. **Rev. 20 — 14 Oktober 2026', '6. **Rev. 20 — 14 Oktober 2026')
        print(f'Fixed line {i+1}: Rev. 20 heading -> 6.')

# Also fix "6. Beranda placeholder" under Rev. 19 -> "7." 
# It's already 6., need to check context
for i, line in enumerate(lines):
    if '**sudah diupdate** ke nilai DB aktual (441/54/18) — `grep` konfirmasi: `totalSantri: 441`' in line:
        # Check if next line is "6. **Struktur kode:**" - if so, this "6." should be "7."
        if i+1 < len(lines) and '6. **Struktur kode:**' in lines[i+1]:
            lines[i] = line.replace('6. **Beranda placeholder:**', '7. **Beranda placeholder:**')
            print(f'Fixed line {i+1}: Beranda placeholder -> 7.')

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(lines)
print('Done')
