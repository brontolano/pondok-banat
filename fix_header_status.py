#!/usr/bin/env python3
# Fix outdated status section in header (rev 163 -> rev 165)
path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old = 'Status: dokumen PRD REVISI - rev 163 = verifikasi fresh ulang & konfirmasi stabilitas; dev.db tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. HEAD = 27ca1d2a53b79c513cae9746cc0be9dfe9d783fa (Rev. 163 fix). Working tree bersih. Branch 1 commit ahead origin/main. Sampling file terverifikasi:'
new = 'Status: dokumen PRD REVISI - rev 165 = verifikasi fresh ulang & konfirmasi stabilitas; dev.db tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. HEAD = 1200c891a0ac4caf3a38389a237cceed7a1f9895 (Rev. 164 fix). Working tree bersih. Branch 1 commit ahead origin/main. Sampling file terverifikasi:'

count = content.count(old)
print(f'Found {count} occurrences to replace')

content = content.replace(old, new)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Header status section updated')
