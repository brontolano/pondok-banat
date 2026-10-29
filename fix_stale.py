import io

path = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"
s = io.open(path, encoding="utf-8").read()

# Fix the remaining stale commit count line
old = "> > - Commit count: **16 / 0** (16 commits ahead origin_main, 0 behind). Branch 16 commits ahead of origin/main (`ed6551d`, Rev. 583)."
new = "> > - Commit count: **17 / 0** (17 commits ahead origin_main, 0 behind). Branch 17 commits ahead of origin/main (`ed6551d`, Rev. 583)."

count = s.count(old)
print("Count of old pattern:", count)
if count == 1:
    s = s.replace(old, new)
    print("Replaced successfully")
else:
    print("ERROR: pattern not found")

# Check for stale patterns
stale_found = []
for pat in ["16 / 0", "**16 commits ahead", "Rev. 598 (final)"]:
    if pat in s:
        stale_found.append(pat)
if stale_found:
    print("STALE FOUND:", stale_found)
else:
    print("No stale patterns found")

io.open(path, "w", encoding="utf-8").write(s)
print("File written")
