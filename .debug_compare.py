path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'
with open(path, 'r') as f:
    content = f.read()
lines = content.split('\n')
header = lines[2]

# My expected old_header
old_header = """Rev. 946 (fresh verification & metadata sync — 04 November 2026 WIB); §11 compact changelog 116–945→116–946; §12 updated. HEAD 5b0b96e0f0edfafc87f6717741bd940ca874a874a837 (Rev. 946 final commit); commit count 1048/6/0 (1048 local commits, 6 ahead / 0 behind origin_main); node_modules present (84072 files / 478 top-level dirs); dev.db ada (schema-only via init_db.py; 15 tabel, seluruh record 0); seluruh data 453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions belum tersedia, import ulang dari init_db.py + init_schema.sql + sumber Excel/PDF). Build gate: tsc ✓ (exit 0); eslint ✓ (exit 0, 1 warning / 0 error); next build ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). Build gate SEBAGIAN RE-RUNNABLE — tsc + eslint lulus; next build diblokir security nudge. Working tree: PRD ditulis ke Rev. 946; 451 tracked files; 0 untracked. Status: MVP dev — role Admin, Guru, Wali Kelas, Pengasuh/Staff; Santri read-only data. Next.js + Prisma + SQLite (dev)."""

print("header length:", len(header))
print("old_header length:", len(old_header))
print()

# Compare character by character
for i, (a, b) in enumerate(zip(header, old_header)):
    if a != b:
        print(f"First diff at index {i}:")
        print(f"  file:   {repr(header[max(0,i-20):i+20])}")
        print(f"  script: {repr(old_header[max(0,i-20):i+20])}")
        # Show unicode code points
        print(f"  file codepoints: {[hex(ord(c)) for c in header[max(0,i-10):i+10]]}")
        print(f"  script codepoints: {[hex(ord(c)) for c in old_header[max(0,i-10):i+10]]}")
        break
else:
    print("Strings are identical up to min length")
    print("Lengths:", len(header), len(old_header))
    if len(header) != len(old_header):
        print("Extra in header:", repr(header[len(old_header):][:50]))
        print("Extra in old_header:", repr(old_header[len(header):][:50]))
