import io

path = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"
with io.open(path, "r", encoding="utf-8") as f:
    s = f.read()

fixes = [
    # Header line 4: "HEAD = 500c643" -> current HEAD bf676c9
    ("HEAD = `500c643908097f1638366a77efd10a36da6a2a5f`; 23 skrip bantuan",
     "HEAD = `bf676c9f302a6b50255b208800598c36880e16c2`; 23 skrip bantuan"),
    # Section 63 verification bullet: "git rev-parse HEAD = 500c643" -> bf676c9
    ("git rev-parse HEAD` = `500c643908097f1638366a77efd10a36da6a2a5f`). Local branch **58**",
     "git rev-parse HEAD` = `bf676c9f302a6b50255b208800598c36880e16c2`). Local branch **58**"),
]

for i, (old, new) in enumerate(fixes):
    cnt = s.count(old)
    assert cnt == 1, "B-EDIT %d MISMATCH for %r: count=%d" % (i, old[:50], cnt)
    s = s.replace(old, new)

with io.open(path, "w", encoding="utf-8") as f:
    f.write(s)

print("B-EDITS OK")
print("500c643 remaining:", s.count("500c643"))
print("bf676c9 total:", s.count("bf676c9"))
