#!/usr/bin/env python3
"""Find and replace footer using a shorter distinctive substring"""
import os
import re

base = "/opt/data/home/workspace/dev/pondok-banat"
prd = os.path.join(base, "PRD-PONDOK-BANAT.md")

with open(prd, encoding="utf-8") as f:
    txt = f.read()

# Find all occurrences of "Rev. 6"
positions = [m.start() for m in re.finditer(r'Rev\. 6', txt)]
print("Rev. 6 occurrences:", len(positions))
for p in positions:
    print(f"  Position {p}: ...{txt[p:p+80].replace(chr(10),' ')}...")

# Get the footer area (after the last "Rev. 6")
last_idx = positions[-1]
# Find the start of this footer (previous newline)
footer_start = txt.rfind("\n", 0, last_idx)
# Find the end of this footer (next newline after the * at the end)
# The footer ends with ".*" then a newline
footer_end = txt.find("*\n", last_idx)
if footer_end == -1:
    footer_end = txt.find("\n", last_idx + 100)

# Extract actual footer
actual_footer = txt[footer_start:footer_end]
print()
print("=== ACTUAL FOOTER ===")
print(repr(actual_footer[:300]))
print()

# Build new footer
new_footer = """*Rev. 7 — 14 Oktober 2026. Perubahan: 1) laporkan status aktual backend: 10 siswa (`inactive`), 13 kelas, 5 guru (semua Wali Kelas), 0 record tabel kurikulum/akademik/komunikasi; 2) sesuaikan status modul M03–M05, M07, M08 dari `🔜 Direncanakan` → `📋 Implementasi` (schema + seed + dashboard statis); 3) laporan `role_permissions` = 0 record (perizinan belum di-enforce); 4) catat `Beranda` statis totalSantri=42/totalGuru=27 vs DB 10/5; 5) koreksi folder data sumber `.data-pondokanat`. Rev. 6 = dokumen PRD sebelumnya.*"""

print("=== NEW FOOTER ===")
print(repr(new_footer[:300]))
print()

# Replace
new_txt = txt[:footer_start] + new_footer + "\n" + txt[footer_end+1:]  # +1 to skip the \n

# Verify
if new_footer in new_txt:
    print("REPLACEMENT SUCCESSFUL")
else:
    print("REPLACEMENT FAILED")

# Count
print("Lines:", new_txt.count(chr(10)) + 1)
print("Size:", len(new_txt))

# Save
with open(prd, "w", encoding="utf-8") as f:
    f.write(new_txt)

print("Saved.")
