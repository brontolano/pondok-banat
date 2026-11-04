#!/usr/bin/env python3
# Fix §13 main status line to Rev. 931
path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'

with open(path, 'r') as f:
    content = f.read()

old = """> - **Status:** dokumen PRD **REVISI** — rev 926: PRD fresh verification & stability confirmation (04 November 2026 WIB); HEAD `456510b` (Rev. 926 final sync — PRD synced ke Rev. 926); **1019 / 18/0** (1019 local commits, 18 ahead / 0 behind origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 925 (data terkonsisten). Revision 926 bumps document revision dari 925 ke 926."""
new = """> - **Status:** dokumen PRD **REVISI** — rev 931: PRD fresh verification & metadata sync (04 November 2026 WIB); HEAD `cc4d80eb1ea0d81682339467d865ad4f3c0e892b` (Rev. 930 final commit); **1024 / 23/0** (1024 local commits, 23 ahead / 0 behind origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 930 (data terkonsisten). Revision 931 bumps document revision dari 930 ke 931."""
assert old in content, '§13 status line not found'
content = content.replace(old, new)

with open(path, 'w') as f:
    f.write(content)

print('Fixed §13 main status line to Rev. 931')
