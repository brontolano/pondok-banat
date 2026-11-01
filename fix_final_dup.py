with open('PRD-PONDOK-BANAT.md', 'r') as f:
    content = f.read()

# The corrupted section is at the end of §11 Rev. 858 entry
# It has multiple duplicated "Status: dokumen PRD REVISI — rev 858" lines
# We need to find the first correct one and remove the duplicates

import re
# Pattern for the corrupted section
corrupted = '''> - **Status:** dokumen PRD **REVISI** — rev 858: PRD fresh verification > - **Status:** dokumen PRD **REVISI** — rev 858: PRD fresh verification > - **Status:** dokumen PRD **REVISI** — rev 858: PRD fresh verification > - **Status:** dokumen PRD **REVISI** — rev 858: PRD fresh verification & stability confirmation (03 November 2026 (WIB)); HEAD `29e772c` (Rev. 858 committed — PRD synced ke Rev. 858); **907 / 14/0** (907 local commits, 14 ahead / 0 behind origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 857 (data terkonsisten). stability confirmation (03 November 2026 (WIB)); HEAD `29e772c` (Rev. 858 committed — PRD synced ke Rev. 858); **907 / 14/0** (907 local commits, 14 ahead / 0 behind origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 857 (data terkonsisten).'''

fixed = '''> - **Status:** dokumen PRD **REVISI** — rev 858: PRD fresh verification & stability confirmation (03 November 2026 (WIB)); HEAD `29e772c` (Rev. 858 committed — PRD synced ke Rev. 858); **907 / 14/0** (907 local commits, 14 ahead / 0 behind origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 857 (data terkonsisten).'''

if corrupted in content:
    content = content.replace(corrupted, fixed)
    with open('PRD-PONDOK-BANAT.md', 'w') as f:
        f.write(content)
    print("Fixed corrupted tail")
else:
    print("Pattern not found exactly, trying alternative...")
    # Try to find what's actually there
    idx = content.find('Status:** dokumen PRD **REVISI** — rev 858: PRD fresh verification > - **Status:**')
    if idx >= 0:
        print(f"Found at position {idx}")
        print(content[idx:idx+500])
