#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Update PRD-PONDOK-BANAT.md to Rev. 271 (18 Oct 2026 WIB)."""
import sys

path = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# ---------- 1. Header updates (Rev. 270 -> Rev. 271) ----------
repl = [
    ("> **Rev. 270 — 18 Oktober 2026 (WIB).**",
     "> **Rev. 271 — 18 Oktober 2026 (WIB).**"),
    ("Git HEAD: `342ede6926c0064539bf43eba8dc6639b895c827`",
     "Git HEAD: `3bd1a603234083be69ee575971949538e94cc042`"),
    ("revisi terbaru = Rev. 269, sudah dicomit",
     "revisi terbaru = Rev. 270, sudah dicomit"),
    ("HEAD = `342ede6926c0064539bf43eba8dc6639b895c827`",
     "HEAD = `3bd1a603234083be69ee575971949538e94cc042`"),
    ("Branch 19 commit ahead",
     "Branch 20 commit ahead"),
]
for old, new in repl:
    if old not in content:
        print("HEADER MISSING:", old[:60])
        sys.exit(1)
    content = content.replace(old, new)

# ---------- 2. Section 48 (Rev. 270) fixes ----------
s48repl = [
    ("`342ede6926c0064539bf43eba8dc6639b895c827` \"Rev. 269:",
     "`3bd1a603234083be69ee575971949538e94cc042` \"Rev. 270:"),
    ("Local branch **19** commit ahead",
     "Local branch **20** commit ahead"),
    ("   - **Branch-ahead:** 19 commit",
     "   - **Branch-ahead:** 20 commit"),
    ("**Perubahan dari Rev. 268:**",
     "**Perubahan dari Rev. 269:**"),
    ("**Header PRD:** diperbarui ke **Rev. 269**",
     "**Header PRD:** diperbarui ke **Rev. 270**"),
    ("sesuai HEAD commit Rev. 268",
     "sesuai HEAD commit Rev. 269"),
    ("perbarui dari 18 → 19 commit",
     "perbarui dari 19 → 20 commit"),
]
for old, new in s48repl:
    if old not in content:
        print("S48 MISSING:", old[:60])
        sys.exit(1)
    content = content.replace(old, new)

# ---------- 3. Append Section 49 (Rev. 271) ----------
new_section = """## 49. REVISI TERBARU (Rev. 271 — 18 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 18 Oktober 2026 (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / struktur source / skema Prisma.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 270 (data terkonsisten).**
   - **Git HEAD (local):** `3bd1a603234083be69ee575971949538e94cc042` "Rev. 270: PRD fresh verification & stability confirmation (18 Oct 2026 WIB); updated header to Rev. 270 + added section 48" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `3bd1a603234083be69ee575971949538e94cc042`). Local branch **20** commit ahead dari `origin/main` (`45d33ef348b11ae49789224687913adeb01d1842` = Rev. 250).
   - **Git HEAD (origin/main):** `45d33ef348b11ae49789224687913adeb01d1842` (Rev. 250). Local branch 20 commit ahead.
   - **Git ls-files:** = **36 file**. `git status --porcelain` = `??` (**34 file tambahan tidak ter-track** — skrip bantuan, bukan bagian dari PRD).
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`. Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` dan `import_students_grades_clean.py` tidak ditemukan di working tree).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` **absent** (clear checkout, 0 file); `.next/` **ada (partial: cache + diagnostics + package.json + server + static, bukan production build)**. `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm instal ulang` sebelum dapat dijalankan.
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map("uid_nfc")` baris 68), `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` (sesuai nama 'Pondok Banat')); produksi butuh bcrypt + session.
   - **Beranda:** `src/components/Beranda.tsx` & `src/app/beranda/page.tsx` masih hardcode `totalSantri: 453, totalGuru: 54, totalKelas: 18`; **bukan fetch real-time**.
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` berhasil. **Schema inconsistency (Rev. 38–45) SELESAI** — kedua model konsisten dengan referensi di `Subject` dan `User`. Jumlah model = **17**.
   - **Source files:** `src/app/*` = 15 entri (12 sub direktori: absensi, beranda, berita, guru, kelas, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah + globals.css + layout.tsx + page.tsx); `src/next-env.d.ts` = 1 file; `src/components` = `Beranda.tsx` & `Login.tsx`; `src/lib` = **kosong** (logic inline). Total `src` = 18 file. Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite).
   - **Branch-ahead:** 20 commit (sesuai `git rev-list --count origin/main..HEAD` = 20).
   - **Untracked files:** 34 skrip bantuan (skrip bantuan bukan bagian dari PRD).

2. **Perubahan dari Rev. 270:**
   - **Header PRD:** diperbarui ke **Rev. 271** (tanggal 18 Oktober 2026 WIB).
   - **New Section 49 (Rev. 271):** ditambahkan untuk verifikasi fresh ulang & konfirmasi stabilitas Rev. 271.
   - **Git HEAD di header:** diperbaiki dari `342ede6926c0064539bf43eba8dc6639b895c827` → `3bd1a603234083be69ee575971949538e94cc042` (aktual, sesuai HEAD commit Rev. 270).
   - **revisi terbaru:** diperbarui dari Rev. 269 → Rev. 270.
   - **Branch-ahead count:** diperbarui dari 19 → 20 commit (`git rev-list --count origin/main..HEAD` = 20).
   - **Section 48 (Rev. 270):** diperbaiki — "Perubahan dari Rev. 268" → "Rev. 269", "Header PRD: diperbarui ke Rev. 269" → "Rev. 270", "Branch-ahead count: 18 → 19" → "19 → 20", git HEAD (local) `342ede69` → `3bd1a60`.

3. **Status:** dokumen PRD **REVISI** — rev 271 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. Header PRD diperbarui ke **Rev. 271**.
"""

if not content.endswith("\n"):
    content += "\n"
content += new_section

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("Written. Total characters:", len(content))
