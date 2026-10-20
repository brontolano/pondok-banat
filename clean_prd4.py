with open('PRD-PONDOK-BANAT.md', 'r') as f:
    lines = f.readlines()

# The legitimate sections are numbered sequentially: ## 1., ## 2., ..., ## 57. (Rev. 170)
# Then the final section should be ## 58. (Rev. 171)
# All the spurious "## 58. REVISI TERBARU (Rev. 171" inserted between legitimate sections need removal

# Strategy: Keep only the FIRST occurrence of each legitimate section number
# And keep only the LAST occurrence of ## 58. (the final Rev. 171 section)

legitimate_sections_seen = set()
clean_lines = []
i = 0

while i < len(lines):
    line = lines[i]
    
    # Check if this is a section header
    if line.startswith('## '):
        # Check if it's a spurious ## 58. Rev. 171 section
        if '## 58. REVISI TERBARU (Rev. 171' in line:
            # This is a spurious section - skip it and its content until next legitimate section
            # Skip until we find the next legitimate section header (## N. where N < 58, or the final ## 58. at the end)
            i += 1
            # Skip content until next section header that's not a spurious ## 58.
            while i < len(lines):
                if lines[i].startswith('## ') and '## 58. REVISI TERBARU (Rev. 171' not in lines[i]:
                    # This is a legitimate section, stop skipping
                    break
                i += 1
            continue
    
    clean_lines.append(line)
    i += 1

print(f"Original lines: {len(lines)}")
print(f"Clean lines: {len(clean_lines)}")

with open('PRD-PONDOK-BANAT.md', 'w') as f:
    f.writelines(clean_lines)
print("Done")