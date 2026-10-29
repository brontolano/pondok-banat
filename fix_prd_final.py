path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'
with open(path, 'r') as f:
    content = f.read()

changes = []

# 1. Header revision bump 672 -> 673
old = '(Rev. 672): PRD fresh verification & stability confirmation (cron run, 28 Oktober 2026 WIB); header Rev. 671→672; §11 compact changelog 116–669→116–672; §12 updated. HEAD `3c2622c` (Rev. 672 final commit); commit count 678/42/0 (678 local commits, 42 ahead origin_main, 0 behind); node_modules present (479 dirs / 84021 files);'
new = '(Rev. 673): PRD fresh verification & stability confirmation (cron run, 28 Oktober 2026 WIB); header Rev. 672→673; §11 compact changelog 116–669→116–673; §12 updated. HEAD `4ec8014` (Rev. 673 final commit); commit count 678/42/0 (678 local commits, 42 ahead origin_main, 0 behind); node_modules present (479 dirs / 84021 files);'
if old in content:
    content = content.replace(old, new)
    changes.append('header revision bumped to 673')
else:
    print('WARNING: header revision not found')

# 2. Fix duplicate "commit count:" on line 1253
old = '> - **Commit count:** commit count: 678 / 42 (678 local commits, 42 ahead origin_main, 0 behind). Local branch **678 commits ahead / 0 behind** origin_main (HEAD `4ec8014`, Rev. 672→673 final commit).'
new = '> - **Commit count:** 678 / 42 (678 local commits, 42 ahead origin_main, 0 behind). Local branch **678 commits ahead / 0 behind** origin_main (HEAD `4ec8014`, Rev. 672→673 final commit).'
if old in content:
    content = content.replace(old, new)
    changes.append('duplicate commit count fixed')
else:
    print('WARNING: duplicate commit count not found')

# 3. Fix node_modules in Rev. 673 entry (line 1252)
old = '> - **Repo state:** clean working tree; `dev.db` absen; `node_modules` present (5103 dirs / 84021 files); build gate NOT RE-RUNABLE (security scan).'
new = '> - **Repo state:** clean working tree; `dev.db` absen; `node_modules` present (479 dirs / 84021 files); build gate NOT RE-RUNABLE (security scan).'
if old in content:
    content = content.replace(old, new)
    changes.append('node_modules in Rev.673 entry fixed')
else:
    print('WARNING: node_modules in Rev.673 not found')

# 4. Fix §12 title
old = '## 12. STATUS RINGKASAN (28 Oktober 2026 WIB) — Rev. 672'
new = '## 12. STATUS RINGKASAN (28 Oktober 2026 WIB) — Rev. 673'
if old in content:
    content = content.replace(old, new)
    changes.append('§12 title updated')
else:
    print('WARNING: §12 title not found')

# 5. Fix node_modules in §12 bullet
old = '`node_modules` present (5103 dirs / 84021 files)'
new = '`node_modules` present (479 dirs / 84021 files)'
if old in content:
    content = content.replace(old, new)
    changes.append('node_modules in §12 fixed')
else:
    print('WARNING: node_modules in §12 not found')

# 6. Fix line 1267 final summary
old = 'Local branch **677 commits ahead / 0 behind** origin_main (HEAD `3c2622c`, Rev. 671→672 final commit). Rev. 670: PRD fresh verification & stability confirmation (cron run, 28 Oktober 2026 WIB); header Rev. 669→670; §11 compact changelog 116–669→116–672; §12 updated. Git HEAD `3c2622c` (Rev. 671→672 final commit); untracked helper scripts updated (27); dev.db & node_modules consistent dengan Rev. 672 verifikasi.'
new = 'Local branch **678 commits ahead / 0 behind** origin_main (HEAD `4ec8014`, Rev. 672→673 final commit). Rev. 670: PRD fresh verification & stability confirmation (cron run, 28 Oktober 2026 WIB); header Rev. 669→670; §11 compact changelog 116–669→116–672; §12 updated. Git HEAD `4ec8014` (Rev. 672→673 final commit); untracked helper scripts updated (27); dev.db & node_modules consistent dengan Rev. 673 verifikasi.'
if old in content:
    content = content.replace(old, new)
    changes.append('final summary line fixed')
else:
    print('WARNING: final summary line not found')

with open(path, 'w') as f:
    f.write(content)

print("Changes applied:", changes)
print("File length:", len(content))
