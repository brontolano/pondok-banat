path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'
with open(path, 'rb') as f:
    data = f.read()

# Find the exact position of the hash
idx = data.find(b'5b0b96e0')
print("Position of '5b0b96e0':", idx)

# Get the exact bytes from idx to idx+40
hash_bytes = data[idx:idx+40]
print("=== Exact bytes of hash (40 bytes) ===")
print(repr(hash_bytes))
print("Length:", len(hash_bytes))

# Check if it's a valid hex string
print()
print("=== Hex check ===")
try:
    # Convert bytes to hex string
    hex_str = hash_bytes.decode('ascii')
    print("Decoded to ASCII:", hex_str)
    print("Length of hex string:", len(hex_str))
    # Check if it's a valid SHA-1 (40 hex chars)
    print("Is valid hex:", all(c in '0123456789abcdefABCDEF' for c in hex_str))
except Exception as e:
    print("Error:", e)

# Check each byte
print()
print("=== Byte-by-byte ===")
for i, b in enumerate(hash_bytes):
    print(f"  [{i}] 0x{b:02x} = {chr(b) if 32 <= b < 127 else '.'}{repr(chr(b))}")

# Compare with expected
expected = b'5b0b96e0f0edfafc87f6717741bd940ca874a874a837'
print()
print("=== Expected hash ===")
print(repr(expected))
print("Match:", hash_bytes == expected)
