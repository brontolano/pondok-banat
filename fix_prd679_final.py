#!/usr/bin/env python3
"""Fix remaining Rev. 678 references and newline issues in PRD."""

FILE = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"

with open(FILE, 'r') as f:
    content = f.read()

# 1. Change the second "### Rev. 678" to "### Rev. 679"
old_head2 = "### Rev. 678\n"
new_head2 = "### Rev. 679\n"
count_head2 = content.count(old_head2)
print(f"'# # # Rev. 678' remaining: {count_head2}")
content = content.replace(old_head2, new_head2)

# 2. Change "Rev. 678 (fresh)" to "Rev. 679 (fresh)" in section content
old_fresh = "> **Rev. 678 (fresh).**"
new_fresh = "> **Rev. 679 (fresh).**"
count_fresh = content.count(old_fresh)
print(f"'Rev. 678 (fresh)' remaining: {count_fresh}")
content = content.replace(old_fresh, new_fresh)

# 3. Fix the newline issue: "data terkonsisten).### Rev. 679" -> "data terkonsisten).\n### Rev. 679"
old_no_newline = "data terkonsisten).### Rev. 679"
new_with_newline = "data terkonsisten).### Rev. 679"
if old_no_newline in content:
    print("Fixing newline issue...")
    content = content.replace(old_no_newline, new_with_newline)

# 4. Verify
count_rev678 = content.count("Rev. 678")
count_rev679 = content.count("Rev. 679")
print(f"Final check - 'Rev. 678': {count_rev678}, 'Rev. 679': {count_rev679}")

with open(FILE, 'w') as f:
    f.write(content)

print("Fixes applied successfully.")
