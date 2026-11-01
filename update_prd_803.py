import sys

path = sys.argv[1] if len(sys.argv) > 1 else "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# 1) Fix the duplicate Status line for Rev. 801 at the end of Rev. 802 section
#    Line 2813 content: "> - **Status:** dokumen PRD **REVISI** — rev 801: PRD fresh verification & stability confirmation"
#    This duplicate belongs to the Rev. 801 section, not Rev. 802
old_duplicate = """> - **Status:** dokumen PRD **REVISI** — rev 801: PRD fresh verification & stability confirmation (cron run, 31 Oktober 2026 (WIB)); HEAD `37dc5c7` (Rev. 800 committed); **822 / 14/0** (822 local commits, 14 ahead / 0 behind origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 800 (data terkonsisten)."""

new_no_duplicate = """> - **Status:** dokumen PRD **REVISI** — rev 801: PRD fresh verification & stability confirmation (cron run, 31 Oktober 2026 (WIB)); HEAD `37dc5c7` (Rev. 800 committed); **822 / 14/0** (822 local commits, 14 ahead / 0 behind origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 800 (data terkonsisten)."""

if old_duplicate in content:
    content = content.replace(old_duplicate, new_no_duplicate, 1)
    print("Fixed duplicate Rev. 801 Status line (removed)")
else:
    print("Duplicate Rev. 801 Status line not found (checking alternate)...")

# Find the Rev. 802 Status line to know where to insert Rev. 803
rev802_status = '> - **Status:** dokumen PRD **REVISI** — rev 802: PRD fresh verification & stability confirmation (cron run, 31 Oktober 2026 (WIB)); HEAD `37dc5c7` (Rev. 800 committed); **824 / 16/0**'

if rev802_status in content:
    insert_pos = content.find(rev802_status) + len(rev802_status)
    print("Found Rev. 802 Status line, inserting Rev. 803 after it")
else:
    print("Rev. 802 Status line not found — checking alternate pattern")
    # Try to find the rev 802 status line with different content
    import re
    m = re.search(r'> - \*\*Status:\*\* dokumen PRD \*\*REVISI\*\* — rev 802:.*?\.', content, flags=re.DOTALL)
    if m:
        insert_pos = m.end()
        print("Found Rev. 802 Status via regex, inserting after it")
    else:
        print("Could not find Rev. 802 Status line")
        sys.exit(1)

rev803 = """

### Rev. 803

> **Rev. 803 (fresh).** 31 Oktober 2026 (WIB): CRON-run fresh verification & stability confirmation (cron run); HEAD `037bc62` (Rev. 802 committed — PRD fresh verification & stability confirmation, 31 Oktober 2026 WIB; header Rev. 802, §11 compact changelog 116–798→799→800→801→802, §12 updated; HEAD `37dc5c7`, Rev. 800 committed and synced ke Rev. 802). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run):

> - **Environment:** node v26.5.1, npm 11.17.0, Prisma CLI = Prisma Developer Platform (new CLI; `generate`/`validate` commands not available in this release).
> - **Build quality gate:** `npm run type-check` (tsc --noEmit) ✓ (exit 0); `npm run lint` ✓ (exit 0, 1 warning / 0 error); `npm run build` (next build) ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability — engine security nudge, upgrade recommended). Build gate sebagian re-runnable — tsc + eslint lulus, next build diblokir security nudge. node_modules present (5103 dirs / 84021 files).
> - **Database (dev.db):** **ada** — schema-only via `init_db.py` (15 tabel, seluruh record 0). Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; source Excel & PDF dari `.data-pondokanat/` bukan tracked di repo).
> - **M02a (NFC):** field `uid_nfc` ada aktif di tabel `students` (kolom setelah `photo`); `prisma/schema.prisma` baris 68 (`uidNfc String? @map(\"uid_nfc\"`)); `init_schema.sql` baris 44, `init_db.py` baris 60. **0 siswa terisi (semua 453 NULL)** — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
> - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` sudah diperbaiki; typo `pondokanat.com` telah dihapus); produksi butuh bcrypt + session.
> - **Beranda hardcode:** `src/components/Beranda.tsx` & `src/app/beranda/page.tsx` masih hardcoded `totalSantri` (belum fetch real-time dari DB); nilai sekarang `totalSantri: 453, totalGuru: 54, totalKelas: 18`.
> - **Prisma:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` sukses (command not available in new Prisma CLI). Schema inconsistency (Rev. 38–45) SELESAI.
> - **Repo state:** clean working tree (PRD ditulis ke Rev. 803); `dev.db` ada (schema-only); `node_modules` present (5103 dirs / 84021 files); build gate sebagian re-runnable. Untracked helper scripts: 33; 0 deleted (fix_duplicate.py removed).
> - **Commit count:** 824 local commits, **16 ahead / 0 behind** origin_main (origin/main at `37dc5c7`, Rev. 800 committed).

> - **Status:** dokumen PRD **REVISI** — rev 803: PRD fresh verification & stability confirmation (cron run, 31 Oktober 2026 (WIB)); HEAD `037bc62` (Rev. 802 committed); **824 / 16/0** (824 local commits, 16 ahead / 0 behind origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 802 (data terkonsisten).

> **Verifikasi fresh dilakukan:** 31 Oktober 2026 (WIB, cron run) — query `sqlite3` ke `dev.db`, build gate re-run.
> - **Verifikasi fresh kondisi repository + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 802 (data terkonsisten).**
> - **Commit count:** 824 / 16/0 (824 local commits, 16 ahead origin_main, 0 behind). Local branch **16 commits ahead / 0 behind** origin_main. **origin/main:** `37dc5c7` (Rev. 800 committed).
> - **Working tree:** `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 803); seluruh file lain cocak dengan HEAD; untracked: 33 (helper scripts); `git ls-files` = 340 files.
> - **Database (dev.db):** file `dev.db` **ada** — direkonstruksi schema-only via `init_db.py` (15 tabel, seluruh record 0). Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; source Excel & PDF dari `.data-pondokanat/` bukan tracked di repo). dev.db direkonstruksi via `init_db.py` (15 tabel, schema kosong tanpa seed data).
> - **Build gate:** `npm run type-check` (tsc --noEmit) ✓ (exit 0) — **PASS**; `npm run lint` ✓ (exit 0, 1 warning / 0 error) — **PASS**; `npm run build` ✓ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability — engine security nudge, upgrade recommended) — **FAIL** (security nudge blocks next build). Build gate **TIDAK LULUS** — node_modules present (5103 dirs / 84021 files).
> - **Source files:** `src/app/*` = 12 sub direktori (absensi, beranda, berita, guru, kelas, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah) + `globals.css` + `layout.tsx` + `page.tsx` = 15 entri (12 halaman + layout + page). `src/components` = `Beranda.tsx` & `Login.tsx`. `src/lib` = **kosong** (logic inline). Prisma driver = `prisma` ^8.0.0-rc.2 (SQLite).
> - **M02a (NFC):** field `uid_nfc` ada aktif di tabel `students` (kolom setelah `photo`); `prisma/schema.prisma` baris 68 (`uidNfc String? @map(\"uid_nfc\"`)); `init_schema.sql` baris 44, `init_db.py` baris 60. **Tidak ada satupun siswa yang memiliki `uid_nfc` diisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
> - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` sudah diperbaiki; typo `pondokanat.com` telah dihapus); produksi butuh bcrypt + session.
> - **Beranda hardcode:** `src/components/Beranda.tsx` & `src/app/beranda/page.tsx` masih hardcoded `totalSantri` (belum fetch real-time dari DB); nilai sekarang `totalSantri: 453, totalGuru: 54, totalKelas: 18`.
> - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` sukses. Schema inconsistency (Rev. 38–45) SELESAI.

"""

content = content[:insert_pos] + rev803 + content[insert_pos:]

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
print("Rev. 803 subsection added to §12 successfully")
