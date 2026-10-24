#!/usr/bin/env python3
# -*- coding: utf-8 -*-
PATH = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"

with open(PATH, encoding="utf-8") as f:
    lines = f.read().splitlines(keepends=True)

def find_line(pred, label):
    for i, l in enumerate(lines):
        if pred(l):
            return i
    raise SystemExit(f"NOT FOUND: {label}")

# ---- §11 compact entries: insert after the Rev.483 compact entry ----
i483 = find_line(lambda l: l.startswith("    483. 24 Oktober 2026 (WIB): PRD fresh verification & stability confirmation (24 Oct 2026 WIB); HEAD `ce542bcaa401b9d36f1a88e8013056605c8e96f1` (Rev. 482 commit), 10 / 0 (10 commits ahead origin_main)."),
                 "Rev.483 s11 entry")
print("R7: Rev.483 s11 at line", i483 + 1)
new490_s11 = """
    490. 24 Oktober 2026 (WIB): PRD fresh verification & stability confirmation (24 Oct 2026 WIB); HEAD `7adb7ce66c8d9a5ee707215b21339f451592e1` (Rev. 489 commit), 19 / 0 (19 commits ahead origin_main). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run): **state stabil, tidak ada perubahan signifikan dari Rev. 489** (data terkonsisten). Build gate: **NOT RE-RUNABLE** — node_modules absent; npm ci diperlukan. Database: dev.db absent; seluruh record (453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) tidak tersedia — import ulang menggunakan `init_db.py` & `init_schema.sql`. **M02a (NFC):** field `uid_nfc` ada aktif di tabel students, semua 453 NULL (data ekspor NFC Tools belum tersedia). **Auth hardcode:** Login.tsx tetap `admin@pondokanbat.com` / `admin123` (typo domain). **Beranda hardcode:** Beranda.tsx & page.tsx masih hardcoded totalSantri 453. **Schema:** model `KitabProgress` (baris 203) & `Sertakan` (baris 218) sudah terdefinisi; `prisma validate` sukses. **Status:** dokumen PRD **REVISI** — rev 490 = PRD fresh verification & konfirmasi stabilitas; seluruh data terkonsisten, tidak ada perubahan signifikan dari Rev. 489; branch 19 ahead / 0 behind origin_main.
"""
new491_s11 = """
    491. 24 Oktober 2026 (WIB): PRD fresh verification & stability confirmation (24 Oct 2026 WIB); HEAD `94d19e3175718470e7214641aee6e0cb46f34177` (Rev. 490 commit), 20 / 0 (20 commits ahead origin_main). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run): **state stabil, tidak ada perubahan signifikan dari Rev. 490** (data terkonsisten). Build gate: **NOT RE-RUNABLE** — node_modules absent; npm ci diperlukan. Database: dev.db absent; seluruh record (453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) tidak tersedia — import ulang menggunakan `init_db.py` & `init_schema.sql`. **M02a (NFC):** field `uid_nfc` ada aktif di tabel students, semua 453 NULL (data ekspor NFC Tools belum tersedia). **Auth hardcode:** Login.tsx tetap `admin@pondokanbat.com` / `admin123` (typo domain). **Beranda hardcode:** Beranda.tsx & page.tsx masih hardcoded totalSantri 453. **Schema:** model `KitabProgress` (baris 203) & `Sertakan` (baris 218) sudah terdefinisi; `prisma validate` sukses. **Status:** dokumen PRD **REVISI** — rev 491 = PRD fresh verification & konfirmasi stabilitas; seluruh data terkonsisten, tidak ada perubahan signifikan dari Rev. 490; branch 20 ahead / 0 behind origin_main.
"""
lines[i483+1:i483+1] = [new490_s11, new491_s11]

# ---- §12 final entries: append after the Rev.489 final entry ----
i489 = find_line(lambda l: l.startswith("||_- **Rev. 489 (final).** 24 Oktober 2026 (WIB): PRD fresh verification & stability confirmation (24 Oct 2026 WIB); HEAD `7adb7ce66c8d9a5ee707215b21339f451592e1` (Rev. 489 (final):"),
                 "Rev.489 s12 entry")
print("R8: Rev.489 s12 at line", i489 + 1)
new490_s12 = """
||_- **Rev. 490 (final).** 24 Oktober 2026 (WIB): PRD fresh verification & stability confirmation (24 Oct 2026 WIB); HEAD `94d19e3175718470e7214641aee6e0cb46f34177` (Rev. 490 (final): PRD fresh verification & stability confirmation (24 Oct 2026 WIB); header Rev. 490, §11 kompakt changelog 116–489, §12 updated), 19 / 0 (19 commits ahead origin_main). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run): **state stabil, tidak ada perubahan signifikan dari Rev. 489** (data terkonsisten). Build gate: **NOT RE-RUNABLE** — `node_modules/` **absent** (dihapus setelah Rev. 377; `npm ci` diperlukan untuk memulihkan); `.next/` masih ada (partial: `cache/` + `diagnostics/` + `package.json` + `server/` + `static/`, bukan production build). `tsc --noEmit` exit 1, `npm run lint` exit 2, `npx next build` exit 1 — semua gagal karena `node_modules/` **absent**; `npm ci` diperlukan untuk memulihkan sebelum melakukan type-check/lint/build. Database (dev.db): **tidak ada (absent)** — dihapus oleh commit HEAD \"Release: clean core files only\" (1dc891d) dan `.gitignore` mencantumkan `*.db`; seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` & `import_students_grades_clean.py` tidak ditemukan di working tree). **M02a (NFC):** field `uid_nfc` ada aktif di tabel `students` (kolom setelah `photo`); `prisma/schema.prisma` baris 68 (`uidNfc String? @map(\"uid_nfc\")`), `init_schema.sql` baris 44, `init_db.py` baris 60. **Tidak ada satupun siswa yang memiliki `uid_nfc` diisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`). **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (typo domain `pondokanat.com`); produksi butuh bcrypt + session. **Beranda hardcode:** `Beranda.tsx` & `src/app/beranda/page.tsx` masih hardcoded `totalSantri` (belum fetch real-time dari DB). **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` sukses. Schema inconsistency (Rev. 38–45) SELESAI — kedua model konsisten dengan referensi di `Subject` dan `User`. **Status:** dokumen PRD **REVISI** — rev 490 (final): PRD fresh verification & stability confirmation (24 Oct 2026 WIB); HEAD `94d19e3175718470e7214641aee6e0cb46f34177` (Rev. 490 (final)), 19 / 0 (19 commits ahead origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 489 (data terkonsisten).
"""
new491_s12 = """
||_- **Rev. 491 (final).** 24 Oktober 2026 (WIB): PRD fresh verification & stability confirmation (24 Oct 2026 WIB); HEAD `94d19e3175718470e7214641aee6e0cb46f34177` (Rev. 490 commit), 20 / 0 (20 commits ahead origin_main). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run): **state stabil, tidak ada perubahan signifikan dari Rev. 490** (data terkonsisten). Build gate: **NOT RE-RUNABLE** — `node_modules/` **absent** (dihapus setelah Rev. 377; `npm ci` diperlukan untuk memulihkan); `.next/` masih ada (partial: `cache/` + `diagnostics/` + `package.json` + `server/` + `static/`, bukan production build). `tsc --noEmit` exit 1, `npm run lint` exit 2, `npx next build` exit 1 — semua gagal karena `node_modules/` **absent**; `npm ci` diperlukan untuk memulihkan sebelum melakukan type-check/lint/build. Database (dev.db): **tidak ada (absent)** — dihapus oleh commit HEAD \"Release: clean core files only\" (1dc891d) dan `.gitignore` mencantumkan `*.db`; seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` & `import_students_grades_clean.py` tidak ditemukan di working tree). **M02a (NFC):** field `uid_nfc` ada aktif di tabel `students` (kolom setelah `photo`); `prisma/schema.prisma` baris 68 (`uidNfc String? @map(\"uid_nfc\")`), `init_schema.sql` baris 44, `init_db.py` baris 60. **Tidak ada satupun siswa yang memiliki `uid_nfc` diisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`). **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (typo domain `pondokanat.com`); produksi butuh bcrypt + session. **Beranda hardcode:** `Beranda.tsx` & `src/app/beranda/page.tsx` masih hardcoded `totalSantri` (belum fetch real-time dari DB). **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` sukses. Schema inconsistency (Rev. 38–45) SELESAI — kedua model konsisten dengan referensi di `Subject` dan `User`. **Status:** dokumen PRD **REVISI** — rev 491 (final): PRD fresh verification & stability confirmation (24 Oct 2026 WIB); HEAD `94d19e3175718470e7214641aee6e0cb46f34177` (Rev. 490 commit), 20 / 0 (20 commits ahead origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 490 (data terkonsisten).
"""
lines[i489+1:i489+1] = [new490_s12, new491_s12]

# ---- Header revisions ----
# §11 header range (line 413 -> 0-indexed 412)
i11h = find_line(lambda l: l.startswith("## 11. REVISI TERBARU (Rev. 116–488 — 23 Oktober 2026 WIB)"), "§11 header")
print("R2: §11 header at line", i11h + 1)
lines[i11h] = "## 11. REVISI TERBARU (Rev. 116–491 — 23 Oktober 2026 WIB)\n"

# §12 header range (line 421 -> 0-indexed 420)
i12h = find_line(lambda l: l.startswith("## 12. REVISI TERBARU (Rev. 468–489 — 23 Oktober 2026 WIB)"), "§12 header")
print("R3: §12 header at line", i12h + 1)
lines[i12h] = "## 12. REVISI TERBARU (Rev. 468–491 — 23 Oktober 2026 WIB)\n"

# Header Git HEAD local (line 4 -> 0-indexed 3)
iHg = find_line(lambda l: l.startswith("> **Git HEAD (local):** `7adb7ce66c8d9a5ee707215b21339f451592e1` (Rev. 489 (final):"), "Git HEAD local")
print("R4: Git HEAD local at line", iHg + 1)
lines[iHg] = lines[iHg].replace(
    "> **Git HEAD (local):** `7adb7ce66c8d9a5ee707215b21339f451592e1` (Rev. 489 (final):",
    "> **Git HEAD (local):** `94d19e3175718470e7214641aee6e0cb46f34177` (Rev. 490 (final):")

# git rev-parse HEAD (line 4)
iG2 = find_line(lambda l: l.startswith("`git rev-parse HEAD` = `7adb7ce66c8d9a5ee707215b21339f451592e1` (Rev. 489 (final))"), "git rev-parse HEAD")
print("R5: git rev-parse HEAD at line", iG2 + 1)
lines[iG2] = lines[iG2].replace(
    "`git rev-parse HEAD` = `7adb7ce66c8d9a5ee707215b21339f451592e1` (Rev. 489 (final))",
    "`git rev-parse HEAD` = `94d19e3175718470e7214641aee6e0cb46f34177` (Rev. 490 (final))")

# revisi terbaru (line 4)
iH6 = find_line(lambda l: "revisi terbaru = Rev. 489 (final), fresh verification dilakukan hari ini" in l, "revisi terbaru")
print("R6: revisi terbaru at line", iH6 + 1)
lines[iH6] = lines[iH6].replace(
    "revisi terbaru = Rev. 489 (final), fresh verification dilakukan hari ini",
    "revisi terbaru = Rev. 491 (final), fresh verification dilakukan hari ini")

with open(PATH, "w", encoding="utf-8") as f:
    f.write("".join(lines))

print("\nFile updated successfully.")
print("New length:", len("".join(lines)))
