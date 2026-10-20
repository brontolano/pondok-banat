with open('PRD-PONDOK-BANAT.md', 'r') as f:
    content = f.read()

# Fix header internal references
old_header = 'Git HEAD (local): `f62fee56215d49e6989b47b4c1a604d03e7b9cb3` (Rev. 336, commit `f62fee5`) (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `f62fee56215d49e6989b47b4c1a604d03e7b9cb3`). **origin/main:** `9bbeee0bcebbac0c1326cc662e50a3cf4e7b27e4` (Rev. 333). Local branch **4 commits ahead**, **0 commit behind** origin.main. Working tree: PRD cocak dengan HEAD (revisi terbaru = Rev. 337);'

new_header = 'Git HEAD (local): `246cfe08234ff889a7f6b74fb4b2f41d558996c7` (Rev. 337, commit `246cfe0`) (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `246cfe08234ff889a7f6b74fb4b2f41d558996c7`). **origin/main:** `9bbeee0bcebbac0c1326cc662e50a3cf4e7b27e4` (Rev. 333). Local branch **4 commits ahead**, **0 commit behind** origin.main. Working tree: PRD cocak dengan HEAD (revisi terbaru = Rev. 338);'

if old_header in content:
    content = content.replace(old_header, new_header)
    print('Header fixed')
else:
    print('Header pattern not found')
    if 'revisi terbaru = Rev. 337' in content:
        print('Found revisi terbaru = Rev. 337')
    if 'f62fee56215d49e6989b47b4c1a604d03e7b9cb3' in content:
        print('Found f62fee562... in header')

with open('PRD-PONDOK-BANAT.md', 'w') as f:
    f.write(content)
print('Done')
