path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'
with open(path, 'rb') as f:
    data = f.read()

# Search for the SHA-1 hash in raw bytes
target = b'5b0b96e0f0edfafc87f6717741bd940ca874a874a837'
idx = data.find(target)
print("Target found at:", idx)

# Search with different variations
variants = [
    b'5b0b96e0f0edfafc87f6717741bd940ca874a874a837',
    b'5b0b96e0f0edfafc87f6717741bd940ca874a874a837 ',
    b'5b0b96e0f0edfafc87f6717741bd940ca874a874a837\xff',
]

for v in variants:
    idx2 = data.find(v)
    print(f"Variant {v[:10]}... found at:", idx2)

# Get the exact bytes around position 278
print("\n=== Bytes around position 273-330 ===")
chunk = data[273:330]
print(repr(chunk))
print()

# Check each byte
print("=== Byte values ===")
for i, b in enumerate(chunk):
    print(f"  [{i}] 0x{b:02x} = {chr(b) if 32 <= b < 127 else '.'}")
