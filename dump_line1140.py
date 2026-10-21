path = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"
with open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()

line = lines[1139]  # line 1140
print("LENGTH:", len(line))
print("REPR (first 400):", repr(line[:400]))
print("REPR (next 300):", repr(line[400:700]))
