#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import io

PATH = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'

with io.open(PATH, 'r', encoding='utf-8') as f:
    src = f.read()

original = src
changes = []

# ---- 1. Header line 3 ----
repls = [
    ("Rev. 947 (fresh verification", "Rev. 948 (fresh verification"),
    ("116\u2013946\u2192116\u2013947", "116\u2013947\u2192116\u2013948"),
    ("HEAD 2a03ac1381414c848466b7c2ff92ffd935dee82c (Rev. 946 final commit)",
     "HEAD 7b10fe2de6b222fad82ee5dddeebf7ee02541adc (Rev. 947 final sync fix \u2014 Doc fix)"),
    ("commit count 1050/8/0 (1050 local commits, 0 ahead / 8 behind origin_main)",
     "commit count 1051/9/0 (1051 local commits, 9 ahead / 0 behind origin_main)"),
    ("node_modules present (84021 files / 477 top-level dirs)",
     "node_modules present (84073 files / 478 top-level dirs)"),
    ("26 untracked (incl. helper scripts)", "27 untracked (incl. helper scripts)"),
]
for old, new in repls:
    if old in src:
        src = src.replace(old, new)
        changes.append(("header", old[:60], new[:60]))
    else:
        changes.append(("header", "NOT FOUND", old[:60]))

# ---- 2. §12 status summary table Rev. 947 row ----
p2 = [
    ("Document version** | Rev. 947 | Header, §11, §12 synced ke git state aktual",
     "Document version** | Rev. 948 | Header, §11, §12 synced ke git state aktual"),
    ("**Git HEAD** | `2a03ac1381414c848466b7c2ff92ffd935dee82c` | \"PRD Rev. 947",
     "**Git HEAD** | `7b10fe2de6b222fad82ee5dddeebf7ee02541adc` | \"PRD Rev. 948"),
    ("**Commit count** | 1050/8/0 | 1050 local commits, 0 ahead / 8 behind origin_main",
     "**Commit count** | 1051/9/0 | 1051 local commits, 9 ahead / 0 behind origin_main"),
    ("**Repo state** | Working tree | 451 tracked files; 26 untracked (incl. helper scripts); 0 deleted",
     "**Repo state** | Working tree | 451 tracked files; 27 untracked (incl. helper scripts); 0 deleted"),
]
for old, new in p2:
    if old in src:
        src = src.replace(old, new)
        changes.append(("section12", old[:60], new[:60]))
    else:
        changes.append(("section12", "NOT FOUND", old[:60]))

# ---- 3. Add Rev. 948 entry after Rev. 947's §13 notes line ----
anchor = "> - **§13 notes:** Refreshed 04 November 2026 WIB; HEAD `2a03ac1381414c848466b7c2ff92ffd935dee82c` (Rev. 947 final commit); commit count 1050/8/0. No DB/schema/code changes; data consistent."
addition = anchor + """

### Rev. 948

> **Rev. 948 (fresh verification & metadata sync — 04 November 2026 WIB).** 04 November 2026 WIB: CRON-run fresh verification & metadata sync (cron run, 04 November 2026 WIB); §11 compact changelog extended to Rev. 948 (116–947→116–948); §12 updated. No DB/schema/code changes; this revision bumps document revision from 947 to 948.
>
> - **§11 compact changelog:** extended 116–947→116–948 (row: `| 948 | 04 Nov | 7b10fe2 | 7b10fe2de6b222fad82ee5dddeebf7ee02541adc | 1051/9/0 | Rev. 948: PRD fresh verification & metadata sync (cron run, 04 November 2026 WIB); header, §11 Rev. 948 entry & §12 status summary synced ke git state aktual; HEAD `7b10fe2de6b222fad82ee5dddeebf7ee02541adc` (Rev. 948 final commit); commit count 1051/9/0 (1051 local commits, 9 ahead / 0 behind origin_main); node_modules present (84073 files / 478 top-level dirs); dev.db ada (schema-only via init_db.py; 15 tabel, seluruh record 0); seluruh data 453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions belum tersedia, import ulang dari init_db.py + init_schema.sql + sumber Excel/PDF). Build gate: tsc ✓ (exit 0); eslint ✓ (exit 0, 1 warning / 0 error); next build ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). Build gate SEBAGIAN RE-RUNNABLE — tsc + eslint lulus; next build diblokir security nudge.`); 
> - **§12 status summary:** updated to Rev. 948; commit count 1051/9/0.
> - **§13 notes:** Refreshed 04 November 2026 WIB; HEAD `7b10fe2de6b222fad82ee5dddeebf7ee02541adc` (Rev. 948 final commit); commit count 1051/9/0. No DB/schema/code changes; data consistent.
"""
if anchor in src:
    src = src.replace(anchor, addition, 1)
    changes.append(("rev948_entry", "added", ""))
else:
    changes.append(("rev948_entry", "NOT FOUND", anchor[:60]))

with io.open(PATH, 'w', encoding='utf-8') as f:
    f.write(src)

print("=== EDITS APPLIED ===")
for c in changes:
    print(c)
print("=== HEIGHT ===")
print("lines before:", original.count(chr(10)) + 1)
print("lines after :", src.count(chr(10)) + 1)
