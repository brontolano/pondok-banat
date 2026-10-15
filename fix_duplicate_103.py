#!/usr/bin/env python3
"""Remove duplicate §10.3 section in PRD."""

path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'

with open(path, 'r') as f:
    lines = f.readlines()

# Find all occurrences of "10.3 Perubahan Rev. 17"
sec103_indices = [i for i, line in enumerate(lines) if '10.3 Perubahan Rev. 17' in line]
print(f"§10.3 found at line indices: {sec103_indices}")

if len(sec103_indices) >= 2:
    dup_start = sec103_indices[1]
    
    # Find the end of the duplicate section: the "*Catatan:* revisi sebelumnya" line
    dup_end = None
    for i in range(dup_start + 1, len(lines)):
        if '*Catatan:* revisi sebelumnya' in lines[i]:
            dup_end = i
            break
    
    if dup_end:
        # Remove lines from dup_start to dup_end (inclusive)
        del lines[dup_start:dup_end + 1]
        print(f"Removed {dup_end - dup_start + 1} lines (duplicate §10.3 section)")
    else:
        print("Could not find *Catatan* line after second §10.3")
else:
    print("Not enough §10.3 occurrences")

with open(path, 'w') as f:
    f.writelines(lines)

print("PRD updated")
