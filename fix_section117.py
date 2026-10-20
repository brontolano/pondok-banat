# -*- coding: utf-8 -*-
import io

PATH = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'

with io.open(PATH, encoding='utf-8') as f:
    text = f.read()

# Revert section 117's "git rev-parse HEAD" (it describes Rev.331 state, not Rev.332)
old = "`git rev-parse HEAD` = `a725883b7a661e45ce99ca3dd6674db390a99d04`), **origin/main:** `4bcbb7c9bbea23b9807260d3c497a7ab862cd8e6` (Rev. 330). Local branch **1 commit ahead**"
new = "`git rev-parse HEAD` = `f94ce02771d46c40e9f4cfe2f158e4d5e8d9418d`), **origin/main:** `4bcbb7c9bbea23b9807260d3c497a7ab862cd8e6` (Rev. 330). Local branch **1 commit ahead**"
print('fix3 count:', text.count(old))
text = text.replace(old, new)

with io.open(PATH, 'w', encoding='utf-8') as f:
    f.write(text)

# Verify
with io.open(PATH, encoding='utf-8') as f:
    lines = f.readlines()
print('--- verify section 117 line 7487 (git rev-parse) ---')
print(lines[7486][700:900])
print('--- verify header line 4 (git rev-parse) ---')
print(lines[3][1200:1450])
