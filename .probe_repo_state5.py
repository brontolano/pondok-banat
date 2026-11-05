path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'
with open(path, 'rb') as f:
    data = f.read()

# Show context around position 668113
idx = data.find(b'451 tracked files')
print("=== Context around position", idx, "===")
print(repr(data[idx-80:idx+120]))

# Also check the Rev. 946 table section (around the Git HEAD row)
# The §12 table starts around position 652000
idx2 = data.find(b'**Git HEAD**')
print("\n=== §12 table Git HEAD rows ===")
positions = []
start = 0
while True:
    pos = data.find(b'**Git HEAD**', start)
    if pos == -1:
        break
    positions.append(pos)
    start = pos + 1
print("Git HEAD positions:", positions)
for pos in positions:
    context = data[pos:pos+80]
    print(f"  [{pos}]: {repr(context)}")
