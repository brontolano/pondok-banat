#!/usr/bin/env python3
path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Search for "Verifikasi Rev. 49" and replace with "Verifikasi Rev. 50"
old = 'Verifikasi Rev. 49'
new = 'Verifikasi Rev. 50'

count = content.count(old)
print(f"Found '{old}' {count} times")

if count > 0:
    # Only replace the header one (line 4), not the one in section 9.1 which is "Verifikasi Rev. 19"
    # The header one is on line 4
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if 'Verifikasi Rev. 49' in line:
            print(f"Line {i+1}: {line[:80]}...")
            lines[i] = line.replace(old, new, 1)
            break
    content = '\n'.join(lines)
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Done: replaced first occurrence of 'Verifikasi Rev. 49' with 'Verifikasi Rev. 50'")
else:
    print("NOT FOUND")
