#!/usr/bin/env python3
with open('/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md', 'r') as f:
    content = f.read()

old_final_status = '> **Status:** dokumen PRD **REVISI** — rev 703: PRD fresh verification & stability confirmation (28 Oktober 2026 (WIB)); HEAD `fd81e38d231cfae6bed25d8f2a9e65649748348e` (Rev. 703 final commit); **715 / 11/0** (715 local commits, 11 ahead origin_main, 0 behind). State stabil, tidak ada perubahan signifikan dari Rev. 702 (data terkonsisten). Build gate: tsc ✓, eslint ✓ (1 warning), next build ✗ (SecurityFatalError Next.js 16.4.0).'

lines = content.split('\n')
for i, line in enumerate(lines, 1):
    if 'rev 703' in line and 'Status:' in line and '715' in line:
        print('Comparing script string vs file content:')
        for j, (a, b) in enumerate(zip(old_final_status, line)):
            if a != b:
                print(f'  Diff at position {j}:')
                print(f'    Script:  {repr(a)} (U+{ord(a):04X})')
                print(f'    File:    {repr(b)} (U+{ord(b):04X})')
                print(f'    Context: ...{old_final_status[max(0,j-20):j+20]!r}...')
                print(f'    FileCtx: ...{line[max(0,j-20):j+20]!r}...')
                break
        else:
            print('  Strings are same length and identical?')
            if len(old_final_status) == len(line):
                print('  Same length')
            else:
                print(f'  Different lengths: script={len(old_final_status)}, file={len(line)}')
        break
