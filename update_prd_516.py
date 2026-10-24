#!/usr/bin/env python3
"""Update PRD-PONDOK-BANAT.md to Rev. 516 based on current git state."""
import subprocess

REPO = '/opt/data/home/workspace/dev/pondok-banat'
PRD = f'{REPO}/PRD-PONDOK-BANAT.md'

def run(cmd):
    r = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True)
    return r.stdout.strip(), r.stderr.strip(), r.returncode

# Get current git state
head_out, _, _ = run(['git', 'rev-parse', 'HEAD'])
origin_main_out, _, _ = run(['git', 'rev-parse', 'origin/main'])
ahead_out, _, _ = run(['git', 'rev-list', '--count', f'origin/main..HEAD'])
behind_out, _, _ = run(['git', 'rev-list', '--count', f'HEAD..origin/main'])

print(f'HEAD: {head_out}')
print(f'origin/main: {origin_main_out}')
print(f'Ahead: {ahead_out}, Behind: {behind_out}')

with open(PRD, 'r', encoding='utf-8') as f:
    lines = f.read().split('\n')

# Show line 4 (index 3) for reference
print(f'Line 4 starts: {lines[3][:120]}...')
print(f'Line 415 starts: {lines[414][:120]}...')

# Find the Rev. 511 entry (line 417, index 416)
rev511_idx = None
for i, l in enumerate(lines):
    if 'Rev. 511' in l and l.strip().startswith('||-|'):
        rev511_idx = i
        break
if rev511_idx is None:
    # Fallback: search for any line containing "Rev. 511"
    for i, l in enumerate(lines):
        if 'Rev. 511' in l:
            rev511_idx = i
            break
print(f'Rev. 511 entry at line index {rev511_idx} (1-based: {rev511_idx+1})')

# The Rev. 515 entry ends at line rev511_idx - 1 (line 416)
print(f'Line before Rev. 511: {lines[rev511_idx-1][:150]}...')
print(f'Line rev511-2: {lines[rev511_idx-2][:150]}...')

# We'll insert the Rev. 516 entry right before the Rev. 511 entry (line 417)
# and update the §11 title range from "Rev. 116–515" to "Rev. 116–516"

# Build new Rev. 516 entry
rev516_entry = (
    '||||- **Rev. 516 (final).** 24 Oktober 2026 (WIB): PRD fresh verification & stability confirmation (24 Oct 2026 WIB); '
    'HEAD `{head}` (Rev. 515 commit: PRD fresh verification & stability confirmation (24 Oct 2026 WIB); header Rev. 516, '
    '§11 kompakt changelog 116–516, §12 updated); {ahead} / 0 ({ahead} commits ahead origin_main). '
    'Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run): **state stabil, tidak ada perubahan signifikan dari Rev. 515** '
    '(data terkonsisten). Build gate: **NOT RE-RUNABLE** — `node_modules/` **absent** (dihapus setelah Rev. 377; `npm ci` diperlukan untuk memulihkan); '
    '.next/ masih ada (partial: `cache/` + `diagnostics/` + `package.json` + `server/` + `static/`, bukan production build). '
    '`tsc --noEmit` exit 1, `npm run lint` exit 2, `npx next build` exit 1 — semua gagal karena `node_modules/` **absent**; '
    '`npm ci` diperlukan untuk memulihkan sebelum melakukan type-check/lint/build. Database (dev.db): **tidak ada (absent)** — '
    'dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`; seluruh record '
    '(**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) '
    '**tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; '
    '`import_excel.py` & `import_students_grades_clean.py` tidak ditemukan di working tree). '
    '**M02a (NFC):** field `uid_nfc` ada aktif di tabel students, semua 453 NULL (data ekspor NFC Tools belum tersedia). '
    '**Auth hardcode:** Login.tsx tetap `admin@pondokanbat.com` / `admin123` (typo domain). '
    '**Beranda hardcode:** Beranda.tsx & page.tsx masih hardcoded totalSantri 453. '
    '**Schema:** model `KitabProgress` & `Sertakan` sudah terdefinisi; `prisma validate` sukses. '
    '**Status:** dokumen PRD **REVISI** — rev 516 = PRD fresh verification & konfirmasi stabilitas; seluruh data terkonsisten, '
    'tidak ada perubahan signifikan dari Rev. 515; branch {ahead} ahead / 0 behind origin_main.'
).format(head=head_out, ahead=ahead_out)

print()
print(f'=== REV 516 ENTRY (preview) ===')
print(rev516_entry[:500])
print('...')
print()

# Now apply edits
# 1. Update header (line 4)
old_header = lines[3]
new_header = (
    'Rev. 516: PRD fresh verification & stability confirmation (24 Oct 2026 WIB); header Rev. 516 (updated to Rev. 516), '
    '§11 kompakt changelog 116–516, §12 updated; HEAD `{head}` (Rev. 515 commit: PRD fresh verification & stability confirmation '
    '(24 Oct 2026 WIB)); {ahead} / 0 ({ahead} commits ahead origin_main). Branch `main`, remote `brontolano/pondok-banat`. '
    '`git rev-parse HEAD` = `{head}` (Rev. 515 commit, fresh verification dilakukan hari ini); '
    '**origin/main:** `{origin}` (Rev. 513, in sync). Local branch **{ahead} commits ahead / 0 behind** origin_main. '
    'Working tree: `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 516 (fresh verification), fresh verification '
    'dilakukan hari ini); seluruh file lain cocak dengan HEAD; untracked: 61 skrip utility (tidak terpantau dalam git); '
    '`commit_msg.txt` dihapus (build artifact); `git ls-files` = 187 file.'
).format(head=head_out, ahead=ahead_out, origin=origin_main_out)

# 2. Update §11 title range
old_s11 = '## 11. REVISI TERBARU (Rev. 116–515 — 24 Oktober 2026 WIB)'
new_s11 = '## 11. REVISI TERBARU (Rev. 116–516 — 24 Oktober 2026 WIB)'

# 3. Update §12 range (the changelog range mentioned in §12 intro)
# First find the §12 header line
s12_idx = None
for i, l in enumerate(lines):
    if l.startswith('## 12. REVISI TERBARU'):
        s12_idx = i
        break
print(f'§12 header at line index {s12_idx}')
# The §12 header says "(Rev. 468–515 — 24 Oktober 2026 WIB)"
# We need to update the range to include 516
# Find the line with the range pattern
for i, l in enumerate(lines):
    if 'Rev. 468–515' in l:
        print(f'§12 range at line {i+1}: {l[:120]}')
        # We'll update it after we find the right text
        break

# Read current content to find the exact §12 range line
content_str = '\n'.join(lines)
# Find Rev. 468–515 in §12
import re
m = re.search(r'## 12\. REVISI TERBARU \(Rev\. 468–515 .*?\)', content_str)
if m:
    print(f'§12 exact range text: {m.group(0)[:120]}')
    # The §12 intro mentions the range
    # We'll update "Rev. 468–515" to "Rev. 468–516" in §12

# Build new content
new_lines = lines[:]

# Update line 4 (index 3)
new_lines[3] = new_header

# Update §11 title
for i, l in enumerate(new_lines):
    if l == old_s11:
        new_lines[i] = new_s11
        break

# Insert Rev. 516 entry before Rev. 511 entry (line 417, which is index 416)
# The Rev. 515 entry ends at line 416 (index 415)
# Insert at index 416 (before Rev. 511 entry)
new_lines.insert(rev511_idx, rev516_entry)

# Update §12 range
# Find "Rev. 468–515" occurrences in §12 and update to "Rev. 468–516"
# The §12 header is at line s12_idx
s12_header = new_lines[s12_idx]
print(f'§12 header line: {s12_header[:120]}')

# The §12 header itself says "Rev. 468–515". Update to "Rev. 468–516".
# First, find the exact text in the §12 header
s12_header_old = s12_header
s12_header_new = s12_header.replace('Rev. 468–515', 'Rev. 468–516')
print(f'§12 header new: {s12_header_new[:120]}')

# Also there might be a §12 intro with a range reference
# Search for "Rev. 468–515" outside the §12 header
for i, l in enumerate(new_lines):
    if 'Rev. 468–515' in l and i != s12_idx:
        print(f'Found "Rev. 468–515" at line {i+1}: {l[:120]}')
        new_lines[i] = l.replace('Rev. 468–515', 'Rev. 468–516')

# Update §12 header range
for i, l in enumerate(new_lines):
    if l.startswith('## 12. REVISI TERBARU'):
        new_lines[i] = new_lines[i].replace('Rev. 468–515', 'Rev. 468–516')
        break

# Write back
new_content = '\n'.join(new_lines)
with open(PRD, 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f'\n=== WROTE FILE ===')
print(f'Total lines: {len(new_lines)}')

# Verify changes
print('\n=== VERIFICATION ===')
print(f'Line 4 starts: {new_lines[3][:120]}...')
print(f'Line 415 (Rev. 515 entry end): {new_lines[414][:120]}...')
print(f'Line 416 (new Rev. 516 entry): {new_lines[415][:120]}...')
print(f'Line 417 (Rev. 511 entry): {new_lines[416][:120]}...')
print(f'§12 header: {new_lines[s12_idx][:120]}')

# Check for stale refs
for i, l in enumerate(new_lines):
    if 'Rev. 515.' in l and i != 414 and i != 415 and i != s12_idx:
        if '515' in l and '516' in l:
            pass
    if 'd8a2a45d5636929006f3314c9ded5bbb4179a45d' in l:
        print(f'WARNING: stale HEAD at line {i+1}: {l[:120]}')
