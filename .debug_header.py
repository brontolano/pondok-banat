path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'
with open(path, 'r') as f:
    lines = f.read().split('\n')

header = lines[3]
print("=== HEADER FROM FILE (repr) ===")
print(repr(header))
print()

# Expected header from my script
old_header = """Rev. 946 (fresh verification & metadata sync — 04 November 2026 WIB); §11 compact changelog 116–945→116–946; §12 updated. HEAD 5b0b96e0f0edfafc87f6717741bd940ca874a874a837 (Rev. 946 final commit); commit count 1048/6/0 (1048 local commits, 6 ahead / 0 behind origin_main); node_modules present (84072 files / 478 top-level dirs); dev.db ada (schema-only via init_db.py; 15 tabel, seluruh record 0); seluruh data 453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions belum tersedia, import ulang dari init_db.py + init_schema.sql + sumber Excel/PDF). Build gate: tsc ✓ (exit 0); eslint ✓ (exit 0, 1 warning / 0 error); next build ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). Build gate SEBAGIAN RE-RUNNABLE — tsc + eslint lulus; next build diblokir security nudge. Working tree: PRD ditulis ke Rev. 946; 451 tracked files; 0 untracked. Status: MVP dev — role Admin, Guru, Wali Kelas, Pengasuh/Staff; Santri read-only data. Next.js + Prisma + SQLite (dev)."""

print("=== MATCH ===", header == old_header)
if header != old_header:
    # Find first differing position
    for i, (a, b) in enumerate(zip(header, old_header)):
        if a != b:
            print(f"First diff at index {i}: file='{repr(a)}' vs script='{repr(b)}'")
            break
    else:
        print(f"Lengths differ: file={len(header)} vs script={len(old_header)}")
        if len(header) > len(old_header):
            print("File extra:", repr(header[len(old_header):][:100]))
        else:
            print("Script extra:", repr(old_header[len(header):][:100]))
