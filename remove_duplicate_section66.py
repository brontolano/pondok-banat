#!/usr/bin/env python3
"""Remove duplicate section 66 from the PRD file."""

path = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Find all occurrences of section 66
import re
# Match "## 66. REVISI TERBARU (Rev. 288" and capture until "3. **Status:** dokemen PRD **REVISI**"
pattern = r"## 66\. REVISI TERBARU \(Rev\. 288 — 20 Oktober 2026 \(WIB\)\).*?(?=^## 66\. REVISI TERBARU \(Rev\. 288)"
matches = list(re.finditer(pattern, content, re.DOTALL | re.MULTILINE))

print(f"Found {len(matches)} occurrence(s) of section 66")

if len(matches) >= 2:
    # Keep the last occurrence, remove all before it
    last_match = matches[-1]
    # The next occurrence starts after the last match
    # Remove everything from the start of the first occurrence to the start of the second occurrence
    first_match = matches[0]
    second_match = matches[1]
    
    # Remove the content from the end of section 65 (which ends with "origin/main.") 
    # up to the start of the second occurrence
    end_of_section_65 = content.rfind("origin/main.", 0, first_match.start())
    if end_of_section_65 == -1:
        # Fallback: remove from beginning of first section 66
        end_of_section_65 = first_match.start()
    
    # Keep: content before the first section 66 (until end of section 65)
    before = content[:end_of_section_65]
    # Keep: from the second occurrence to end of file
    after = content[second_match.start():]
    
    new_content = before + after
    
    # Verify the count decreased
    old_content = content
    lines_before = old_content.count("\n")
    lines_after = new_content.count("\n")
    print(f"Lines before: {lines_before}, after: {lines_after}")
    
    with open(path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Duplicate section 66 removed")
else:
    print("Unexpected number of matches")
    print(f"Matches: {len(matches)}")
