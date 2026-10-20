# -*- coding: utf-8 -*-
import io
PATH = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'
with io.open(PATH, encoding='utf-8') as f:
    text = f.read()

# Fix header Beranda hardcoded values: totalGuru: 0 -> 54, totalKelas: 0 -> 18
old = "Beranda.tsx: totalSantri: 453, totalGuru: 0, totalKelas: 0"
new = "Beranda.tsx: totalSantri: 453, totalGuru: 54, totalKelas: 18"
print('count:', text.count(old))
text = text.replace(old, new)

with io.open(PATH, 'w', encoding='utf-8') as f:
    f.write(text)

# Verify
with io.open(PATH, encoding='utf-8') as f:
    lines = f.readlines()
l4 = lines[3]
i = l4.find('Beranda: src/components/Beranda.tsx')
print('--- header Beranda region ---')
print(l4[i:i+220])
