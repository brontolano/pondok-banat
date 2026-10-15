#!/usr/bin/env python3
"""Check current state of PRD around header and end."""
PATH = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'

with open(PATH, 'r', encoding='utf-8') as f:
    content = f.read()

# Check header
idx = content.find('> **Rev. 66')
if idx != -1:
    print(f'Header "Rev. 66" found at position {idx}')
    print(repr(content[idx:idx+80]))
else:
    print('Header "Rev. 66" NOT found')

# Check for "Rev. 67" occurrences
count67 = content.count('Rev. 67')
print(f'"Rev. 67" appears {count67} times')
# Show context around first "Rev. 67"
idx67 = content.find('Rev. 67')
if idx67 != -1:
    print(f'First "Rev. 67" context: {repr(content[idx67-30:idx67+80])}')

# Check if section 26 is present
if '## 26. REVISI TERBARU' in content:
    print('Section 26 header found')
else:
    print('Section 26 header NOT found')
