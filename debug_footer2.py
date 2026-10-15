#!/usr/bin/env python3
"""Compare old_footer with actual footer character by character"""
import os

base = "/opt/data/home/workspace/dev/pondok-banat"
prd = os.path.join(base, "PRD-PONDOK-BANAT.md")

with open(prd, encoding="utf-8") as f:
    txt = f.read()

# Extract actual footer
idx = txt.find("Rev. 6")
start = txt.rfind("\n", 0, idx)
end = txt.find("\n", idx)
if end == -1:
    end = len(txt)
actual_footer = txt[start:end]
print("=== ACTUAL FOOTER (repr) ===")
print(repr(actual_footer))
print()

# My old footer (copy from update_prd_v7.py)
old_footer = """*Rev. 6 — 14 Oktober 2026. Perubahan: 1) ekspansi §2.2 M02a: tambah tech spec `uid_nfc` (STRING, format `AF:C2:99:E7`, index unik) + data flow NFC; 2) §8.1 koreksi nama folder `data-pondokanat` (typo); 3) §8.1 catatan data NFC: UID siswa belum ada file terpisah, manual dari ekspor NFC Tools; 4) §9.1 tambah baris M02a status `🔜 Direncanakan` (uid_nfc belum di-seed, mapping UID→NISN belum diuji). Rev. 5 = dokumen PRD sebelumnya.*"""

print("=== MY OLD FOOTER (repr) ===")
print(repr(old_footer))
print()

# Compare
if actual_footer == old_footer:
    print("FOUND EXACT MATCH")
else:
    print("MISMATCH")
    print()
    # Find first difference
    for i, (a, b) in enumerate(zip(actual_footer, old_footer)):
        if a != b:
            print(f"First diff at position {i}:")
            print(f"  actual: {repr(actual_footer[max(0,i-20):i+20])}")
            print(f"  mine:   {repr(old_footer[max(0,i-20):i+20])}")
            break
    else:
        print("Lengths differ:")
        print(f"  actual: {len(actual_footer)}")
        print(f"  mine:   {len(old_footer)}")
