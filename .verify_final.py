#!/usr/bin/env python3
path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'
with open(path, 'r') as f:
    content = f.read()

# Final verification checks
checks = {
    'Header Rev. 947': 'Rev. 947 (fresh verification' in content,
    'Header HEAD 201f494c': 'HEAD 201f494c284b1943f8cf77298ab448488c200197' in content,
    'Commit count 1049/7/0': 'commit count 1049/7/0' in content,
    'Changelog 116-946->116-947': '116–946→116–947' in content,
    '§11 Rev.947 section': '### Rev. 947' in content,
    '§11 Rev.946 changelog row updated': 'Rev. 947: PRD fresh verification' in content,
    '§12 table Rev.947 git head': '201f494c284b1943f8cf77298ab448488c200197` | "PRD Rev. 947' in content,
    '§13 notes Rev.947': 'Refreshed 04 November 2026 WIB; HEAD `201f494c284b1943f8cf77298ab448488c200197` (Rev. 947 final commit)' in content,
    'Node modules 84021': 'node_modules present (84021 files / 478 top-level dirs)' in content,
    'Working tree 3 untracked': '3 untracked (.probe_devdb.py, .probe_devdb2.py, .probe_final.py)' in content,
}

all_pass = True
for check, result in checks.items():
    status = '✓' if result else '✗'
    if not result:
        all_pass = False
    print(f'  {status} {check}')

print(f'\nAll checks passed: {all_pass}')
