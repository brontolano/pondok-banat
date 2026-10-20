# Fix the PRD file - add newline between Rev. 205 and Rev. 206 sections
with open('PRD-PONDOK-BANAT.md', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the problematic spot and fix it
old = '*Verifikasi dilakukan lewat: query `sqlite3` ke `dev.db` (tidak ada), `git` (HEAD/status/ahead/ls-files), `ls` (dev.db/node_modules/.data-pondokanat), `cat` (quality_gate.sh), `grep` (prisma schema, init_schema.sql, source files).## 93. REVISI TERBARU'
new = '*Verifikasi dilakukan lewat: query `sqlite3` ke `dev.db` (tidak ada), `git` (HEAD/status/ahead/ls-files), `ls` (dev.db/node_modules/.data-pondokanat), `cat` (quality_gate.sh), `grep` (prisma schema, init_schema.sql, source files).\n\n## 93. REVISI TERBARU'

if old in content:
    content = content.replace(old, new)
    with open('PRD-PONDOK-BANAT.md', 'w', encoding='utf-8') as f:
        f.write(content)
    print('Fixed successfully!')
else:
    print('Pattern not found!')
    # Debug
    idx = content.find('## 93. REVISI TERBARU')
    if idx != -1:
        print('Context:', repr(content[idx-150:idx+50]))
