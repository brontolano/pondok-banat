import re

path = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"
with open(path, "r") as f:
    content = f.read()

# 1. Header: Rev. 634 -> Rev. 635, commit count 637/1/0 -> 638/2/0, HEAD a700d10 -> 52a6e27
old_header = '''> **Rev. 634:** PRD fresh verification & stability confirmation (cron run, 27 Oktober 2026 WIB); header Rev. 633→634; §11 compact changelog 116–633→116–634; §12 updated. HEAD `a700d1073dbaf9c5c866d204ab40c0a3ec7cdd77` (Rev. 634 final commit); commit count **637 / 1/0** (637 local commits, 1 ahead origin_main, 0 behind); node_modules present (5103 dirs / 84,021 files); dev.db absent (removed by HEAD "Release: clean core files only"); build gate: tsc ✓ (exit 0), eslint ✓ (1 warning / 0 error), next build ✗ (blocked by Next.js security nudge — NOT RE-RUNABLE). Working tree: PRD-PONDOK-BANAT.md cocak dengan HEAD (revisi terbaru = Rev. 634); seluruh file lain cocak dengan HEAD; untracked: 14 (correct_sha.py, fix_line713.py, fix_stale.py, table_fix.py, update_prd.py, update_prd603.py, update_prd609.py, update_prd616.py, update_prd619.py, update_prd619_sha.py, update_prd620.py, update_prd_626.py, update_prd_627.py, update_prd_sha2.py); git ls-files = 268 files.'''

new_header = '''> **Rev. 635:** PRD fresh verification & stability confirmation (cron run, 27 Oktober 2026 WIB); header Rev. 634→635; §11 compact changelog 116–634→116–635; §12 updated. HEAD `52a6e27` (Rev. 635 final commit); commit count **638 / 2/0** (638 local commits, 2 ahead origin_main, 0 behind); node_modules present (477 dirs / 84,021 files); dev.db absent (removed by HEAD "Release: clean core files only"); build gate: tsc ✓ (exit 0), eslint ✓ (1 warning / 0 error), next build ✗ (blocked by Next.js security nudge — NOT RE-RUNABLE). Working tree: PRD-PONDOK-BANAT.md cocak dengan HEAD (revisi terbaru = Rev. 635); seluruh file lain cocak dengan HEAD; untracked: 14 (correct_sha.py, fix_line713.py, fix_stale.py, table_fix.py, update_prd.py, update_prd603.py, update_prd609.py, update_prd616.py, update_prd619.py, update_prd619_sha.py, update_prd620.py, update_prd_626.py, update_prd_627.py, update_prd_sha2.py); git ls-files = 268 files.'''

assert old_header in content, "Header not found"
content = content.replace(old_header, new_header)

# 2. Section 11 header: Rev. 116-634 -> Rev. 116-635
old_s11 = "## 11. REVISI TERBARU (Rev. 116–634 — 27 Oktober 2026 WIB)"
new_s11 = "## 11. REVISI TERBARU (Rev. 116–635 — 27 Oktober 2026 WIB)"
assert old_s11 in content, "Section 11 header not found"
content = content.replace(old_s11, new_s11)

# 3. Add Rev. 635 row to changelog
old_changelog = '''||||||| 634 | 27 Okt | a700d1073dbaf9c5c866d204ab40c0a3ec7cdd77 | a700d1073dbaf9c5c866d204ab40c0a3ec7cdd77 | 1/0 | Rev. 634: PRD fresh verification & stability confirmation (cron run, 27 Oktober 2026 WIB); header Rev. 633→634; §11 compact changelog 116–633→116–634; §12 updated. HEAD a700d10 (Rev. 634 final commit); commit count 637/1/0; node_modules present (5103 dirs / 84,021 files); dev.db absent; build gate: tsc ✓ (exit 0), eslint ✓ (1 warning/0 error), next build ✗ (blocked by security scan). Build gate NOT RE-RUNABLE.'''

new_changelog = '''||||||| 634 | 27 Okt | a700d1073dbaf9c5c866d204ab40c0a3ec7cdd77 | a700d1073dbaf9c5c866d204ab40c0a3ec7cdd77 | 1/0 | Rev. 634: PRD fresh verification & stability confirmation (cron run, 27 Oktober 2026 WIB); header Rev. 633→634; §11 compact changelog 116–633→116–634; §12 updated. HEAD a700d10 (Rev. 634 final commit); commit count 637/1/0; node_modules present (5103 dirs / 84,021 files); dev.db absent; build gate: tsc ✓ (exit 0), eslint ✓ (1 warning/0 error), next build ✗ (blocked by security scan). Build gate NOT RE-RUNABLE.

||||||| 635 | 27 Okt | 52a6e2797f0d5c2c3229217230c53c4461e0c60e | 52a6e2797f0d5c2c3229217230c53c4461e0c60e | 2/0 | Rev. 635: PRD fresh verification & stability confirmation (cron run, 27 Oktober 2026 WIB); header Rev. 634→635; §11 compact changelog 116–634→116–635; §12 updated. HEAD 52a6e27 (Rev. 635 final commit); commit count 638/2/0; node_modules present (477 dirs / 84,021 files); dev.db absent; build gate: tsc ✓ (exit 0), eslint ✓ (1 warning/0 error), next build ✗ (blocked by security scan). Build gate NOT RE-RUNABLE.'''

assert old_changelog in content, "Changelog row not found"
content = content.replace(old_changelog, new_changelog)

# 4. Section 12: commit count 637/1/0 -> 638/2/0
old_s12 = '''> > - Commit count: **637 / 1/0** (637 local commits, 1 ahead origin_main, 0 behind). Local branch 637 commits ahead / 0 behind origin_main (HEAD a700d1073dbaf9c5c866d204ab40c0a3ec7cdd77, Rev. 634 final commit).'''
new_s12 = '''> > - Commit count: **638 / 2/0** (638 local commits, 2 ahead origin_main, 0 behind). Local branch 638 commits ahead / 0 behind origin_main (HEAD 52a6e2797f0d5c2c3229217230c53c4461e0c60e, Rev. 635 final commit).'''
assert old_s12 in content, "Section 12 commit count not found"
content = content.replace(old_s12, new_s12)

with open(path, "w") as f:
    f.write(content)

print("Updated PRD to Rev. 635 successfully.")
