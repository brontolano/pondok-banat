path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'
with open(path, 'r') as f:
    content = f.read()

import re

# Search for HEAD patterns
print("=== Searching for HEAD patterns ===")
for m in re.finditer(r'HEAD\s+\S+', content):
    print(f"Found at {m.start()}: {repr(m.group(0))[:80]}")

print()
print("=== Searching for '5b0b96e0f0edf' ===")
idx = content.find('5b0b96e0f0edf')
while idx != -1:
    print(f"Found at {idx}: {repr(content[idx:idx+80])}")
    idx = content.find('5b0b96e0f0edf', idx + 1)

print()
print("=== Searching for 'Commit count' ===")
for m in re.finditer(r'Commit count\s*\|', content):
    print(f"Found at {m.start()}: {repr(content[m.start():m.start()+120])}")
