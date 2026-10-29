import io

path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'
with open(path, 'r') as f:
    content = f.read()

sha = '9881fb2bb82e4015d5ea42b889d6045f615891f0'

# Update header
old_header = 'HEAD `PENDING` (Rev. 619 final commit)'
new_header = 'HEAD `9881fb2bb82e4015d5ea42b889d6045f615891f0` (Rev. 619 final commit)'
content = content.replace(old_header, new_header)

# Update changelog row
old_cl = '|| 619 | 26 Okt | PENDING | PENDING | 2/0 | Rev. 619: PRD fresh verification & stability confirmation (cron run, 26 Oktober 2026 WIB); header Rev. 618→619; §11 compact changelog 116–618→116–619; §12 updated; HEAD PENDING (Rev. 619 final commit); commit count 2/0; node_modules present (479 dirs / 84021 files); dev.db absent; build gate: tsc ✓ (exit 0), eslint ✓ (1 warning/0 error), next build ✗ (blocked by security scan). Build gate NOT RE-RUNABLE. |'
new_cl = '|| 619 | 26 Okt | 9881fb2bb82e4015d5ea42b889d6045f615891f0 | 9881fb2bb82e4015d5ea42b889d6045f615891f0 | 2/0 | Rev. 619: PRD fresh verification & stability confirmation (cron run, 26 Oktober 2026 WIB); header Rev. 618→619; §11 compact changelog 116–618→116–619; §12 updated; HEAD 9881fb2bb82e4015d5ea42b889d6045f615891f0 (Rev. 619 final commit); commit count 2/0; node_modules present (479 dirs / 84021 files); dev.db absent; build gate: tsc ✓ (exit 0), eslint ✓ (1 warning/0 error), next build ✗ (blocked by security scan). Build gate NOT RE-RUNABLE. |'
content = content.replace(old_cl, new_cl)

# Update §12
old_s12 = 'Commit count: **2 / 0** (2 commits ahead origin_main, 0 behind). Local branch 2 commits ahead / 0 behind origin_main (HEAD PENDING, Rev. 619 final commit).'
new_s12 = 'Commit count: **2 / 0** (2 commits ahead origin_main, 0 behind). Local branch 2 commits ahead / 0 behind origin_main (HEAD 9881fb2bb82e4015d5ea42b889d6045f615891f0, Rev. 619 final commit).'
content = content.replace(old_s12, new_s12)

# Update Rev. 619 section
old_rev619 = '> **Rev. 619 (fresh).** 27 Oktober 2026 (WIB): CRON-run fresh verification & stability confirmation (cron run); HEAD `PENDING` (Rev. 619 final commit); **2 / 0** (2 commits ahead origin_main, 0 behind). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run):'
new_rev619 = '> **Rev. 619 (fresh).** 27 Oktober 2026 (WIB): CRON-run fresh verification & stability confirmation (cron run); HEAD `9881fb2bb82e4015d5ea42b889d6045f615891f0` (Rev. 619 final commit); **2 / 0** (2 commits ahead origin_main, 0 behind). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run):'
content = content.replace(old_rev619, new_rev619)

with open(path, 'w') as f:
    f.write(content)

print('Updated all PENDING references to SHA')
