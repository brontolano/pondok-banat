import io

PATH = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"
with io.open(PATH, encoding="utf-8") as f:
    lines = f.read().splitlines(keepends=True)

s13_head = None
for i, l in enumerate(lines):
    if l.startswith("## 13. DAFTAR REVISI"):
        s13_head = i
        break
assert s13_head is not None, "§13 heading not found"

new_s13 = [
    "## 13. DAFTAR REVISI (REFERENSI)\n",
    "- **Rev. 415:** header Rev. 415, §11 compact changelog 116–414, §12 updated, §13 updated to Rev. 415. HEAD `a564301` (Rev. 415: PRD fresh verification & stability confirmation (21 Oct 2026 WIB)), 20 / 0 (20 commits ahead origin_main).\n",
    "|- **Rev. 414:** header Rev. 414, §11 compact changelog 116–413, §12 updated, §13 updated to Rev. 414. HEAD `63facea` (Rev. 414: PRD fresh verification & stability confirmation), 19 / 0 (19 commits ahead origin_main).\n",
    "|- **Rev. 413:** header Rev. 413, §11 compact changelog 116–412, §12 updated, §13 updated to Rev. 413. HEAD `62e3a13` (Rev. 413: PRD fresh verification & stability confirmation), 18 / 0 (18 commits ahead origin_main).\n",
    "|- **Rev. 412:** header Rev. 412, §11 compact changelog 116–411, §12 updated; HEAD `f2f0235` (Rev. 412: PRD fresh verification & stability confirmation), 17 / 0 (17 commits ahead origin_main).\n",
    "- **Rev. 411:** header Rev. 411, §11 compact changelog 116–410, §12 updated, §13 added. HEAD `80a450d` (Rev. 411: PRD fresh verification & stability confirmation), 16 / 0 (16 commits ahead origin_main).\n",
    "- **Rev. 410:** header Rev. 410, §11 compact changelog 116–409, §12 updated, §13 updated to Rev. 410. HEAD `2091a7d` (Rev. 410: PRD fresh verification & stability confirmation), 15 / 0 (15 commits ahead origin_main).\n",
    "- **Rev. 409–380:** header Rev. 409–380, §11 compact changelog 116–408, §12 updated, §13 updated to corresponding rev.\n",
    "- **Rev. 377–378:** header Rev. 377–378, §11 changelog 116–377/378, §12 updated.\n",
    "- **Rev. 376 and below:** various header and §12 updates.\n",
]
lines[s13_head:] = new_s13

with io.open(PATH, "w", encoding="utf-8") as f:
    f.write("".join(lines))

print("§13 replaced. new total lines:", len(lines))
