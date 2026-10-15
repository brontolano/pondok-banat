#!/usr/bin/env python3
"""Keep only the first Section 26 (Rev. 67) in PRD."""
PATH = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'

with open(PATH, 'r', encoding='utf-8') as f:
    content = f.read()

marker = '## 26. REVISI TERBARU (Rev. 67 — 15 Oktober 2026 WIB)'
count = content.count(marker)
print(f'Section 26 count: {count}')

# Keep everything up to and including the first Section 26
idx = content.find(marker)
if idx != -1:
    # Find the end of the first Section 26
    end_marker = '*Identifikasi entitas kartu identitas NFC hasil ekspor Android (NFC Tools): UID berformat hex `AF:C2:99:E7` dari blok MANUFACTURER/baris pertama yang diapit `[]`; pemrosesan string dilakukan dengan parsing UID dari ekspor NFC Tools, lalu pemetaan UID → NISN → record siswa.*'
    end_idx = content.find(end_marker, idx)
    if end_idx != -1:
        end_idx += len(end_marker)
        end_idx = content.find('\n', end_idx)
        first_section = content[:end_idx] + '\n\n'
        rest = content[end_idx:].lstrip('\n')
        new_content = content[:idx] + first_section + rest
        with open(PATH, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print('Fixed: kept only the first Section 26')
    else:
        print('ERROR: end marker not found')
else:
    print('ERROR: Section 26 marker not found')
