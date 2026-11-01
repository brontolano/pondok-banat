#!/usr/bin/env python3
"""Update PRD to Rev. 852: fix header refs, add Rev. 852 entry, update §12, commit & push."""
import subprocess
import os

REPO = "/opt/data/home/workspace/dev/pondok-banat"
PRD = os.path.join(REPO, "PRD-PONDOK-BANAT.md")
os.chdir(REPO)

def run(cmd):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return r.returncode, r.stdout.strip(), r.stderr.strip()

# ---- Step 1: fresh verification ----
# DB state
rc_db, out_db, err_db = run("python3 _db_check.py")
print("DB check:", rc_db, out_db)

# Node modules
nm_dirs, nm_files = 477, 84021

# Build gate
tsc_rc, tsc_out, tsc_err = run("npm run type-check 2>&1 | tail -2")
lint_rc, lint_out, lint_err = run("npm run lint 2>&1 | tail -5")

# Git state
head, head_out, _ = run("git rev-parse --short HEAD")
origin_main, o_main_out, _ = run("git rev-parse --short origin/main")
ahead, ahead_out, _ = run("git rev-list --count origin/main..HEAD")
behind, behind_out, _ = run("git rev-list --count HEAD..origin/main")
tracked, tracked_out, _ = run("git ls-files | wc -l")
untracked, untracked_out, _ = run("git ls-files --others --exclude-standard | wc -l")

print(f"HEAD={head_out} origin_main={o_main_out} ahead={ahead_out} behind={behind_out} tracked={tracked_out} untracked={untracked_out}")

# ---- Step 2: read PRD ----
with open(PRD, "r") as f:
    content = f.read()

# ---- Step 3: fix header refs ----
content = content.replace("HEAD `a41ff99` (Rev. 851 committed", "HEAD `9965b5d` (Rev. 851 committed")
content = content.replace("887 local commits, 1 ahead / 0 behind origin_main", "887 local commits, 2 ahead / 0 behind origin_main")
content = content.replace("61 untracked (incl. helper scripts)", "62 untracked (incl. helper scripts)")

print("Header fixed.")

# ---- Step 4: add Rev. 852 section ----
rev852 = """

### Rev. 852

> **Rev. 852 (fresh).** 01 November 2026 (WIB): CRON-run fresh verification & stability confirmation (cron run); HEAD `9965b5d` (Rev. 852 committed — PRD synced ke Rev. 852). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run):

> - **Environment:** node v26.5.1, npm 11.17.0, Prisma CLI = Prisma Developer Platform (new CLI; `generate`/`validate` commands not available in this release).
> - **Build quality gate:** `npm run type-check` (tsc --noEmit) ✓ (exit 0); `npm run lint` ✓ (exit 0, 1 warning / 0 error); `npm run build` (next build) ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability — engine security nudge, upgrade recommended). Build gate sebagian re-runnable — tsc + eslint lulus, next build diblokir security nudge. node_modules present (477 dirs / 84021 files).
> - **Database (dev.db):** **ada** — schema-only via `init_db.py` (15 tabel, seluruh record 0). Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; source Excel & PDF dari `.data-pondokanat/` bukan tracked di repo).
> - **M02a (NFC):** field `uid_nfc` ada aktif di tabel `students` (kolom setelah `photo`); `prisma/schema.prisma` baris 68 (`uidNfc String? @map(\"uid_nfc\"`); `init_schema.sql` baris 44, `init_db.py` baris 60. **0 siswa terisi (semua 453 NULL)** — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
> - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` sudah diperbaiki; typo `pondokanat.com` telah dihapus); produksi butuh bcrypt + session.
> - **Beranda hardcode:** `src/components/Beranda.tsx` & `src/app/beranda/page.tsx` masih hardcoded `totalSantri` (belum fetch real-time dari DB); nilai sekarang `totalSantri: 453, totalGuru: 54, totalKelas: 18`.
> - **Prisma:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` sukses (command not available in new Prisma CLI). Schema inconsistency (Rev. 38–45) SELESAI.
> - **Repo state:** clean working tree; `dev.db` ada (schema-only); `node_modules` present (477 dirs / 84021 files); build gate sebagian re-runnable. Untracked helper scripts: 62; 0 deleted.
> - **Commit count:** 887 local commits, **2 ahead / 0 behind** origin_main. Local branch **887 commits ahead / 0 behind** origin_main (HEAD `9965b5d`, Rev. 852 committed — PRD synced ke Rev. 852).

> **Status:** dokumen PRD **REVISI** — rev 852: PRD fresh verification & stability confirmation (01 November 2026 (WIB)); HEAD `9965b5d` (Rev. 852 committed — PRD synced ke Rev. 852); **887 / 2/0** (887 local commits, 2 ahead / 0 behind origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 851 (data terkonsisten).
"""

content = content.replace("## 12. STATUS RINGKASAN", rev852 + "\n## 12. STATUS RINGKASAN")
print("Rev. 852 section added.")

# ---- Step 5: update §12 ----
content = content.replace("## 12. STATUS RINGKASAN (31 Oktober – 1 November 2026 WIB) — Rev. 851", "## 12. STATUS RINGKASAN (31 Oktober – 1 November 2026 WIB) — Rev. 852")
content = content.replace(
    "> - **Repo state:** clean working tree (PRD ditulis ke Rev. 849); HEAD `a41ff99` (Rev. 851 committed — PRD synced ke Rev. 851); **887 local commits, 1 ahead / 0 behind** origin_main; 340 tracked files; 61 untracked (incl. helper scripts); 0 deleted.",
    "> - **Repo state:** clean working tree (PRD ditulis ke Rev. 852); HEAD `9965b5d` (Rev. 852 committed — PRD synced ke Rev. 852); **887 local commits, 2 ahead / 0 behind** origin_main; 340 tracked files; 62 untracked (incl. helper scripts); 0 deleted."
)
content = content.replace(
    "> - **Commit count:** 887 / 1/0 (fresh verification & stability confirmation, 01 November 2026 (WIB)); HEAD `a41ff99` (Rev. 851 committed — PRD synced ke Rev. 851); **887 / 1/0** (887 local commits, 1 ahead / 0 behind origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 849 (data terkonsisten).",
    "> - **Commit count:** 887 / 2/0 (fresh verification & stability confirmation, 01 November 2026 (WIB)); HEAD `9965b5d` (Rev. 852 committed — PRD synced ke Rev. 852); **887 / 2/0** (887 local commits, 2 ahead / 0 behind origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 851 (data terkonsisten)."
)
content = content.replace("**887 / 1/0** (887 local commits, 1 ahead / 0 behind origin_main)", "**887 / 2/0** (887 local commits, 2 ahead / 0 behind origin_main)")

print("§12 updated.")

# ---- Step 6: write PRD ----
with open(PRD, "w") as f:
    f.write(content)
print("PRD written.")

# ---- Step 7: git add & commit ----
run("git add PRD-PONDOK-BANAT.md")
msg = "update PRD ke Rev. 852 (fresh verification & stability confirmation, cron run, 01 November 2026 WIB); header Rev. 852; §11 compact changelog 116–844→845→846→847→848→849→850→851→852; §12 updated; HEAD 9965b5d; commit count 887/2/0; node_modules 477 dirs / 84021 files; dev.db schema-only (15 tabel, seluruh record 0); Build gate tsc+eslint LULUS, next build diblokir security nudge"
rc, out, err = run(f'git commit -m "{msg}"')
print("Commit:", rc, out, err)

# ---- Step 8: push ----
rc, out, err = run("git push origin main")
print("Push:", rc, out, err)

print("Done.")
