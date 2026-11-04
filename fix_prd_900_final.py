with open('PRD-PONDOK-BANAT.md', 'r') as f:
    content = f.read()

# Fix header: HEAD 64322dd -> 0290cc9, commit count 981/8/0 -> 982/9/0
content = content.replace(
    'HEAD `64322dd` (Rev. 900 final sync — PRD synced ke Rev. 900); commit count 981/8/0 (981 local commits, 8 ahead / 0 behind origin_main)',
    'HEAD `0290cc9` (Rev. 900 final sync — PRD synced ke Rev. 900); commit count 982/9/0 (982 local commits, 9 ahead / 0 behind origin_main)'
)

# Fix §11 compact changelog row for Rev. 900
content = content.replace(
    '| 900 | 03 Nov | 64322dd | 64322ddad234015532d94dd572d2df4f9c5a7518 | 981/8/0 |',
    '| 900 | 03 Nov | 0290cc9 | 0290cc9f5581a0adae70546e744d928f94697f18 | 982/9/0 |'
)

# Fix §12 status summary table - Git HEAD
content = content.replace(
    '| Git HEAD | `64322dd` |',
    '| Git HEAD | `0290cc9` |'
)

# Fix §12 status summary table - Commit count
content = content.replace(
    '| Commit count | 981/8/0 |',
    '| Commit count | 982/9/0 |'
)

# Fix §12 status summary table - Commit count detail
content = content.replace(
    '981 local commits, 8 ahead / 0 behind',
    '982 local commits, 9 ahead / 0 behind'
)

# Fix §13 header
content = content.replace(
    'HEAD `64322dd`, 981 / 8/0',
    'HEAD `0290cc9`, 982 / 9/0'
)

# Fix §11 Rev. 900 entry - HEAD and commit count
content = content.replace(
    'HEAD `64322dd` (Rev. 900 final sync — PRD synced ke Rev. 900); commit count 981/8/0 (981 local commits, 8 ahead / 0 behind origin_main)',
    'HEAD `0290cc9` (Rev. 900 final sync — PRD synced ke Rev. 900); commit count 982/9/0 (982 local commits, 9 ahead / 0 behind origin_main)'
)

# Fix §11 Rev. 900 entry - in the status line
content = content.replace(
    'HEAD `64322dd`, 981 / 8/0',
    'HEAD `0290cc9`, 982 / 9/0'
)

# Fix §11 Rev. 900 entry - the compact changelog extended line
content = content.replace(
    '§11 compact changelog extended to Rev. 900 (116–899→116–900); §12 updated. No DB/schema/code changes; this revision confirms state stability and bumps document revision from 899 to 900.',
    '§11 compact changelog extended to Rev. 900 (116–899→116–900); §12 updated. No DB/schema/code changes; this revision confirms state stability and bumps document revision from 899 to 900. (Note: this Rev. 900 entry documents the state at commit 0290cc9 — 982/9/0).'
)

# Fix §13 notes - the Rev. 900 entry status line
content = content.replace(
    'rev 900: PRD fresh verification & stability confirmation (03 November 2026 WIB); HEAD `64322dd` (Rev. 900 final sync — PRD synced ke Rev. 900); 981 / 8/0 (981 local commits, 8 ahead / 0 behind origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 899 (data terkonsisten). Revision 900 bumps document revision dari 899 to 900.',
    'rev 900: PRD fresh verification & stability confirmation (03 November 2026 WIB); HEAD `0290cc9` (Rev. 900 final sync — PRD synced ke Rev. 900); 982 / 9/0 (982 local commits, 9 ahead / 0 behind origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 899 (data terkonsisten). Revision 900 bumps document revision dari 899 to 900.'
)

# Fix §13 notes - the older status line
content = content.replace(
    'Status: dokumen PRD **REVISI** — rev 900: PRD fresh verification & stability confirmation (03 November 2026 WIB); HEAD `64322dd` (Rev. 900 final sync — PRD synced ke Rev. 900); **981 / 8/0** (981 local commits, 8 ahead / 0 behind origin_main).',
    'Status: dokumen PRD **REVISI** — rev 900: PRD fresh verification & stability confirmation (03 November 2026 WIB); HEAD `0290cc9` (Rev. 900 final sync — PRD synced ke Rev. 900); **982 / 9/0** (982 local commits, 9 ahead / 0 behind origin_main).'
)

with open('PRD-PONDOK-BANAT.md', 'w') as f:
    f.write(content)

print("Done fixing PRD to actual git state (HEAD 0290cc9, 982/9/0)")
