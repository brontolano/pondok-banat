BASE = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'
with open(BASE, 'r', encoding='utf-8') as f:
    lines = f.read().split('\n')

# Find the header line (contains "diblokir Tir" and "Beranda hardcode")
for i, ln in enumerate(lines, 1):
    if 'diblokir Tir' in ln or 'Beranda hardcode' in ln:
        print('LINE', i, 'len=', len(ln))
        print(repr(ln[-150:]))
        print('---')
