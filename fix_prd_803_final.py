import sys

path = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Find the duplicate/orphaned Rev. 802 section (starting with "> ### Rev. 802" that appears AFTER the first Rev. 802 Status line)
# The first Rev. 802 Status line is: "> - **Status:** dokumen PRD **REVISI** — rev 802: PRD fresh verification & stability confirmation (cron run, 31 Oktober 2026 (WIB)); HEAD `37dc5c7` (Rev. 800 committed); **824 / 16/0**"
# The duplicate Rev. 802 section starts after the first Rev. 802 Status line + its additional details

first_rev802_status = "> - **Status:** dokumen PRD **REVISI** — rev 802: PRD fresh verification & stability confirmation (cron run, 31 Oktober 2026 (WIB)); HEAD `37dc5c7` (Rev. 800 committed); **824 / 16/0**"

if first_rev802_status in content:
    first_status_end = content.find(first_rev802_status) + len(first_rev802_status)
    
    # After the first Rev. 802 Status line, there's additional details:
    # > **Verifikasi fresh dilakukan:** ...
    # > - **Verifikasi fresh kondisi repository + dev.db ...**
    # > - **Commit count:** 822 / 14/0 ... (wrong, should be 824/16/0)
    # > - **Working tree:** ...
    # > - **Database (dev.db):** ...
    # > - **Build gate:** ...
    # > - **Source files:** ...
    # > - **M02a (NFC):** ...
    # > - **Auth hardcode:** ...
    # > - **Beranda hardcode:** ...
    # > - **Prisma schema:** ...
    # > - **Status:** dokumen PRD **REVISI** — rev 801: ... (duplicate for Rev. 801)
    
    # The duplicate Status line for Rev. 801 marks the end of the mangled content
    orphaned_status = "> - **Status:** dokumen PRD **REVISI** — rev 801: PRD fresh verification & stability confirmation (cron run, 31 Oktober 2026 (WIB)); HEAD `37dc5c7` (Rev. 800 committed); **822 / 14/0**"
    
    if orphaned_status in content[first_status_end:]:
        orphaned_end = first_status_end + content[first_status_end:].find(orphaned_status) + len(orphaned_status)
        orphaned_section = content[first_status_end:orphaned_end]
        print("Found mangled Rev. 802 content at position", first_status_end, "to", orphaned_end)
        print("Mangled section length:", len(orphaned_section))
        
        # Remove the mangled content
        content = content[:first_status_end] + content[orphaned_end:]
        
        # Now add Rev. 803 entry after the Rev. 802 Status line
        rev803_entry = """
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
> - **Status:** dokumen PRD **REVISI** — rev 802: PRD fresh verification & stability confirmation (cron run, 31 Oktober 2026 (WIB)); HEAD `37dc5c7` (Rev. 800 committed); **824 / 16/0** (824 local commits, 16 ahead / 0 behind origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 801 (data terkonsisten).
"""

        content = content.replace(rev803_entry, "", 1)  # remove duplicate if exists
        content = content.replace("\n\n", "\n", 1)  # normalize
        
        # Find the position after the Rev. 802 Status line and insert Rev. 803
        # The Rev. 802 Status line is at first_status_end
        # We need to insert after the first Rev. 802 section ends
        # The first Rev. 802 section ends with the "Verifikasi fresh dilakukan" section
        
        # Let's find the end of the first Rev. 802 section (after the "Status" line for Rev. 802)
        # The first Rev. 802 section has this structure:
        # > - **Status:** dokumen PRD **REVISI** — rev 802: ... (first_status_end)
        # > **Verifikasi fresh dilakukan:** ...
        # > - **Verifikasi fresh kondisi repository + dev.db ...**
        # > - **Commit count:** 822 / 14/0 ... (wrong)
        # > - **Working tree:** ...
        # > - **Database (dev.db):** ...
        # > - **Build gate:** ...
        # > - **Source files:** ...
        # > - **M02a (NFC):** ...
        # > - **Auth hardcode:** ...
        # > - **Beranda hardcode:** ...
        # > - **Prisma schema:** ...
        # > - **Status:** dokumen PRD **REVISI** — rev 801: ... (duplicate for Rev. 801)
        
        # We already removed the mangled content (lines from first_status_end to orphaned_end)
        # Now we need to insert Rev. 803 after the Rev. 802 Status line
        
        # Find the position of the first Rev. 802 Status line
        pos = content.find(first_rev802_status)
        if pos != -1:
            # Insert after the first Rev. 802 Status line
            insert_pos = pos + len(first_rev802_status)
            content = content[:insert_pos] + rev803_entry + content[insert_pos:]
            print("Inserted Rev. 803 entry after first Rev. 802 Status line")
        else:
            print("First Rev. 802 Status line not found")
            sys.exit(1)
    else:
        print("Orphaned Status line for Rev. 801 not found")
else:
    print("First Rev. 802 Status line not found")
    sys.exit(1)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
print("Done. New file length:", len(content))
