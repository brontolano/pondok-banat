import io

PATH = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"
src = io.open(PATH, encoding="utf-8").read()

old_r10 = ("> **Status:** dokumen PRD **REVISI** \u2014 rev 704: PRD fresh verification & stability confirmation "
           "(28 Oktober 2026 (WIB)); HEAD `fd81e38d231cfae6bed25d8f2a9e65649748348e` (Rev. 703 final commit); "
           "**715 / 11/0** (715 local commits, 11 ahead origin_main, 0 behind). State stabil, tidak ada perubahan "
           "signifikan dari Rev. 703 (data terkonsisten). Build gate: tsc \u2713, eslint \u2713 (1 warning), "
           "next build \u2717 (SecurityFatalError Next.js 16.4.0).")

print("count:", src.count(old_r10))
# Find the longest common substring to diagnose
import difflib
# Try a simpler distinctive substring
for probe in ["> **Status:** dokumen PRD **REVISI** \u2014 rev 704:", "715 / 11/0", "Build gate: tsc \u2713, eslint"]:
    print(probe, "->", src.count(probe))

# Show repr of the actual line 1399 to compare
lines = src.split("\n")
print("=== line 1399 repr ===")
print(repr(lines[1398]))
print("=== line 1279 repr ===")
print(repr(lines[1278]))
