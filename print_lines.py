with open('/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md', 'r') as f:
    lines = f.readlines()

# Print lines 426-441 (1-indexed, so index 425-440)
for i in range(425, 441):
    print(f"LINE {i+1}: {lines[i]!r}")
