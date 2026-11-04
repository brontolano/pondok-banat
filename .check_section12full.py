with open('/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md', 'r') as f:
    lines = f.readlines()

# Print full content of lines 3654-3722 (1-indexed)
for i in range(3653, 3722):
    line = lines[i]
    # Count leading pipes
    leading = len(line) - len(line.lstrip('|'))
    print(f"L{i+1} [{leading}pipes]: {line.rstrip()}")
