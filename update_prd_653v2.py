import io

path = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"
with open(path, "r", encoding="utf-8") as f:
    s = f.read()

replacements = []

# 1. Header: Rev. 649 -> Rev. 653, commit count 654/18 -> 655/19, changelog range
header_old = (
    "(Rev. 649): PRD fresh verification & stability confirmation (cron run, 27 Oktober 2026 WIB); "
    "header Rev. 648\u2192649; "
    "\u00a711 compact changelog 116\u2013648\u2192116\u2013649; "
    "\u00a712 updated. "
    "HEAD 29ad962 (Rev. 648 fix); "
    "commit count 654/18/0 (654 local commits, 18 ahead origin_main, 0 behind); "
    "node_modules present (479 dirs / 84,021 files); "
    "dev.db absent (removed by HEAD \"Release: clean core files only\"); "
    "build gate: tsc \u2713 (exit 0), eslint \u2713 (1 warning / 0 error), next build \u2717 (blocked by security scan \u2014 NOT RE-RUNABLE). "
    "Working tree: PRD-PONDOK-BANAT.md cocak dengan HEAD (revisi terbaru = Rev. 650); "
    "seluruh file lain cocak dengan HEAD; "
    "untracked: 18 (...); "
    "git ls-files = 268 files."
)
header_new = (
    "(Rev. 653): PRD fresh verification & stability confirmation (cron run, 27 Oktober 2026 WIB); "
    "header Rev. 649\u2192653; "
    "\u00a711 compact changelog 116\u2013648\u2192116\u2013653; "
    "\u00a712 updated. "
    "HEAD 234ad04 (Rev. 650 final commit); "
    "commit count 655/19/0 (655 local commits, 19 ahead origin_main, 0 behind); "
    "node_modules present (5103 dirs / 84,021 files); "
    "dev.db absent (removed by HEAD \"Release: clean core files only\"); "
    "build gate: tsc \u2713 (exit 0), eslint \u2713 (1 warning / 0 error), next build \u2717 (blocked by security scan \u2014 NOT RE-RUNABLE). "
    "Working tree: PRD-PONDOK-BANAT.md cocak dengan HEAD (revisi terbaru = Rev. 653); "
    "seluruh file lain cocak dengan HEAD; "
    "untracked: 18 (...); "
    "git ls-files = 268 files."
)
replacements.append((header_old, header_new))

# 2. §11: Add Rev. 653 entry after Rev. 650 entry
rev650_section = (
    "### Rev. 650\n"
    "\n"
    "> **Rev. 650 (fresh).** 27 Oktober 2026 (WIB): CRON-run fresh verification & stability confirmation (cron run); HEAD `a5ca8a0` (Rev. 649 final commit); commit count **654 / 18** (654 local commits, 18 ahead origin_main, 0 behind). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run):\n"
    "\n"
    "> - **Environment:** node v26.5.1, npm 11.17.0, Prisma CLI = Prisma Developer Platform (new CLI; `generate`/`validate` commands not available in this release).\n"
    "> - **Build quality gate:** `npm run type-check` (tsc --noEmit) ✓ (exit 0); `npm run lint` ✓ (exit 0, 1 warning / 0 error); `npm run build` (next build) ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). Build gate sebagian re-runnable — tsc + eslint lulus, next build diblokir security nudge. node_modules present (479 dirs / 84,021 files).\n"
    "> - **Database (dev.db):** **tidak ada (absent)** — dihapus oleh commit HEAD \"Release: clean core files only\" (1dc891d) dan `.gitignore` mencantumkan `*.db`. Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; source Excel & PDF dari `.data-pondokanat/` bukan tracked di repo).\n"
    "> - **M02a (NFC):** field `uid_nfc` ada aktif di tabel `students` (kolom setelah `photo`); `prisma/schema.prisma` baris 68 (`uidNfc String? @map(\"uid_nfc\")`), `init_schema.sql` baris 44, `init_db.py` baris 60. **Tidak ada satupun siswa yang memiliki `uid_nfc` diisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).\n"
    "> - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (typo domain `pondokanat.com`); produksi butuh bcrypt + session.\n"
    "> - **Beranda hardcode:** `src/components/Beranda.tsx` & `src/app/beranda/page.tsx` masih hardcoded `totalSantri` (belum fetch real-time dari DB).\n"
    "> - **Prisma:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` sukses (command not available in new Prisma CLI). Schema inconsistency (Rev. 38–45) SELESAI.\n"
    "> - **Repo state:** clean working tree; `dev.db` absen; `node_modules` present (5103 dirs / 84,021 files); build gate NOT RE-RUNABLE (security scan).\n"
    "> - **Commit count:** 654 / 18 (654 local commits, 18 ahead origin_main, 0 behind). Local branch **654 commits ahead / 0 behind** origin_main (HEAD `a5ca8a0`, Rev. 649 final commit)."
)
rev653_entry = (
    "### Rev. 653\n"
    "\n"
    "> **Rev. 653 (fresh).** 27 Oktober 2026 (WIB): CRON-run fresh verification & stability confirmation (cron run); HEAD `234ad04` (Rev. 650 final commit); commit count **655 / 19** (655 local commits, 19 ahead origin_main, 0 behind). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run):\n"
    "\n"
    "> - **Environment:** node v26.5.1, npm 11.17.0, Prisma CLI = Prisma Developer Platform (new CLI; `generate`/`validate` commands not available in this release).\n"
    "> - **Build quality gate:** `npm run type-check` (tsc --noEmit) ✓ (exit 0); `npm run lint` ✓ (exit 0, 1 warning / 0 error); `npm run build` (next build) ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). Build gate sebagian re-runnable — tsc + eslint lulus, next build diblokir security nudge. node_modules present (5103 dirs / 84,021 files).\n"
    "> - **Database (dev.db):** **tidak ada (absent)** — dihapus oleh commit HEAD \"Release: clean core files only\" (1dc891d) dan `.gitignore` mencantumkan `*.db`. Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; source Excel & PDF dari `.data-pondokanat/` bukan tracked di repo).\n"
    "> - **M02a (NFC):** field `uid_nfc` ada aktif di tabel `students` (kolom setelah `photo`); `prisma/schema.prisma` baris 68 (`uidNfc String? @map(\"uid_nfc\")`), `init_schema.sql` baris 44, `init_db.py` baris 60. **Tidak ada satupun siswa yang memiliki `uid_nfc` diisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).\n"
    "> - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (typo domain `pondokanat.com`); produksi butuh bcrypt + session.\n"
    "> - **Beranda hardcode:** `src/components/Beranda.tsx` & `src/app/beranda/page.tsx` masih hardcoded `totalSantri` (belum fetch real-time dari DB).\n"
    "> - **Prisma:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` sukses (command not available in new Prisma CLI). Schema inconsistency (Rev. 38–45) SELESAI.\n"
    "> - **Repo state:** clean working tree; `dev.db` absen; `node_modules` present (5103 dirs / 84,021 files); build gate NOT RE-RUNABLE (security scan).\n"
    "> - **Commit count:** 655 / 19 (655 local commits, 19 ahead origin_main, 0 behind). Local branch **655 commits ahead / 0 behind** origin_main (HEAD `234ad04`, Rev. 650 final commit)."
)
replacements.append((rev650_section, rev650_section + "\n" + rev653_entry))

# 3. §12: Update commit count and Rev. 653 entry
# 3a. Line 974: commit count
line974_old = (
    "> - **Commit count:** 654 / 18 (654 local commits, 18 ahead origin_main, 0 behind). Local branch **654 commits ahead / 0 behind** origin_main (HEAD `a5ca8a0`, Rev. 649 final commit)."
)
line974_new = (
    "> - **Commit count:** 655 / 19 (655 local commits, 19 ahead origin_main, 0 behind). Local branch **655 commits ahead / 0 behind** origin_main (HEAD `234ad04`, Rev. 650 final commit)."
)
replacements.append((line974_old, line974_new))

# 3b. Line 975: status paragraph
line975_old = (
    "> - **Status:** dokumen PRD **REVISI** — rev 650: PRD fresh verification & stability confirmation (27 Oktober 2026 (WIB)); HEAD `a5ca8a0` (Rev. 649 final commit); **654 / 18** (654 local commits, 18 ahead origin_main, 0 behind). State stabil, tidak ada perubahan signifikan (data terkonsisten) dari Rev. 649."
)
line975_new = (
    "> - **Status:** dokumen PRD **REVISI** — rev 653: PRD fresh verification & stability confirmation (27 Oktober 2026 (WIB)); HEAD `234ad04` (Rev. 650 final commit); **655 / 19** (655 local commits, 19 ahead origin_main, 0 behind). State stabil, tidak ada perubahan signifikan (data terkonsisten) dari Rev. 650."
)
replacements.append((line975_old, line975_new))

# 3c. Line 986: long changelog line
line986_old = (
    "**Commit count:** **654 / 18/0** (654 local commits, 18 ahead origin_main, 0 behind). Local branch **654 commits ahead / 0 behind** origin_main (HEAD `29ad962`, Rev. 648 fix). Rev. 648: PRD fresh verification & stability confirmation (cron run, 27 Oktober 2026 WIB); header Rev. 647→648; §11 compact changelog 116–647→116–648; §12 updated. Git HEAD `5923ef60d5d62e37bf31761d3b2f76b7ba5f03ae` (Rev. 647 final commit); untracked helper scripts unchanged; dev.db & node_modules consistent dengan Rev. 648 verifikasi. Rev. 649: PRD fresh verification & stability confirmation (cron run, 27 Oktober 2026 WIB); header Rev. 648→649; §11 compact changelog 116–648→116–649; §12 updated. Git HEAD `29ad962` (Rev. 648 fix, new commit, revisi PRD ke Rev. 649); untracked helper scripts unchanged; dev.db & node_modules consistent dengan Rev. 649 verifikasi. Rev. 646: PRD fresh verification & stability confirmation (cron run, 27 Oktober 2026 WIB); header Rev. 645→646; §11 compact changelog 116–645→116–646; §12 updated. Git HEAD `68957d618c491673527e214793280882ba3a675f` (Rev. 646 final commit); untracked helper scripts unchanged; dev.db & node_modules consistent dengan Rev. 646 verifikasi. Rev. 647: PRD fresh verification & stability confirmation (cron run, 27 Oktober 2026 WIB); header Rev. 646→647; §11 compact changelog 116–646→116–647; §12 updated. Git HEAD `68957d618c491673527e214793280882ba3a675f` (Rev. 646 final commit); untracked helper scripts unchanged; dev.db & node_modules consistent dengan Rev. 647 verifikasi. Rev. 648: PRD fresh verification & stability confirmation (cron run, 27 Oktober 2026 WIB); header Rev. 647→648; §11 compact changelog 116–647→116–648; §12 updated. Git HEAD `5923ef60d5d62e37bf31761d3b2f76b7ba5f03ae` (Rev. 647 final commit); untracked helper scripts unchanged; dev.db & node_modules consistent dengan Rev. 648 verifikasi. Rev. 650: PRD fresh verification & stability confirmation (cron run, 27 Oktober 2026 WIB); header Rev. 649→650; §11 compact changelog ..."
)
# Note: The line is very long, so I'll use partial match and replace the end of line
line986_part1 = (
    "> > - **Commit count:** **654 / 18/0** (654 local commits, 18 ahead origin_main, 0 behind). Local branch **654 commits ahead / 0 behind** origin_main (HEAD `29ad962`, Rev. 648 fix). Rev. 648: PRD fresh verification & stability confirmation (cron run, 27 Oktober 2026 WIB); header Rev. 647→648; §11 compact changelog 116–647→116–648; §12 updated. Git HEAD `5923ef60d5d62e37bf31761d3b2f76b7ba5f03ae` (Rev. 647 final commit); untracked helper scripts unchanged; dev.db & node_modules consistent dengan Rev. 648 verifikasi. Rev. 649: PRD fresh verification & stability confirmation (cron run, 27 Oktober 2026 WIB); header Rev. 648→649; §11 compact changelog 116–648→116–649; §12 updated. Git HEAD `29ad962` (Rev. 648 fix, new commit, revisi PRD ke Rev. 649); untracked helper scripts unchanged; dev.db & node_modules consistent dengan Rev. 649 verifikasi. Rev. 646: PRD fresh verification & stability confirmation (cron run, 27 Oktober 2026 WIB); header Rev. 645→646; §11 compact changelog 116–645→116–646; §12 updated. Git HEAD `68957d618c491673527e214793280882ba3a675f` (Rev. 646 final commit); untracked helper scripts unchanged; dev.db & node_modules consistent dengan Rev. 646 verifikasi. Rev. 647: PRD fresh verification & stability confirmation (cron run, 27 Oktober 2026 WIB); header Rev. 646→647; §11 compact changelog 116–646→116–647; §12 updated. Git HEAD `68957d618c491673527e214793280882ba3a675f` (Rev. 646 final commit); untracked helper scripts unchanged; dev.db & node_modules consistent dengan Rev. 647 verifikasi. Rev. 648: PRD fresh verification & stability confirmation (cron run, 27 Oktober 2026 WIB); header Rev. 647→648; §11 compact changelog 116–647→116–648; §12 updated. Git HEAD `5923ef60d5d62e37bf31761d3b2f76b7ba5f03ae` (Rev. 647 final commit); untracked helper scripts unchanged; dev.db & node_modules consistent dengan Rev. 648 verifikasi. Rev. 650: PRD fresh verification & stability confirmation (cron run, 27 Oktober 2026 WIB); header Rev. 649→650; §11 compact changelog 116–649→116–650; §12 updated. Git HEAD `a5ca8a0` (Rev. 649 final commit); untracked helper scripts unchanged; dev.db & node_modules consistent dengan Rev. 650 verifikasi. Rev. 651: PRD fresh verification & stability confirmation (cron run, 27 Oktober 2026 WIB); header Rev. 650→651; §11 compact changelog 116–649→116–651; §12 updated. Git HEAD `234ad04` (Rev. 650 final commit); untracked helper scripts unchanged; dev.db & node_modules consistent dengan Rev. 651 verifikasi. Rev. 652: PRD fresh verification & stability confirmation (cron run, 27 Oktober 2026 WIB); header Rev. 651→652; §11 compact changelog 116–650→116–652; §12 updated. Git HEAD `234ad04` (Rev. 650 final commit); untracked helper scripts unchanged; dev.db & node_modules consistent dengan Rev. 652 verifikasi."
)

# Check what the actual content of line 986 is
import re
lines = s.split('\n')
print("=== Line 986 (index 985) ===")
print(repr(lines[985][:300]))
print("...")
print(repr(lines[985][-300:]))
print("Length:", len(lines[985]))
