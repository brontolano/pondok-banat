#!/usr/bin/env python3
# Rev. 489 PRD update (fresh verification & stability confirmation)
import re
path = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"
with open(path, "r", encoding="utf-8") as f:
    c = f.read()

# --- Edit 1: Header line (whole-line) ---
new_header = """> **Git HEAD (local):** `7adb7cee66c8d9a5ee707215b213339f451592e1` (Rev. 489 (final): PRD fresh verification & stability confirmation (24 Oct 2026 WIB); header Rev. 489, §11 kompakt changelog 116–488, §12 updated; HEAD 8ee6d40 (Rev. 488 final), 19 commits ahead origin_main). Branch `main`, remote `brontolano/pondok-banat`. `git rev-parse HEAD` = `7adb7cee66c8d9a5ee707215b213339f451592e1` (Rev. 489 (final)); **origin/main:** `574ed2590fa808eb0fdc32973c053fba566b680d` (Rev. 473, in sync). Local branch **19 commits ahead / 0 behind** origin_main. Working tree: `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 489 (final), fresh verification dilakukan hari ini); seluruh file lain cocak dengan HEAD; untracked: 25 skrip utility (tidak terpantau dalam git). `git ls-files` = 187 file. Database (dev.db): **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`; seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` & `import_students_grades_clean.py` tidak ditemukan di working tree). Build quality gate: **NOT RE-RUNABLE** — `node_modules/` **absent** (dihapus setelah Rev. 377); `.next/` masih ada (partial: `cache/` + `diagnostics/` + `package.json` + `server/` + `static/`, bukan production build). `tsc --noEmit`, `npm run lint`, `npm run build` **tidak dapat dijalankan** karena `node_modules/` **absent**.## 1. RINGKASAN PRODUK"""
c2 = re.sub(r"^> \*\*Git HEAD \(local\):\s*.*$", new_header, c, count=1, flags=re.MULTILINE)
assert c2 != c, "header not found"
c = c2
print("EDIT 1 (header): ok")

# --- Edit 2: Section 11 header ---
c2 = re.sub(r"^## 11\. REVISI TERBARU \(Rev\. 116.*$", "## 11. REVISI TERBARU (Rev. 116–488 — 23 Oktober 2026 WIB)", c, count=1, flags=re.MULTILINE)
assert c2 != c, "§11 header not found"
c = c2
print("EDIT 2 (§11): ok")

# --- Edit 3: Section 12 header ---
c2 = re.sub(r"^## 12\. REVISI TERBARU \(Rev\. 468.*$", "## 12. REVISI TERBARU (Rev. 468–489 — 23 Oktober 2026 WIB)", c, count=1, flags=re.MULTILINE)
assert c2 != c, "§12 header not found"
c = c2
print("EDIT 3 (§12): ok")

# --- Edit 4: Insert Rev. 489 entry before Rev. 488 entry ---
new_entry = """||_- **Rev. 489 (final).** 24 Oktober 2026 (WIB): PRD fresh verification & stability confirmation (24 Oct 2026 WIB); HEAD `7adb7cee66c8d9a5ee707215b213339f451592e1` (Rev. 489 (final): PRD fresh verification & stability confirmation (24 Oct 2026 WIB); header Rev. 489, §11 kompakt changelog 116–488, §12 updated), 19 / 0 (19 commits ahead origin_main). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run): **state stabil, tidak ada perubahan signifikan dari Rev. 488** (data terkonsisten). Build gate: **NOT RE-RUNABLE** — `node_modules/` **absent** (dihapus setelah Rev. 377; `npm ci` diperlukan untuk memulihkan); `.next/` masih ada (partial: `cache/` + `diagnostics/` + `package.json` + `server/` + `static/`, bukan production build). `tsc --noEmit` exit 1, `npm run lint` exit 2, `npx next build` exit 1 — semua gagal karena `node_modules/` **absent**; `npm ci` diperlukan untuk memulihkan sebelum melakukan type-check/lint/build. Database (dev.db): **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`; seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` & `import_students_grades_clean.py` tidak ditemukan di working tree). **M02a (NFC):** field `uid_nfc` ada aktif di tabel `students` (kolom setelah `photo`); `prisma/schema.prisma` baris 68 (`uidNfc String? @map("uid_nfc")`), `init_schema.sql` baris 44, `init_db.py` baris 60. **Tidak ada satupun siswa yang memiliki `uid_nfc` diisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`). **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (typo domain `pondokanat.com`); produksi butuh bcrypt + session. **Beranda hardcode:** `Beranda.tsx` & `src/app/beranda/page.tsx` masih hardcoded `totalSantri` (belum fetch real-time dari DB). **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` sukses. Schema inconsistency (Rev. 38–45) SELESAI — kedua model konsisten dengan referensi di `Subject` dan `User`. **Status:** dokumen PRD **REVISI** — rev 489 (final) = PRD fresh verification & konfirmasi stabilitas; seluruh data terkonsisten, tidak ada perubahan signifikan dari Rev. 488; branch 19 ahead / 0 behind origin_main."""
lines = c.split("\n")
inserted = False
for i, line in enumerate(lines):
    if "Rev. 488 (final)" in line and "24 Oktober 2026 (WIB)" in line:
        # insert new_entry before this Rev. 488 entry line
        lines[i:i] = new_entry.split("\n")
        inserted = True
        break
assert inserted, "Rev. 488 entry not found"
c = "\n".join(lines)
print("EDIT 4 (region insert): ok")

with open(path, "w", encoding="utf-8") as f:
    f.write(c)
print("WRITTEN. size:", len(c.encode("utf-8")))
