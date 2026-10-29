import io

PATH = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"
with io.open(PATH, encoding="utf-8") as f:
    src = f.read()
lines = src.split("\n")

print("Total lines:", len(lines))
print()

# Status lines
print("=== Status lines ===")
for i, ln in enumerate(lines, 1):
    if "> **Status:** dokumen PRD **REVISI**" in ln:
        print(f"Line {i}: {ln[:150]}...")
        print()

# Marker counts
checks = [
    ("Rev. 707", "header rev 707"),
    ("2396ea51fcafed468f7476aa385c0a4cc635bf09", "HEAD hash (new)"),
    ("fd81e38d231cfae6bed25d8f2a9e65649748348e", "OLD HEAD hash (should be 0)"),
    ("718 / 14/0", "commit count"),
    ("Rev. 116–707", "section 11 title"),
    ("Rev. 116–704", "section 11 title (old)"),
]
print("=== Marker counts ===")
for marker, label in checks:
    count = sum(1 for ln in lines if marker in ln)
    print(f"  {label}: '{marker}' -> {count}")
