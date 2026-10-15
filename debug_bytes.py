# Debug: check the actual bytes of the pattern in the file
path = '/opt/data/home/workspace/dev/pondok-banat/update_prd_rev20.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find the pattern line
idx = content.find('pattern = r')
print('Found at:', idx)
print('Context:', repr(content[idx:idx+120]))
print()
# Check if the old pattern is present
old = r"pattern = r'> \*\*Rev\. 19.*?\\*\\*Perbaikan:"
new = r"pattern = r'> \*\*Rev\. 19.*?\*\*Perbaikan:"
print('Old pattern in content:', old in content)
print('New pattern in content:', new in content)
if old in content:
    print('Replace target found.')
    content2 = content.replace(old, new)
    print('Replace happened:', content2 != content)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content2)
    print('File written.')
else:
    print('Old pattern NOT found. Checking bytes:')
    # Show the actual bytes
    import re
    m = re.search(r"pattern = r'[^']+'", content)
    if m:
        print('Matched pattern line:', repr(m.group(0)))
