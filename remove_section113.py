#!/usr/bin/env python3
"""Remove existing section 113 from the PRD file."""
import re
import os

prd_path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'
with open(prd_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Remove existing section 113 (from '---\n\n## 113. REVISI' up to '\n\n## 114.' or end of file)
content_new, n = re.subn(r'\n---\n\n## 113\. REVISI TERBARU.*?(?=\n\n## 114\.|\Z)', '\n', content, flags=re.DOTALL)

with open(prd_path, 'w', encoding='utf-8') as f:
    f.write(content_new)

print('Removed existing section 113' if n else 'Section 113 not found')
print('New line count:', content_new.count(chr(10)) + 1)
