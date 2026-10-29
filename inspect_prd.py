path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'
with open(path, 'rb') as f:
    content = f.read()

# Find the commit count line
idx = content.find(b'Commit count:')
if idx >= 0:
    print('Line 1253 (decoded):')
    print(content[idx:idx+200].decode('utf-8', errors='replace'))
print()
# Find the final line
idx = content.find(b'Local branch **677')
if idx >= 0:
    print('Line 1267 (decoded):')
    print(content[idx:idx+400].decode('utf-8', errors='replace'))
