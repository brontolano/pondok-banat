path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'
with open(path, 'rb') as f:
    data = f.read()

print("=== File size (bytes) ===", len(data))
print("=== File encoding check ===")
# Try to decode
try:
    text = data.decode('utf-8')
    print("UTF-8 decode OK")
except:
    print("UTF-8 decode FAILED")

# Find the hex string in raw bytes
target = b'5b0b96e0f0edfafc87f6717741bd940ca874a874a837'
idx = data.find(target)
print("=== Raw bytes: target found at ===", idx)
if idx != -1:
    print("context:", repr(data[idx-20:idx+60]))
else:
    # Search for just the beginning of the hash
    idx2 = data.find(b'5b0b96e0')
    print("=== Raw bytes: '5b0b96e0' found at ===", idx2)
    if idx2 != -1:
        print("context:", repr(data[idx2-10:idx2+80]))

# Also check the header text
print()
print("=== Header text (first 300 bytes) ===")
print(repr(data[:300]))

# Find the header position
idx3 = data.find(b'HEAD 5b0b96e0')
print("=== Raw bytes: 'HEAD 5b0b96e0' found at ===", idx3)
if idx3 != -1:
    print("context:", repr(data[idx3:idx3+80]))
