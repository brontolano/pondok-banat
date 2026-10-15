path = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"

with open(path, "r", encoding="utf-8") as f:
    lines = f.read().split("\n")

changed = 0
out = []
for line in lines:
    if line.startswith("> **Rev. 56 — 15 Oktober 2026 (WIB).**"):
        # Update header synopsis from Rev. 56 to Rev. 57 (keep body Rev. 56 notes unchanged)
        nl = line.replace("Rev. 56 — 15 Oktober 2026", "Rev. 57 — 15 Oktober 2026")
        nl = nl.replace("(Verifikasi Rev. 56)", "(Verifikasi Rev. 57)")
        nl = nl.replace("rev 56 = verifikasi fresh ulang", "rev 57 = verifikasi fresh ulang")
        out.append(nl)
        changed += 1
    else:
        out.append(line)

print("header lines changed:", changed)
new_text = "\n".join(out)

with open(path, "w", encoding="utf-8") as f:
    f.write(new_text)

# Verify
with open(path, "r", encoding="utf-8") as f:
    v = f.read()

print("Rev. 57 header present:", "> **Rev. 57 — 15 Oktober 2026" in v)
print("Header still Rev. 56 (should be 0):", v.count("> **Rev. 56 — 15 Oktober 2026"))
print("Body Rev. 56 (§16) still present:", "## 16. REVISI TERBARU (Rev. 56" in v)
print("Header Rev. 57 synopsis count:", v.count("> **Rev. 57 — 15 Oktober 2026"))
