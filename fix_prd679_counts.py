#!/usr/bin/env python3
"""Fix remaining commit count and newline issues."""

FILE = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"

with open(FILE, 'r') as f:
    content = f.read()

# 1. Fix commit count "688 / 52" -> "689 / 53" (in the Rev. 679 sections)
old_rc = """commit count **688 / 52** (688 local commits, 52 ahead origin_main, 0 behind). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run):"""
new_rc = """commit count **689 / 53** (689 local commits, 53 ahead origin_main, 0 behind). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run):"""
count_rc = content.count(old_rc)
print(f"'commit count **688 / 52**' remaining: {count_rc}")
content = content.replace(old_rc, new_rc)

# 2. Fix the newline issue: "data terkonsisten).### Rev. 679" -> "data terkonsisten).\n### Rev. 679"
old_nn = "data terkonsisten).### Rev. 679"
new_nn = "data terkonsisten).\n### Rev. 679"
if old_nn in content:
    print("Fixing newline issue...")
    content = content.replace(old_nn, new_nn)

# 3. Verify
count_rev678 = content.count("Rev. 678")
count_rev679 = content.count("Rev. 679")
print(f"Final check - 'Rev. 678': {count_rev678}, 'Rev. 679': {count_rev679}")
print(f"File size: {len(content)} bytes")

with open(FILE, 'w') as f:
    f.write(content)

print("Fixes applied successfully.")
