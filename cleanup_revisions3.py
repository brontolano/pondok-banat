# Clean up the orphaned/old revisions section at the bottom of the PRD.

path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'
with open(path, 'r') as f:
    lines = f.readlines()

# Find the start of the orphaned revision section ("Nama file folder asli")
start_idx = None
end_idx = None

for i, line in enumerate(lines):
    if 'Nama file folder asli' in line:
        start_idx = i
        break

# Find the end: the "Dibuat dari data + riset" final note
for i, line in enumerate(lines):
    if 'Dibuat dari data + riset' in line:
        end_idx = i
        break

print(f"start_idx: {start_idx}, end_idx: {end_idx}")

if start_idx is not None and end_idx is not None:
    # Remove lines [start_idx, end_idx] inclusive (the orphaned section)
    # Keep everything before start_idx and after end_idx
    # The line after end_idx should be the final note
    new_lines = lines[:start_idx] + lines[end_idx+1:]
    
    with open(path, 'w') as f:
        f.writelines(new_lines)
    
    print(f"Cleaned up orphaned revisions. Removed lines {start_idx+1} to {end_idx+1}.")
    print(f"New total lines: {len(new_lines)}")
    print(f"Last line: {new_lines[-1].rstrip()}")
else:
    print(f"Could not find clean-up markers. start_idx={start_idx}, end_idx={end_idx}")
