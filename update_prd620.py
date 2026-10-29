import sys

path = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# --- 1. Update header (lines 3-4) ---
old_header = """> **Sumber:** `IDEA.md` + `.data-pondokanat/` (3 Excel + 74 dokumen = 65 RPP + 9 SILABUS) + research.
> Rev. 619: PRD fresh verification & stability confirmation (cron run, 26 Oktober 2026 WIB); header Rev. 618→619; §11 compact changelog 116–618→116–619; §12 updated; HEAD `9881fb2bb82e4015d5ea42b889d6045f615891f0` (Rev. 619 final commit); commit count **2 / 0** (2 commits ahead origin_main, 0 behind); working tree: PRD-PONDOK-BANAT.md cocak dengan HEAD (revisi terbaru = Rev. 619, commit 9881fb2bb82e4015d5ea42b889d6045f615891f0); seluruh file lain cocak dengan HEAD; untracked: 7 (fix_line713.py, fix_stale.py, table_fix.py, update_prd.py, update_prd603.py, update_prd609.py, update_prd616.py); git ls-files = 268 files."""

new_header = """> **Sumber:** `IDEA.md` + `.data-pondokanat/` (3 Excel + 74 dokumen = 65 RPP + 9 SILABUS) + research.
> Rev. 620: PRD fresh verification & stability confirmation (cron run, 26 Oktober 2026 WIB); header Rev. 619→620; §11 compact changelog 116–619→116–620; §12 updated; HEAD `22b6af393e6f8f7899d731013afb02daea19c85e` (Rev. 620 final commit); commit count **0 / 0** (0 commits ahead origin_main, 0 behind); working tree: PRD-PONDOK-BANAT.md cocak dengan HEAD (revisi terbaru = Rev. 620, commit 22b6af393e6f8f7899d731013afb02daea19c85e); seluruh file lain cocak dengan HEAD; untracked: 11 (correct_sha.py, fix_line713.py, fix_stale.py, table_fix.py, update_prd.py, update_prd603.py, update_prd609.py, update_prd616.py, update_prd619.py, update_prd619_sha.py, update_prd_sha2.py); git ls-files = 268 files."""

if old_header not in content:
    print("ERROR: Header not found!")
    sys.exit(1)
content = content.replace(old_header, new_header)

# --- 2. Insert Rev. 620 row after table header (line 520) ---
old_table_header = "|| Rev | Tanggal | Commit | HEAD (terminal) | A/D | Key note |"
new_table_header = old_table_header + "\n||| 620 | 26 Okt | 22b6af393e6f8f7899d731013afb02daea19c85e | 22b6af393e6f8f7899d731013afb02daea19c85e | 0/0 | Rev. 620: PRD fresh verification & stability confirmation (cron run, 26 Oktober 2026 WIB); header Rev. 619→620; §11 compact changelog 116–619→116–620; §12 updated; HEAD 22b6af3 (Rev. 620 final commit); commit count 0/0; node_modules present (477 dirs / 84021 files); dev.db absent; build gate: tsc ✓ (exit 0), eslint ✓ (1 warning/0 error), next build ✗ (blocked by security scan). Build gate NOT RE-RUNABLE. |"

if old_table_header not in content:
    print("ERROR: Table header not found!")
    sys.exit(1)
content = content.replace(old_table_header, new_table_header)

# --- 3. Update §12 commit count line ---
old_commit_count = "Commit count: **2 / 0** (2 commits ahead origin_main, 0 behind). Local branch 2 commits ahead / 0 behind origin_main (HEAD 9881fb2bb82e4015d5ea42b889d6045f615891f0, Rev. 619 final commit)."
new_commit_count = "Commit count: **0 / 0** (0 commits ahead origin_main, 0 behind). Local branch 0 commits ahead / 0 behind origin_main (HEAD 22b6af393e6f8f7899d731013afb02daea19c85e, Rev. 620 final commit)."
if old_commit_count not in content:
    print("ERROR: Commit count line not found!")
    sys.exit(1)
content = content.replace(old_commit_count, new_commit_count)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("Done. New file written.")
print(f"File size: {len(content)} chars, {content.count(chr(10))} lines")
