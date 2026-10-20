# -*- coding: utf-8 -*-
import io
PATH = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'
with io.open(PATH, encoding='utf-8') as f:
    lines = f.readlines()
l4 = lines[3]
# Find "Beranda" in header line 4
i = l4.find('Beranda: src/components/Beranda.tsx')
if i >= 0:
    print('HEADER Beranda region:', l4[i:i+260])
else:
    print('Beranda NOT found in header line 4')
# Also confirm totalGuru / totalKelas counts
print('totalGuru: 0 count in header:', l4.count('totalGuru: 0'))
print('totalKelas: 0 count in header:', l4.count('totalKelas: 0'))
