# Clean up the orphaned/old revisions section at the bottom of the PRD.

path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'
with open(path, 'r') as f:
    lines = f.readlines()

# Find the start of the orphaned revision section (the "Nama file folder asli" note)
start_idx = None
end_idx = None

for i, line in enumerate(lines):
    if 'Nama file folder asli' in line:
        start_idx = i
        break

# Find the end: the Rev. 9 revision line + the line after it (blank)
for i, line in enumerate(lines):
    if 'Rev. 9 — 14 Oktober 2026' in line and 'Rev. 9 = dokumen PRD sebelumnya' in line:
        end_idx = i
        break

print(f"start_idx: {start_idx}, end_idx: {end_idx}")

if start_idx is not None and end_idx is not None:
    # Remove the orphaned note (start_idx) through end_idx (inclusive),
    # i.e., remove lines [start_idx, end_idx] inclusive
    new_lines = lines[:start_idx]
    
    # Add a clean closing section
    closing = [
        '\n\n---\n',
        '> *Rev. 22 — 14 Oktober 2026 (WIB).* **Status akhir PRD:** Dokumen telah diverifikasi dengan kondisi repo + DB aktual. Semua modul M01–M05 sudah diimplementasikan / di-seed; M06, M10, M11 tertunda di roadmap. Build quality gate lulus tanpa error (`tsc --noEmit` ✓ exit 0, `npm run lint` ✓ exit 0, `npm run build` ✓ BUILD_EXIT=0). Rev. 22 = dokumen PRD akhir.\n',
        '\n'
    ]
    new_lines.extend(closing)
    
    with open(path, 'w') as f:
        f.writelines(new_lines)
    
    print(f"Cleaned up orphaned revisions. Removed lines {start_idx+1} to {end_idx+1}.")
    print(f"New total lines: {len(new_lines)}")
else:
    print(f"Could not find clean-up markers. start_idx={start_idx}, end_idx={end_idx}")
