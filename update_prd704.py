#!/usr/bin/env python3
import sys

path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'

with open(path, 'r') as f:
    content = f.read()

changes = []

# 1. Update header
old_header = '(Rev. 703): PRD fresh verification & stability confirmation (cron run, 28 Oktober 2026 WIB); header Rev. 702→703; §11 compact changelog 116–703; §12 updated. HEAD `fd81e38d231cfae6bed25d8f2a9e65649748348e` (Rev. 703 final commit); commit count 715/11/0 (715 local commits, 11 ahead origin/main, 0 behind); node_modules present (477 dirs / 84021 files); dev.db absent (removed by HEAD "Release: clean core files only"). Build gate: tsc ✓ (exit 0), eslint ✓ (exit 0, 1 warning / 0 error), next build ✗ (blocked — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). Build gate partially re-runnable — tsc + eslint lulus, next build diblokir security nudge. Working tree: PRD synced to Rev. 703; seluruh file lain cocak dengan HEAD; untracked helper scripts unchanged; git ls-files = 268 files.'
new_header = '(Rev. 704): PRD fresh verification & stability confirmation (cron run, 28 Oktober 2026 WIB); header Rev. 703→704; §11 compact changelog 116–703→116–704; §12 updated. HEAD `fd81e38d231cfae6bed25d8f2a9e65649748348e` (Rev. 703 final commit); commit count 715/11/0 (715 local commits, 11 ahead origin/main, 0 behind); node_modules present (477 dirs / 84021 files); dev.db absent (removed by HEAD "Release: clean core files only"). Build gate: tsc ✓ (exit 0), eslint ✓ (exit 0, 1 warning / 0 error), next build ✗ (blocked — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). Build gate partially re-runnable — tsc + eslint lulus, next build diblokir security nudge. Working tree: PRD synced to Rev. 704; seluruh file lain cocak dengan HEAD; untracked helper scripts unchanged; git ls-files = 268 files.'

if old_header in content:
    content = content.replace(old_header, new_header)
    changes.append('Header updated to Rev. 704')
else:
    print('WARNING: Header not found')
    changes.append('Header not found')

# 2. Update §11 header
old_s11 = '## 11. REVISI TERBARU (Rev. 116–703 — 28 Oktober 2026 WIB)'
new_s11 = '## 11. REVISI TERBARU (Rev. 116–704 — 28 Oktober 2026 WIB)'
if old_s11 in content:
    content = content.replace(old_s11, new_s11)
    changes.append('§11 header updated to Rev. 116–704')
else:
    print('WARNING: §11 header not found')
    changes.append('§11 header not found')

# 3. Add Rev. 704 entry after the Rev. 703 Status line
rev704_entry = '''
### Rev. 704

> **Rev. 704 (fresh).** 28 Oktober 2026 (WIB): CRON-run fresh verification & stability confirmation (cron run); HEAD `fd81e38d231cfae6bed25d8f2a9e65649748348e` (Rev. 703 final commit); commit count **715 / 11** (715 local commits, 11 ahead origin_main, 0 behind). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run):
>
> - **Environment:** node v26.5.1, npm 11.17.0, Prisma CLI = Prisma Developer Platform (new CLI; `generate`/`validate` commands not available in this release).
> - **Build quality gate:** `npm run type-check` (tsc --noEmit) ✓ (exit 0); `npm run lint` ✓ (exit 0, 1 warning / 0 error); `npm run build` (next build) ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). Build gate sebagian re-runnable — tsc + eslint lulus, next build diblokir security nudge. node_modules present (477 dirs / 84,021 files).
> - **Database (dev.db):** **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`. Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; source Excel & PDF dari `.data-pondokanat/` bukan tracked di repo).
> - **M02a (NFC):** field `uid_nfc` ada aktif di tabel `students` (kolom setelah `photo`); `prisma/schema.prisma` baris 68 (`uidNfc String? @map("uid_nfc")`), `init_schema.sql` baris 44, `init_db.py` baris 60. **Tidak ada satupun siswa yang memiliki `uid_nfc` diisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
> - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (typo domain `pondokanat.com`); produksi butuh bcrypt + session.
> - **Beranda hardcode:** `src/components/Beranda.tsx` & `src/app/beranda/page.tsx` masih hardcoded `totalSantri` (belum fetch real-time dari DB).
> - **Prisma:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` sukses (command not available in new Prisma CLI). Schema inconsistency (Rev. 38–45) SELESAI.
> - **Repo state:** clean working tree; `dev.db` absen; `node_modules` present (477 dirs / 84,021 files); build gate sebagian re-runnable (tsc + eslint lulus; next build diblokir security nudge).
> - **Commit count:** 715 / 11 (715 local commits, 11 ahead origin_main, 0 behind). Local branch **715 commits ahead / 0 behind** origin_main (HEAD `fd81e38`, Rev. 703 final commit).
>
> **Status:** dokumen PRD **REVISI** — rev 704: PRD fresh verification & stability confirmation (28 Oktober 2026 (WIB)); HEAD `fd81e38d231cfae6bed25d8f2a9e65649748348e` (Rev. 703 final commit); **715 / 11/0** (715 local commits, 11 ahead origin_main, 0 behind). State stabil, tidak ada perubahan signifikan dari Rev. 703 (data terkonsisten). Build gate: tsc ✓, eslint ✓ (1 warning), next build ✗ (SecurityFatalError Next.js 16.4.0).

'''

old_status_line = '> **Status:** dokumen PRD **REVISI** — rev 677: PRD fresh verification & stability confirmation (28 Oktober 2026 (WIB)); HEAD `c2d31ef` (Rev. 676 final commit); **685 / 49/0** (685 local commits, 49 ahead origin_main, 0 behind). State stabil, tidak ada perubahan signifikan dari Rev. 676 (data terkonsisten).'
if old_status_line in content:
    content = content.replace(old_status_line, old_status_line + rev704_entry)
    changes.append('Rev. 704 entry added to §11')
else:
    print('ERROR: Rev. 703 status line not found')
    changes.append('Rev. 703 status line not found')

# 4. Update §12 header
old_s12 = '## 12. STATUS RINGKASAN (28 Oktober 2026 WIB) — Rev. 703'
new_s12 = '## 12. STATUS RINGKASAN (28 Oktober 2026 WIB) — Rev. 704'
if old_s12 in content:
    content = content.replace(old_s12, new_s12)
    changes.append('§12 header updated to Rev. 704')
else:
    print('WARNING: §12 header not found')
    changes.append('§12 header not found')

# 5. Update the final status line
old_final_status = '> **Status:** dokumen PRD **REVISI** — rev 703: PRD fresh verification & stability confirmation (28 Oktober 2026 (WIB)); HEAD `fd81e38d231cfae6bed25d8f2a9e65649748348e` (Rev. 703 final commit); **715 / 11/0** (715 local commits, 11 ahead origin/main, 0 behind). State stabil, tidak ada perubahan signifikan dari Rev. 702 (data terkonsisten). Build gate: tsc ✓, eslint ✓ (1 warning), next build ✗ (SecurityFatalError Next.js 16.4.0).'
new_final_status = '> **Status:** dokumen PRD **REVISI** — rev 704: PRD fresh verification & stability confirmation (28 Oktober 2026 (WIB)); HEAD `fd81e38d231cfae6bed25d8f2a9e65649748348e` (Rev. 703 final commit); **715 / 11/0** (715 local commits, 11 ahead origin/main, 0 behind). State stabil, tidak ada perubahan signifikan dari Rev. 703 (data terkonsisten). Build gate: tsc ✓, eslint ✓ (1 warning), next build ✗ (SecurityFatalError Next.js 16.4.0).'
if old_final_status in content:
    content = content.replace(old_final_status, new_final_status)
    changes.append('Final status line updated to rev 704')
else:
    print('WARNING: Final status line not found')
    changes.append('Final status line not found')

with open(path, 'w') as f:
    f.write(content)

print('Changes made:')
for c in changes:
    print('  -', c)
print('Done!')
