#!/usr/bin/env python3
with open('/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md', 'r') as f:
    content = f.read()
idx = content.find('Catatan statis')
if idx >= 0:
    print(content[idx:idx+300])
print()
# Also check the Beranda mention in DB block
idx2 = content.find('Beranda')
if idx2 >= 0:
    print("Beranda mentions:")
    print(content[max(0,idx2-200):idx2+300])
