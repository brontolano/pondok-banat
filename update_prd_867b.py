path = 'PRD-PONDOK-BANAT.md'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Update the Rev. 867 entry with the actual commit hash
old_entry = '''> - **§11 compact changelog:** extended 116–866→116–867 (row: `| 867 | 03 Nov | PENDING | ed4c449 | 927/15/0 | Rev. 867: PRD fresh verification & stability confirmation (cron run, 03 November 2026 WIB); header, §11 Rev. 867 entry & §12 status summary synced; HEAD `ed4c449` (Rev. 867 final sync — PRD synced ke Rev. 867); commit count 927/15/0 (927 local commits, 15 ahead / 0 behind origin_main).`);  // PENDING: commit hash to be filled after committing
> - **§12 status summary:** updated to Rev. 867; commit count 927/15/0 (927 local commits, 15 ahead / 0 behind origin_main).
> - **Status:** dokumen PRD **REVISI** — rev 867: PRD fresh verification & stability confirmation (03 November 2026 (WIB)); HEAD `ed4c449` (Rev. 867 committed — PRD synced ke Rev. 867); **927 / 15/0** (927 local commits, 15 ahead / 0 behind origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 866 (data terkonsisten). Revision 867 confirms the completeness update of Rev. 866: §11 extended changelog & §12 updated.'''

new_entry = '''> - **§11 compact changelog:** extended 116–866→116–867 (row: `| 867 | 03 Nov | 2ea8f6c | ed4c449 | 928/16/0 | Rev. 867: PRD fresh verification & stability confirmation (cron run, 03 November 2026 WIB); header, §11 Rev. 867 entry & §12 status summary synced; HEAD `2ea8f6c` (Rev. 867 committed — PRD synced ke Rev. 867); commit count 928/16/0 (928 local commits, 16 ahead / 0 behind origin_main).`);  // commit hash 2ea8f6c after committing
> - **§12 status summary:** updated to Rev. 867; commit count 928/16/0 (928 local commits, 16 ahead / 0 behind origin_main).
> - **Status:** dokumen PRD **REVISI** — rev 867: PRD fresh verification & stability confirmation (03 November 2026 (WIB)); HEAD `2ea8f6c` (Rev. 867 committed — PRD synced ke Rev. 867); **928 / 16/0** (928 local commits, 16 ahead / 0 behind origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 866 (data terkonsisten). Revision 867 confirms the completeness update of Rev. 866: §11 extended changelog & §12 updated.'''

if old_entry not in content:
    print('ERROR: old_rev867_entry not found')
    raise SystemExit(1)

content = content.replace(old_entry, new_entry)

# Update the "Repo state" bullet
old_repo = '''> - **Repo state:** clean working tree (PRD ditulis ke Rev. 867); HEAD `ed4c449` (Rev. 867 committed — PRD synced ke Rev. 867); **927 local commits, 15 ahead / 0 behind** origin_main; 413 tracked files; 1 untracked (`fix_dup_s12.py`); 0 deleted.'''
new_repo = '''> - **Repo state:** clean working tree (PRD ditulis ke Rev. 867); HEAD `2ea8f6c` (Rev. 867 committed — PRD synced ke Rev. 867); **928 local commits, 16 ahead / 0 behind** origin_main; 413 tracked files; 2 untracked (incl. helper scripts); 0 deleted.'''
if old_repo not in content:
    print('ERROR: old_repo not found')
    raise SystemExit(1)
content = content.replace(old_repo, new_repo)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Done')
print('File length:', len(content))
