REPO = '/opt/data/home/workspace/dev/pondok-banat'

with open(f'{REPO}/PRD-PONDOK-BANAT.md', 'r') as f:
    content = f.read()

# Fix 1: HEAD 29ad962 (29ad962 fix) -> HEAD 29ad962 (Rev. 648 fix)
content = content.replace('HEAD 29ad962 (29ad962 fix)',
                         'HEAD 29ad962 (Rev. 648 fix)')

# Fix 2: commit count 653/17/0 (652 local commits, 16 ahead origin_main, 0 behind)
# The old "652 local commits, 16 ahead" is still there but should be "653 local commits, 17 ahead"
content = content.replace('commit count 653/17/0 (652 local commits, 16 ahead origin_main, 0 behind)',
                         'commit count 653/17/0 (653 local commits, 17 ahead origin_main, 0 behind)')

with open(f'{REPO}/PRD-PONDOK-BANAT.md', 'w') as f:
    f.write(content)

print('Header fixes applied.')
