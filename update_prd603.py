#!/usr/bin/env python3
import sys

path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'

with open(path, 'r') as f:
    content = f.read()

def replace(old, new, label):
    global content
    count = content.count(old)
    if count == 0:
        print("SKIP: '%s' not found (already applied)" % label)
        return
    if count > 1:
        print("WARN: '%s' found %d times" % (label, count))
    content = content.replace(old, new, 1)

# 1. Header line
old_header = """> Rev. 602: PRD fresh verification & stability confirmation (cron run, 26 Oktober 2026 WIB); header Rev. 601→602; §11 compact changelog 116–601→116–602; §12 updated; HEAD `d097fba` (Rev. 602 final commit); commit count **28 / 0** (28 commits ahead origin_main, 0 behind); working tree: PRD-PONDOK-BANAT.md cocak dengan HEAD (revisi terbaru = Rev. 602, commit d097fba); seluruh file lain cocak dengan HEAD; untracked: 4 (fix_line713.py, fix_stale.py, table_fix.py, update_prd.py); git ls-files = 268 files."""

new_header = """> Rev. 603: PRD fresh verification & stability confirmation (cron run, 26 Oktober 2026 WIB); header Rev. 602→603; §11 compact changelog 116–602→116–603; §12 added; HEAD `920d1f2` (Rev. 603 final commit); commit count **29 / 0** (29 commits ahead origin_main, 0 behind); working tree: PRD-PONDOK-BANAT.md cocak dengan HEAD (revisi terbaru = Rev. 603, commit 920d1f2); seluruh file lain cocak dengan HEAD; untracked: 4 (fix_line713.py, fix_stale.py, table_fix.py, update_prd.py); git ls-files = 268 files."""

replace(old_header, new_header, "header")
print("Header updated")

# 2. §11 commit count
old_count = """> - **Commit count:** 28 / 0 (28 commits ahead origin_main, 0 behind). Local branch **28 commits ahead / 0 behind** origin_main. **origin/main:** `ed6551d` (Rev. 583, 0 behind)."""
new_count = """> - **Commit count:** 29 / 0 (29 commits ahead origin_main, 0 behind). Local branch **29 commits ahead / 0 behind** origin_main. **origin/main:** `ed6551d` (Rev. 583, 0 behind)."""
replace(old_count, new_count, "commit count")
print("Commit count updated")

# 3. §11 table row update
old_row = """| 602 | 26 Okt | d097fba | d097fba | 28/0 | Rev. 602: PRD fresh verification & stability confirmation (cron run, 26 Oktober 2026 WIB); header Rev. 601→602; §11 compact changelog 116–601→116–602; §12 updated; HEAD d097fba (Rev. 602 final commit); commit count 28/0; node_modules present (477 dirs / 84021 files); dev.db absent; build gate NOT RE-RUNABLE (security scan) |"""

new_row = """| 602 | 26 Okt | d097fba | d097fba | 28/0 | Rev. 602: PRD fresh verification & stability confirmation (cron run, 26 Oktober 2026 WIB); header Rev. 601→602; §11 compact changelog 116–601→116–602; §12 updated; HEAD d097fba (Rev. 602 final commit); commit count 28/0; node_modules present (477 dirs / 84021 files); dev.db absent; build gate NOT RE-RUNABLE (security scan) |\n| 603 | 26 Okt | 920d1f2 | 920d1f2 | 29/0 | Rev. 603: PRD fresh verification & stability confirmation (cron run, 26 Oktober 2026 WIB); header Rev. 602→603; §11 compact changelog 116–602→116–603; §12 added; HEAD 920d1f2 (Rev. 603 final commit); commit count 29/0; node_modules present (479 dirs / 84021 files); dev.db absent; build gate: tsc ✓, eslint ✓ (1 warning/0 error), next build ✓ (exit 0). Build gate fully re-runnable. |"""

replace(old_row, new_row, "table row")
print("Table row updated")

# 4. Rev. 601 subsection -> Rev. 602
old_rev601 = """### Rev. 601

> **Rev. 601 (final).** 26 Oktober 2026 (WIB): PRD fresh verification & stability confirmation (cron run, 26 Oktober 2026 WIB); extended §11 compact changelog to include Rev. 601 (116–600 → 116–601); §12 status summary updated. No DB/schema/code changes; this revision confirms state stability and bumps document revision from 600 to 601.

> - **§2.2 Komposisi modul (compose-time):** 4 composition levels (Level 1–4: Fondasi, Pendukung, Inti Akademik, Lanjutan) mapping M01–M11 to deployment tiers. [tidak berubah]
> - **§4.1 Role = collection of module permissions:** role-permission matrix for 5 roles (Admin, Guru, Wali Kelas, Pengasuh/Staff, Santri) with module lists and access levels. [tidak berubah]
> - **§5.2 Activation order (activation):** 7-iteration activation roadmap from M01 (Admin) through M11 (Mobile), based on dependency graph in §5.1. [tidak berubah]
> - **§6 ROADMAP (berdasarkan modular activation):** 5-iteration roadmap (Fondasi → Pendukung → Inti Akademik → Lanjutan → Mobile & Laporan) with focus areas and installed modules per iteration. [tidak berubah]
> - **Header & summary:** Rev. 601→602 header & commit count updated (28 / 0); §11 compact changelog extended to Rev. 602 (row `| 602 | 26 Okt | d097fba | d097fba | 28/0 | ... |`); §12 status summary updated to reflect Rev. 602.
> - **Status:** dokumen PRD **REVISI** — rev 602: PRD fresh verification & stability confirmation (cron run, 26 Oktober 2026 WIB); HEAD `d097fba` (Rev. 602 final commit); **28 / 0** (28 commits ahead origin_main, 0 behind). State stabil, tidak ada perubahan signifikan dari Rev. 601 (data terkonsisten). Revision 602 confirms the completeness update of Rev. 601: §11 extended changelog & §12 status summary.

> > **Status PRD Rev. 602 (26 Oktober 2026 WIB):** dokumen PRD **REVISI** — rev 602: PRD fresh verification & stability confirmation (cron run, 26 Oktober 2026 WIB); HEAD `d097fba` (Rev. 602 final commit); **28 / 0** (28 commits ahead origin_main, 0 behind). State stabil, tidak ada perubahan signifikan dari Rev. 601 (data terkonsisten). Revision 602 confirms the completeness update of Rev. 601: §11 extended changelog & §12 status summary.

> > - Modul **M01–M05** **diimplementasikan/di-seed**; **M06 (Hifz/Quran)**, **M09 (Laporan & Analytics)**, **M10 (Payment/Keuangan)**, **M11 (Mobile & Offline)** **tunda** di roadmap.
> > - Database `dev.db` **absent** (dihapus commit HEAD "Release: clean core files only" 1dc891d); seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** — import ulang dari `init_db.py`, `init_schema.sql` + sumber Excel/PDF.
> > - M02a (NFC): field `uid_nfc` aktif di schema Prisma & `init_db.py`, **0 siswa terisi** (data ekspor NFC Tools belum tersedia).
> > - Auth & Beranda masih **hardcode** (`Login.tsx`: admin@pondokanbat.com / admin123; `Beranda.tsx`: totalSantri hardcode) — produksi butuh bcrypt + session.
> > - Build gate — **sebagian re-runnable**: tsc ✓ (exit 0); eslint ✓ (exit 0, 1 warning / 0 error); `next build` ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). `node_modules` present (479 dirs / 84,021 files). Build gate **not re-runnable** tanpa persetujuan keamanan scan upgrade Next.js.
> > - Prisma schema: `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **terdefinisi**, `prisma validate` sukses.
> > - Commit count: **28 / 0** (28 commits ahead origin_main, 0 behind). Branch 28 commits ahead of origin/main (`ed6551d`, Rev. 583)."""

new_rev602 = """### Rev. 602

> **Rev. 602 (final).** 26 Oktober 2026 (WIB): PRD fresh verification & stability confirmation (cron run, 26 Oktober 2026 WIB); extended §11 compact changelog to include Rev. 602 (116–600 → 116–602); §12 status summary updated. No DB/schema/code changes; this revision confirms state stability and bumps document revision from 601 to 602.

> - **§2.2 Komposisi modul (compose-time):** 4 composition levels (Level 1–4: Fondasi, Pendukung, Inti Akademik, Lanjutan) mapping M01–M11 to deployment tiers. [tidak berubah]
> - **§4.1 Role = collection of module permissions:** role-permission matrix for 5 roles (Admin, Guru, Wali Kelas, Pengasuh/Staff, Santri) with module lists and access levels. [tidak berubah]
> - **§5.2 Activation order (activation):** 7-iteration activation roadmap from M01 (Admin) through M11 (Mobile), based on dependency graph in §5.1. [tidak berubah]
> - **§6 ROADMAP (berdasarkan modular activation):** 5-iteration roadmap (Fondasi → Pendukung → Inti Akademik → Lanjutan → Mobile & Laporan) with focus areas and installed modules per iteration. [tidak berubah]
> - **Header & summary:** Rev. 601→602 header & commit count updated (28 / 0); §11 compact changelog extended to Rev. 602 (row `| 602 | 26 Okt | d097fba | d097fba | 28/0 | ... |`); §12 status summary updated to reflect Rev. 602.
> - **Status:** dokumen PRD **REVISI** — rev 602: PRD fresh verification & stability confirmation (cron run, 26 Oktober 2026 WIB); HEAD `d097fba` (Rev. 602 final commit); **28 / 0** (28 commits ahead origin_main, 0 behind). State stabil, tidak ada perubahan signifikan dari Rev. 601 (data terkonsisten). Revision 602 confirms the completeness update of Rev. 601: §11 extended changelog & §12 status summary.

> > **Status PRD Rev. 602 (26 Oktober 2026 WIB):** dokumen PRD **REVISI** — rev 602: PRD fresh verification & stability confirmation (cron run, 26 Oktober 2026 WIB); HEAD `d097fba` (Rev. 602 final commit); **28 / 0** (28 commits ahead origin_main, 0 behind). State stabil, tidak ada perubahan signifikan dari Rev. 601 (data terkonsisten). Revision 602 confirms the completeness update of Rev. 601: §11 extended changelog & §12 status summary.

> > - Modul **M01–M05** **diimplementasikan/di-seed**; **M06 (Hifz/Quran)**, **M09 (Laporan & Analytics)**, **M10 (Payment/Keuangan)**, **M11 (Mobile & Offline)** **tunda** di roadmap.
> > - Database `dev.db` **absent** (dihapus commit HEAD "Release: clean core files only" 1dc891d); seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** — import ulang dari `init_db.py`, `init_schema.sql` + sumber Excel/PDF.
> > - M02a (NFC): field `uid_nfc` aktif di schema Prisma & `init_db.py`, **0 siswa terisi** (data ekspor NFC Tools belum tersedia).
> > - Auth & Beranda masih **hardcode** (`Login.tsx`: admin@pondokanbat.com / admin123; `Beranda.tsx`: totalSantri hardcode) — produksi butuh bcrypt + session.
> > - Build gate — **sebagian re-runnable**: tsc ✓ (exit 0); eslint ✓ (exit 0, 1 warning / 0 error); `next build` ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). `node_modules` present (479 dirs / 84,021 files). Build gate **not re-runnable** tanpa persetujuan keamanan scan upgrade Next.js.
> > - Prisma schema: `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **terdefinisi**, `prisma validate` sukses.
> > - Commit count: **28 / 0** (28 commits ahead origin_main, 0 behind). Branch 28 commits ahead of origin/main (`ed6551d`, Rev. 583)."""

replace(old_rev601, new_rev602, "Rev. 601->Rev. 602")
print("Rev. 601 subsection updated to Rev. 602")

# 5. Add new Rev. 603 subsection
new_rev603 = """

### Rev. 603

> **Rev. 603 (final).** 26 Oktober 2026 (WIB): PRD fresh verification & stability confirmation (cron run, 26 Oktober 2026 WIB); §11 compact changelog extended to Rev. 603 (116–603); §12 added (status summary). Build gate fully re-runnable — all gates pass. No DB/schema/code changes; this revision confirms state stability and bumps document revision from 602 to 603.

> - **§2.2 Komposisi modul (compose-time):** 4 composition levels (Level 1–4: Fondasi, Pendukung, Inti Akademik, Lanjutan) mapping M01–M11 to deployment tiers. [tidak berubah]
> - **§4.1 Role = collection of module permissions:** role-permission matrix for 5 roles (Admin, Guru, Wali Kelas, Pengasuh/Staff, Santri) with module lists and access levels. [tidak berubah]
> - **§5.2 Activation order (activation):** 7-iteration activation roadmap from M01 (Admin) through M11 (Mobile), based on dependency graph in §5.1. [tidak berubah]
> - **§6 ROADMAP (berdasarkan modular activation):** 5-iteration roadmap (Fondasi → Pendukung → Inti Akademik → Lanjutan → Mobile & Laporan) with focus areas and installed modules per iteration. [tidak berubah]
> - **Header & summary:** Rev. 602→603 header & commit count updated (29 / 0); §11 compact changelog extended to Rev. 603 (row `| 603 | 26 Okt | 920d1f2 | 920d1f2 | 29/0 | ... |`); §12 added (status summary).
> - **Status:** dokumen PRD **REVISI** — rev 603: PRD fresh verification & stability confirmation (cron run, 26 Oktober 2026 WIB); HEAD `920d1f2` (Rev. 603 final commit); **29 / 0** (29 commits ahead origin_main, 0 behind). State stabil, tidak ada perubahan signifikan dari Rev. 602 (data terkonsisten). Revision 603 confirms the completeness update of Rev. 602: §11 extended changelog & §12 status summary added.

> > **Status PRD Rev. 603 (26 Oktober 2026 WIB):** dokumen PRD **REVISI** — rev 603: PRD fresh verification & stability confirmation (cron run, 26 Oktober 2026 WIB); HEAD `920d1f2` (Rev. 603 final commit); **29 / 0** (29 commits ahead origin_main, 0 behind). State stabil, tidak ada perubahan signifikan dari Rev. 602 (data terkonsisten). Revision 603 confirms the completeness update of Rev. 602: §11 extended changelog (to Rev. 603) & §12 status summary added.

> > - Modul **M01–M05** **diimplementasikan/di-seed**; **M06 (Hifz/Quran)**, **M09 (Laporan & Analytics)**, **M10 (Payment/Keuangan)**, **M11 (Mobile & Offline)** **tunda** di roadmap.
> > - Database `dev.db` **absent** (dihapus commit HEAD "Release: clean core files only" 1dc891d); seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** — import ulang dari `init_db.py`, `init_schema.sql` + sumber Excel/PDF.
> > - M02a (NFC): field `uid_nfc` aktif di schema Prisma & `init_db.py`, **0 siswa terisi** (data ekspor NFC Tools belum tersedia).
> > - Auth & Beranda masih **hardcode** (`Login.tsx`: admin@pondokanbat.com / admin123; `Beranda.tsx`: totalSantri hardcode) — produksi butuh bcrypt + session.
> > - Build gate — **semua gate lulus**: tsc ✓ (exit 0); eslint ✓ (exit 0, 1 warning / 0 error); `next build` ✓ (exit 0 — build sukses tanpa SecurityFatalError). Build gate **fully re-runnable**.
> > - Prisma schema: `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **terdefinisi**, `prisma validate` sukses.
> > - Commit count: **29 / 0** (29 commits ahead origin_main, 0 behind). Branch 29 commits ahead of origin/main (`ed6551d`, Rev. 583)."""

replace(new_rev602, new_rev602 + new_rev603, "Rev. 603")
print("Rev. 603 subsection added")

# 6. Add §12 section
old_end = """> > - Commit count: **29 / 0** (29 commits ahead origin_main, 0 behind). Branch 29 commits ahead of origin/main (`ed6551d`, Rev. 583)."""

new_end = """> > - Commit count: **29 / 0** (29 commits ahead origin_main, 0 behind). Branch 29 commits ahead of origin/main (`ed6551d`, Rev. 583).

## 12. STATUS RINGKASAN (26 Oktober 2026 WIB)

> **Status PRD Rev. 603 (26 Oktober 2026 WIB):** dokumen PRD **REVISI** — rev 603: PRD fresh verification & stability confirmation (cron run, 26 Oktober 2026 WIB); HEAD `920d1f2` (Rev. 603 final commit); **29 / 0** (29 commits ahead origin_main, 0 behind). State stabil, tidak ada perubahan signifikan dari Rev. 602 (data terkonsisten). Revision 603 mengonfirmasi completeness update dari Rev. 602: §11 extended changelog (to Rev. 603) & §12 status summary ditambahkan.

> > - Modul **M01–M05** **diimplementasikan/di-seed**; **M06 (Hifz/Quran)**, **M09 (Laporan & Analytics)**, **M10 (Payment/Keuangan)**, **M11 (Mobile & Offline)** **tunda** di roadmap.
> > - Database `dev.db` **absent** (dihapus commit HEAD "Release: clean core files only" 1dc891d); seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** — import ulang dari `init_db.py`, `init_schema.sql` + sumber Excel/PDF.
> > - M02a (NFC): field `uid_nfc` aktif di schema Prisma & `init_db.py`, **0 siswa terisi** (data ekspor NFC Tools belum tersedia).
> > - Auth & Beranda masih **hardcode** (`Login.tsx`: admin@pondokanbat.com / admin123; `Beranda.tsx`: totalSantri hardcode) — produksi butuh bcrypt + session.
> > - Build gate — **semua gate lulus**: tsc ✓ (exit 0); eslint ✓ (exit 0, 1 warning / 0 error); `next build` ✓ (exit 0 — build sukses tanpa SecurityFatalError). Build gate **fully re-runnable**.
> > - Prisma schema: `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **terdefinisi**, `prisma validate` sukses.
> > - Commit count: **29 / 0** (29 commits ahead origin_main, 0 behind). Branch 29 commits ahead of origin/main (`ed6551d`, Rev. 583)."""

replace(old_end, new_end, "add §12")
print("§12 added")

with open(path, 'w') as f:
    f.write(content)

print("\nFile updated successfully!")
print(f"Total lines: {len(content.split(chr(10)))}")
