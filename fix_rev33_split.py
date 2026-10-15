with open('/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md', 'r') as f:
    lines = f.readlines()

# Find the Rev. 33 prefix line (line 428, 0-indexed 427)
rev33_prefix_line_idx = None
rev33_status_line_idx = None
for i, line in enumerate(lines):
    if line.startswith('10. **Rev. 33 — 14 Oktober 2026 (WIB).**'):
        rev33_prefix_line_idx = i
    if line.startswith('  - **Status:** dokumen PRD **FINAL**; state stabil; rev 34 = verifikasi ulang & konfirmasi stabilitas (tidak ada perubahan dari Rev. 33). Re-verification final kondisi repo'):
        rev33_status_line_idx = i

print("Rev33 prefix line:", rev33_prefix_line_idx)
print("Rev34 status line:", rev33_status_line_idx)

# The Rev. 33 content is the full line 437 minus the status bullet prefix
status_bullet_prefix = '  - **Status:** dokeman PRD **FINAL**; state stabil; rev 34 = verifikasi ulang & konfirmasi stabilitas (tidak ada perubahan dari Rev. 33).'
# Actually, the prefix uses 3 spaces before the dash (as shown in the line)
status_bullet_prefix = '   - **Status:** dokumen PRD **FINAL**; state stabil; rev 34 = verifikasi ulang & konfirmasi stabilitas (tidak ada perubahan dari Rev. 33).'

assert rev33_prefix_line_idx is not None
assert rev33_status_line_idx is not None

# Get the full Rev. 33 content from line 437 (after the status bullet prefix)
rev33_content_line = lines[rev33_status_line_idx]
assert rev33_content_line.startswith(status_bullet_prefix), f"Prefix mismatch: {rev33_content_line[:80]!r}"
rev33_content = rev33_content_line[len(status_bullet_prefix):]

# Build the full Rev. 33 entry
full_rev33_entry = '10. **Rev. 33 — 14 Oktober 2026 (WIB).** ' + rev33_content

# Replace line 428 with full Rev. 33 entry
lines[rev33_prefix_line_idx] = full_rev33_entry

# Replace line 437 with just the status bullet (removing the Rev. 33 content)
lines[rev33_status_line_idx] = status_bullet_prefix + '\n'

with open('/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md', 'w') as f:
    f.writelines(lines)

print("Fixed.")
print("New file size:", sum(len(l) for l in lines), "bytes")
