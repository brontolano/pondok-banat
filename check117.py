# -*- coding: utf-8 -*-
import io
PATH = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'
with io.open(PATH, encoding='utf-8') as f:
    lines = f.readlines()

# Header line 4 (index 3): check git rev-parse and origin/main
l4 = lines[3]
i = l4.find('git rev-parse HEAD')
print('HEADER git rev-parse:', l4[i:i+120])

j = l4.find('origin/main')
print('HEADER origin/main:', l4[j:j+80])

# Section 117 (Rev.332) line 7487 (index 7486): check git rev-parse
l7487 = lines[7486]
k = l7487.find('git rev-parse HEAD')
print('S117 git rev-parse:', l7487[k:k+120] if k>=0 else 'NOT FOUND')

# Section 117 line 7486 (index 7485): check "Git HEAD (local)"
l7486 = lines[7485]
m = l7486.find('Git HEAD (local)')
print('S117 Git HEAD (local):', l7486[m:m+120] if m>=0 else 'NOT FOUND')
