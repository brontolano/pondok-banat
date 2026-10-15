#!/usr/bin/env python3
"""Remove duplicate notes section - simpler approach."""

path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'

with open(path, 'r') as f:
    lines = f.readlines()

# Find all lines containing "Catatan Prisma"
prisma_indices = [i for i, line in enumerate(lines) if 'Catatan Prisma' in line]
print(f"Catatan Prisma found at line indices: {prisma_indices}")

if len(prisma_indices) >= 2:
    # Second occurrence starts the duplicate
    dup_start = prisma_indices[1]
    
    # Find "Perubahan lint" after the duplicate start
    # Look for lines after dup_start that contain "Perubahan lint"
    dup_end = None
    for i in range(dup_start + 1, len(lines)):
        if 'Perubahan lint' in lines[i]:
            dup_end = i
            break
    
    if dup_end:
        # Remove lines from dup_start to dup_end (inclusive)
        # Keep one blank line before the next section
        # The next section starts at ### 9.2
        # Find the next ### line after dup_start
        next_section = None
        for i in range(dup_end + 1, len(lines)):
            if lines[i].startswith('### '):
                next_section = i
                break
        
        if next_section:
            # Remove lines dup_start through dup_end (inclusive)
            # Add one blank line before the next section
            del lines[dup_start:dup_end + 1]
            print(f"Removed {dup_end - dup_start + 1} lines (duplicate notes section)")
        else:
            print("Could not find next section marker")
    else:
        print("Could not find Perubahan lint after duplicate start")
else:
    print("Not enough occurrences")

with open(path, 'w') as f:
    f.writelines(lines)

print("PRD updated")
