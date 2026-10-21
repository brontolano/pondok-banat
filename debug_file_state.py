#!/usr/bin/env python3
with open('/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md', 'r') as f:
    lines = f.readlines()
# Print line 413
print('Line 413:', repr(lines[412]))
# Check if "116–398" is in the file
content = open('/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md').read()
print('Contains "116–398":', '116–398' in content)
print('Contains "116–393":', '116–393' in content)
# Check the exact bytes of line 413
idx = content.find('REVISI TERBARU')
print('Around §11 title:', repr(content[idx:idx+80]))
