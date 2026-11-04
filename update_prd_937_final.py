import re

path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'
with open(path, 'r') as f:
    content = f.read()

# --- §12 status summary (line 4023) ---
old_12 = '**§12 status summary:** updated to Rev. 937; commit count 1033/32/0.'
new_12 = '§12 status summary: updated to Rev. 937; commit count 1034/33/0.'
assert old_12 in content, "§12 pattern not found"
content = content.replace(old_12, new_12)

# --- §13 notes (line 4024) ---
old_13 = 'HEAD `7f87c48cab41f24afc36d30ae26ffcd2ab628da1` (Rev. 937 final commit); commit count 1033/32/0.'
new_13 = 'HEAD `47189d2135d039474f948c776942bb80ab1f704d` (Rev. 937 final commit); commit count 1034/33/0.'
assert old_13 in content, "§13 pattern not found"
content = content.replace(old_13, new_13)

# --- §11 Rev. 937 entry (line 4022) ---
old_11 = '| 937 | 04 Nov | 7f87c48 | 7f87c48cab41f24afc36d30ae26ffcd2ab628da1 | 1033/32/0 | Rev. 937:'
new_11 = '| 937 | 04 Nov | 47189d2 | 47189d2135d039474f948c776942bb80ab1f704d | 1034/33/0 | Rev. 937:'
assert old_11 in content, "§11 row pattern not found"
content = content.replace(old_11, new_11)

old_11b = 'HEAD `7f87c48` (Rev. 937 final commit); commit count 1033/32/0 (1033 local commits, 32 ahead / 0 behind origin_main); node_modules present (479 top-level dirs / 84021 files); dev.db ada (schema-only via init_db.py; 15 tabel, seluruh record 0); seluruh data 453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions belum tersedia'
new_11b = 'HEAD `47189d2` (Rev. 937 final commit); commit count 1034/33/0 (1034 local commits, 33 ahead / 0 behind origin_main); node_modules present (477 top-level dirs / 84021 files); dev.db ada (schema-only via init_db.py; 15 tabel, seluruh record 0); seluruh data 453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions belum tersedia'
assert old_11b in content, "§11 description pattern not found"
content = content.replace(old_11b, new_11b)

with open(path, 'w') as f:
    f.write(content)

print("Done. Changes written.")
print("Total file size:", len(content.encode('utf-8')), "bytes")
