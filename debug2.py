#!/usr/bin/env python3
# -*- coding: utf-8 -*-
with open("/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md", encoding="utf-8") as f:
    lines = f.read().splitlines()
with open("/opt/data/home/workspace/dev/pondok-banat/update_prd491_v2.py", encoding="utf-8") as f:
    script = f.read()

target = '||_- **Rev. 489 (final).** 24 Oktober 2026 (WIB): PRD fresh verification & stability confirmation (24 Oct 2026 WIB); HEAD `7adb7ce66c8d9a5ee707215b21339f451592e1` (Rev. 489 (final):'
for i, l in enumerate(lines):
    if '||_- **Rev. 489 (final).** 24 Oktober 2026 (WIB): PRD fresh verification & stability confirmation (24 Oct 2026 WIB); HEAD' in l:
        print("line idx:", i, "1-based:", i+1, "len:", len(l))
        print("target len:", len(target))
        print("line len:", len(l))
        print("match full:", target == l)
        print("target == line[:len(target)]:", target == l[:len(target)])
        # find first mismatch
        n = min(len(target), len(l))
        for k in range(n):
            if target[k] != l[k]:
                print("first mismatch at", k, "target char:", repr(target[k]), "line char:", repr(l[k]))
                print("target context:", repr(target[k-20:k+20]))
                print("line context:", repr(l[k-20:k+20]))
                break
        break
