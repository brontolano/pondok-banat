with open('/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()
print('Total lines:', len(lines))
print('Line 4 length:', len(lines[3]))
print('Line 4 starts:', repr(lines[3][:120]))
print('Line 4 has Rev. 19:', 'Rev. 19' in lines[3])
# Find where Rev. 18 = dokumen PRD sebelumnya is
for i, l in enumerate(lines):
    if 'Rev. 18 = dokumen PRD sebelumnya' in l:
        print('Found Rev. 18 at line', i+1)
        break
# Find where Rev. 19 is
for i, l in enumerate(lines):
    if 'Rev. 19' in l:
        print('Found Rev. 19 at line', i+1)
        break
