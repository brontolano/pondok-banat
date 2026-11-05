path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'
with open(path, 'r') as f:
    c = f.read()

# Search for "116–945" in the §11 changelog
idx = c.find('116–945')
print("=== 116–945 found at ===", idx)
if idx != -1:
    print("context:", repr(c[idx-50:idx+150]))

# Search for the §12 Git HEAD row
print()
idx = c.find('Git HEAD | `5b0b96e0')
print("=== Git HEAD | `5b0b96e0 found at ===", idx)
if idx != -1:
    print("context:", repr(c[idx-20:idx+200]))

# Search for Repo state
print()
idx = c.find('Repo state | Working tree')
print("=== Repo state found at ===", idx)
if idx != -1:
    print("context:", repr(c[idx-20:idx+100]))

# Search for header HEAD
print()
idx = c.find('HEAD 5b0b96e0')
print("=== HEAD 5b0b96e0 found at ===", idx)
if idx != -1:
    print("context:", repr(c[idx-20:idx+120]))
