#!/usr/bin/env python3
"""Verify final state of PRD"""
with open('/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md', 'r') as f:
    content = f.read()

print("=== HEAD (first 5 lines) ===")
for line in content.split('\n')[:5]:
    print(line[:100])

print()
print("=== FOOTER (last 5 lines) ===")
for line in content.split('\n')[-5:]:
    print(line[:120])

print()
print("=== TABLE ROWS (section 9.1) ===")
lines = content.split('\n')
in_table = False
for i, line in enumerate(lines):
    if '| M01 |' in line and 'Admin' in line:
        in_table = True
    if in_table:
        if line.startswith('|') and ('| M06 |' in line):
            break
        print(f"  {line[:130]}")
