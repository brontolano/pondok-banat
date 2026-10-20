import re

with open('PRD-PONDOK-BANAT.md', 'r') as f:
    content = f.read()

# Check placeholders
print('Prisma placeholder:', '{prisma_line}' in content)
print('M02a placeholder:', '{m02a_line}' in content)

# Count sections
sections = re.findall(r'^## (\d+)\. REVISI TERBARU \(Rev\. (\d+) —', content, re.MULTILINE)
max_rev = max(int(r) for _, r in sections)
print('Max section/rev in file:', max(sections, key=lambda x: int(x[1])))

# Find the last section
lines = content.rstrip().split('\n')
print('Last line:', lines[-1][:150])
