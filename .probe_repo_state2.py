path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'
with open(path, 'rb') as f:
    data = f.read()

# Search for various repo state patterns
patterns = [
    b'451 tracked files',
    b'0 untracked',
    b'tracked files',
]

for p in patterns:
    idx = data.find(p)
    positions = []
    start = 0
    while True:
        pos = data.find(p, start)
        if pos == -1:
            break
        positions.append(pos)
        start = pos + 1
    print(f"Pattern {repr(p[:30])} found at positions: {positions}")

# Find the specific line with 451 tracked files
idx = data.find(b'451 tracked files')
if idx != -1:
    print("\nContext:", repr(data[idx-50:idx+120]))

# Check the Rev. 946 section (the §12 table)
# The §12 table is around position 650000-660000
# Let's search for "Git HEAD" in the file
idx = data.find(b'**Git HEAD**')
print("\n**Git HEAD** found at:", idx)
if idx != -1:
    print("Context:", repr(data[idx-10:idx+200]))
