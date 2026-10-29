lines = open("/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md").readlines()
target = "## 12. STATUS RINGKASAN (27 Oktober 2026 WIB)\n"
indices = [i for i, line in enumerate(lines) if line == target]
print("Found", len(indices), "occurrences at", [i+1 for i in indices])
if len(indices) > 1:
    dup_idx = indices[1]
    # Remove the duplicate header and the blank line before it
    # The blank line before the duplicate is at dup_idx-1
    del lines[dup_idx]  # Remove the duplicate header
    # Now check if the line before has \n and remove it if so
    # Actually, we want to keep 3 blank lines before the first header
    # Currently there are 4 blank lines (1019,1020,1021,1023) after removing dup header
    # So we need to remove 1 blank line
    del lines[dup_idx - 1]  # Remove the blank line that was before the duplicate
    open("/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md", "w").writelines(lines)
    print("Fixed. New line count:", len(lines))
else:
    print("No duplicate found")
