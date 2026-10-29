path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'
with open(path, 'r') as f:
    content = f.read()

checks = [
    ('(Rev. 673)', '(Rev. 672)'),
    ('header Rev. 672→673', 'header Rev. 671→672'),
    ('HEAD `4ec8014` (Rev. 673 final commit)', 'HEAD `3c2622c` (Rev. 672 final commit)'),
    ('commit count 678/42/0', 'commit count 677/41/0'),
    ('node_modules present (479 dirs', 'node_modules present (5103 dirs'),
    ('## 12. STATUS RINGKASAN (28 Oktober 2026 WIB) — Rev. 673', '## 12. STATUS RINGKASAN (28 Oktober 2026 WIB) — Rev. 672'),
    ('Local branch **678 commits ahead', 'Local branch **677 commits ahead'),
]

print('=== VERIFICATION ===')
all_ok = True
for good, bad in checks:
    if good in content:
        print(f'  OK: {good[:60]}')
    else:
        print(f'  FAIL: expected {good[:60]} but not found')
        if bad in content:
            print(f'  STILL PRESENT: {bad[:60]}')
        all_ok = False

print()
print('=== GIT DIFF STAT ===')
import subprocess
r = subprocess.run(['git', 'diff', '--stat'], cwd='/opt/data/home/workspace/dev/pondok-banat', capture_output=True, text=True)
print(r.stdout)
r2 = subprocess.run(['git', 'diff', '--numstat'], cwd='/opt/data/home/workspace/dev/pondok-banat', capture_output=True, text=True)
print(r2.stdout)
