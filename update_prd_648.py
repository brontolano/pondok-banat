import io

path = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"
s = io.open(path, encoding="utf-8").read()

# --- Replacements for header (line 4) ---
repl1_old = "(Rev. 647): PRD fresh verification & stability confirmation (cron run, 27 Oktober 2026 WIB); header Rev. 646→647; §11 compact changelog 116–646→116–647; §12 updated. HEAD 68957d618c491673527e214793280882ba3a675f (Rev. 646 final commit); commit count 651/15/0 (651 local commits, 15 ahead origin_main, 0 behind); node_modules present (5103 dirs / 84,021 files); dev.db absent (removed by HEAD \"Release: clean core files only\"); build gate: tsc ✓ (exit 0), eslint ✓ (1 warning / 0 error), next build ✗ (blocked by security scan — NOT RE-RUNABLE). Working tree: PRD-PONDOK-BANAT.md cocak dengan HEAD (revisi terbaru = Rev. 647); seluruh file lain cocak dengan HEAD; untracked: 15 (...); git ls-files = 268 files."

repl1_new = "(Rev. 648): PRD fresh verification & stability confirmation (cron run, 27 Oktober 2026 WIB); header Rev. 647→648; §11 compact changelog 116–647→116–648; §12 updated. HEAD 5923ef60d5d62e37bf31761d3b2f76b7ba5f03ae (Rev. 647 final commit); commit count 652/16/0 (652 local commits, 16 ahead origin_main, 0 behind); node_modules present (5103 dirs / 84,021 files); dev.db absent (removed by HEAD \"Release: clean core files only\"); build gate: tsc ✓ (exit 0), eslint ✓ (1 warning / 0 error), next build ✗ (blocked by security scan — NOT RE-RUNABLE). Working tree: PRD-PONDOK-BANAT.md cocak dengan HEAD (revisi terbaru = Rev. 648); seluruh file lain cocak dengan HEAD; untracked: 15 (...); git ls-files = 268 files."

c1 = s.count(repl1_old)
print("repl1 count:", c1)
assert c1 == 1, "header replacement target not unique"
s = s.replace(repl1_old, repl1_new)

# --- Replacement: add Rev. 648 section after Rev. 647 section ---
anchor = "> - **Status:** dokumen PRD **REVISI** — rev 647: PRD fresh verification & stability confirmation (27 Oktober 2026 (WIB)); HEAD `68957d618c491673527e214793280882ba3a675f` (Rev. 646 final commit); **651 / 15** (651 local commits, 15 ahead origin_main, 0 behind). State stabil, tidak ada perubahan signifikan (data terkonsisten) dari Rev. 646."

rev648_section = (
    "\n### Rev. 648\n\n"
    "> **Rev. 648 (fresh).** 27 Oktober 2026 (WIB): CRON-run fresh verification & stability confirmation (cron run); HEAD `5923ef60d5d62e37bf31761d3b2f76b7ba5f03ae` (Rev. 647 final commit); commit count **652 / 16** (652 local commits, 16 ahead origin_main, 0 behind). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run):\n"
    "\n"
    "> - **Environment:** node v26.5.1, npm 11.17.0, Prisma CLI = Prisma Developer Platform (new CLI; `generate`/`validate` commands not available in this release).\n"
    "> - **Build quality gate:** `npm run type-check` (tsc --noEmit) ✓ (exit 0); `npm run lint` ✓ (exit 0, 1 warning / 0 error); `npm run build` (next build) ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). Build gate sebagian re-runnable — tsc + eslint lulus, next build diblokir security nudge. node_modules present (5103 dirs / 84,021 files).\n"
    "> - **Database (dev.db):** **tidak ada (absent)** — dihapus oleh commit HEAD \"Release: clean core files only\" (1dc891d) dan `.gitignore` mencantumkan `*.db`. Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; source Excel & PDF dari `.data-pondokanat/` bukan tracked di repo).\n"
    "> - **M02a (NFC):** field `uid_nfc` ada aktif di tabel `students` (kolom setelah `photo`); `prisma/schema.prisma` baris 68 (`uidNfc String? @map(\"uid_nfc\")`), `init_schema.sql` baris 44, `init_db.py` baris 60. **Tidak ada satupun siswa yang memiliki `uid_nfc` diisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).\n"
    "> - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (typo domain `pondokanat.com`); produksi butuh bcrypt + session.\n"
    "> - **Beranda hardcode:** `src/components/Beranda.tsx` & `src/app/beranda/page.tsx` masih hardcoded `totalSantri` (belum fetch real-time dari DB).\n"
    "> - **Prisma:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` sukses (command not available in new Prisma CLI). Schema inconsistency (Rev. 38–45) SELESAI.\n"
    "> - **Repo state:** clean working tree; `dev.db` absent; `node_modules` present (5103 dirs / 84,021 files); build gate NOT RE-RUNABLE (security scan).\n"
    "> - **Commit count:** 652 / 16 (652 local commits, 16 ahead origin_main, 0 behind). Local branch **652 commits ahead / 0 behind** origin_main.\n"
    "> - **Status:** dokumen PRD **REVISI** — rev 648: PRD fresh verification & stability confirmation (27 Oktober 2026 (WIB)); HEAD `5923ef60d5d62e37bf31761d3b2f76b7ba5f03ae` (Rev. 647 final commit); **652 / 16** (652 local commits, 16 ahead origin_main, 0 behind). State stabil, tidak ada perubahan signifikan (data terkonsisten) dari Rev. 647."
)

c2 = s.count(anchor)
print("rev648 anchor count:", c2)
assert c2 == 1, "rev648 anchor not unique"
s = s.replace(anchor, anchor + rev648_section)

# --- Replacement for §12 status line ---
repl3_old = "**Commit count:** **651 / 15/0** (651 local commits, 15 ahead origin_main, 0 behind). Local branch **651 commits ahead / 0 behind** origin_main (HEAD `68957d618c491673527e214793280882ba3a675f`, Rev. 646 final commit). Rev. 646: PRD fresh verification & stability confirmation (cron run, 27 Oktober 2026 WIB); header Rev. 645→646; §11 compact changelog 116–645→116–646; §12 updated. Git HEAD `68957d618c491673527e214793280882ba3a675f` (Rev. 646 final commit); untracked helper scripts unchanged; dev.db & node_modules consistent with Rev. 646 verification. Rev. 647: PRD fresh verification & stability confirmation (cron run, 27 Oktober 2026 WIB); header Rev. 646→647; §11 compact changelog 116–646→116–647; §12 updated. Git HEAD `68957d618c491673527e214793280882ba3a675f` (Rev. 646 final commit); untracked helper scripts unchanged; dev.db & node_modules consistent with Rev. 647 verification."

repl3_new = "**Commit count:** **652 / 16/0** (652 local commits, 16 ahead origin_main, 0 behind). Local branch **652 commits ahead / 0 behind** origin_main (HEAD `5923ef60d5d62e37bf31761d3b2f76b7ba5f03ae`, Rev. 647 final commit). Rev. 646: PRD fresh verification & stability confirmation (cron run, 27 Oktober 2026 WIB); header Rev. 645→646; §11 compact changelog 116–645→116–646; §12 updated. Git HEAD `68957d618c491673527e214793280882ba3a675f` (Rev. 646 final commit); untracked helper scripts unchanged; dev.db & node_modules consistent with Rev. 646 verification. Rev. 647: PRD fresh verification & stability confirmation (cron run, 27 Oktober 2026 WIB); header Rev. 646→647; §11 compact changelog 116–646→116–647; §12 updated. Git HEAD `68957d618c491673527e214793280882ba3a675f` (Rev. 646 final commit); untracked helper scripts unchanged; dev.db & node_modules consistent with Rev. 647 verification. Rev. 648: PRD fresh verification & stability confirmation (cron run, 27 Oktober 2026 WIB); header Rev. 647→648; §11 compact changelog 116–647→116–648; §12 updated. Git HEAD `5923ef60d5d62e37bf31761d3b2f76b7ba5f03ae` (Rev. 647 final commit); untracked helper scripts unchanged; dev.db & node_modules consistent with Rev. 648 verification."

c3 = s.count(repl3_old)
print("repl3 count:", c3)
assert c3 == 1, "§12 replacement target not unique"
s = s.replace(repl3_old, repl3_new)

# --- Write back ---
io.open(path, "w", encoding="utf-8").write(s)
print("File written successfully")

# --- Verify header line ---
lines = s.split("\n")
print("=== HEADER (line 4) ===")
print(lines[3])
print("=== §12 tail (last line) ===")
print(lines[-1])
print("=== Rev. 648 section present ===")
print("### Rev. 648" in s)
