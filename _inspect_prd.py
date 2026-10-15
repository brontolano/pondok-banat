import sys

with open('PRD-PONDOK-BANAT.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Show lines around the header (line 4 = index 3)
print("=== Header area (lines 1-5) ===")
for i in range(0, 5):
    print(f"{i+1}: {lines[i]}")

print("=== Revision history end (last 5 lines) ===")
for i in range(len(lines)-5, len(lines)):
    print(f"{i+1}: {lines[i]}")

print("=== Line 466 (index 465) ===")
print(f"{466}: {lines[465]}")

print("=== Line 467 (index 466) ===")
print(f"{467}: {lines[466]}")
