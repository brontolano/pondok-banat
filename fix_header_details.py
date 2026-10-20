# -*- coding: utf-8 -*-
import io

PATH = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'

with io.open(PATH, encoding='utf-8') as f:
    text = f.read()

# 1) Fix git rev-parse HEAD hash in header (old Rev.331 hash -> current Rev.332 HEAD)
old1 = "`git rev-parse HEAD` = `f94ce02771d46c40e9f4cfe2f158e4d5e8d9418d`"
new1 = "`git rev-parse HEAD` = `a725883b7a661e45ce99ca3dd6674db390a99d04`"
print('fix1:', text.count(old1))
text = text.replace(old1, new1)

# 2) Fix Beranda hardcoded values in header (stale 0/0/0 -> actual DB values 453/54/18)
old2 = "Beranda: src/components/Beranda.tsx & src/app/beranda/page.tsx masih hardcode (Beranda.tsx: totalSantri: 0"
new2 = "Beranda: src/components/Beranda.tsx & src/app/beranda/page.tsx masih hardcode (Beranda.tsx: totalSantri: 453"
print('fix2:', text.count(old2))
text = text.replace(old2, new2)

with io.open(PATH, 'w', encoding='utf-8') as f:
    f.write(text)

# Verify
with io.open(PATH, encoding='utf-8') as f:
    lines = f.readlines()
l4 = lines[3]
print('--- header line 4 (region: git rev-parse) ---')
i = l4.find('git rev-parse HEAD')
print(l4[i-40:i+120])
print('--- header line 4 (region: Beranda) ---')
j = l4.find('Beranda: src/components/Beranda.tsx')
print(l4[j:j+200])
