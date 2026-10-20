with open('PRD-PONDOK-BANAT.md', 'r') as f:
    lines = f.readlines()

# Find all lines that are the duplicate section header
duplicate_indices = [i for i, line in enumerate(lines) if '## 58. REVISI TERBARU (Rev. 171' in line]
print(f'Found {len(duplicate_indices)} duplicates at lines: {[i+1 for i in duplicate_indices]}')

# Keep everything up to line 3588 (the --- separator), then from line 3590 onwards
clean_lines = lines[:3588] + lines[3589:]
print(f'Original: {len(lines)} lines, Clean: {len(clean_lines)} lines')

with open('PRD-PONDOK-BANAT.md', 'w') as f:
    f.writelines(clean_lines)
print('Done')