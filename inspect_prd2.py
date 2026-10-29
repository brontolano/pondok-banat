path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'
with open(path, 'r') as f:
    lines = f.readlines()

# Find all lines containing 'Commit count' or '677' or '678'
for i, line in enumerate(lines, 1):
    if 'Commit count' in line or '677' in line or '678' in line or 'ahead origin_main' in line:
        print(f"Line {i}: {line.rstrip()}")
