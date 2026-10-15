content = open('/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md', 'r').read()

# Find the header block
header_start = content.find('> **Sumber:**')
header_end_marker = 'rev 42 = verifikasi fresh & konfirmasi stabilitas.'
header_end = content.find(header_end_marker, header_start)
print('Header start:', header_start)
print('Header end:', header_end)
print('Header block:', repr(content[header_start:header_end+60]))

# Find the revision history block
rev42_hist = content.find('> **Rev. 42 — 14 Oktober 2026 (WIB).**', header_end)
print('Revision history Rev.42 start:', rev42_hist)
print('Next 100 chars:', repr(content[rev42_hist:rev42_hist+100]))
