with open('/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()
print('Total lines:', len(lines))
for i in [2, 3, 4]:
    print(f'Line {i+1} repr:', repr(lines[i]))
