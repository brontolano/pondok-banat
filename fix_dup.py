path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find the bare "catatan schema inconsistency." line (no '>' prefix, the duplicate we must remove)
# Lines are 1-indexed in display; find the line that is exactly 'catatan schema inconsistency.\n'
dup_idx = None
for i, ln in enumerate(lines):
    if ln.strip() == 'catatan schema inconsistency.' and not ln.startswith('>'):
        dup_idx = i
        break

print("duplicate line index (0-based):", dup_idx)
assert dup_idx is not None

# Remove the duplicate line, then ensure a blank line before the next '> **Rev. 30' line
del lines[dup_idx]

# Now find the next line that starts with '> **Rev. 30' and ensure a blank line before it
for i in range(dup_idx, len(lines)):
    if lines[i].startswith('> **Rev. 30'):
        # Ensure there's a blank line before it
        if i > 0 and lines[i-1].strip() != '':
            lines.insert(i, '\n')
        break

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("fixed; total lines:", len(lines))
