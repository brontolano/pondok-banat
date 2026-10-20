import io

with io.open('/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md', encoding='utf-8') as f:
    lines = f.readlines()

print('L0:', repr(lines[0]))
print('L1:', repr(lines[1]))
print('L2 (len=%d):' % len(lines[2]), repr(lines[2]))
print('L3 (len=%d):' % len(lines[3]), repr(lines[3]))
