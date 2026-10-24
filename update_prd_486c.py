# -*- coding: utf-8 -*-
import io
PATH = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"
with io.open(PATH, "r", encoding="utf-8") as f:
    src = f.read()

def repl(old, new, label):
    global src
    n = src.count(old)
    if n != 1:
        raise SystemExit("FAIL [%s]: count=%d for: %r" % (label, n, old[:120]))
    src = src.replace(old, new, 1)
    print("OK [%s]" % label)

# Status bullet: ff465bb (hash) + 14/0 -> d918408f + 15/0
repl("HEAD `ff465bba47116093782778b49af31211368cf13d` (Rev. 486), 14 / 0 (14 commits ahead origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 485 (data terkonsisten).",
     "HEAD `d918408f8872e29ac70459f171259a48248a94b5` (Rev. 486), 15 / 0 (15 commits ahead origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 485 (data terkonsisten).",
     "s12-sb-fix")

with io.open(PATH, "w", encoding="utf-8") as f:
    f.write(src)
print("WROTE")
