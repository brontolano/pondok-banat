with open('/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md', 'r') as f:
    lines = f.readlines()

# Print lines 3653-3658 (0-indexed) to see the exact start of §12
for i in range(3653, 3658):
    print(f'L{i+1}: {repr(lines[i][:200])}')
