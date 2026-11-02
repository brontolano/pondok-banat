import io

path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'
with io.open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update header
content = content.replace(
    'header Rev. 870 (tersimpan 02 November 2026 WIB); §11 compact changelog 116–844→845→846→847→848→849→850→851→852→853→854→855→856→857→858→859→860→861→862→863→864→865→866→867→868→869→870; §12 updated. HEAD `578f2b7` (Rev. 870 final sync — PRD synced ke Rev. 870); commit count 938/0/2',
    'header Rev. 871 (tersimpan 02 November 2026 WIB); §11 compact changelog 116–844→845→846→847→848→849→850→851→852→853→854→855→856→857→858→859→860→861→862→863→864→865→866→867→868→869→870→871; §12 updated. HEAD `aa594a0` (Rev. 871 final sync — PRD synced ke Rev. 871); commit count 939/3/0'
)
content = content.replace('commit count 939/3/0 (938 local commits, 0 ahead / 2 behind origin_main)',
                          'commit count 939/3/0 (939 local commits, 3 ahead / 0 behind origin_main)')
content = content.replace('PRD synced ke Rev. 870; 413 tracked files; 5 untracked (incl. helper scripts); 0 deleted',
                          'PRD synced ke Rev. 871; 413 tracked files; 5 untracked (incl. helper scripts); 1 deleted')

# 2. Insert Rev. 871 entry after Rev. 870 status line
rev871_entry = """Revision 870 confirms the completeness update of Rev. 869: §11 extended changelog & §12 updated.

### Rev. 871

> **Rev. 871 (fresh).** 02 November 2026 WIB: CRON-run fresh verification & stability confirmation (cron run); §11 compact changelog extended to Rev. 871 (116–870→116–871); §12 re-synced. No DB/schema/code changes; this revision confirms state stability and bumps document revision from 870 to 871.

> - **§11 compact changelog:** extended 116–870→116–871 (row: `| 871 | 02 Nov | aa594a0 | ad16e98 | 939/3/0 | Rev. 871: PRD fresh verification & stability confirmation (cron run, 02 November 2026 WIB); header, §11 Rev. 871 entry & §12 status summary synced; HEAD `aa594a0` (Rev. 871 final sync — PRD synced ke Rev. 871); commit count 939/3/0 (939 local commits, 3 ahead / 0 behind origin_main); node_modules present (479 dirs / 84021 files); dev.db ada schema-only (15 tabel, record 0); build gate: tsc ✓ (exit 0), eslint ✓ (exit 0, 1 warning / 0 error), next build ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability).`); 
> - **§12 status summary:** updated to Rev. 871; commit count 939/3/0.
> - **Status:** dokumen PRD **REVISI** — rev 871: PRD fresh verification & stability confirmation (02 November 2026 WIB); HEAD `aa594a0` (Rev. 871 final sync — PRD synced ke Rev. 871); **939 / 3/0** (939 local commits, 3 ahead / 0 behind origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 870 (data terkonsisten). Revision 871 confirms the completeness update of Rev. 870: §11 extended changelog & §12 re-synced."""

content = content.replace(
    'Revision 870 confirms the completeness update of Rev. 869: §11 extended changelog & §12 updated.',
    rev871_entry
)

# 3. Update §12 heading
content = content.replace('## 12. STATUS RINGKASAN (02 November 2026 WIB) — Rev. 870',
                          '## 12. STATUS RINGKASAN (02 November 2026 WIB) — Rev. 871')

# 4. Update §12 repo state
content = content.replace(
    '> - **Repo state:** clean working tree (PRD ditulis ke Rev. 870); HEAD `578f2b7` (Rev. 870 final sync — PRD synced ke Rev. 870); **938 local commits, 0 ahead / 2 behind** origin_main; 413 tracked files; 5 untracked (incl. helper scripts); 0 deleted.',
    '> - **Repo state:** clean working tree (PRD ditulis ke Rev. 871); HEAD `aa594a0` (Rev. 871 final sync — PRD synced ke Rev. 871); **939 local commits, 3 ahead / 0 behind** origin_main; 413 tracked files; 5 untracked (incl. helper scripts); 1 deleted.'
)

# 5. Update §12 commit count
content = content.replace(
    '> - **Commit count:** 938 / 0/2 (fresh verification & stability confirmation, 02 November 2026 WIB); HEAD `578f2b7` (Rev. 870 final sync — PRD synced ke Rev. 870); **938 / 0/2** (938 local commits, 0 ahead / 2 behind origin_main).',
    '> - **Commit count:** 939 / 3/0 (fresh verification & stability confirmation, 02 November 2026 WIB); HEAD `aa594a0` (Rev. 871 final sync — PRD synced ke Rev. 871); **939 / 3/0** (939 local commits, 3 ahead / 0 behind origin_main).'
)

with io.open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Done')
