# Fix the regex pattern in update_prd_rev20.py
path = '/opt/data/home/workspace/dev/pondok-banat/update_prd_rev20.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# The pattern has escaped backslashes that need to be fixed
# Old: r'> \*\*Rev\. 19.*?\\*\\*Perbaikan:...'
# New: r'> \*\*Rev\. 19.*?\*\*Perbaikan:...'
old_pattern = r"pattern = r'> \*\*Rev\. 19.*?\\*\\*Perbaikan:"
new_pattern = r"pattern = r'> \*\*Rev\. 19.*?\*\*Perbaikan:"
content = content.replace(old_pattern, new_pattern)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed pattern.")
print("--- Verify ---")
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()
print(lines[10])
