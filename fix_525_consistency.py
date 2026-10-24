import io

path = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Complete list of replacements for Rev. 525 consistency
replacements = [
    # Header (line 4) fixes
    ("git rev-parse HEAD` = `167a1860ea7e3e31caa8202ccc01c741ea62021c` (Rev. 523 commit", "git rev-parse HEAD` = `e811c1b` (Rev. 525 commit"),
    ("Local branch **1 commit ahead / 0 behind** origin_main", "Local branch **3 commit ahead / 0 behind** origin_main"),
    ("HEAD `167a1860ea7e3e31caa8202ccc01c741ea62021c` (Rev. 523 commit)", "HEAD `e811c1b` (Rev. 525 commit)"),
    
    # §90 fixes (lines 459, 460, 484)
    ("`976ec9ec91228ebcd0a22dad865adf3e6aac79bf` (Rev. 525, commit 976ec9e)", "`e811c1b` (Rev. 525, commit e811c1b)"),
    ("Local branch **1 commit ahead**, **0 commit behind** origin.main", "Local branch **3 commits ahead**, **0 commit behind** origin.main"),
    ("HEAD `976ec9e` (Rev. 525)", "HEAD `e811c1b` (Rev. 525)"),
    ("Git HEAD = `976ec9ec91228ebcd0a22dad865adf3e6aac79bf` (Rev. 525)", "Git HEAD = `e811c1b` (Rev. 525)"),
    ("**1 commit ahead**, **0 commit behind**", "**3 commits ahead**, **0 commit behind**"),
    
    # §12 fixes (lines 490-510)
    ("1 / 0 (1 commit ahead origin_main)", "3 / 0 (3 commits ahead origin_main)"),
    ("Local branch **1 commit ahead / 0 behind** origin_main", "Local branch **3 commit ahead / 0 behind** origin_main"),
    
    # §12 long list fixes (lines 512-589) - commit counts
    ("1 / 0 (1 commit ahead origin_main)", "3 / 0 (3 commits ahead origin_main)"),
]

count = 0
for old, new in replacements:
    if old in content:
        content = content.replace(old, new)
        count += content.count(old)  # count total occurrences replaced

print(f"Total replacements made: {count}")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("File updated successfully.")
