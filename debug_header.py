with open('/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md', 'r') as f:
    content = f.read()
lines = content.split('\n')
for i, line in enumerate(lines[:6]):
    print('L' + str(i+1) + ':', repr(line[:300]))
