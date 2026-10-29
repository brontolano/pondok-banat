#!/usr/bin/env python3
with open('/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md', 'r') as f:
    content = f.read()

# Check the exact old_final_status string
old_final_status = '> **Status:** dokumen PRD **REVISI** — rev 703: PRD fresh verification & stability confirmation (28 Oktober 2026 (WIB)); HEAD `fd81e38d231cfae6bed25d8f2a9e65649748348e` (Rev. 703 final commit); **715 / 11/0** (715 local commits, 11 ahead origin_main, 0 behind). State stabil, tidak ada perubahan signifikan dari Rev. 702 (data terkonsisten). Build gate: tsc ✓, eslint ✓ (1 warning), next build ✗ (SecurityFatalError Next.js 16.4.0).'

print('Length of old_final_status:', len(old_final_status))
print('Length of content:', len(content))
print('old_final_status in content:', old_final_status in content)

# Find the actual location
idx = content.find('data terkonsisten')
if idx >= 0:
    print('Context around "data terkonsisten":')
    print(repr(content[idx-100:idx+100]))
