#!/usr/bin/env python3
"""Verify PRD Rev. 67 update."""
PATH = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'

with open(PATH, 'r', encoding='utf-8') as f:
    content = f.read()

print(f'Total lines: {content.count(chr(10)) + 1}')
print(f'Total size: {len(content)} bytes')
print()

# Check header
idx = content.find('> **Rev. 67')
if idx != -1:
    print(f'Header "Rev. 67" found at position {idx}: {repr(content[idx:idx+60])}')
else:
    print('Header "Rev. 67" NOT found')

# Check old "Rev. 66" header still there?
idx66 = content.find('> **Rev. 66')
if idx66 != -1:
    print(f'Old header "Rev. 66" still present at position {idx66}')
else:
    print('Old header "Rev. 66" removed')

# Check section 25 (Rev. 66) still present
if '## 25. REVISI TERBARU (Rev. 66' in content:
    print('Section 25 (Rev. 66) header present')
else:
    print('Section 25 header NOT found')

# Check section 26 (Rev. 67)
if '## 26. REVISI TERBARU (Rev. 67' in content:
    print('Section 26 (Rev. 67) header present')
else:
    print('Section 26 header NOT found')

# Show last 500 chars
print()
print('--- LAST 500 CHARS ---')
print(content[-500:])
