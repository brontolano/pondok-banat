path = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

old = """> > - **Repo state (Rev. 759):** HEAD `1aa511d` (Rev. 758 final commit, Rev. 759 PRD sync); **773 local commits, 5 ahead / 0 behind** origin_main; 340 tracked files; 8 untracked (check_header.py, dev_report.py, prd_update_758.py, prd_update_script.py, update_prd_757.py, verify_current.py, verify_db.py, verify_db_check.py, verify_fresh.py); 0 deleted (fix_duplicate.py removed)."""

new = """> > - **Repo state (Rev. 760):** HEAD `0aa3589` (Rev. 759 committed; Rev. 760 in working tree); **774 local commits, 0 ahead / 0 behind** origin_main; 340 tracked files; 9 untracked (check_header.py, dev_report.py, prd_update_758.py, prd_update_script.py, update_prd_757.py, verify_current.py, verify_db.py, verify_db_check.py, verify_fresh.py); 0 deleted (fix_duplicate.py removed)."""

if old in content:
    content = content.replace(old, new, 1)
    print("Repo state line: updated to Rev. 760")
else:
    print("Repo state line: OLD NOT FOUND")
    import re
    m = re.search(r"> > - \*\*Repo state.*?removed\)\.", content)
    if m:
        print("Found:", m.group(0)[:200])

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("Done")
