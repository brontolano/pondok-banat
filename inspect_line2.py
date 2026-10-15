with open('/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md', 'r') as f:
    lines = f.readlines()

# Find lines containing "Status:" 
for i, line in enumerate(lines):
    if 'Status:' in line and 'verifikasi ulang' in line:
        print(f"Line {i+1}: {line!r}")
        break

# Print line 437 (0-indexed 436) fully
print(f"Line 437: {lines[436]!r}")
