import sys

path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'

with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Print first line to verify
print("First line length:", len(lines[0]) if lines else 0)
print("Line 4 preview:", lines[3][:50] if len(lines) > 3 else "NO LINE 4")
