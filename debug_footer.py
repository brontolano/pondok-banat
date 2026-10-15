#!/usr/bin/env python3
"""Debug: find the exact footer in PRD"""
import os

base = "/opt/data/home/workspace/dev/pondok-banat"
prd = os.path.join(base, "PRD-PONDOK-BANAT.md")

with open(prd, encoding="utf-8") as f:
    txt = f.read()

# Find "Rev. 6"
idx = txt.find("Rev. 6")
if idx == -1:
    print("No 'Rev. 6' found")
else:
    # Find the footer area
    start = txt.rfind("\n", 0, idx)
    end = txt.find("\n", idx)
    if end == -1:
        end = len(txt)
    footer = txt[start:end]
    print("FOUND footer:")
    print(repr(footer))
    print()
    print("Length:", len(footer))

# Now search for my old_footer
old_footer = """*Rev. 6 — 14 Oktober 2026. Perubahan: 1) ekspansi §2.2 M02a: tambah tech spec `uid_nfc` (STRING, format `AF:C2:99:E7`, index unik) + data flow NFC; 2) §8.1 koreksi nama folder `data-pondokanat` (typo); 3) §8.1 catatan data NFC: UID siswa belum ada file terpisah, manual dari ekspor NFC Tools; 4) §9.1 tambah baris M02a status `🔜 Direncanakan` (uid_nfc belum di-seed, mapping UID→NISN belum diuji). Rev. 5 = dokumen PRD sebelumnya.*"""

print()
print("Search for old_footer...")
print("old_footer in txt:", old_footer in txt)
if old_footer not in txt:
    # Try to find differences
    idx2 = txt.find("Rev. 6 — 14 Oktober 2026")
    if idx2 >= 0:
        print("Found 'Rev. 6 — 14 Oktober 2026' at:", idx2)
        # Show 300 chars after
        print(repr(txt[idx2:idx2+300]))
