path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'
with open(path, 'r') as f:
    content = f.read()

# Find the header line
lines = content.split('\n')
header = lines[2]
print("=== HEADER (repr) ===")
print(repr(header[:500]))
print()

# Find HEAD substring
idx = header.find('HEAD ')
print("=== HEAD substring ===")
print(repr(header[idx:idx+120]))
print()

# Check if old HEAD string is present
old_head = 'HEAD 5b0b96e0f0edfafc87f6717741bd940ca874a874a837 (Rev. 946 final commit)'
print("'HEAD 5b0b96e0...' in header:", old_head in header)

# Check the commit count string
old_cc = 'commit count 1048/6/0 (1048 local commits, 6 ahead / 0 behind origin_main)'
print("'commit count 1048/6/0...' in header:", old_cc in header)

# Check node_modules
old_nm = 'node_modules present (84072 files / 478 top-level dirs)'
print("'node_modules present (84072...' in header:", old_nm in header)

# Check working tree
old_wt = 'Working tree: PRD ditulis ke Rev. 946; 451 tracked files; 0 untracked'
print("'Working tree: PRD ditulis ke Rev. 946...' in header:", old_wt in header)

# Check changelog 116-945->946
old_cl = '116–945→116–946'
print("'116–945→116–946' in header:", old_cl in header)
