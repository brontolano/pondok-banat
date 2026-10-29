path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'
with open(path, 'r') as f:
    lines = f.readlines()

# Print lines 1243-1267 with context
for i in range(1242, min(1267, len(lines))):
    print(f"{i+1}: {lines[i].rstrip()}")
