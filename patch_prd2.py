REPO = '/opt/data/home/workspace/dev/pondok-banat'

with open(f'{REPO}/PRD-PONDOK-BANAT.md', 'r') as f:
    content = f.read()

# Fix the section 12 commit count line
old_s12 = '**Commit count:** **653 / 17/0** (652 local commits, 16 ahead origin_main, 0 behind). Local branch **652 commits ahead / 0 behind** origin_main (HEAD `29ad962`, Rev. 648 fix).'
new_s12 = '''**Commit count:** **653 / 17/0** (653 local commits, 17 ahead origin_main, 0 behind). Local branch **653 commits ahead / 0 behind** origin_main (HEAD `29ad962`, Rev. 648 fix). Rev. 648: PRD fresh verification & stability confirmation (cron run, 27 Oktober 2026 WIB); header Rev. 647→648; §11 compact changelog 116–647→116–648; §12 updated. Git HEAD `5923ef60d5d62e37bf31761d3b2f76b7ba5f03ae` (Rev. 647 final commit); untracked helper scripts unchanged; dev.db & node_modules consistent with Rev. 648 verification. Rev. 649: PRD fresh verification & stability confirmation (cron run, 27 Oktober 2026 WIB); header Rev. 648→649; §11 compact changelog 116–648→116–649; §12 updated. Git HEAD `29ad962` (Rev. 648 fix, new commit, revisi PRD ke Rev. 649); untracked helper scripts unchanged; dev.db & node_modules consistent with Rev. 649 verification.'''

if old_s12 in content:
    content = content.replace(old_s12, new_s12)
    print('Section 12 fixed.')
else:
    print('ERROR: section 12 pattern not found')
    # Debug - find the relevant lines
    for i, line in enumerate(content.splitlines()):
        if '**Commit count:**' in line and '653 / 17/0' in line:
            print(f'Line {i+1}: {line[:120]}...')

with open(f'{REPO}/PRD-PONDOK-BANAT.md', 'w') as f:
    f.write(content)

print('Done.')
