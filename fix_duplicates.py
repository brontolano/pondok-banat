#!/usr/bin/env python3
import re

path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'

with open(path, 'r') as f:
    content = f.read()

# Find all "### Rev. 704" entries and their content
# Each entry starts with "### Rev. 704\n\n> **Rev. 704 (fresh).**"
# and ends with the next "### Rev." or end of file

# Find all occurrences of the Rev. 704 entry pattern
entries = []
pattern = r'### Rev\. 704\n\n> \*\*Rev\. 704 \(fresh\)\.\*\* 28 Oktober 2026 \(WIB\): CRON-run fresh verification & stability confirmation \(cron run\); HEAD `fd81e38d231cfae6bed25d8f2a9e65649748348e` \(Rev\. 703 final commit\); commit count \*\*715 / 11\* \(715 local commits, 11 ahead origin/main, 0 behind\)\. Fresh verification seluruh kondisi repository \+ dev\.db \(SQLite, cron run\):\n'
matches = list(re.finditer(pattern, content))

print(f'Found {len(matches)} occurrences of Rev. 704 entry')

if len(matches) > 1:
    # Keep the first occurrence, remove the rest
    # The pattern starts at each match position
    # We need to remove from the 2nd match to the end of the 2nd match
    
    # Find the end of each match (the end of the bullet points)
    # The entry pattern ends with: "node_modules present \(477 dirs / 84021 files\)\."
    
    # Let's find the full entry content for each match
    entry_pattern = r'### Rev\. 704\n\n> \*\*Rev\. 704 \(fresh\)\.\*\* 28 Oktober 2026 \(WIB\): CRON-run fresh verification & stability confirmation \(cron run\); HEAD `fd81e38d231cfae6bed25d8f2a9e65649748348e` \(Rev\. 703 final commit\); commit count \*\*715 / 11\* \(715 local commits, 11 ahead origin/main, 0 behind\)\. Fresh verification seluruh kondisi repository \+ dev\.db \(SQLite, cron run\):\n>\n> - \*\*Environment:** node v26\.5\.1, npm 11\.17\.0, Prisma CLI = Prisma Developer Platform \(new CLI; `generate`/`validate` commands not available in this release\)\.\n> - \*\*Build quality gate:** `npm run type-check` \(tsc --noEmit\) ✓ \(exit 0\); `npm run lint` ✓ \(exit 0, 1 warning / 0 error\); `npm run build` \(next build\) ✗ \(exit 1 — SecurityFatalError: Next\.js 16\.4\.0 has a known security vulnerability\)\. Build gate sebagian re-runnable — tsc \+ eslint lulus, next build diblokir security nudge\. node_modules present \(477 dirs / 84021 files\)\.'
    
    # Actually, let's take a simpler approach: find all "### Rev. 704" anchors
    lines = content.split('\n')
    rev704_lines = [i for i, line in enumerate(lines) if line.strip() == '### Rev. 704']
    
    print(f'"### Rev. 704" appears at lines (0-indexed): {rev704_lines}')
    
    if len(rev704_lines) > 1:
        # Keep the first one (index 0), remove from index 1 onwards
        # Each entry is from "### Rev. 704" to just before the next "### Rev." 
        # or to the end
        
        # Find the extent of each entry
        entry_ends = []
        for idx in rev704_lines:
            # Find the end of this entry (the next "### Rev." or "## 11." or "## 12.")
            next_section = len(lines)
            for j in range(idx + 1, len(lines)):
                if lines[j].strip().startswith('### Rev.'):
                    next_section = j
                    break
            entry_ends.append(next_section)
        
        print(f'Entry extents: {entry_ends}')
        
        # Remove entries 1, 2, 3 (keep entry 0)
        # The lines to remove are from rev704_lines[1] to entry_ends[1]-1, etc.
        remove_ranges = []
        for i in range(1, len(rev704_lines)):
            start = rev704_lines[i]
            end = entry_ends[i]
            remove_ranges.append((start, end))
        
        print(f'Remove ranges: {remove_ranges}')
        
        # Build new content by removing those lines
        new_lines = []
        for i, line in enumerate(lines):
            skip = False
            for start, end in remove_ranges:
                if start <= i < end:
                    skip = True
                    break
            if not skip:
                new_lines.append(line)
        
        new_content = '\n'.join(new_lines)
        
        # Verify
        new_rev704_count = new_content.count('### Rev. 704')
        print(f'New count of "### Rev. 704": {new_rev704_count}')
        
        with open(path, 'w') as f:
            f.write(new_content)
        print('Done!')
