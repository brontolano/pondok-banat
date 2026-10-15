with open('/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md', 'r') as f:
    lines = f.readlines()

# Line 437 (0-indexed 436)
line = lines[436]

# Correct prefix
prefix = '   - **Status:** dokumen PRD **FINAL**; state stabil; rev 34 = verifikasi ulang & konfirmasi stabilitas (tidak ada perubahan dari Rev. 33).'

print("Prefix length:", len(prefix))
print("Line starts with prefix:", line.startswith(prefix))
if line.startswith(prefix):
    rev33_content = line[len(prefix):]
    print("Rev33 content length:", len(rev33_content))
    print("Rev33 content (first 100):", repr(rev33_content[:100]))
    print("Rev33 content (last 100):", repr(rev33_content[-100:]))
    
    # Build the full Rev. 33 entry
    rev33_prefix_line = lines[427]  # Line 428 (0-indexed 427)
    print("Rev33 prefix line:", repr(rev33_prefix_line))
    
    full_rev33_entry = rev33_prefix_line.rstrip('\n') + ' ' + rev33_content + '\n'
    
    # Replace
    lines[427] = full_rev33_entry
    lines[436] = prefix + '\n'
    
    with open('/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md', 'w') as f:
        f.writelines(lines)
    
    print("Fixed.")
    print("New file size:", sum(len(l) for l in lines), "bytes")
else:
    print("Prefix not found")
