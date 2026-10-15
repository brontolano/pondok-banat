with open('/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md', 'r') as f:
    lines = f.readlines()
for i in range(425, 441):
    print(f'LINE {i+1}: {lines[i]!r}')
