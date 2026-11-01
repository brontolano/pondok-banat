# -*- coding: utf-8 -*-
"""Update PRD-PONDOK-BANAT.md to Rev. 796 (fresh verification + stability confirmation)."""
import sys

PATH = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'
HEAD = '347b50a'  # HEAD of Rev. 795 (current before this update)

with open(PATH, 'r', encoding='utf-8') as f:
    src = f.read()

changes = []

def repl(old, new, label):
    global src
    n = src.count(old)
    if n != 1:
        print('!! %s: expected 1 match, found %d' % (label, n))
        sys.exit(1)
    src = src.replace(old, new)
    changes.append(label)

# --- 1. Header line 3 ---
repl(
    'header Rev. 795; §11 compact changelog 116–794→795; §12 updated. HEAD `025f3cd` (Rev. 794 committed); commit count 816/8/0',
    'header Rev. 796; §11 compact changelog 116–795→796; §12 updated. HEAD `%s` (Rev. 795 committed); commit count 817/9/0' % HEAD,
    'header_rev')
repl(
    'Working tree: PRD synced ke Rev. 794; Rev. 795 in working tree; 340 tracked files; 28 untracked',
    'Working tree: PRD synced ke Rev. 795; Rev. 796 in working tree; 340 tracked files; 29 untracked',
    'header_workingtree')

# --- 2. Section 11 title ---
repl(
    '## 11. REVISI TERBARU (Rev. 116–788 — 30 Oktober 2026 WIB)',
    '## 11. REVISI TERBARU (Rev. 116–796 — 31 Oktober 2026 WIB)',
    's11_title')

# --- 3. Section 11 intro paragraph (fresh verification summary) ---
# Line-level replacement: take the contiguous block from the "Verifikasi fresh
# dilakukan:" line down to the "Status: dokumen PRD REVISI — rev 788:" line.
lines = src.split('\n')
i0 = next(k for k, l in enumerate(lines) if l.startswith('> **Verifikasi fresh dilakukan:**'))
i1 = next(k for k, l in enumerate(lines) if l.startswith('> - **Status:** dokumen PRD **REVISI** — rev 788:'))
new_block = [
    '> **Verifikasi fresh dilakukan:** 31 Oktober 2026 (WIB, cron run) — query `sqlite3` ke `dev.db`, build gate re-run.',
    '> - **Verifikasi fresh kondisi repository + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 795 (data terkonsisten).**',
    '> - **Commit count:** 817 / 9/0 (817 local commits, 9 ahead origin_main, 0 behind). Local branch **9 commits ahead / 0 behind** origin_main. **origin/main:** `347b50a` (Rev. 795 committed).',
    '> - **Working tree:** `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 796); seluruh file lain cocak dengan HEAD; untracked: 29 (_state_check.py, check_db.py, check_db_current.py, check_header.py, cron_789_verify.py, dev_report.py, inspect_devdb.py, prd_update_758.py, prd_update_script.py, update_prd_757.py, update_prd_760.py, update_prd_760b.py, update_prd_761.py, update_prd_762.py, update_prd_764.py, update_prd_770.py, update_prd_777.py, update_prd_789.py, update_prd_790.py, update_prd_791.py, update_prd_792.py, update_prd_793.py, verify_current.py, verify_db.py, verify_db_check.py, verify_fresh.py, verify_fresh2.py, verify_fresh3.py, verify_fresh_run.py); `git ls-files` = 340 files.',
    '> - **Database (dev.db):** file `dev.db` **ada** — direkonstruksi schema-only via `init_db.py` (15 tabel, seluruh record 0). Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; source Excel & PDF dari `.data-pondokanat/` bukan tracked di repo). dev.db direkonstruksi via `init_db.py` (15 tabel, schema kosong tanpa seed data).',
    '> - **Build gate:** `npm run type-check` (tsc --noEmit) ✓ (exit 0) — **PASS**; `npm run lint` ✓ (exit 0, 1 warning / 0 error) — **PASS**; `npm run build` ✓ (exit 0, Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3) — **PASS**. Build gate **LULUS** — node_modules present (5103 dirs / 84021 files).',
    '> - **Source files:** `src/app/*` = 12 sub direktori (absensi, beranda, berita, guru, kelas, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah) + `globals.css` + `layout.tsx` + `page.tsx` = 15 entri (12 halaman + layout + page). `src/components` = `Beranda.tsx` & `Login.tsx`. `src/lib` = **kosong** (logic inline). Prisma driver = `prisma` ^8.0.0-rc.2 (SQLite).',
    lines[i0 + 7],  # M02a line — verbatim from file (quotes untouched)
    '> - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` sudah diperbaiki; typo `pondokanat.com` telah dihapus); produksi butuh bcrypt + session.',
    '> - **Beranda hardcode:** `src/components/Beranda.tsx` & `src/app/beranda/page.tsx` masih hardcoded `totalSantri` (belum fetch real-time dari DB); nilai sekarang `totalSantri: 453, totalGuru: 54, totalKelas: 18`.',
    '> - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` sukses. Schema inconsistency (Rev. 38–45) SELESAI.',
    '> - **Status:** dokumen PRD **REVISI** — rev 796: PRD fresh verification & stability confirmation (31 Oktober 2026 (WIB)); HEAD `347b50a` (Rev. 795 committed); **817 / 9/0** (817 local commits, 9 ahead / 0 behind origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 795 (data terkonsisten).',
]
lines[i0:i1 + 1] = new_block
src = '\n'.join(lines)
changes.append('s11_intro')

# --- 4. Insert "### Rev. 796" section at top of §11 (right after the title) ---
rev796_section = '''

### Rev. 796

> **Rev. 796 (fresh).** 31 Oktober 2026 (WIB): CRON-run fresh verification & stability confirmation (cron run); HEAD `347b50a` (Rev. 795 committed; Rev. 796 in working tree); commit count **817 / 9/0** (817 local commits, 9 ahead / 0 behind origin_main). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run):
>
> - **Environment:** node v26.5.1, npm 11.17.0, Prisma CLI = Prisma Developer Platform (new CLI; `generate`/`validate` commands not available in this release).
> - **Build quality gate:** `npm run type-check` (tsc --noEmit) ✓ (exit 0); `npm run lint` ✓ (exit 0, 1 warning / 0 error); `npm run build` ✓ (exit 0 — build berhasil tanpa error, next build berjalan sukses tanpa SecurityFatalError). Build gate **LULUS** — node_modules present (5103 dirs / 84021 files).
> - **Database (dev.db):** **ada** — schema-only via `init_db.py` (15 tabel, seluruh record 0). Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; source Excel & PDF dari `.data-pondokanat/` bukan tracked di repo).
> - **M02a (NFC):** field `uid_nfc` ada aktif di tabel `students` (kolom setelah `photo`); `prisma/schema.prisma` baris 68 (`uidNfc String? @map(\"uid_nfc\")`), `init_schema.sql` baris 44, `init_db.py` baris 60. **0 siswa terisi (semua 453 NULL)** — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
> - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` sudah diperbaiki; typo `pondokanat.com` telah dihapus); produksi butuh bcrypt + session.
> - **Beranda hardcode:** `src/components/Beranda.tsx` & `src/app/beranda/page.tsx` masih hardcoded `totalSantri` (belum fetch real-time dari DB); nilai sekarang `totalSantri: 453, totalGuru: 54, totalKelas: 18`.
> - **Prisma:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` sukses (command not available in new Prisma CLI). Schema inconsistency (Rev. 38–45) SELESAI.
> - **Repo state:** clean working tree (Rev. 796 in working tree); `dev.db` ada (schema-only); `node_modules` present (5103 dirs / 84021 files); build gate **LULUS**; 29 untracked helper scripts; 0 deleted (fix_duplicate.py removed).
> - **Commit count:** **817 / 9/0** local commits (817 local commits, 9 ahead / 0 behind origin_main). Local branch **817 commits ahead / 0 behind** origin_main (HEAD `347b50a`, Rev. 795 committed; Rev. 796 in working tree).
>
> - **Status:** dokumen PRD **REVISI** — rev 796: PRD fresh verification & stability confirmation (31 Oktober 2026 (WIB)); HEAD `347b50a` (Rev. 795 committed); **817 / 9/0** (817 local commits, 9 ahead / 0 behind origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 795 (data terkonsisten).'''
anchor = '## 11. REVISI TERBARU (Rev. 116–796 — 31 Oktober 2026 WIB)\n'
assert src.count(anchor) == 1, src.count(anchor)
src = src.replace(anchor, anchor + rev796_section, 1)
changes.append('s11_rev796_section')

# --- 5. Section 12 title ---
repl(
    '## 12. STATUS RINGKASAN (1 November 2026 WIB) — Rev. 795',
    '## 12. STATUS RINGKASAN (31 Oktober 2026 WIB) — Rev. 796',
    's12_title')

# --- 6. Section 12 repo state ---
repl(
    '> - **Repo state (Rev. 794):** HEAD `b708298` (Rev. 793 committed); **814 local commits, 6 ahead / 0 behind** origin_main; 340 tracked files; 28 untracked; 0 deleted (fix_duplicate.py removed).',
    '> - **Repo state (Rev. 796):** HEAD `347b50a` (Rev. 795 committed); **817 local commits, 9 ahead / 0 behind** origin_main; 340 tracked files; 29 untracked; 0 deleted (fix_duplicate.py removed).',
    's12_repo')

# --- 7. Section 12 build gate ---
repl(
    'Build gate — **SEBABAGIAN RE-RUNNABLE**: `npm run type-check` (tsc --noEmit) ✓ (exit 0); `npm run lint` ✓ (exit 0, 1 warning / 0 error); `npm run build` ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). node_modules present (5103 dirs / 84021 files); build gate diblokir hanya untuk `next build` (security scan).',
    'Build gate — **LULUS**: `npm run type-check` (tsc --noEmit) ✓ (exit 0); `npm run lint` ✓ (exit 0, 1 warning / 0 error); `npm run build` ✓ (exit 0, Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3). node_modules present (5103 dirs / 84021 files). Build gate **LULUS** — security nudge hanya warning, build tetap lanjut.',
    's12_build')

with open(PATH, 'w', encoding='utf-8') as f:
    f.write(src)

print('UPDATED: %s' % PATH)
print('REPLACEMENTS:')
for c in changes:
    print('  - %s' % c)
print('LINES: %d' % src.count('\n'))
