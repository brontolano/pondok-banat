with open('/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md', 'r') as f:
    lines = f.readlines()

# Show the relevant lines
for i in range(467, 474):
    print(f'Line {i+1}: {repr(lines[i])}')
