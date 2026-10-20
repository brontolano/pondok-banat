# -*- coding: utf-8 -*-
import io

PATH = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'

with io.open(PATH, encoding='utf-8') as f:
    lines = f.readlines()

l4 = lines[3]

# Correct replacements (exact strings from header line 4)
replacements = [
    (
        "Git HEAD (local): `f94ce02771d46c40e9f4cfe2f158e4d5e8d9418d` (Rev. 331, commit `4bcbb7c`)",
        "Git HEAD (local): `a725883b7a661e45ce99ca3dd6674db390a99d04` (Rev. 332, commit `a725883`)",
    ),
    (
        "**origin/main:** `4bcbb7c9bbea23b9807260d3c497a7ab862cd8e6` (Rev. 330)",
        "**origin/main:** `a725883b7a661e45ce99ca3dd6674db390a99d04` (Rev. 332)",
    ),
    (
        "Local branch **1 commit ahead**",
        "Local branch **0 commits ahead**",
    ),
    (
        "revisi terbaru = Rev. 332, akan dicomit",
        "revisi terbaru = Rev. 333, akan dicomit",
    ),
    (
        "**Rev. 332 — 20 Oktober 2026 (WIB).**",
        "**Rev. 333 — 20 Oktober 2026 (WIB).**",
    ),
]

for i, (old, new) in enumerate(replacements):
    if old not in l4:
        print(f'Replacement {i} MISS: {old[:50]}')
    l4 = l4.replace(old, new)

lines[3] = l4

with io.open(PATH, 'w', encoding='utf-8') as f:
    f.writelines(lines)

# Verify header
print('--- header line 4 (first 200 chars) ---')
print(l4[:200])
print('--- header line 4 tail ---')
print(l4[-200:])
print('--- verify section 118 present ---')
text = io.open(PATH, encoding='utf-8').read()
print('has "## 118. REVISI TERBARU (Rev. 333" :', '## 118. REVISI TERBARU (Rev. 333' in text)
print('has "## 117. REVISI TERBARU (Rev. 332" :', '## 117. REVISI TERBARU (Rev. 332' in text)
print('total lines:', text.count('\n'))
