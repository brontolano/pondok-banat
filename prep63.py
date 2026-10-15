#!/usr/bin/env python3
# Update PRD with Rev 63
import io

path = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Count occurrences of string patterns
import re
print("Occurrences of 'Rev. 62' in file:")
for i, line in enumerate(content.split("\n"), 1):
    if "Rev. 62" in line:
        print(f"  Line {i}: {line[:120]}...")

print("\nOccurrences of 'Verifikasi Rev. 62':")
for i, line in enumerate(content.split("\n"), 1):
    if "Verifikasi Rev. 62" in line:
        print(f"  Line {i}: {line[:120]}...")
