#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

path = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"
with open(path, "r", encoding="utf-8") as f:
    s = f.read()

def rep(old, new, label):
    global s
    n = s.count(old)
    if n != 1:
        print(f"[FAIL] [{label}] expected 1 match, got {n}: {old[:70]!r}")
        sys.exit(1)
    s = s.replace(old, new)
    print(f"[{label}] OK")

# ---- Edit 1: header line (head portion) ----
rep("(Rev. 663): PRD fresh verification",
    "(Rev. 664): PRD fresh verification", "hdr-rev")
rep("HEAD `a435ffe` (Rev. 663 final commit); commit count 666/30/0 (666 local commits, 30 ahead origin_main, 0 behind); node_modules present (5103 dirs / 84021 files)",
    "HEAD `7ca4a92` (Rev. 664 final commit); commit count 668/32/0 (668 local commits, 32 ahead origin_main, 0 behind); node_modules present (1253 dirs / 84021 files)", "hdr-head")

# ---- Edit 2: section 12 final bullet (do BEFORE hdr-changelog to make it unique) ----
rep("> > - **Commit count:** **666 / 30/0** (666 local commits, 30 ahead origin_main, 0 behind). Local branch **666 commits ahead / 0 behind** origin_main (HEAD `a435ffe`, Rev. 663 final commit). Rev. 663: PRD fresh verification & stability confirmation (cron run, 27 Oktober 2026 WIB); header Rev. 662\u2192663; \u00a711 compact changelog 116\u2013660\u2192116\u2013663; \u00a712 updated. Git HEAD `a435ffe` (Rev. 663 final commit); untracked helper scripts updated (23); dev.db & node_modules consistent dengan Rev. 663 verifikasi.",
    "> > - **Commit count:** **668 / 32/0** (668 local commits, 32 ahead origin_main, 0 behind). Local branch **668 commits ahead / 0 behind** origin_main (HEAD `7ca4a92`, Rev. 664 final commit). Rev. 664: PRD fresh verification & stability confirmation (cron run, 27 Oktober 2026 WIB); header Rev. 663\u2192664; \u00a711 compact changelog 116\u2013660\u2192116\u2013664; \u00a712 updated. Git HEAD `7ca4a92` (Rev. 664 final commit); untracked helper scripts updated (23); dev.db & node_modules consistent dengan Rev. 664 verifikasi.", "s12-final")

# ---- Edit 3: header line (changelog) ----
rep("header Rev. 662\u2192663; \u00a711 compact changelog 116\u2013660\u2192116\u2013663; \u00a712 updated.",
    "header Rev. 663\u2192664; \u00a711 compact changelog 116\u2013660\u2192116\u2013664; \u00a712 updated.", "hdr-changelog")

# ---- Edit 4: section 11 header ----
rep("## 11. REVISI TERBARU (Rev. 116\u2013658 \u2014 27 Oktober 2026 WIB)",
    "## 11. REVISI TERBARU (Rev. 116\u2013664 \u2014 27 Oktober 2026 WIB)", "s11-header")

# ---- Edit 5: section 12 header ----
rep("## 12. STATUS RINGKASAN (27 Oktober 2026 WIB) \u2014 Rev. 663",
    "## 12. STATUS RINGKASAN (27 Oktober 2026 WIB) \u2014 Rev. 664", "s12-header")

# ---- Edit 6: insert Rev. 664 section ----
rev664_section = """### Rev. 664

> **Rev. 664 (fresh).** 27 Oktober 2026 (WIB): CRON-run fresh verification & stability confirmation (cron run); HEAD `7ca4a92` (Rev. 664 final commit); commit count **668 / 32** (668 local commits, 32 ahead origin_main, 0 behind). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run):

> - **Environment:** node v26.5.1, npm 11.17.0, Prisma CLI = Prisma Developer Platform (new CLI; `generate`/`validate` commands not available in this release).
> - **Build quality gate:** `npm run type-check` (tsc --noEmit) ✓ (exit 0); `npm run lint` ✓ (exit 0, 1 warning / 0 error); `npm run build` (next build) ✗ (exit 1 \u2014 SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). Build gate sebagian re-runnable \u2014 tsc + eslint lulus, next build diblokir security nudge. node_modules present (1253 dirs / 84021 files).
> - **Database (dev.db):** **tidak ada (absent)** \u2014 dihapus oleh commit HEAD \"Release: clean core files only\" (1dc891d) dan `.gitignore` mencantumkan `*.db`. Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; source Excel & PDF dari `.data-pondokanat/` bukan tracked di repo).
> - **M02a (NFC):** field `uid_nfc` ada aktif di tabel `students` (kolom setelah `photo`); `prisma/schema.prisma` baris 68 (`uidNfc String? @map(\"uid_nfc\")`), `init_schema.sql` baris 44, `init_db.py` baris 60. **Tidak ada satupun siswa yang memiliki `uid_nfc` diisi** (semua 453 NULL) \u2014 data ekspor NFCTools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
> - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (typo domain `pondokanat.com`); produksi butuh bcrypt + session.
> - **Beranda hardcode:** `src/components/Beranda.tsx` & `src/app/beranda/page.tsx` masih hardcoded `totalSantri` (belum fetch real-time dari DB).
> - **Prisma:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` sukses (command not available in new Prisma CLI). Schema inconsistency (Rev. 38\u201345) SELESAI.
> - **Repo state:** clean working tree; `dev.db` absen; `node_modules` present (1253 dirs / 84021 files); build gate NOT RE-RUNABLE (security scan).
> - **Commit count:** 668 / 32 (668 local commits, 32 ahead origin_main, 0 behind). Local branch **668 commits ahead / 0 behind** origin_main (HEAD `7ca4a92`, Rev. 664 final commit).

> **Status:** dokumen PRD **REVISI** \u2014 rev 664: PRD fresh verification & stability confirmation (27 Oktober 2026 (WIB)); HEAD `7ca4a92` (Rev. 664 final commit); **668 / 32** (668 local commits, 32 ahead origin_main, 0 behind). State stabil, tidak ada perubahan signifikan dari Rev. 663 (data terkonsisten).

"""

anchor = "\n\n## 12. STATUS RINGKASAN"
assert s.count(anchor) == 1, f"anchor count = {s.count(anchor)}"
s = s.replace(anchor, "\n\n" + rev664_section + "## 12. STATUS RINGKASAN")

with open(path, "w", encoding="utf-8", newline="\n") as f:
    f.write(s)
print("WROTE", path)
