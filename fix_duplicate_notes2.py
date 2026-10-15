#!/usr/bin/env python3
"""Remove duplicate notes section (second occurrence of the notes block)."""

path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'

with open(path, 'r') as f:
    content = f.read()

# Find the second (duplicate) occurrence of the Catatan Prisma section
import re

# Pattern for the duplicate section start
dup_start = r'> \*\*Catatan Prisma\*\*: model `KitabProgress` hanya direferensikan di `Subject` \(`KitabProgress\[\]\)] tetapi \*\*tidak didefinisikan\*\* di schema; perlu ditambahkan jika fitur progress kitab akan dibangun\.'

# Find all occurrences
matches = list(re.finditer(dup_start, content))
print(f"Found {len(matches)} occurrences of Catatan Prisma")

if len(matches) >= 2:
    # Second occurrence starts the duplicate section
    start = matches[1].start()
    
    # The duplicate section includes:
    # - Catatan Prisma
    # - (empty line)
    # - Catatan keamanan
    # - (empty line)
    # - Kualitas build
    # - tsc --noEmit
    # - npm run lint
    # - npm run build
    # - (empty line)
    # - Perubahan lint (>> not >)
    
    # Find the end of the duplicate section: the "Perubahan lint" line
    dup_section = content[start:]
    
    # Find the "Perubahan lint" line
    lint_match = re.search(r'> > \*\*Perubahan lint.*?$', dup_section, flags=re.MULTILINE)
    if lint_match:
        lint_end = start + lint_match.end()
        
        # Remove everything from start to lint_end (inclusive of the Perubahan lint line)
        # Keep one blank line before the next section (### 9.2)
        content = content[:start] + content[lint_end:]
        print("Duplicate notes section removed")
    else:
        print("Could not find Perubahan lint in duplicate section")
else:
    print("Not enough occurrences")

with open(path, 'w') as f:
    f.write(content)

print("PRD updated")
