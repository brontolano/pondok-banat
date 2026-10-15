#!/usr/bin/env python3
with open('/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md', 'r') as f:
    lines = f.readlines()

# Print lines around the status table (section 9.1)
for i, line in enumerate(lines):
    if '| M02a' in line:
        print(f"{i+1}: {line.rstrip()}")
    if '| M03' in line and 'Master' in line:
        print(f"{i+1}: {line.rstrip()}")
    if '| M04' in line and 'Kurikulum' in line:
        print(f"{i+1}: {line.rstrip()}")
    if '| M05' in line and 'Akademik' in line:
        print(f"{i+1}: {line.rstrip()}")
