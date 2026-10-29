with open('/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md', 'r') as f:
    content = f.read()

old_header = """> Rev. 618: PRD fresh verification & stability confirmation (cron run, 26 Oktober 2026 WIB); header Rev. 617→618; §11 compact changelog 116–617→116–618; §12 updated; HEAD `b77a5ec` (Rev. 618 final commit); commit count **1 / 0** (1 commit ahead origin_main, 0 behind); working tree: PRD-PONDOK-BANAT.md cocak dengan HEAD (revisi terbaru = Rev. 618, commit b77a5ec); seluruh file lain cocak dengan HEAD; untracked: 7 (fix_line713.py, fix_stale.py, table_fix.py, update_prd.py, update_prd603.py, update_prd609.py, update_prd616.py); git ls-files = 268 files."""

new_header = """> Rev. 619: PRD fresh verification & stability confirmation (cron run, 26 Oktober 2026 WIB); header Rev. 618→619; §11 compact changelog 116–618→116–619; §12 updated; HEAD `PENDING` (Rev. 619 final commit); commit count **2 / 0** (2 commits ahead origin_main, 0 behind); working tree: PRD-PONDOK-BANAT.md cocak dengan HEAD (revisi terbaru = Rev. 619, commit PENDING); seluruh file lain cocak dengan HEAD; untracked: 7 (fix_line713.py, fix_stale.py, table_fix.py, update_prd.py, update_prd603.py, update_prd609.py, update_prd616.py); git ls-files = 268 files."""

content = content.replace(old_header, new_header)

# Add changelog row after the 618 row
old_changelog_row = """|| 618 | 26 Okt | b77a5ec | b77a5ec | 1/0 | Rev. 618: PRD fresh verification & stability confirmation (cron run, 26 Oktober 2026 WIB); header Rev. 617→618; §11 compact changelog 116–617→116–618; §12 updated; HEAD b77a5ec (Rev. 618 final commit); commit count 1/0; node_modules present (477 dirs / 84,021 files); dev.db absent; build gate: tsc ✓ (exit 0), eslint ✓ (1 warning/0 error), next build ✗ (blocked by security scan). Build gate NOT RE-RUNABLE. |"""

new_changelog_row = """|| 618 | 26 Okt | b77a5ec | b77a5ec | 1/0 | Rev. 618: PRD fresh verification & stability confirmation (cron run, 26 Oktober 2026 WIB); header Rev. 617→618; §11 compact changelog 116–617→116–618; §12 updated; HEAD b77a5ec (Rev. 618 final commit); commit count 1/0; node_modules present (477 dirs / 84,021 files); dev.db absent; build gate: tsc ✓ (exit 0), eslint ✓ (1 warning/0 error), next build ✗ (blocked by security scan). Build gate NOT RE-RUNABLE. |


|| 619 | 26 Okt | PENDING | PENDING | 2/0 | Rev. 619: PRD fresh verification & stability confirmation (cron run, 26 Oktober 2026 WIB); header Rev. 618→619; §11 compact changelog 116–618→116–619; §12 updated; HEAD PENDING (Rev. 619 final commit); commit count 2/0; node_modules present (479 dirs / 84021 files); dev.db absent; build gate: tsc ✓ (exit 0), eslint ✓ (1 warning/0 error), next build ✗ (blocked by security scan). Build gate NOT RE-RUNABLE. |"""

content = content.replace(old_changelog_row, new_changelog_row)

# Update §12 status summary
old_s12 = """Commit count: **1 / 0** (1 commit ahead origin_main, 0 behind). Local branch 1 commit ahead / 0 behind origin_main (HEAD b77a5ec, Rev. 618 final commit)."""
new_s12 = """Commit count: **2 / 0** (2 commits ahead origin_main, 0 behind). Local branch 2 commits ahead / 0 behind origin_main (HEAD PENDING, Rev. 619 final commit)."""
content = content.replace(old_s12, new_s12)

with open('/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md', 'w') as f:
    f.write(content)

print("Done")
