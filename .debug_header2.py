path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'
with open(path, 'r') as f:
    content = f.read()
lines = content.split('\n')

print("=== LINE 2 (index 2) ===")
print(repr(lines[2]))
print("=== LINE 3 (index 3) ===")
print(repr(lines[3]))
print()

# Check if the old_header is in content
old_header = """Rev. 946 (fresh verification & metadata sync — 04 November 2026 WIB); §11 compact changelog 116–945→116–946; §12 updated. HEAD 5b0b96e0f0edfafc87f6717741bd940ca874a874a837 (Rev. 946 final commit); commit count 1048/6/0 (1048 local commits, 6 ahead / 0 behind origin_main); node_modules present (84072 files / 478 top-level dirs); dev.db ada (schema-only via init_db.py; 15 tabel, seluruh record 0); seluruh data 453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions belum tersedia, import ulang dari init_db.py + init_schema.sql + sumber Excel/PDF). Build gate: tsc ✓ (exit 0); eslint ✓ (exit 0, 1 warning / 0 error); next build ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). Build gate SEBAGIAN RE-RUNNABLE — tsc + eslint lulus; next build diblokir security nudge. Working tree: PRD ditulis ke Rev. 946; 451 tracked files; 0 untracked. Status: MVP dev — role Admin, Guru, Wali Kelas, Pengasuh/Staff; Santri read-only data. Next.js + Prisma + SQLite (dev)."""

print("old_header in content:", old_header in content)
print("lines[2] in content:", lines[2] in content)
print()

# Check character by character
import difflib
if old_header in content:
    print("OLD HEADER FOUND!")
else:
    # Try to find where the header starts
    idx = content.find("Rev. 946 (fresh")
    print("Found 'Rev. 946 (fresh' at index:", idx)
    if idx != -1:
        print("Context:", repr(content[idx:idx+200]))
