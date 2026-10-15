import re

path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'
with open(path, 'r') as f:
    content = f.read()

# Check for literal backslash-n sequences
literal_count = content.count('\\n')
print(f"Literal backslash-n count: {literal_count}")

# If we see literal backslash-n (not actual newlines), replace them
if literal_count > 0:
    fixed = content.replace('\\n', '\n')
    with open(path, 'w') as f:
        f.write(fixed)
    print(f"Fixed {literal_count} literal \\n sequences")
else:
    print("No literal \\n found - file appears to be OK")
