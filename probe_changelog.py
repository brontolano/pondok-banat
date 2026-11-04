#!/usr/bin/env python3
"""Find changelog sequence patterns in PRD."""
import re

with open("/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md") as f:
    content = f.read()

# Find the changelog sequence in the header
m = re.search(r'§11 compact changelog ([^;]+);', content)
if m:
    print("HEADER changelog:", repr(m.group(1)[:300]))

# Find the Rev. 914 entry
for pat in [r'extended 116–91[34]→116–91[34]', r'116–91\d→116–91\d']:
    for mm in re.finditer(pat, content):
        print(f"Pattern {pat}:", repr(mm.group()))

# Find all '116–' sequences in Rev. 914 area
idx = content.find("### Rev. 914")
if idx >= 0:
    section = content[idx:idx+2000]
    seqs = re.findall(r'116–91\d→116–91\d', section)
    print("Rev. 914 area 116-91x sequences:", seqs)

# Check if header has 116-914
if "116–914" in content:
    print("Header contains 116-914")
else:
    print("Header does NOT contain 116-914")

# Show the header line
lines = content.split("\n")
print("Line 3 start:", lines[2][:200])
