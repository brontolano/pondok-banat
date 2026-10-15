import io

path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'

with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find and remove the duplicate Rev. 59 section and duplicate bottom notes
# The duplicate starts at line 525 (1-indexed) with "## 19. REVISI TERBARU"
# and ends at line 534 (1-indexed) with the second "*Identifikasi entitas..." note

# Find the first occurrence of the duplicate section header
dup_header = "## 19. REVISI TERBARU (Rev. 59 — 15 Oktober 2026 WIB)\n"
first_idx = None
last_idx = None
for i in range(len(lines)):
    if lines[i].startswith(dup_header):
        if first_idx is None:
            first_idx = i
        last_idx = i

print("First Rev. 59 header at line:", first_idx + 1)
print("Last Rev. 59 header at line:", last_idx + 1)

# The duplicate section starts at the second occurrence and ends before the final "Dibuat" note
if first_idx is not None and last_idx is not None:
    # Remove from second occurrence to end of file (minus the final note)
    # Find the final "Dibuat" note
    final_idx = None
    for i in range(len(lines)):
        if 'Dibuat dari data + riset' in lines[i]:
            final_idx = i
            break
    print("Final note at line:", final_idx + 1)
    
    if final_idx is not None:
        # Remove lines from last_idx to final_idx - 1, keep the final note and everything after
        removed = lines[last_idx:final_idx]
        print("Removed lines:", last_idx + 1, "to", final_idx)
        print("Removed content:")
        for i, l in enumerate(removed):
            print(f"  {last_idx + i + 1}: {l.rstrip()[:100]}")
        lines = lines[:last_idx] + lines[final_idx:]
        
        with open(path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        
        print("File updated successfully")
        print("New total lines:", len(lines))
    else:
        print("Final note not found!")
