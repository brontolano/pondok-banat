path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'
with open(path, 'rb') as f:
    data = f.read()

# Search for "451 tracked files; 0 untracked"
idx = data.find(b'451 tracked files; 0 untracked')
print("451 tracked files; 0 untracked found at:", idx)

# Search for "451 tracked files" with surrounding context
idx = data.find(b'451 tracked files')
positions = []
start = 0
while True:
    pos = data.find(b'451 tracked files', start)
    if pos == -1:
        break
    positions.append(pos)
    start = pos + 1
print("451 tracked files positions:", positions)

# For each, show context
for pos in positions:
    context = data[pos:pos+100]
    print(f"  [{pos}]: {repr(context)}")
