# Update PRD header, §11, and §12 to Rev. 726
path = "PRD-PONDOK-BANAT.md"
with open(path, encoding="utf-8") as f:
    content = f.read()

# 1. Update header line (Rev. 725→726)
content = content.replace(
    "(Rev. 724→725): PRD fresh verification",
    "(Rev. 725→726): PRD fresh verification"
)
content = content.replace(
    "header Rev. 724→725; §11 compact changelog 116–724→116–725",
    "header Rev. 725→726; §11 compact changelog 116–725→116–726"
)
content = content.replace(
    "HEAD `4d9854e` (Rev. 724 final commit); commit count 735/0/0",
    "HEAD `4e4eb9a` (Rev. 725 final commit); commit count 736/1/0"
)
content = content.replace(
    "0 ahead origin_main, 0 behind",
    "1 ahead origin_main, 0 behind"
)
content = content.replace(
    "67 untracked helper scripts",
    "72 untracked helper scripts"
)

# 2. Update §11 heading
content = content.replace(
    "## 11. REVISI TERBARU (Rev. 116–725 — 29 Oktober 2026 WIB)",
    "## 11. REVISI TERBARU (Rev. 116–726 — 29 Oktober 2026 WIB)"
)

# 3. Update §12 heading
content = content.replace(
    "## 12. STATUS RINGKASAN (29 Oktober 2026 WIB) — Rev. 725",
    "## 12. STATUS RINGKASAN (29 Oktober 2026 WIB) — Rev. 726"
)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("Header, §11, and §12 updated to Rev. 726.")
