import io
path = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"
s = io.open(path, encoding="utf-8").read()

# Unique anchor: only appears in changelog table row "556"
anchor = "Rev. 555\u2192556"
idx = s.find(anchor)
if idx == -1:
    print("Anchor NOT found")
else:
    row_start = s.rfind("|||||||", 0, idx)
    if row_start == -1:
        print("Row start not found")
    else:
        row_end = s.find("\n", idx)
        if row_end == -1:
            row_end = len(s)
        old_row = s[row_start:row_end]
        print("Matched row (len=%d):" % len(old_row))
        print(old_row)
        new_row = (
            "||||||| 598 | 26 Okt | 62b5eaf | 62b5eaf | 16/0 | Rev. 598: PRD fresh verification & stability confirmation (cron run, 26 Oktober 2026 WIB); header Rev. 597\u2192598; §11 compact changelog 116\u2013597; §12 updated; HEAD 62b5eaf (Rev. 598 final commit); commit count 16/0; node_modules present (5103 dirs / 84,021 files); dev.db absent; build gate NOT RE-RUNABLE (security scan) |"
        )
        s = s[:row_start] + new_row + s[row_end:]
        io.open(path, "w", encoding="utf-8").write(s)
        print("Done")
