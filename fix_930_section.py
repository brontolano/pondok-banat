#!/usr/bin/env python3
# Fix remaining stale spots in Rev.930 section
path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'

with open(path, 'r') as f:
    content = f.read()

# Fix 1: Rev.930 section §12 status summary commit count is stale (1023/22/0 -> 1024/23/0)
old1 = """> - **§12 status summary:** updated to Rev. 930; commit count 1023/22/0.
> - **§13 notes:** Refreshed 04 November 2026 WIB; HEAD `cc4d80eb1ea0d81682339467d865ad4f3c0e892b` (Rev. 931 final commit); commit count 1024/23/0. No DB/schema/code changes; data consistent."""
new1 = """> - **§12 status summary:** updated to Rev. 930; commit count 1024/23/0.
> - **§13 notes:** Refreshed 04 November 2026 WIB; HEAD `cc4d80eb1ea0d81682339467d865ad4f3c0e892b` (Rev. 930 final commit); commit count 1024/23/0. No DB/schema/code changes; data consistent."""
assert old1 in content, 'Fix1 target not found'
content = content.replace(old1, new1)

with open(path, 'w') as f:
    f.write(content)

print('Fixed Rev.930 section §12/§13 notes')
