import io

PATH = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"
src = io.open(PATH, encoding="utf-8").read()
lines = src.split("\n")

# Rebuild old_r10 exactly as the patch script does
old_r10 = ("> **Status:** dokumen PRD **REVISI** \u2014 rev 704: PRD fresh verification & stability confirmation "
           "(28 Oktober 2026 (WIB)); HEAD `fd81e38d231cfae6bed25d8f2a9e65649748348e` (Rev. 703 final commit); "
           "**715 / 11/0** (715 local commits, 11 ahead origin_main, 0 behind). State stabil, tidak ada perubahan "
           "signifikan dari Rev. 703 (data terkonsisten). Build gate: tsc \u2713, eslint \u2713 (1 warning), "
           "next build \u2717 (SecurityFatalError Next.js 16.4.0).")

# Compare with each occurrence line
for i, ln in enumerate(lines):
    if "715 / 11/0" in ln:
        print(f"=== line {i+1} ===")
        # find first differing position
        for j, (a, b) in enumerate(zip(old_r10, ln)):
            if a != b:
                print(f"  first diff at pos {j}: script={a!r} file={b!r}")
                break
        else:
            print("  strings are identical")
        print("  length script:", len(old_r10), " length file:", len(ln))
