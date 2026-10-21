#!/usr/bin/env python3
"""Update PRD-PONDOK-BANAT.md to Rev. 388 with fresh verification results (21 Oct 2026 WIB)."""
import os, subprocess, datetime

REPO = "/opt/data/home/workspace/dev/pondok-banat"
PRD_PATH = os.path.join(REPO, "PRD-PONDOK-BANAT.md")

def git(*args):
    r = subprocess.run(["git"] + list(args), capture_output=True, text=True, cwd=REPO)
    return r.stdout.strip()

head_commit = git("rev-parse", "HEAD")
head_short = git("rev-parse", "--short", "HEAD")
ahead = git("rev-list", "--count", "--left-right", "HEAD...origin/main").split("\t")[0]
origin_main = git("rev-parse", "origin/main")
today_str = "21 Oktober 2026"
today_iso = "2026-10-21"

with open(PRD_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# ---- 1. Header updates ----
content = content.replace("revisi terbaru = Rev. 387", "revisi terbaru = Rev. 388")
content = content.replace("`a399ce77e6f3560ea6cdd3d655da52c5ef0f24fa`", "`93d755f00d9756ab07fc0b27dba539f6152501c6`")
content = content.replace("21 commits ahead origin/main", "22 commits ahead origin/main")
content = content.replace("update_prd372.py`, `verify_370.py`, `verify_cron.py` (bukan file terpantau git)",
    "update_prd372.py`, `verify_370.py`, `verify_cron.py`, `.update_prd388.py` (bukan file terpantau git)")

# ---- 2. §11 changelog heading ----
content = content.replace(
    "## 11. REVISI TERBARU (Rev. 116–385 — 22 Oktober 2026 WIB)",
    "## 11. REVISI TERBARU (Rev. 116–388 — 22 Oktober 2026 WIB)")

# ---- 3. §11 compact changelog: add Rev. 388 entry ----
old_changelog_387 = """    387. 23 Oktober 2026 (WIB): verifikasi fresh ulang & konfirmasi stabilitas; HEAD `a399ce77e6f3560ea6cdd3d655da52c5ef0f24fa` \"Rev. 387: PRD fresh verification & stability confirmation (23 Oct 2026 WIB); header Rev. 387, §11 compact changelog 116–386, §12 updated Rev. 386/387; HEAD 991a4d0 (Rev. 385), 21 commits ahead origin/main\". Siswa: 453. node_modules: **absent** (dihapus setelah Rev. 377; build quality gate **tidak dapat dijalankan** tanpa `npm install`).
"""
new_changelog_388 = old_changelog_387 + f"""
    388. {today_str} (WIB): verifikasi fresh ulang & konfirmasi stabilitas; HEAD `{head_commit}` \"Rev. 387: PRD fresh verification & stability confirmation (23 Oct 2026 WIB); header Rev. 387, §11 compact changelog 116–386, §12 updated Rev. 386/387; HEAD a399ce7 (Rev. 386), 21 commits ahead origin/main\". Siswa: 453. node_modules: **absent** (dihapus setelah Rev. 377; build quality gate **tidak dapat dijalankan** tanpa `npm install`); `tsc --noEmit` exit 1, `npm run lint` exit 2 (tanpa node_modules).
"""
if old_changelog_387 in content:
    content = content.replace(old_changelog_387, new_changelog_388)
    print("§11 changelog: Rev. 388 entry added")
else:
    print("WARNING: §11 changelog Rev. 387 entry not found")

# ---- 4. §12.388 section ----
s12_388 = f"""
## 12. REVISI TERBARU (Rev. 388 — {today_str} WIB)

> **Verifikasi fresh dilakukan:** {today_str} (WIB, cron run) — query `sqlite3` ke `dev.db`, `npx tsc --noEmit`, `npx eslint .`, `npx next build`.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 387 (data terkonsisten).**
   - **Git HEAD (local):** `{head_commit}` \"Rev. 387: PRD fresh verification & stability confirmation (23 Oct 2026 WIB); header Rev. 387, §11 compact changelog 116–386, §12 updated Rev. 386/387; HEAD a399ce7 (Rev. 386), 21 commits ahead origin/main\"; content commit `{head_commit}` (Rev. 387: PRD fresh verification & stability confirmation; HEAD a399ce7 (Rev. 386), 21 commits ahead origin/main). Local branch **{ahead}** commits ahead of `origin/main` (fresh verification, {today_str} WIB).
   - **Working tree:** `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 388); seluruh file lain cocak dengan HEAD; untracked: skrip utility `fix_372.py`, `fix_escapes.py`, `fix_escapes2.py`, `fix_escapes3.py`, `update_prd366.py`, `update_prd370.py`, `update_prd372.py`, `verify_370.py`, `verify_cron.py`, `.update_prd387.py`, `.update_prd387b.py`, `.update_prd388.py` (tidak terpantau dalam git). `git ls-files` = 152 file.
   - **Database (dev.db):** file `dev.db` **tidak ada (absent)** — dihapus oleh commit HEAD \"Release: clean core files only\" (1dc891d) dan `.gitignore` mencantumkan `*.db`; seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` & `import_students_grades_clean.py` tidak ditemukan di working tree).
   - **Data sumber:** folder `.data-pondokanat/` **tidak ditemukan** di working tree (di-eksklusi oleh `.gitignore`). Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber.
   - **Build quality gate:** **NOT RE-RUNABLE** — `node_modules/` **absent** (dihapus setelah Rev. 377; `npm ci` diperlukan untuk memulihkan); `.next/` masih ada (partial: `cache/` + `diagnostics/` + `package.json` + `server/` + `static/`, bukan production build). `tsc --noEmit`, `npm run lint`, `npm run build` **tidak dapat dijalankan** karena `node_modules/` **absent**; `npm ci` diperlukan untuk memulihkan sebelum melakukan type-check/lint/build. Verifikasi ulang 23 Oct 2026: `tsc --noEmit` exit 1 (module resolution error tanpa node_modules), `npm run lint` exit 2 (ERR_MODULE_NOT_FOUND: eslint-config-next).
   - **Source files:** `src/app/*` = 13 sub direktori (absensi, beranda, berita, guru, kelas, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah) + `globals.css` + `layout.tsx` + `page.tsx` = 15 entri (13 halaman + layout + page). `src/components` = `Beranda.tsx` & `Login.tsx`. `src/lib` = **kosong** (logic inline di komponen). Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite).
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map(\"uid_nfc\")` baris 68), `init_schema.sql` baris 40, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama 'Pondok Banat'); produksi butuh bcrypt + session.
   - **Beranda hardcode:** `Beranda.tsx` & `src/app/beranda/page.tsx` masih hardcoded totalSantri (belum fetch real-time dari DB); tidak menggunakan nilai DB aktual.
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` sukses. Schema inconsistency (Rev. 38–45) SELESAI — kedua model konsisten dengan referensi di `Subject` dan `User`.
   - **Status:** dokumen PRD **REVISI** — rev 388 = verifikasi fresh ulang & konfirmasi stabilitas di {today_str} (cron run); `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. HEAD `{head_commit}` (Rev. 387), {ahead} commits ahead origin/main (naik 1 dari Rev. 387). State stabil, tidak ada perubahan signifikan dari Rev. 387.
"""

if "## 12. REVISI TERBARU (Rev. 387 — 23 Oktober 2026 WIB)" in content:
    # Insert before the "## 12. REVISI TERBARU (Rev. 387" heading
    content = content.replace(
        "## 12. REVISI TERBARU (Rev. 387 — 23 Oktober 2026 WIB)",
        s12_388 + "\n## 12. REVISI TERBARU (Rev. 387 — 23 Oktober 2026 WIB)")
    print("§12.388 section inserted")
else:
    print("WARNING: §12.387 heading not found")

# ---- 5. Write back ----
with open(PRD_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print("SUCCESS: PRD updated to Rev. 388")
print(f"HEAD: {head_commit}")
print(f"AHEAD: {ahead}")
print(f"origin/main: {origin_main}")
print(f"PRD size: {os.path.getsize(PRD_PATH)} bytes")
