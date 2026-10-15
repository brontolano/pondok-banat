import re

path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'
with open(path, 'r') as f:
    content = f.read()

# Fix literal \\n in table rows (replace with actual newlines)
content = content.replace('|\\n|', '|\n|')
content = content.replace('||\\n', '|\n')

with open(path, 'w') as f:
    f.write(content)

print("Fixed literal \\n in table rows")
print(f"File size: {len(content)} chars, {content.count(chr(10)) + 1} lines")
