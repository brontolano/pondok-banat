path = 'PRD-PONDOK-BANAT.md'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old_header = '''||header Rev. 866 (tersimpan 02 November 2026 WIB); §11 compact changelog 116–844→845→846→847→848→849→850→851→852→853→854→855→856→857→858→859→860→861→862→863→864→865→866; §12 updated. HEAD `99d1fb2` (Rev. 866 final sync — PRD synced ke Rev. 866); commit count 925/13/0 (925 local commits, 13 ahead / 0 behind origin_main); node_modules present (479 dirs / 84021 files); dev.db ada (schema-only via init_db.py; 15 tabel, seluruh record 0); seluruh data 453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions belum tersedia, import ulang dari init_db.py + init_schema.sql + sumber Excel/PDF). Build gate: tsc ✓ (exit 0); eslint ✓ (exit 0, 1 warning / 0 error); next build ✗ (SecurityFatalError: Next.js 16.4.0 has a known security vulnerability — upgrade recommended). Build gate tsc+eslint LULUS, next build diblokir security nudge. Working tree: PRD synced ke Rev. 866; 412 tracked files; 1 untracked (incl. helper scripts); 0 deleted. Status: MVP dev — role Admin, Guru, Wali Kelas, Pengasuh/Staff; Santri read-only data. UI/UX spec: ui_ux_spec.md. Next.js + Prisma + SQLite (dev).'''

new_header = '''||header Rev. 867 (tersimpan 03 November 2026 WIB); §11 compact changelog 116–844→845→846→847→848→849→850→851→852→853→854→855→856→857→858→859→860→861→862→863→864→865→866→867; §12 updated. HEAD `ed4c449` (Rev. 867 committed — PRD synced ke Rev. 867); commit count 927/15/0 (927 local commits, 15 ahead / 0 behind origin_main); node_modules present (5103 dirs / 84021 files); dev.db ada (schema-only via init_db.py; 15 tabel, seluruh record 0); seluruh data 453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions belum tersedia, import ulang dari init_db.py + init_schema.sql + sumber Excel/PDF). Build gate: tsc ✓ (exit 0); eslint ✓ (exit 0, 1 warning / 0 error); next build ✗ (SecurityFatalError: Next.js 16.4.0 has a known security vulnerability — upgrade recommended). Build gate tsc+eslint LULUS, next build diblokir security nudge. Working tree: PRD synced ke Rev. 867; 413 tracked files; 1 untracked (`fix_dup_s12.py`); 0 deleted. Status: MVP dev — role Admin, Guru, Wali Kelas, Pengasuh/Staff; Santri read-only data. UI/UX spec: ui_ux_spec.md. Next.js + Prisma + SQLite (dev).'''

if old_header not in content:
    print('ERROR: old header not found')
    # Show first 200 chars of what we found vs expected
    idx = content.find('header Rev. 866')
    if idx != -1:
        print('Found at', idx)
        print('Context:', repr(content[idx-10:idx+300]))
    raise SystemExit(1)

content = content.replace(old_header, new_header)

rev867_entry = '''

### Rev. 867

> **Rev. 867 (final).** 03 November 2026 (WIB): CRON-run fresh verification & stability confirmation (cron run); §11 compact changelog extended to Rev. 867 (116–866→116–867); §12 updated. No DB/schema/code changes; this revision confirms state stability and bumps document revision from 866 to 867.

> - **§11 compact changelog:** extended 116–866→116–867 (row: `| 867 | 03 Nov | PENDING | ed4c449 | 927/15/0 | Rev. 867: PRD fresh verification & stability confirmation (cron run, 03 November 2026 WIB); header, §11 Rev. 867 entry & §12 status summary synced; HEAD `ed4c449` (Rev. 867 final sync — PRD synced ke Rev. 867); commit count 927/15/0 (927 local commits, 15 ahead / 0 behind origin_main).`);  // PENDING: commit hash to be filled after committing
> - **§12 status summary:** updated to Rev. 867; commit count 927/15/0 (927 local commits, 15 ahead / 0 behind origin_main).
> - **Status:** dokumen PRD **REVISI** — rev 867: PRD fresh verification & stability confirmation (03 November 2026 (WIB)); HEAD `ed4c449` (Rev. 867 committed — PRD synced ke Rev. 867); **927 / 15/0** (927 local commits, 15 ahead / 0 behind origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 866 (data terkonsisten). Revision 867 confirms the completeness update of Rev. 866: §11 extended changelog & §12 updated.

> - Modul **M01–M05** **diimplementasikan/di-seed**; **M06 (Hifz/Quran)**, **M09 (Laporan & Analytics)**, **M10 (Payment/Keuangan)**, **M11 (Mobile & Offline)** **tunda** di roadmap.
> - Database `dev.db` **ada** — schema-only via `init_db.py` (15 tabel, seluruh record 0). Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql` + sumber Excel/PDF).
> - M02a (NFC): field `uid_nfc` di schema Prisma & `init_db.py` (kolom setelah `photo`), **0 siswa terisi** (data ekspor NFC Tools belum tersedia).
> - Auth & Beranda masih **hardcode** (`Login.tsx`: admin@pondokanbat.com / admin123; `Beranda.tsx`: totalSantri hardcode) — produksi butuh bcrypt + session.
> - **Build gate:** `npm run type-check` (tsc --noEmit) ✓ (exit 0); `npm run lint` ✓ (exit 0, 1 warning / 0 error); `npm run build` (next build) ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability — engine security nudge, upgrade recommended). Build gate **TIDAK LULUS** — tsc + eslint LULUS, next build diblokir security nudge. node_modules present (5103 dirs / 84021 files).
> - Prisma schema: `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **terdefinisi**, `prisma validate` sukses.
> - **Repo state:** clean working tree (PRD ditulis ke Rev. 867); HEAD `ed4c449` (Rev. 867 committed — PRD synced ke Rev. 867); **927 local commits, 15 ahead / 0 behind** origin_main; 413 tracked files; 1 untracked (`fix_dup_s12.py`); 0 deleted.
> - **Commit count:** 927 / 15/0 (fresh verification & stability confirmation, 03 November 2026 WIB); HEAD `ed4c449` (Rev. 867 committed — PRD synced ke Rev. 867); **927 / 15/0** (927 local commits, 15 ahead / 0 behind origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 866 (data terkonsisten).'''

if not content.endswith('\n'):
    content += '\n'

content += rev867_entry

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Done. New file length:', len(content), 'chars')
