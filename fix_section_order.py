#!/usr/bin/env python3
"""
Fix the PRD section ordering issue:
- §92 was added at line 6945 (wrong location, after §90)
- §91 was added at line 6979
- §92 should come after §91 (section 92 > 91)
- There is a duplicate content in §92 (the duplicate adds the "## 92." section when it shouldn't)
- Also there is a duplicate "Verifikasi fresh..." content inside §92 (lines 6947, 6951)

Correct order should be:
  §89 (305) at 6875
  §90 (306) at 6911
  §91 (307) at 6979
  §92 (308) should be the last section
"""
import re

PATH = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"

with open(PATH, "r") as f:
    content = f.read()

# Create a normalized copy for comparison
content_norm = content.replace("\r\n", "\n")

# Step 1: Remove the duplicate §92 content (the one at line 6945, before §91 at line 6979)
# The §92 section at line 6945 has a duplicate "Verifikasi fresh..." (lines 6947 and 6951)
# We need to remove the duplicate section

# Find the §92 section (the one that appears before §91)
section_92_pattern = r"## 92\. REVISI TERBARU \(Rev\. 313 — 19 Oktober 2026 WIB\)\n\n> \*\*Verifikasi fresh dilakukan:\*\* 19 Oktober 2026 \(WIB, cron run\) — query `sqlite3` ke `dev\.db`, `npx tsc --noEmit`, `npx eslint \., `npx eslint \., `npx next build`\.(?:\n\n1\. \*\*Verifikasi fresh kondisi repo \+ dev\.db \(SQLite, cron run\): state stabil\. Tidak ada perubahan signifikan dari Rev\. 312 \(data terkonsisten\)\.\)\n\n> \*\*Verifikasi fresh dilakukan:\*\* 19 Oktober 2026 \(WIB, cron run\) — query `sqlite3` ke `dev\.db`, `npx tsc --noEmit`, `npx eslint \., `npx eslint \., `npx next build`\.)?\n(1\. \*\*Verifikasi fresh kondisi repo \+ dev\.db \(SQLite, cron run\): state stabil\. Tidak ada perubahan signifikan dari Rev\. 312 \(data terkonsisten\)\.\n\s*-\*\* Git HEAD \(local\): .*?origin/main: .*?4 commits ahead.*?0 commit behind.*?)\n\n---\n\n## 91\. REVISI TERBARU \(Rev\. 312 — 19 Oktober 2026 WIB\)"

# Actually, let me do a simpler approach: find the §92 section that is BEFORE §91 and remove it
# The §92 section at line 6945 should be removed, and the §92 content should be added after §91

# Let me find the §92 section content by splitting the file
lines = content.split("\n")

# Find the line numbers of each section
section_positions = {}
for i, line in enumerate(lines):
    if line.startswith("## "):
        section_positions[line.split(".")[0]] = i

print("Section positions:")
for k, v in sorted(section_positions.items(), key=lambda x: int(x[0].split('.')[0]) if x[0].split('.')[0].isdigit() else 0):
    print(f"  {k}: line {v}")

# The §92 section is at ~6945, and §91 is at ~6979
# The §92 section is duplicated (appears at line 6945 and in lines 6951-6953)
# We need to remove the §92 section that appears BEFORE §91

# Find the §92 section start (the one before §91)
# The §92 section should end right before the "## 91." section
# Let's find the content between "## 92." and "## 91."

# Actually, let me take a simpler approach: remove the duplicate section

# The §92 section starts at line ~6945 and ends at line ~6975 (right before "## 91.")
# Let me extract the §92 content by finding the block between "## 92." and "## 91."

# Find the §92 section start
start_92 = None
end_92 = None
for i, line in enumerate(lines):
    if line.startswith("## 92. REVISI TERBARU"):
        start_92 = i
        break

# Find the §91 section start (the first one after §92)
for i in range(start_92 + 1, len(lines)):
    if lines[i].startswith("## 91. REVISI TERBARU"):
        end_92 = i
        break

print(f"§92 starts at line {start_92} (0-indexed), §91 starts at line {end_92}")

# The §92 section is from start_92 to end_92 (exclusive)
# Remove the §92 section
lines = lines[:start_92] + lines[end_92:]

# Now write the file back
with open(PATH, "w") as f:
    f.write("\n".join(lines))

print(f"Removed §92 section. New file has {len(lines)} lines.")
