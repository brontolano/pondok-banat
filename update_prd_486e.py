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

# Rev. 486 row: branch 14 -> 15 (already applied by e script? re-apply to be safe)
repl("rev 486 = PRD fresh verification & stability confirmation; seluruh data terkonsisten, tidak ada perubahan signifikan dari Rev. 485; branch 14 ahead / 0 behind origin_main.",
     "rev 486 = PRD fresh verification & stability confirmation; seluruh data terkonsisten, tidak ada perubahan signifikan dari Rev. 485; branch 15 ahead / 0 behind origin_main.",
     "row-branch")

# Header untracked 19 -> 25 (unique: followed by '. Database')
repl("revisi terbaru = Rev. 486, fresh verification dilakukan hari ini); seluruh file lain cocak dengan HEAD; untracked: 19 skrip utility (tidak terpantau dalam git). `git ls-files` = 187 file. Database",
     "revisi terbaru = Rev. 486, fresh verification dilakukan hari ini); seluruh file lain cocak dengan HEAD; untracked: 25 skrip utility (tidak terpantau dalam git). `git ls-files` = 187 file. Database",
     "header-untracked")

# §12 Working tree bullet untracked 19 -> 25
repl("HEAD `d918408f8872e29ac70459f171259a48248a94b5` (Rev. 486); seluruh file lain cocak dengan HEAD; untracked: 19 skrip utility",
     "HEAD `d918408f8872e29ac70459f171259a48248a94b5` (Rev. 486); seluruh file lain cocak dengan HEAD; untracked: 25 skrip utility",
     "wt-untracked")

with io.open(PATH, "w", encoding="utf-8") as f:
    f.write(src)
print("WROTE")
