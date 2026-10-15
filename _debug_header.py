#!/usr/bin/env python3
with open('/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f'Total lines: {len(lines)}')
print(f'Line 4 (index 3) length: {len(lines[3])}')
print(f'Line 4 (index 3) first 100 chars: {lines[3][:100]}')
print('Rev. 66 in line 4:', 'Rev. 66' in lines[3])
print('Verifikasi Rev' in lines[3])
idx = lines[3].find('Verifikasi Rev')
if idx != -1:
    print(f'Context around "Verifikasi Rev": {repr(lines[3][idx-20:idx+30])}')
# Also check what follows " 66" after "Verifikasi Rev"
seg = lines[3][idx:]
print(f'After Verifikasi Rev: {repr(seg[:30])}')
