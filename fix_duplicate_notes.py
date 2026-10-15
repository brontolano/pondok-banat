#!/usr/bin/env python3
"""Remove duplicate notes section in PRD."""

path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'

with open(path, 'r') as f:
    content = f.read()

# The duplicate section starts with "> **Catatan Prisma:** model `KitabProgress` hanya direferensikan di `Subject` (`KitabProgress[]`) tetapi **tidak didefinisikan** di schema; perlu ditambahkan jika fitur progress kitab akan dibangun."
# This appears twice: once in new notes (line 313) and once in old notes (line 324)

# Find all occurrences
import re
pattern = r'> \*\*Catatan Prisma\*\*: model `KitabProgress` hanya direferensikan di `Subject` \(`KitabProgress\[\]\)] tetapi \*\*tidak didefinisikan\*\* di schema; perlu ditambahkan jika fitur progress kitab akan dibangun\.'
matches = list(re.finditer(pattern, content))

print(f"Found {len(matches)} occurrences of Catatan Prisma")

if len(matches) >= 2:
    # The second occurrence is the duplicate. Remove from the start of the second occurrence
    # to the line before "### 9.2 Build & Database"
    
    # Find the position of "### 9.2 Build & Database"
    m92 = re.search(r'^### 9\.2 Build & Database$', content, flags=re.MULTILINE)
    if m92:
        pos92 = m92.start()
        
        # Remove from the second Catatan Prisma occurrence to just before ### 9.2
        # The duplicate section is:
        # > **Catatan Prisma:** ... (2nd occurrence)
        # (empty line)
        # > **Catatan keamanan:** ... 
        # (empty line)
        # > **Kualitas build (quality gate)... 
        # (empty line)
        # > - `tsc --noEmit` ...
        # > - `npm run lint` ...
        # > - `npm run build` ...
        # (empty line)
        # > > **Perubahan lint... 
        # (empty line)
        
        # Find the end of the second occurrence
        start = matches[1].start()
        
        # Find the end: from second occurrence, find the following "> > **Perubahan lint" line and remove through it
        dup_pattern = r'> \*\*Catatan Prisma\*\*:.*?(> \*\*Kualitas build.*?(> \*\*Catatan keamanan:.*?(> \*\*Kualitas build.*?(> > \*\*Perubahan lint.*?)'
        dup_match = re.search(dup_pattern, content[start:], flags=re.DOTALL)
        
        if dup_match:
            dup_end = start + dup_match.end()
            # Remove up to and including the "> > **Perubahan lint" line and the following empty line
            # Find the exact text
            dup_text = content[start:dup_end]
            print("Duplicate section to remove:")
            print(dup_text[:500])
            print("...")
            
            # Remove the duplicate section
            content = content[:start] + content[dup_end:]
            print("Duplicate section removed")
        else:
            print("Could not find duplicate pattern end")
    else:
        print("Could not find ### 9.2 marker")
else:
    print("Not enough occurrences (need >= 2)")

with open(path, 'w') as f:
    f.write(content)

print("PRD updated")
