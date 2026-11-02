path = 'PRD-PONDOK-BANAT.md'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update the §11 compact changelog row
old1 = '''> - **§11 compact changelog:** extended 116–866→116–867 (row: `| 867 | 03 Nov | PENDING | ed4c449 | 927/15/0 | Rev. 867: PRD fresh verification & stability confirmation (cron run, 03 November 2026 WIB); header, §11 Rev. 867 entry & §12 status summary synced; HEAD `ed4c449` (Rev. 867 final sync — PRD synced ke Rev. 867); commit count 927/15/0 (927 local commits, 15 ahead / 0 behind origin_main).`);  // PENDING: commit hash to be filled after committing'''
new1 = '''> - **§11 compact changelog:** extended 116–866→116–867 (row: `| 867 | 03 Nov | 2ea8f6c | ed4c449 | 928/16/0 | Rev. 867: PRD fresh verification & stability confirmation (cron run, 03 November 2026 WIB); header, §11 Rev. 867 entry & §12 status summary synced; HEAD `2ea8f6c` (Rev. 867 committed — PRD synced ke Rev. 867); commit count 928/16/0 (928 local commits, 16 ahead / 0 behind origin_main).`);'''
if old1 not in content:
    print('ERROR: old1 not found')
else:
    content = content.replace(old1, new1)
    print('old1 replaced')

# 2. Update the §12 status summary
old2 = '''> - **§12 status summary:** updated to Rev. 867; commit count 927/15/0 (927 local commits, 15 ahead / 0 behind origin_main).'''
new2 = '''> - **§12 status summary:** updated to Rev. 867; commit count 928/16/0 (928 local commits, 16 ahead / 0 behind origin_main).'''
if old2 not in content:
    print('ERROR: old2 not found')
else:
    content = content.replace(old2, new2)
    print('old2 replaced')

# 3. Update the Status bullet
old3 = '''> - **Status:** dokumen PRD **REVISI** — rev 867: PRD fresh verification & stability confirmation (03 November 2026 (WIB)); HEAD `ed4c449` (Rev. 867 committed — PRD synced ke Rev. 867); **927 / 15/0** (927 local commits, 15 ahead / 0 behind origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 866 (data terkonsisten). Revision 867 confirms the completeness update of Rev. 866: §11 extended changelog & §12 updated.'''
new3 = '''> - **Status:** dokumen PRD **REVISI** — rev 867: PRD fresh verification & stability confirmation (03 November 2026 (WIB)); HEAD `2ea8f6c` (Rev. 867 committed — PRD synced ke Rev. 867); **928 / 16/0** (928 local commits, 16 ahead / 0 behind origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 866 (data terkonsisten). Revision 867 confirms the completeness update of Rev. 866: §11 extended changelog & §12 updated.'''
if old3 not in content:
    print('ERROR: old3 not found')
else:
    content = content.replace(old3, new3)
    print('old3 replaced')

# 4. Update the Repo state bullet
old4 = '''> - **Repo state:** clean working tree (PRD ditulis ke Rev. 867); HEAD `ed4c449` (Rev. 867 committed — PRD synced ke Rev. 867); **927 local commits, 15 ahead / 0 behind** origin_main; 413 tracked files; 1 untracked (`fix_dup_s12.py`); 0 deleted.'''
new4 = '''> - **Repo state:** clean working tree (PRD ditulis ke Rev. 867); HEAD `2ea8f6c` (Rev. 867 committed — PRD synced ke Rev. 867); **928 local commits, 16 ahead / 0 behind** origin_main; 413 tracked files; 2 untracked (incl. helper scripts); 0 deleted.'''
if old4 not in content:
    print('ERROR: old4 not found')
else:
    content = content.replace(old4, new4)
    print('old4 replaced')

# 5. Update the Commit count bullet
old5 = '''> - **Commit count:** 927 / 15/0 (fresh verification & stability confirmation, 03 November 2026 WIB); HEAD `ed4c449` (Rev. 867 committed — PRD synced ke Rev. 867); **927 / 15/0** (927 local commits, 15 ahead / 0 behind origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 866 (data terkonsisten).'''
new5 = '''> - **Commit count:** 928 / 16/0 (fresh verification & stability confirmation, 03 November 2026 WIB); HEAD `2ea8f6c` (Rev. 867 committed — PRD synced ke Rev. 867); **928 / 16/0** (928 local commits, 16 ahead / 0 behind origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 866 (data terkonsisten).'''
if old5 not in content:
    print('ERROR: old5 not found')
else:
    content = content.replace(old5, new5)
    print('old5 replaced')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('File length:', len(content))
