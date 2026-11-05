path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'
with open(path, 'r') as f:
    content = f.read()
lines = content.split('\n')
header = lines[2]

# Extract the exact HEAD substring from file
start = header.find('HEAD ')
end = header.find('; commit count', start)
file_head = header[start:end]
print("=== FILE HEAD SUBSTRING ===")
print(f"Length: {len(file_head)}")
print("Codepoints:")
for i, c in enumerate(file_head):
    print(f"  [{i}] '{c}' U+{ord(c):04X} {repr(c)}")

print()
# My old_head
old_head = 'HEAD 5b0b96e0f0edfafc87f6717741bd940ca874a874a837 (Rev. 946 final commit)'
print("=== MY OLD_HEAD ===")
print(f"Length: {len(old_head)}")
print("Codepoints:")
for i, c in enumerate(old_head):
    print(f"  [{i}] '{c}' U+{ord(c):04X} {repr(c)}")
