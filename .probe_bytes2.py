path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'
with open(path, 'r') as f:
    c = f.read()

# Get the exact 100 chars starting from position 250
chunk = c[250:360]
print("=== Exact chunk (250:360) ===")
print(repr(chunk))
print()

# Compare with search string
search = 'HEAD 5b0b96e0f0edfafc87f6717741bd940ca874a874a837'
print("=== Search string ===")
print(repr(search))
print()

# Find the position of 'HEAD 5b0b96e0' in the file
pos = c.find('HEAD 5b0b96e0')
print("Position of 'HEAD 5b0b96e0':", pos)
if pos != -1:
    # Get 80 chars from that position
    chunk2 = c[pos:pos+80]
    print("=== Chunk from position 261 ===")
    print(repr(chunk2))
    print()
    print("=== Match check ===")
    print("chunk2 == search?", chunk2 == search)
    print("chunk2[:45] == search[:45]?", chunk2[:45] == search[:45])

# Check if the file contains the exact string
print()
print("=== Direct check ===")
print("'HEAD 5b0b96e0f0edfafc87f6717741bd940ca874a874a837' in c?", 'HEAD 5b0b96e0f0edfafc87f6717741bd940ca874a874a837' in c)

# Check with different search
print("'5b0b96e0f0edfafc87f6717741bd940ca874a874a837' in c?", '5b0b96e0f0edfafc87f6717741bd940ca874a874a837' in c)
