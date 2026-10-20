path = "PRD-PONDOK-BANAT.md"
with open(path, "r") as f:
    lines = f.readlines()

# Line 4 (index 3) is the header line
# It starts with "> **Rev. 283 — 19 Oktober 2026 (WIB).**"
# Rewrite the entire header content after the initial marker

old_line = lines[3]

# Find what needs to change
print("OLD HEADER (first 300 chars):")
print(old_line[:300])
print("...")
print("OLD HEADER (last 200 chars):")
print(old_line[-200:])
