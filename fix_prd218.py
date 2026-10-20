import io

path = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"
with io.open(path, "r", encoding="utf-8") as f:
    s = f.read()

edits = [
    # ---- Header line 4 ----
    ("> **Rev. 217 — 18 Oktober 2026 (WIB).", "> **Rev. 218 — 18 Oktober 2026 (WIB)."),
    ("Git HEAD: `500c643908097f1638366a77efd10a36da6a2a5f` (branch", "Git HEAD: `bf676c9f302a6b50255b208800598c36880e16c2` (branch"),
    ("git rev-parse HEAD` = `500c643908097f1638366a77efd10a36da6a2a5f`). Working tree", "git rev-parse HEAD` = `bf676c9f302a6b50255b208800598c36880e16c2`). Working tree"),
    ("revisi terbaru = Rev. 217, akan dicomit", "revisi terbaru = Rev. 218, akan dicomit"),
    ("Branch 57 commits ahead origin/main", "Branch 58 commits ahead origin/main"),
    # ---- Section 63 -> 64 ----
    ("## 63. REVISI TERBARU (Rev. 217 — 18 Oktober 2026 WIB)", "## 64. REVISI TERBARU (Rev. 218 — 18 Oktober 2026 WIB)"),
    ("**Git HEAD (local):** `500c643908097f1638366a77efd10a36da6a2a5f` \"Rev. 216: PRD fresh verification & stability confirmation (18 Oct 2026 WIB); updated header to Rev. 216 + added section 62\"", "**Git HEAD (local):** `bf676c9f302a6b50255b208800598c36880e16c2` \"Rev. 217: PRD fresh verification & stability confirmation (18 Oct 2026 WIB); updated header to Rev. 217 + added section 63\""),
    ("Local branch **57** commits ahead", "Local branch **58** commits ahead", 2),
    ("Branch ahead:** **57** commit (sebelumnya 56).", "Branch ahead:** **58** commit (sebelumnya 57)."),
    ("New Section 63 (Rev. 217):** ditambahkan", "New Section 64 (Rev. 218):** ditambahkan"),
    ("rev 217 = verifikasi fresh ulang", "rev 218 = verifikasi fresh ulang"),
    ("HEAD = `500c643908097f1638366a77efd10a36da6a2a5f`. Working tree bersih untuk tracked files. Branch **57** commits ahead", "HEAD = `bf676c9f302a6b50255b208800598c36880e16c2`. Working tree bersih untuk tracked files. Branch **58** commits ahead"),
]

for i, item in enumerate(edits):
    old, new = item[0], item[1]
    exp = item[2] if len(item) == 3 else 1
    cnt = s.count(old)
    assert cnt == exp, "EDIT %d MISMATCH for %r: expected %d got %d" % (i, old[:50], exp, cnt)
    s = s.replace(old, new)

with io.open("/opt/data/home/workspace/dev/pondok-banat/rev218_content.md", "r", encoding="utf-8") as f:
    section64 = f.read()

assert section64.startswith("## 64. REVISI TERBARU"), section64[:40]
s = s.rstrip() + "\n\n" + section64

with io.open(path, "w", encoding="utf-8") as f:
    f.write(s)

print("EDITS OK")
print("bytes=%d lines=%d" % (len(s.encode("utf-8")), s.count("\n") + 1))
print("HEAD refs remaining 500c643:", s.count("500c643"))
print("section64 header present:", section64.startswith("## 64. REVISI TERBARU"))
