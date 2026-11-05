path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'
with open(path, 'rb') as f:
    data = f.read()

# Find the section with Rev. 945 -> Rev. 946 transition
# Search for "Rev. 945" 
idx = data.find(b'Rev. 945')
positions = []
start = 0
while True:
    pos = data.find(b'Rev. 945', start)
    if pos == -1:
        break
    positions.append(pos)
    start = pos + 1
print("Rev. 945 positions:", positions)

# The §12 table's "Document version | Rev. 945" should be near the Rev. 946 entry
# Search for the pattern "Repo state | Working tree | 451 tracked files"
# The current §12 table has "Repo state" for Rev. 946
# Let's find all "Repo state" occurrences
idx = data.find(b'Repo state**')
positions = []
start = 0
while True:
    pos = data.find(b'Repo state**', start)
    if pos == -1:
        break
    positions.append(pos)
    start = pos + 1
print("\n**Repo state** positions:", positions)

# For each, show context
for pos in positions:
    context = data[pos:pos+80]
    print(f"  [{pos}]: {repr(context)}")
