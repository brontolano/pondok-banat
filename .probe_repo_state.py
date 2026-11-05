path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'
with open(path, 'rb') as f:
    data = f.read()

# Search for the repo state row with different patterns
patterns = [
    b'**Repo state** | Working tree | 451 tracked files; 0 untracked; 0 deleted',
    b'Repo state** | Working tree | 451 tracked files; 0 untracked',
    b'451 tracked files; 0 untracked',
]

for p in patterns:
    idx = data.find(p)
    print(f"Pattern {repr(p[:40])} found at:", idx)

# Find the actual repo state row
idx = data.find(b'451 tracked files; 0 untracked')
if idx != -1:
    print("Context:", repr(data[idx-30:idx+100]))

# Check if **Repo state** is in the file
idx = data.find(b'**Repo state**')
print("**Repo state** found at:", idx)
if idx != -1:
    print("Context:", repr(data[idx-20:idx+100]))
