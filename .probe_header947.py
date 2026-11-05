path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'
with open(path, 'rb') as f:
    data = f.read()

# Check the current header
print("=== Current header (first 200 bytes) ===")
print(repr(data[:200]))

# Find "HEAD 5b0b96e0" in the file
idx = data.find(b'HEAD 5b0b96e0')
print("\n=== HEAD 5b0b96e0 found at:", idx, "===")
if idx != -1:
    print(repr(data[idx:idx+80]))

# Find "HEAD 201f494c" in the file
idx2 = data.find(b'HEAD 201f494c')
print("\n=== HEAD 201f494c found at:", idx2, "===")
if idx2 != -1:
    print(repr(data[idx2:idx2+80]))

# Check the header's working tree line
idx3 = data.find(b'PRD ditulis ke Rev. 947')
print("\n=== PRD ditulis ke Rev. 947 found at:", idx3, "===")
if idx3 != -1:
    print(repr(data[idx3:idx3+100]))
