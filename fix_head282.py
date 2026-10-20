#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fix remaining 793c7bd (Old HEAD Rev.280) references in PRD -> b32ad67 (HEAD Rev.281)."""
PATH = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"
OLD = "793c7bdf0ea0ba6327f6899a6e0d00c31beb2f09"
NEW = "b32ad6767eef819aa6fb704ed856bb331d72108d"

with open(PATH, "r", encoding="utf-8") as f:
    c = f.read()

cnt = c.count(OLD)
c = c.replace(OLD, NEW)

with open(PATH, "w", encoding="utf-8") as f:
    f.write(c)

print("replaced", cnt, "occurrences of the old HEAD hash")
print("old HEAD remaining:", c.count(OLD))
print("new HEAD count:", c.count(NEW))
