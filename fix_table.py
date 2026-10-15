#!/usr/bin/env python3
"""
Fix the markdown table structure in PRD-PONDOK-BANAT.md (Rev 5).
The notes for M01 and M04 were added as extra table cells, breaking the
table structure (header has 3 columns, rows have 4-5 cells).
Moves the notes out of the table into separate paragraphs.
"""
import os
import re

base = "/opt/data/home/workspace/dev/pondok-banat"
prd = os.path.join(base, "PRD-PONDOK-BANAT.md")

with open(prd, encoding="utf-8") as f:
    lines = f.readlines()

# Process line by line
new_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    
    # M01 row: has note appended after the table row
    if "| M01 |" in line and "Catatan statis" in line:
        # Remove the note from the table row
        line = line.split("> **Catatan statis:**")[0].rstrip() + " |\n"
        new_lines.append(line)
        # Add note as a separate paragraph after the row
        note = "\n> **Catatan statis:** Komponen `Beranda` menunjukkan `totalSantri: 42`, `totalGuru: 27` (placeholder statis), tidak mencerminkan jumlah sesungguhnya di `dev.db` (10 siswa, 5 guru).\n"
        new_lines.append(note)
        # Skip the original next line (the note was appended to the same line)
        i += 1
        continue
    
    # M04 row: has note appended after the table row
    if "| M04 |" in line and "Catatan Prisma" in line:
        # Remove the note from the table row
        line = line.split("> **Catatan Prisma:**")[0].rstrip() + " |\n"
        new_lines.append(line)
        # Add note as a separate paragraph after the row
        note = "\n> **Catatan Prisma:** model `KitabProgress` hanya direferensikan di `Subject` (`KitabProgress[]`) tetapi **tidak didefinisikan** di schema; perlu ditambahkan jika fitur progress kitab akan dibangun.\n"
        new_lines.append(note)
        i += 1
        continue
    
    new_lines.append(line)
    i += 1

# Write back
with open(prd, "w", encoding="utf-8") as f:
    f.writelines(new_lines)

print("=== Table structure fixed ===")
print("Lines:", len(new_lines))
