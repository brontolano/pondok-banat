#!/usr/bin/env python3
with open('/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md', 'r') as f:
    content = f.read()

# The exact old_final_status string from the script
old_final_status = '> **Status:** dokumen PRD **REVISI** — rev 703: PRD fresh verification & stability confirmation (28 Oktober 2026 (WIB)); HEAD `fd81e38d231cfae6bed25d8f2a9e65649748348e` (Rev. 703 final commit); **715 / 11/0** (715 local commits, 11 ahead origin_main, 0 behind). State stabil, tidak ada perubahan signifikan dari Rev. 702 (data terkonsisten). Build gate: tsc ✓, eslint ✓ (1 warning), next build ✗ (SecurityFatalError Next.js 16.4.0).'

# Find the line 1479 content
lines = content.split('\n')
for i, line in enumerate(lines, 1):
    if 'rev 703' in line and 'Status:' in line and '715' in line:
        print(f'Line {i}:')
        print('  Script string:  ', repr(old_final_status))
        print('  File content:   ', repr(line))
        print('  Match:          ', old_final_status == line)
        break
