#!/usr/bin/env python3
"""Clean up §11 list: remove duplicate Rev. 507 entries."""
path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'

with open(path, 'r') as f:
    lines = f.readlines()

# Find §11 section (lines 414-439 based on awk output)
# Look for lines with "Rev. 507 (final)" in §11 section
# §11 section starts at line 416 (after "## 11." header)
# Keep only the first Rev. 507 entry, remove others in §11

in_s11 = False
s11_started = False
removed_count = 0
new_lines = []

for i, line in enumerate(lines):
    # Detect §11 section start
    if "## 11. REVISI TERBARU" in line:
        s11_started = True
        in_s11 = True
    
    # Detect §12 section start
    if "## 12. REVISI TERBARU" in line:
        in_s11 = False
    
    # Check for Rev. 507 entries
    if in_s11 and "Rev. 507 (final)" in line:
        # Skip duplicate Rev. 507 entries (keep the first one)
        if removed_count == 0:
            new_lines.append(line)
            removed_count += 1
        else:
            # This is a duplicate, skip it
            removed_count += 1
            continue
    
    new_lines.append(line)

# Write back
with open(path, 'w') as f:
    f.writelines(new_lines)

print(f"Removed {removed_count} duplicate Rev. 507 entries in §11")
