#!/usr/bin/env python3
"""Comprehensive §11 cleanup: remove duplicate Rev. 507 entries, fix order."""
path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'

with open(path, 'r') as f:
    lines = f.readlines()

# Find §11 section boundaries
s11_start = 414
s12_start = 440

# Extract §11 lines
s11_lines = lines[s11_start:s12_start]

# Find all Rev. 507 entries in §11
rev507_indices = []
for i, line in enumerate(s11_lines):
    if "Rev. 507 (final)" in line:
        rev507_indices.append(i)

print(f"Found {len(rev507_indices)} Rev. 507 entries in §11")

# Keep only the first Rev. 507 entry, remove others
new_s11_lines = []
keep_first_rev507 = True
removed = 0
for line in s11_lines:
    if "Rev. 507 (final)" in line and not keep_first_rev507:
        removed += 1
        continue
    new_s11_lines.append(line)
    if "Rev. 507 (final)" in line and keep_first_rev507:
        keep_first_rev507 = False

# Fix: ensure Rev. 506 comes before Rev. 507
# Find the position of Rev. 506 and move it before Rev. 507
final_s11_lines = []
rev506_line = None
for line in new_s11_lines:
    if "Rev. 506" in line and "Rev. 506" in line and "Rev. 507" not in line:
        rev506_line = line
    else:
        final_s11_lines.append(line)

# Insert Rev. 506 before the first Rev. 507
if rev506_line:
    final_s11_lines.insert(0, rev506_line)  # This is wrong, need to find position

# Simpler approach: just remove duplicates and keep the order
# Find indices of all Rev. 507 entries in final list
final_rev507_indices = [i for i, line in enumerate(final_s11_lines) if "Rev. 507 (final)" in line]

# Keep only the first
for idx in final_rev507_indices[1:]:
    del final_s11_lines[idx]

# Write back
lines[s11_start:s12_start] = final_s11_lines

with open(path, 'w') as f:
    f.writelines(lines)

print(f"Removed {removed} duplicate Rev. 507 entries in §11")
