#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import io

PATH = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'

with io.open(PATH, 'r', encoding='utf-8') as f:
    src = f.read()

fixed = []
problems = []

# 1. Header: "Working tree: PRD ditulis ke Rev. 947" -> Rev. 948
old = "Working tree: PRD ditulis ke Rev. 947"
new = "Working tree: PRD ditulis ke Rev. 948"
if old in src:
    src = src.replace(old, new, 1)
    fixed.append("header_working_tree")
else:
    problems.append("header_working_tree NOT FOUND")

# 2. §12 table Git HEAD description: "HEAD 2a03ac1... (Rev. 947 final commit)" -> "7b10fe2... (Rev. 948 final commit)"
old = "HEAD 2a03ac1381414c848466b7c2ff92ffd935dee82c (Rev. 947 final commit)"
new = "HEAD 7b10fe2de6b222fad82ee5dddeebf7ee02541adc (Rev. 948 final commit)"
if old in src:
    src = src.replace(old, new, 1)
    fixed.append("section12_githead_desc")
else:
    problems.append("section12_githead_desc NOT FOUND")

# 3. Rev. 947 entry: "Rev. 948 (fresh verification" -> "Rev. 947 (fresh verification"
old = "> **Rev. 948 (fresh verification & metadata sync — 04 November 2026 WIB).** 04 November 2026 WIB: CRON-run fresh verification & metadata sync (cron run, 04 November 2026 WIB); §11 compact changelog extended to Rev. 947 (116–947→116–948); §12 updated. No DB/schema/code changes; this revision bumps document revision from 946 to 947."
new = "> **Rev. 947 (fresh verification & metadata sync — 04 November 2026 WIB).** 04 November 2026 WIB: CRON-run fresh verification & metadata sync (cron run, 04 November 2026 WIB); §11 compact changelog extended to Rev. 947 (116–946→116–947); §12 updated. No DB/schema/code changes; this revision bumps document revision from 946 to 947."
if old in src:
    src = src.replace(old, new, 1)
    fixed.append("rev947_first_line")
else:
    problems.append("rev947_first_line NOT FOUND")

# 4. Rev. 947 entry §11 compact changelog: "extended 116–947→116–948" -> "extended 116–946→116–947"
old = "> - **§11 compact changelog:** extended 116–947→116–948 (row: `| 947 | 04 Nov | 2a03ac1381414c848466b7c2ff92ffd935dee82c"
new = "> - **§11 compact changelog:** extended 116–946→116–947 (row: `| 947 | 04 Nov | 2a03ac1381414c848466b7c2ff92ffd935dee82c"
if old in src:
    src = src.replace(old, new, 1)
    fixed.append("rev947_changelog_range")
else:
    problems.append("rev947_changelog_range NOT FOUND")

# 5. Rev. 947 entry §11 compact changelog: commit count 1051/9/0 -> 1050/8/0
old = "HEAD `2a03ac1381414c848466b7c2ff92ffd935dee82c` (Rev. 947 final commit); commit count 1051/9/0 (1051 local commits, 9 ahead / 0 behind origin_main); node_modules present (84073 files / 478 top-level dirs); dev.db ada (schema-only via init_db.py; 15 tabel, seluruh record 0); seluruh data 453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions belum tersedia, import ulang dari init_db.py + init_schema.sql + sumber Excel/PDF). Build gate: tsc ✓ (exit 0); eslint ✓ (exit 0, 1 warning / 0 error); next build ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). Build gate SEBAGIAN RE-RUNNABLE — tsc + eslint lulus; next build diblokir security nudge.`); "
new = "HEAD `2a03ac1381414c848466b7c2ff92ffd935dee82c` (Rev. 947 final commit); commit count 1050/8/0 (1050 local commits, 0 ahead / 8 behind origin_main); node_modules present (84021 files / 477 top-level dirs); dev.db ada (schema-only via init_db.py; 15 tabel, seluruh record 0); seluruh data 453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions belum tersedia, import ulang dari init_db.py + init_schema.sql + sumber Excel/PDF). Build gate: tsc ✓ (exit 0); eslint ✓ (exit 0, 1 warning / 0 error); next build ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). Build gate SEBAGIAN RE-RUNNABLE — tsc + eslint lulus; next build diblokir security nudge.`); "
if old in src:
    src = src.replace(old, new, 1)
    fixed.append("rev947_commit_count_node_modules")
else:
    problems.append("rev947_commit_count_node_modules NOT FOUND")

# 6. Rev. 943 entry: "commit count 1042/0/0 ... node_modules present (84073 files / 478 top-level dirs)" -> "84021 files / 477 top-level dirs"
old = "commit count 1042/0/0 (1042 local commits, 0 ahead / 0 behind origin_main); node_modules present (84073 files / 478 top-level dirs)"
new = "commit count 1042/0/0 (1042 local commits, 0 ahead / 0 behind origin_main); node_modules present (84021 files / 477 top-level dirs)"
if old in src:
    src = src.replace(old, new, 1)
    fixed.append("rev943_node_modules")
else:
    problems.append("rev943_node_modules NOT FOUND")

with io.open(PATH, 'w', encoding='utf-8') as f:
    f.write(src)

print("=== FIXES APPLIED ===")
for x in fixed:
    print(x)
print("=== PROBLEMS ===")
for x in problems:
    print(x)
