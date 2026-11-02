with open('PRD-PONDOK-BANAT.md', 'r') as f:
    content = f.read()

# Replace the entire tail section from "### Rev. 868" to end with proper structure
old_tail = '''### Rev. 868

> **Rev. 868 (final).** 04 November 2026 (WIB): CRON-run fresh verification & stability confirmation (cron run); §11 compact changelog extended to Rev. 868 (116–867→116–868); §12 updated. No DB/schema/code changes; this revision confirms state stability and bumps document revision from 867 to 868.

> - **§11 compact changelog:** extended 116–867→116–868 (row: `| 868 | 04 Nov | 8db0e89 | 8db0e89 | 933/21/0 | Rev. 868: PRD fresh verification & stability confirmation (cron run, 04 November 2026 WIB); header, §11 Rev. 868 entry & §12 status summary synced; HEAD `8db0e89` (Rev. 868 final sync — PRD synced ke Rev. 868); commit count 933/21/0 (933 local commits, 21 ahead / 0 behind origin_main).`);
> - **§12 status summary:** updated to Rev. 868; commit count 933/21/0 (933 local commits, 21 ahead / 0 behind origin_main).
> - **Status:** dokumen PRD **REVISI** — rev 868: PRD fresh verification & stability confirmation (04 November 2026 (WIB)); HEAD `8db0e89` (Rev. 868 final sync — PRD synced ke Rev. 868); **933 / 21/0** (933 local commits, 21 ahead / 0 behind origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 867 (data terkonsisten). Revision 868 confirms the completeness update of Rev. 867: §11 extended changelog & §12 updated.

> - Modul **M01–M05** **diimplementasikan/di-seed**; **M06 (Hifz/Quran)**, **M09 (Laporan & Analytics)**, **M10 (Payment/Keuangan)**, **M11 (Mobile & Offline)** **tunda** di roadmap.
> - Database `dev.db` **ada** — schema-only via `init_db.py` (15 tabel, seluruh record 0). Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql` + sumber Excel/PDF).
> - M02a (NFC): field `uid_nfc` di schema Prisma & `init_db.py` (kolom setelah `photo`), **0 siswa terisi** (data ekspor NFC Tools belum tersedia).
> - Auth & Beranda masih **hardcode** (`Login.tsx`: admin@pondokanbat.com / admin123; `Beranda.tsx`: totalSantri hardcode) — produksi butuh bcrypt + session.
> - **Build gate:** `npm run type-check` (tsc --noEmit) ✓ (exit 0); `npm run lint` ✓ (exit 0, 1 warning / 0 error); `npm run build` (next build) ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability — engine security nudge, upgrade recommended). Build gate **TIDAK LULUS** — tsc + eslint LULUS, next build diblokir security nudge. node_modules present (5103 dirs / 84021 files).
> - Prisma schema: `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **terdefinisi**, `prisma validate` sukses.
> - **Repo state:** clean working tree (PRD ditulis ke Rev. 868); HEAD `d9fe9a1` (Rev. 868 committed — PRD synced ke Rev. 868); **932 local commits, 20 ahead / 0 behind** origin_main; 413 tracked files; 4 untracked (incl. helper scripts); 0 deleted.
> - **Commit count:** 932 / 20/0 (fresh verification & stability confirmation, 02 November 2026 WIB); HEAD `d9fe9a1` (Rev. 868 committed — PRD synced ke Rev. 868); **932 / 20/0** (932 local commits, 20 ahead / 0 behind origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 867 (data terkonsisten).'''

new_tail = '''### Rev. 868

> **Rev. 868 (final).** 04 November 2026 (WIB): CRON-run fresh verification & stability confirmation (cron run); §11 compact changelog extended to Rev. 868 (116–867→116–868); §12 updated. No DB/schema/code changes; this revision confirms state stability and bumps document revision from 867 to 868.

> - **§11 compact changelog:** extended 116–867→116–868 (row: `| 868 | 04 Nov | 8db0e89 | 8db0e89 | 933/21/0 | Rev. 868: PRD fresh verification & stability confirmation (cron run, 04 November 2026 WIB); header, §11 Rev. 868 entry & §12 status summary synced; HEAD `8db0e89` (Rev. 868 final sync — PRD synced ke Rev. 868); commit count 933/21/0 (933 local commits, 21 ahead / 0 behind origin_main).`);
> - **§12 status summary:** updated to Rev. 868; commit count 933/21/0 (933 local commits, 21 ahead / 0 behind origin_main).
> - **Status:** dokumen PRD **REVISI** — rev 868: PRD fresh verification & stability confirmation (04 November 2026 (WIB)); HEAD `8db0e89` (Rev. 868 final sync — PRD synced ke Rev. 868); **933 / 21/0** (933 local commits, 21 ahead / 0 behind origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 867 (data terkonsisten). Revision 868 confirms the completeness update of Rev. 867: §11 extended changelog & §12 updated.

## 12. STATUS RINGKASAN (04 November 2026 WIB) — Rev. 868

> - Modul **M01–M05** **diimplementasikan/di-seed**; **M06 (Hifz/Quran)**, **M09 (Laporan & Analytics)**, **M10 (Payment/Keuangan)**, **M11 (Mobile & Offline)** **tunda** di roadmap.
> - Database `dev.db` **ada** — schema-only via `init_db.py` (15 tabel, seluruh record 0). Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql` + sumber Excel/PDF).
> - M02a (NFC): field `uid_nfc` di schema Prisma & `init_db.py` (kolom setelah `photo`), **0 siswa terisi** (data ekspor NFC Tools belum tersedia).
> - Auth & Beranda masih **hardcode** (`Login.tsx`: admin@pondokanbat.com / admin123; `Beranda.tsx`: totalSantri hardcode) — produksi butuh bcrypt + session.
> - **Build gate:** `npm run type-check` (tsc --noEmit) ✓ (exit 0); `npm run lint` ✓ (exit 0, 1 warning / 0 error); `npm run build` (next build) ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability — engine security nudge, upgrade recommended). Build gate **TIDAK LULUS** — tsc + eslint LULUS, next build diblokir security nudge. node_modules present (5103 dirs / 84021 files).
> - Prisma schema: `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **terdefinisi**, `prisma validate` sukses.
> - **Repo state:** clean working tree (PRD ditulis ke Rev. 868); HEAD `8db0e89` (Rev. 868 final sync — PRD synced ke Rev. 868); **933 local commits, 21 ahead / 0 behind** origin_main; 413 tracked files; 4 untracked (incl. helper scripts); 0 deleted.
> - **Commit count:** 933 / 21/0 (fresh verification & stability confirmation, 04 November 2026 WIB); HEAD `8db0e89` (Rev. 868 final sync — PRD synced ke Rev. 868); **933 / 21/0** (933 local commits, 21 ahead / 0 behind origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 867 (data terkonsisten).'''

if old_tail in content:
    content = content.replace(old_tail, new_tail)
    print("Fixed final tail")
else:
    print("Tail pattern not found")
    # Debug: show what's at the end
    print("Last 500 chars of content:")
    print(content[-500:])

with open('PRD-PONDOK-BANAT.md', 'w') as f:
    f.write(content)

print("Done")
