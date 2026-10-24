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

H1 = "d918408f8872e29ac70459f171259a48248a94b5"

# Header long line
repl("`ff465bba47116093782778b49af31211368cf13d` (Rev. 486: PRD fresh verification & stability confirmation (24 Oct 2026 WIB); header Rev. 486, §11 kompakt changelog 116–485, §12 updated). Branch `main`",
     "`d918408f8872e29ac70459f171259a48248a94b5` (Rev. 486: PRD fresh verification & stability confirmation (24 Oct 2026 WIB); header Rev. 486, §11 kompakt changelog 116–485, §12 updated). Branch `main`",
     "hdr-1")

# Header HEAD ref
repl("`git rev-parse HEAD` = `ff465bba47116093782778b49af31211368cf13d` (Rev. 486); **origin/main:**",
     "`git rev-parse HEAD` = `d918408f8872e29ac70459f171259a48248a94b5` (Rev. 486); **origin/main:**",
     "hdr-2")

# Header ahead
repl("Local branch **14 commits ahead / 0 behind** origin_main. Working tree:",
     "Local branch **15 commits ahead / 0 behind** origin_main. Working tree:",
     "hdr-3")

# §12 Git HEAD bullet
repl("`ff465bba47116093782778b49af31211368cf13d` (Rev. 486: PRD fresh verification & stability confirmation (24 Oct 2026 WIB); header Rev. 486, §11 kompakt changelog 116–485, §12 updated). Local branch **14 commits ahead / 0 behind** origin_main. **origin/main:**",
     "`d918408f8872e29ac70459f171259a48248a94b5` (Rev. 486: PRD fresh verification & stability confirmation (24 Oct 2026 WIB); header Rev. 486, §11 kompakt changelog 116–485, §12 updated). Local branch **15 commits ahead / 0 behind** origin_main. **origin/main:**",
     "s12-gh")

# §12 Working tree bullet
repl("HEAD `ff465bba47116093782778b49af31211368cf13d` (Rev. 486); seluruh file lain cocak dengan HEAD; untracked: 19 skrip utility",
     "HEAD `d918408f8872e29ac70459f171259a48248a94b5` (Rev. 486); seluruh file lain cocak dengan HEAD; untracked: 19 skrip utility",
     "s12-wt")

# §12 Rev. 486 row (has ff465bb hash + 14/0)
repl("`ff465bba47116093782778b49af31211368cf13d` (Rev. 486: PRD fresh verification & stability confirmation (24 Oct 2026 WIB); header Rev. 486, §11 kompakt changelog 116–485, §12 updated), 14 / 0 (14 commits ahead origin_main)",
     "`d918408f8872e29ac70459f171259a48248a94b5` (Rev. 486: PRD fresh verification & stability confirmation (24 Oct 2026 WIB); header Rev. 486, §11 kompakt changelog 116–485, §12 updated), 15 / 0 (15 commits ahead origin_main)",
     "s12-row")

with io.open(PATH, "w", encoding="utf-8") as f:
    f.write(src)
print("WROTE")
