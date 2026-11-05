path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'
with open(path, 'rb') as f:
    data = f.read()

# Get exact bytes at the hash position
hash_bytes = data[278:318]
print("=== Hash bytes from file ===")
print("Length:", len(hash_bytes))
print(repr(hash_bytes))

# Compare with target
target = b'5b0b96e0f0edfafc87f6717741bd940ca874a874a837'
print("\n=== Target bytes ===")
print("Length:", len(target))
print(repr(target))

print("\n=== Comparison ===")
print("hash_bytes == target:", hash_bytes == target)

# Print byte-by-byte
print("\n=== byte-by-byte ===")
for i in range(max(len(hash_bytes), len(target))):
    h = hash_bytes[i] if i < len(hash_bytes) else None
    t = target[i] if i < len(target) else None
    match = "✓" if h == t else "✗"
    print(f"  [{i}] file: 0x{h:02x} = {chr(h) if isinstance(h, int) and 32 <= h < 127 else '.'} | target: 0x{t:02x} = {chr(t) if isinstance(t, int) and 32 <= t < 127 else '.'} | {match}")

# Check if "5b0b96e0" is at position 278
print("\n=== Check '5b0b96e0' at 278 ===")
print("data[278:286] =", data[278:286])
print("Expected:", b'5b0b96e0')
