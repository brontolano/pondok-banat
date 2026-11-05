path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'
with open(path, 'r') as f:
    c = f.read()

# Search for §11 Rev.946 section markers
print("=== Search §11 Rev.946 ===")
idx = c.find('### Rev. 946')
print("### Rev. 946 found at:", idx)
if idx != -1:
    print("context:", repr(c[idx:idx+400]))

# Search for the §11 Rev.946 changelog row
print()
print("=== Search §11 Rev.946 changelog ===")
idx = c.find('116–945→116–946')
print("116–945→116–946 found at:", idx)
if idx != -1:
    print("context:", repr(c[idx-50:idx+200]))

# Search for the §11 Rev.947 section
print()
print("=== Search §11 Rev.947 ===")
idx = c.find('### Rev. 947')
print("### Rev. 947 found at:", idx)
if idx != -1:
    print("context:", repr(c[idx:idx+400]))

# Search for the §12 table Git HEAD row
print()
print("=== Search §12 Git HEAD ===")
# Try different patterns
for pat in ['Git HEAD | `5b0b96e0', 'Git HEAD | `5b0b96e0']:
    idx = c.find(pat)
    print(f"'{pat}' found at:", idx)
    if idx != -1:
        print("context:", repr(c[idx-20:idx+200]))
