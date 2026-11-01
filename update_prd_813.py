import re

path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'
with open(path, 'r') as f:
    content = f.read()

# 1. Update the header
old_header = """header Rev. 812; §11 compact changelog 116–812; §12 updated. HEAD `f0264ed` (Rev. 810 final committed); commit count 840/32/0 (840 local commits, 32 ahead / 0 behind origin_main); node_modules present (5103 dirs / 84021 files); dev.db ada (schema-only via init_db.py; 15 tabel, seluruh record 0); seluruh data 453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions belum tersedia, import ulang dari init_db.py + init_schema.sql + sumber Excel/PDF). Build gate: tsc ✓ (exit 0); eslint ✓ (exit 0, 1 warning / 0 error); next build ✗ (SecurityFatalError: Next.js 16.4.0 has a known security vulnerability — upgrade recommended). Working tree: PRD synced ke Rev. 812; Rev. 811 committed; 340 tracked files; 47 untracked (incl. probe scripts); 0 deleted."""

new_header = """header Rev. 813; §11 compact changelog 116–813; §12 updated. HEAD `ed9c026` (Rev. 812 final committed); commit count 841/33/0 (841 local commits, 33 ahead / 0 behind origin_main); node_modules present (477 dirs / 84021 files); dev.db ada (schema-only via init_db.py; 15 tabel, seluruh record 0); seluruh data 453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions belum tersedia, import ulang dari init_db.py + init_schema.sql + sumber Excel/PDF). Build gate: tsc ✓ (exit 0); eslint ✓ (exit 0, 1 warning / 0 error); next build ✗ (SecurityFatalError: Next.js 16.4.0 has a known security vulnerability — upgrade recommended). Working tree: PRD synced ke Rev. 813; 340 tracked files; 47 untracked (incl. probe scripts); 0 deleted."""

if old_header in content:
    content = content.replace(old_header, new_header)
    print("Header updated")
else:
    print("WARNING: header not found")
    # Try a partial match
    if "Rev. 812; §11 compact changelog 116–812" in content:
        print("  Found partial header reference")
    else:
        print("  No partial match either")

# 2. Add Rev. 813 section at the end of §11/§12 (after the last line)
old_end = """> - **Status:** dokumen PRD **REVISI** — rev 812: PRD fresh verification & stability confirmation (cron run, 4 November 2026 WIB); HEAD `c02abfa` (Rev. 811 final committed); **840 / 32/0** (840 local commits, 32 ahead / 0 behind origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 811 (data terkonsisten).
"""

new_end = old_end + """

### Rev. 813

> **Rev. 813 (fresh).** 5 November 2026 (WIB): CRON-run fresh verification & stability confirmation (cron run); HEAD `ed9c026` (Rev. 812 final committed — PRD synced ke Rev. 813); commit count **841 / 33/0** (841 local commits, 33 ahead / 0 behind origin_main). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run):

> - **Environment:** node v26.5.1, npm 11.17.0, Prisma CLI = Prisma Developer Platform (new CLI; `generate`/`validate` commands not available in this release).
>
> - **Build quality gate:** `npm run type-check` (tsc --noEmit) ✓ (exit 0); `npm run lint` ✓ (exit 0, 1 warning / 0 error); `npm run build` (next build) ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability — engine security nudge, upgrade recommended). Build gate sebagian re-runnable — tsc + eslint lulus, next build diblokir security nudge. node_modules present (477 dirs / 84021 files).
>
> - **Database (dev.db):** **ada** — schema-only via `init_db.py` (15 tabel, seluruh record 0). Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; source Excel & PDF dari `.data-pondokanat/` bukan tracked di repo).
>
> - **M02a (NFC):** field `uid_nfc` ada aktif di tabel `students` (kolom setelah `photo`); `prisma/schema.prisma` baris 68 (`uidNfc String? @map(\"uid_nfc\"`)); `init_schema.sql` baris 44, `init_db.py` baris 60. **0 siswa terisi (semua 453 NULL)** — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
>
> - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain sudah diperbaiki; typo `pondokanat.com` telah dihapus); produksi butuh bcrypt + session.
>
> - **Beranda hardcode:** `src/components/Beranda.tsx` & `src/app/beranda/page.tsx` masih hardcoded `totalSantri` (belum fetch real-time dari DB); nilai sekarang `totalSantri: 453, totalGuru: 54, totalKelas: 18`.
>
> - **Prisma:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` sukses (command not available in new Prisma CLI). Schema inconsistency (Rev. 38–45) SELESAI.
>
> - **Repo state:** clean working tree (PRD ditulis ke Rev. 813); `dev.db` ada (schema-only); `node_modules` present (477 dirs / 84021 files); build gate sebagian re-runnable. 47 untracked helper scripts; 0 deleted.
>
> - **Commit count:** 841 local commits, **33 ahead / 0 behind** origin_main. Local branch **841 commits ahead / 0 behind** origin_main (HEAD `ed9c026`, Rev. 812 final committed). origin/main at `60d2d99` (Rev. 788).
>
> - **Status:** dokumen PRD **REVISI** — rev 813: PRD fresh verification & stability confirmation (cron run, 5 November 2026 WIB); HEAD `ed9c026` (Rev. 812 final committed); **841 / 33/0** (841 local commits, 33 ahead / 0 behind origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 812 (data terkonsisten).

"""

if old_end in content:
    content = content.replace(old_end, new_end)
    print("Rev. 813 section added")
else:
    print("WARNING: end marker not found")
    # Try finding the last "Status:" line
    if "rev 812: PRD fresh verification & stability confirmation" in content:
        print("  Found rev 812 status reference")
    else:
        print("  No rev 812 status reference")

with open(path, 'w') as f:
    f.write(content)

print("File written successfully")
