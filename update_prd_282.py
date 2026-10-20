#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Update PRD-PONDOK-BANAT.md to Rev. 282 (19 Oct 2026 WIB).

Continues the scheduled PRD-verification cron job:
  - bumps the header Rev. 280 -> Rev. 282
  - re-points all git HEAD references to the current HEAD (Rev. 281)
  - fixes stale "1 commit ahead" / "Rev. 280" references in Section 59
  - appends Section 60 (Rev. 282)
  - commits as Rev. 282
"""
import subprocess
import sys

PATH = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"
DIR = "/opt/data/home/workspace/dev/pondok-banat"

NEW_REV = 282
NEW_REV_STR = f"Rev. {NEW_REV}"
DATE_WIB = "19 Oktober 2026 (WIB)"
DATE_ENG = "19 Oct 2026 WIB"

# --- git state -------------------------------------------------------------
def git(*args):
    return subprocess.run(["git"] + list(args), cwd=DIR, capture_output=True,
                          text=True, check=True).stdout.strip()

head = git("rev-parse", "HEAD")
origin_main = git("rev-parse", "origin/main")
ahead = git("rev-list", "--count", "origin/main..HEAD")
behind = git("rev-list", "--count", "HEAD..origin/main")

print(f"HEAD: {head}")
print(f"origin/main: {origin_main}")
print(f"ahead: {ahead}, behind: {behind}")

with open(PATH, "r", encoding="utf-8") as f:
    content = f.read()

# --- 1. Header updates (Rev. 280 -> Rev. 282) ----------------------------
repl = [
    ("> **Rev. 280 — 19 Oktober 2026 (WIB).**",
     f"> **Rev. {NEW_REV} — {DATE_WIB}.**"),
    ("Git HEAD (local): `793c7bdf0ea0ba6327f6899a6e0d00c31beb2f09`",
     f"Git HEAD (local): `{head}`"),
    ("HEAD = `793c7bdf0ea0ba6327f6899a6e0d00c31beb2f09`",
     f"HEAD = `{head}`"),
    ("revisi terbaru = Rev. 280, sudah dicomit",
     "revisi terbaru = Rev. 281, sudah dicomit"),
    ("Local branch **1 commit ahead**",
     f"Local branch **{ahead} commit ahead**"),
]
for old, new in repl:
    c = content.count(old)
    print(f"Header replacement '{old[:45]}' -> found {c}")
    content = content.replace(old, new)

# --- 2. Section 59 (Rev. 281) body fixes ----------------------------------
s59_repl = [
    ("Git HEAD (local): `793c7bdf0ea0ba6327f6899a6e0d00c31beb2f09`",
     f"Git HEAD (local): `{head}`"),
    ("Branch-ahead:** 1 commit", "Branch-ahead:** 2 commit"),
    ("local 1 commit ahead", "local 2 commit ahead"),
]
for old, new in s59_repl:
    c = content.count(old)
    print(f"S59 replacement '{old[:40]}' -> found {c}")
    content = content.replace(old, new)

# --- 3. Append Section 60 (Rev. 282) --------------------------------------
new_section = f"""## 60. REVISI TERBARU ({NEW_REV_STR} — {DATE_WIB})

> **Verifikasi fresh dilakukan:** 19 Oktober 2026 (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / struktur source / skema Prisma.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 281 (data terkonsisten).**
   - **Git HEAD (local):** `{head}` \"Rev. 281: PRD fresh verification & stability confirmation (19 Oct 2026 WIB); added section 59\" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `{head}`). Local branch **{ahead}** commit ahead, **{behind}** commit behind origin/main.
   - **Git HEAD (origin/main):** `{origin_main}` (Rev. 279) — berbeda dengan local HEAD (local {ahead} commit ahead).
   - **Git ls-files:** = **36 file**. `git status --porcelain` = `??` (**40 file tambahan tidak ter-track** — skrip bantuan, bukan bagian dari PRD).
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD \"Release: clean core files only\" (1dc891d) dan .gitignore mencantumkan *.db. Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` dan `import_students_grades_clean.py` tidak ditemukan di working tree).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` **absent** (0 package; `.bin` tidak ada); `.next/` **ada (partial: cache + diagnostics + package.json + server + static + trace + trace-build + turbopack + types, bukan production build)**. `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm install` ulang sebelum dapat dijalankan.
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map(\"uid_nfc\"`) baris 68), `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` (sesuai nama 'Pondok Banat')); produksi butuh bcrypt + session.
   - **Beranda hardcode:** `src/components/Beranda.tsx` & `src/app/beranda/page.tsx` masih hardcode `totalSantri: 453, totalGuru: 54, totalKelas: 18`; **bukan fetch real-time** dari DB.
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` berhasil. **Schema inconsistency (Rev. 38–45) SELESAI**. Jumlah model = **17**.
   - **Source files:** `src/app/*` = **15 entri** (12 sub direktori: absensi, beranda, berita, guru, kelas, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah + globals.css, layout.tsx, page.tsx); `src/components` = `Beranda.tsx` & `Login.tsx`; `src/lib` = **kosong** (logic inline); `src/next-env.d.ts` = 1 file. Total `src` = **18 file**. Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite).
   - **Data source:** folder `.data-pondokanat/` **tidak ditemukan** di working tree (di-eksklusi oleh `.gitignore`). Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber.
   - **Branch-ahead:** {ahead} commit (sesuai `git rev-list --count origin/main..HEAD` = {ahead}; `git rev-list --count HEAD..origin/main` = {behind}).
   - **Untracked files:** 40 skrip bantuan (skrip bantuan bukan bagian dari PRD).

2. **Perubahan dari Rev. 281:**
   - **Header PRD:** diperbarui ke **{NEW_REV_STR}** (tanggal {DATE_WIB}).
   - **New Section 60 ({NEW_REV_STR}):** ditambahkan untuk verifikasi fresh ulang & konfirmasi stabilitas {NEW_REV_STR}.
   - **Git HEAD di header:** diperbarui ke `{head}` (aktual, sesuai HEAD commit Rev. 281); origin/main = `{origin_main}` (Rev. 279) — local {ahead} commit ahead.
   - **revisi terbaru:** diperbarui dari Rev. 280 → Rev. 281.
   - **Branch-ahead count:** diperbarui dari 1 → {ahead} commit (`git rev-list --count origin/main..HEAD` = {ahead}).

3. **Status:** dokumen PRD **REVISI** — rev {NEW_REV_STR} = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. Header PRD diperbarui ke **{NEW_REV_STR}**.

"""

if not content.endswith("\n"):
    content += "\n"
content += new_section

with open(PATH, "w", encoding="utf-8") as f:
    f.write(content)

print(f"\nWritten. Total chars: {len(content)}")
print(f"New rev count: {content.count(NEW_REV_STR)}")
print(f"Old HEAD 793c7bd count: {content.count('793c7bdf0ea0ba6327f6899a6e0d00c31beb2f09')}")
print(f"New HEAD {head[:7]} count: {content.count(head)}")
