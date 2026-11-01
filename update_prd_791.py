import os

path = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

updates = []

# === Update §12 content (Repo state line) ===
# Replace the Rev. 790 repo state with Rev. 791 repo state
old_repo_state = """> - **Repo state (Rev. 790):** HEAD `83aeb1ff863414dd83c6cd51dae3bb648474c014` (Rev. 789 committed); **809 local commits, 1 ahead / 0 behind** origin_main; 340 tracked files; 23 untracked; 0 deleted (fix_duplicate.py removed).
"""

new_repo_state = """> - **Repo state (Rev. 791):** HEAD `c603cf6` (Rev. 790 committed); **810 local commits, 2 ahead / 0 behind** origin_main; 340 tracked files; 23 untracked; 0 deleted (fix_duplicate.py removed).
"""

if old_repo_state in content:
    content = content.replace(old_repo_state, new_repo_state)
    updates.append("§12 Repo state: updated to Rev. 791 with correct commit count")
else:
    print("ERROR: §12 Repo state not found")
    # Show what's there
    idx = content.find("Repo state")
    if idx != -1:
        print("Context:", repr(content[idx-100:idx+100]))

# Write updated file
with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("Done.")
for u in updates:
    print("  -", u)
