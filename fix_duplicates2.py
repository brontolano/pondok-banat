#!/usr/bin/env python3
import re

path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'

with open(path, 'r') as f:
    content = f.read()

# Find all occurrences of "### Rev. 704" anchor
# Each entry starts with "### Rev. 704\n\n> **Rev. 704 (fresh).**"
# We need to keep only the first one and remove subsequent ones

# Split by "### Rev. 704" anchor
parts = content.split('### Rev. 704')

print(f'Split into {len(parts)} parts')

if len(parts) > 1:
    # First part is before the first Rev. 704 entry
    # Each subsequent part starts with " Rev. 704..."
    # We need to keep only the first Rev. 704 entry
    
    # Reconstruct: first_part + first_rev704_entry
    # The first Rev. 704 entry is: "### Rev. 704" + "\n\n> **Rev. 704 (fresh).**..." up to the next "### Rev."
    
    # Find the next "### Rev." or "## 11." or "## 12." after the first Rev. 704
    first_rev704 = '### Rev. 704' + parts[1]  # First Rev. 704 entry
    
    # Find where the first Rev. 704 entry ends
    # It ends at the next "### Rev." (which would be Rev. 677, etc.)
    # or at "## 12." or end of file
    
    # Find the position after "### Rev. 704" in the original content
    first_anchor_pos = content.find('### Rev. 704')
    
    # Find the end of the first Rev. 704 entry
    # Look for the next "### Rev." after the first anchor
    next_rev_anchor = content.find('### Rev.', first_anchor_pos + len('### Rev. 704'))
    
    # The first Rev. 704 entry ends before the next Rev. anchor
    if next_rev_anchor != -1:
        first_entry_end = next_rev_anchor
    else:
        first_entry_end = len(content)
    
    # Find the end of the first Rev. 704 entry more precisely
    # The entry starts at "### Rev. 704" and includes everything until the next "### Rev."
    # But we need to find the actual end of the entry content
    
    # Actually, let's take a different approach:
    # Find all "### Rev. 704" anchors with their positions
    positions = [m.start() for m in re.finditer(r'### Rev\. 704', content)]
    print(f'Positions: {positions}')
    
    if len(positions) > 1:
        # Keep the first occurrence, remove the rest
        # The entries are:
        # 1. positions[0] to next "### Rev." (or end)
        # 2. positions[1] to next "### Rev."
        # etc.
        
        # Construct new content with only the first entry
        new_content = content[:positions[0]]  # Everything before the first Rev. 704
        
        # Find where the first entry ends (next "### Rev.")
        next_after_first = positions[0]
        next_rev_pos = content.find('### Rev.', next_after_first + len('### Rev. 704'))
        if next_rev_pos != -1:
            new_content += content[next_after_first:next_rev_pos]
        else:
            new_content += content[next_after_first:]
        
        # Append everything from the last Rev. 704 entry onwards
        last_rev_pos = positions[-1]
        new_content += content[last_rev_pos:]
        
        # Actually, the correct approach is:
        # new_content = content[:positions[0]] + content[positions[0]:positions[1]] + content[positions[-1]:]
        # Wait, no. We need to keep the first Rev. 704 entry and remove entries 2..N.
        
        # Let me think about this more carefully.
        # content[:positions[0]] = everything before first Rev. 704
        # content[positions[0]:positions[1]] = first Rev. 704 entry
        # content[positions[1]:positions[2]] = second Rev. 704 entry
        # ...
        # content[positions[-1]:] = last Rev. 704 entry and everything after
        
        # We want: content[:positions[0]] + content[positions[0]:positions[1]] + content[positions[-1]:]
        # = content[:positions[1]] + content[positions[-1]:]
        
        new_content = content[:positions[1]] + content[positions[-1]:]
        
        # Verify
        new_count = new_content.count('### Rev. 704')
        print(f'New count of "### Rev. 704": {new_count}')
        
        with open(path, 'w') as f:
            f.write(new_content)
        print('Done!')
