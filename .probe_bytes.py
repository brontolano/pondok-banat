path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'
with open(path, 'r') as f:
    c = f.read()

# Get exact header HEAD substring
idx = c.find('HEAD 5b0b96e0')
print("=== HEAD 5b0b96e0 found at:", idx, "===")
if idx != -1:
    # Get the full header (70 chars from start)
    header = c[:70]
    print("=== Header first 70 chars ===")
    print(repr(header))
    print()
    # Compare with search string
    search = 'HEAD 5b0b96e0f0edfafc87f6717741bd940ca874a874a837'
    print("=== Search string ===")
    print(repr(search))
    print()
    print("=== Comparison ===")
    print("header[:50] == search[:50]?", header[:50] == search[:50])
    print("header[:70] == search?", header[:70] == search)

# Get exact §11 Rev.946 changelog row
print()
print("=== §11 Rev.946 changelog ===")
idx = c.find('116–945→116–946')
if idx != -1:
    chunk = c[idx:idx+300]
    print("chunk:", repr(chunk))

# Get exact §12 Git HEAD row
print()
print("=== §12 Git HEAD ===")
idx = c.find('5b0b96e0f0edfafc87f6717741bd940ca874a874a837` | "PRD Rev. 946')
if idx != -1:
    chunk = c[idx-50:idx+200]
    print("chunk:", repr(chunk))
else:
    # Find all occurrences of the pattern
    idx = c.find('5b0b96e0f0edfafc87f6717741bd940ca874a874a837')
    print("First occurrence at:", idx)
    if idx != -1:
        print("context:", repr(c[idx-10:idx+150]))
