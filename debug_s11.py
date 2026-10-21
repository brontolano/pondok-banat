#!/usr/bin/env python3
with open('/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md', 'rb') as f:
    content = f.read()
idx = content.find(b'## 11. REVISI TERBARU')
if idx != -1:
    line = content[idx:idx+120]
    print('Line bytes:', line)
    print('Line text:', line.decode('utf-8'))
