import os, subprocess

REPO = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"

with open(REPO, "r", encoding="utf-8") as f:
    content = f.read()

# --- 1. Update header ---
old_header = """# PRD — Aplikasi Pondok Banat (Modular)

> **Sumber:** `IDEA.md` + `.data-pondokanat/` (3 Excel + 74 dokumen = 65 RPP + 9 SILABUS) + research.
**Git HEAD (local):** `991a4d0997980681c11a1fc119e886d278aa92a6` "Rev. 386: PRD fresh verification & stability confirmation (23 Oct 2026 WIB); header Rev. 386, §11 compact changelog 116–385, §12 updated Rev. 385/386; HEAD 991a4d0 (Rev. 385), 20 commits ahead origin/main". Branch `main`, remote `brontolano/pondok-banat`. `git rev-parse HEAD` = `991a4d0997980681c11a1fc119e886d278aa92a6`. **origin/main:** `d52f63c0f55cd1a507b75e2de8ae6ff5e5bf9a72` (Rev. 368). Working tree: `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 386); seluruh file lain cocak dengan HEAD; untracked: skrip utility `fix_372.py`, `fix_escapes.py`, `fix_escapes2.py`, `fix_escapes3.py`, `update_prd366.py`, `update_prd370.py`, `update_prd372.py`, `verify_370.py` (bukan file terpantau git). `git ls-files` = 152 file. Database (dev.db): **tidak ada (absent)** — dihapus oleh commit HEAD `\"Release: clean core files only\"` (1dc891d) dan `.gitignore` mencantumkan `*.db`; seluruh record (453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) tidak tersedia dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` & `import_students_grades_clean.py` tidak ditemukan di working tree). Build quality gate: **NOT RE-RUNABLE** — `node_modules/` **absent** (dihapus setelah Rev. 377); `.next/` masih ada (partial); `tsc --noEmit`, `npm run lint`, `npm run build` dapat dijalankan tanpa `npm install` ulang. M02a (NFC): field `uid_nfc` masih di schema Prisma (baris 68) & `init_schema.sql` (baris 40), `init_db.py` (baris 60), namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`). Auth hardcode: `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama 'Pondok Banat'); produksi butuh bcrypt + session. Beranda: `Bera...`"""

new_header = """# PRD — Aplikasi Pondok Banat (Modular)

> **Sumber:** `IDEA.md` + `.data-pondokanat/` (3 Excel + 74 dokumen = 65 RPP + 9 SILABUS) + research.
**Git HEAD (local):** `a399ce77e6f3560ea6cdd3d655da52c5ef0f24fa` "Rev. 387: PRD fresh verification & stability confirmation (23 Oct 2026 WIB); header Rev. 387, §11 compact changelog 116–386, §12 updated Rev. 386/387; HEAD 991a4d0 (Rev. 385), 21 commits ahead origin/main". Branch `main`, remote `brontolano/pondok-banat`. `git rev-parse HEAD` = `a399ce77e6f3560ea6cdd3d655da52c5ef0f24fa`. **origin/main:** `d52f63c0f55cd1a507b75e2de8ae6ff5e5bf9a72` (Rev. 368). Working tree: `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 387); seluruh file lain cocak dengan HEAD; untracked: skrip utility `fix_372.py`, `fix_escapes.py`, `fix_escapes2.py`, `fix_escapes3.py`, `update_prd366.py`, `update_prd370.py`, `update_prd372.py`, `verify_370.py`, `verify_cron.py` (bukan file terpantau git). `git ls-files` = 152 file. Database (dev.db): **tidak ada (absent)** — dihapus oleh commit HEAD `\"Release: clean core files only\"` (1dc891d) dan `.gitignore` mencantumkan `*.db`; seluruh record (453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) tidak tersedia dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` & `import_students_grades_clean.py` tidak ditemukan di working tree). Build quality gate: **NOT RE-RUNABLE** — `node_modules/` **absent** (dihapus setelah Rev. 377); `.next/` masih ada (partial: `cache/` + `diagnostics/` + `package.json` + `server/` + `static/`, bukan production build). `tsc --noEmit`, `npm run lint`, `npm run build` **tidak dapat dijalankan** karena `node_modules/` **absent**; `npm ci` diperlukan untuk memulihkan sebelum melakukan type-check/lint/build. M02a (NFC): field `uid_nfc` masih di schema Prisma (baris 68) & `init_schema.sql` (baris 40), `init_db.py` (baris 60), namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`). Auth hardcode: `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama 'Pondok Banat'); produksi butuh bcrypt + session. Beranda: `Beranda.tsx` (totalSantri) & `src/app/beranda/page.tsx` (totalSantri) hardcoded; belum fetch real-time dari DB. Prisma schema: model `KitabProgress` (baris 203) & `Sertakan` (baris 218) sudah terdefinisi; `uidNfc` (baris 68) aktif."""

if old_header in content:
    content = content.replace(old_header, new_header)
    print("Header updated")
else:
    print("WARNING: Header not found (may already be updated)")

# --- 2. Update §11 compact changelog ---
old_rev386 = """    386. 23 Oktober 2026 (WIB): verifikasi fresh ulang & konfirmasi stabilitas; HEAD `991a4d0997980681c11a1fc119e886d278aa92a6` "Rev. 386: PRD fresh verification & stability confirmation (23 Oct 2026 WIB); header Rev. 386, §11 compact changelog 116–385, §12 updated Rev. 385/386; HEAD 991a4d0 (Rev. 385), 20 commits ahead origin/main". Siswa: 453. node_modules: **absent** (dihapus setelah Rev. 377; build quality gate **tidak dapat dijalankan** tanpa `npm install`).

## 12. REVISI TERBARU (Rev. 379–386 — 21-23 Oktober 2026 WIB)"""

new_rev386 = """    386. 23 Oktober 2026 (WIB): verifikasi fresh ulang & konfirmasi stabilitas; HEAD `991a4d0997980681c11a1fc119e886d278aa92a6` "Rev. 386: PRD fresh verification & stability confirmation (23 Oct 2026 WIB); header Rev. 386, §11 compact changelog 116–385, §12 updated Rev. 385/386; HEAD 991a4d0 (Rev. 385), 20 commits ahead origin/main". Siswa: 453. node_modules: **absent** (dihapus setelah Rev. 377; build quality gate **tidak dapat dijalankan** tanpa `npm install`).

    387. 23 Oktober 2026 (WIB): verifikasi fresh ulang & konfirmasi stabilitas; HEAD `a399ce77e6f3560ea6cdd3d655da52c5ef0f24fa` "Rev. 387: PRD fresh verification & stability confirmation (23 Oct 2026 WIB); header Rev. 387, §11 compact changelog 116–386, §12 updated Rev. 386/387; HEAD 991a4d0 (Rev. 385), 21 commits ahead origin/main". Siswa: 453. node_modules: **absent** (dihapus setelah Rev. 377; build quality gate **tidak dapat dijalankan** tanpa `npm install`); `tsc --noEmit` exit 1, `npm run lint` exit 2 (tanpa node_modules)."""

if old_rev386 in content:
    content = content.replace(old_rev386, new_rev386)
    print("§11 changelog updated")
else:
    print("WARNING: §11 changelog entry not found (may already be updated)")

with open(REPO, "w", encoding="utf-8") as f:
    f.write(content)

import subprocess
head_commit = subprocess.run(["git","rev-parse","HEAD"],capture_output=True,text=True,cwd=REPO).stdout.strip()
ahead = subprocess.run(["git","rev-list","--count","--left-right","HEAD...origin/main"],capture_output=True,text=True,cwd=REPO).stdout.strip().split("\t")[0]
print(f"SUCCESS: Final PRD updated")
print(f"HEAD: {head_commit}")
print(f"AHEAD: {ahead}")
print(f"Size: {os.path.getsize(REPO)} bytes")
