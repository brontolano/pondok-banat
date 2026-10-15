#!/usr/bin/env python3
with open('/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md', 'r') as f:
    lines = f.readlines()

# Find the M03 row in the status table (around line 290)
for i, line in enumerate(lines):
    if '| M03' in line and 'Master' in line:
        print(f"{i+1}: {line.rstrip()}")
    if '| M04' in line and 'Kurikulum' in line:
        print(f"{i+1}: {line.rstrip()}")
    if '| M05' in line and 'Akademik' in line:
        print(f"{i+1}: {line.rstrip()}")
    if '| M07' in line and 'Kesiswaan' in line:
        print(f"{i+1}: {line.rstrip()}")
    if '| M08' in line and 'Komunikasi' in line:
        print(f"{i+1}: {line.rstrip()}")
    if '| M09' in line and 'Laporan' in line:
        print(f"{i+1}: {line.rstrip()}")
