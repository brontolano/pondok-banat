with open('/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md', 'r') as f:
    lines = f.readlines()

# Print full content of lines 3654-3665 (1-indexed)
for i in range(3653, 3665):
    print(f"L{i+1}: {repr(lines[i])}")
