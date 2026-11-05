path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'
with open(path, 'rb') as f:
    data = f.read()

# Show context around Rev. 947 Git HEAD (position 666337)
idx = 666337
print("=== Context around Rev. 947 Git HEAD (position", idx, ") ===")
print(repr(data[idx-200:idx+300]))

# Search for 'Repo state' after position 666337
idx2 = data.find(b'Repo state**', 666337)
print("\n=== Repo state after 666337 ===")
print("Found at:", idx2)
if idx2 != -1:
    print(repr(data[idx2:idx2+120]))

# Check the §12 table structure - what revisions are in the table?
# Search for Document version rows
idx3 = data.find(b'Document version**')
positions = []
start = 0
while True:
    pos = data.find(b'Document version**', start)
    if pos == -1:
        break
    positions.append(pos)
    start = pos + 1
print("\n=== Document version positions ===")
print(positions)
for pos in positions:
    context = data[pos:pos+60]
    print(f"  [{pos}]: {repr(context)}")
