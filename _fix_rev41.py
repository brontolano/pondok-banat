with open('/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md', 'r') as f:
    lines = f.readlines()

# Fix line 470 (index 469): change Rev. 42 to Rev. 41, Rev. 41 to Rev. 40, rev 42 to rev 41
# This is the original Rev. 41 entry that was incorrectly changed
line_470 = lines[469]
# Replace Rev. 42 with Rev. 41 at the start of the line
line_470 = line_470.replace('> **Rev. 42 — 14 Oktober 2026 (WIB).**', '> **Rev. 41 — 14 Oktober 2026 (WIB).**')
# Replace 'dari Rev. 41' with 'dari Rev. 40'
line_470 = line_470.replace('dari Rev. 41 (data terverifikasi ulang)', 'dari Rev. 40 (data terverifikasi ulang)')
# Replace 'rev 42' with 'rev 41' in the status
line_470 = line_470.replace('rev 42 = verifikasi fresh & konfirmasi stabilitas.', 'rev 41 = verifikasi fresh & konfirmasi stabilitas.')
lines[469] = line_470

with open('/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md', 'w') as f:
    f.writelines(lines)

print('Fixed line 470')
print('Line 470:', repr(lines[469]))
