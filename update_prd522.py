#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Update PRD-PONDOK-BANAT.md from Rev. 521 to Rev. 522 (fresh verification)."""
import io

PATH = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"

with io.open(PATH, "r", encoding="utf-8") as f:
    c = f.read()

orig = c

# ---- 1. Header update ----
old_header = (
    "Rev. 521: PRD fresh verification & stability confirmation (24 Oct 2026 WIB); header Rev. 521 (updated from Rev. 520), "
    "§11 kompakt changelog 116–521, §12 updated; HEAD `ea1ac69d39efdcf87346274f5ede6e5b55b714b5` "
    "(Rev. 519 commit: PRD fresh verification & stability confirmation (24 Oct 2026 WIB)); "
    "3 / 0 (3 commits ahead origin_main). Branch `main`, remote `brontolano/pondok-banat`. "
    "`git rev-parse HEAD` = `ea1ac69d39efdcf87346274f5ede6e5b55b714b5` "
    "(Rev. 519 commit, fresh verification dilakukan hari ini); **origin/main:** `d36eb62911dc50d7d2e452ac1d37a801024dd3b6` "
    "(Rev. 517, in sync). Local branch **3 commit ahead / 0 behind** origin_main. "
    "Working tree: `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 521 (fresh verification), fresh verification dilakukan hari ini); "
    "seluruh file lain cocak dengan HEAD; untracked: 67 skrip utility (tidak terpantau dalam git); "
    "`commit_msg.txt` dihapus (build artifact); `git ls-files` = 187 file."
)
new_header = (
    "Rev. 522: PRD fresh verification & stability confirmation (24 Oct 2026 WIB); header Rev. 522 (updated from Rev. 521), "
    "§11 kompakt changelog 116–522, §12 updated; HEAD `632bebb6824eee5ab8d3399af40aacad11ab5c2a` "
    "(Rev. 521 commit: PRD fresh verification & stability confirmation (24 Oct 2026 WIB)); "
    "4 / 0 (4 commits ahead origin_main). Branch `main`, remote `brontolano/pondok-banat`. "
    "`git rev-parse HEAD` = `632bebb6824eee5ab8d3399af40aacad11ab5c2a` "
    "(Rev. 521 commit, fresh verification dilakukan hari ini); **origin/main:** `d36eb62911dc50d7d2e452ac1d37a801024dd3b6` "
    "(Rev. 517, in sync). Local branch **4 commit ahead / 0 behind** origin_main. "
    "Working tree: `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 522 (fresh verification), fresh verification dilakukan hari ini); "
    "seluruh file lain cocak dengan HEAD; untracked: 67 skrip utility (tidak terpantau dalam git); "
    "`commit_msg.txt` dihapus (build artifact); `git ls-files` = 187 file."
)
assert old_header in c, "Header not found"
c = c.replace(old_header, new_header)

# ---- 2. §11 header range ----
old_s11 = "## 11. REVISI TERBARU (Rev. 116–521 — 24 Oktober 2026 WIB)"
new_s11 = "## 11. REVISI TERBARU (Rev. 116–522 — 24 Oktober 2026 WIB)"
assert old_s11 in c, "§11 header not found"
c = c.replace(old_s11, new_s11)

# ---- 3. §12 header range ----
old_s12 = "## 12. REVISI TERBARU (Rev. 468–521 — 24 Oktober 2026 WIB)"
new_s12 = "## 12. REVISI TERBARU (Rev. 468–522 — 24 Oktober 2026 WIB)"
assert old_s12 in c, "§12 header not found"
c = c.replace(old_s12, new_s12)

# ---- 4. §12 verification notes update ----
old_note1 = "> **Verifikasi fresh kondisi repository + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 518 (data terkonsisten).**"
new_note1 = "> **Verifikasi fresh kondisi repository + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 521 (data terkonsisten).**"
assert old_note1 in c, "§12 verification note not found"
c = c.replace(old_note1, new_note1)

old_note2 = "> - **Commit count:** 1 / 0 (1 commit ahead origin_main). Local branch **1 commit ahead / 0 behind** origin_main."
new_note2 = "> - **Commit count:** 4 / 0 (4 commits ahead origin_main). Local branch **4 commits ahead / 0 behind** origin_main."
assert old_note2 in c, "§12 commit count not found"
c = c.replace(old_note2, new_note2)

old_note3 = "> - **Working tree:** `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 519 (final)); HEAD `0cb6019d39efdcf87346274f5ede6e5b55b714b5` (Rev. 518 commit);"
new_note3 = "> - **Working tree:** `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 521 (final)); HEAD `632bebb6824eee5ab8d3399af40aacad11ab5c2a` (Rev. 521 commit);"
assert old_note3 in c, "§12 working tree not found"
c = c.replace(old_note3, new_note3)

old_note4 = "> - **Status:** dokumen PRD **REVISI** — rev 519: PRD fresh verification & stability confirmation (24 Oct 2026 WIB); HEAD `0cb6019d39efdcf87346274f5ede6e5b55b714b5` (Rev. 518 commit); 1 / 0 (1 commit ahead origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 518 (data terkonsisten)."
new_note4 = "> - **Status:** dokumen PRD **REVISI** — rev 522: PRD fresh verification & stability confirmation (24 Oct 2026 WIB); HEAD `632bebb6824eee5ab8d3399af40aacad11ab5c2a` (Rev. 521 commit); 4 / 0 (4 commits ahead origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 521 (data terkonsisten)."
assert old_note4 in c, "§12 status not found"
c = c.replace(old_note4, new_note4)

# ---- 5. Add Rev. 522 entry to §11 (after last §11 entry, before §12) ----
idx_s12_header = c.find("## 12. REVISI TERBARU (Rev. 468–522 — 24 Oktober 2026 WIB)")
assert idx_s12_header != -1, "§12 header not found after replacement"
idx_rev514 = c.rfind("    |||- **Rev. 514 (final).** 24 Oktober 2026 (WIB): PRD fresh verification & stability confirmation (24 Oct 2026 WIB); HEAD `c4c93184cd749250bdf8b258efe60f22c9dbe258` (Rev. 514 commit")
assert idx_rev514 != -1, "§11 Rev. 514 entry not found"
end_rev514 = c.find("\n", idx_rev514)
assert end_rev514 != -1, "Rev. 514 entry end not found"

rev522_s11 = (
    "\n"
    "    ||- **Rev. 522 (final).** 24 Oktober 2026 (WIB): PRD fresh verification & stability confirmation (24 Oct 2026 WIB); HEAD `632bebb6824eee5ab8d3399af40aacad11ab5c2a` (Rev. 521 commit: PRD fresh verification & stability confirmation (24 Oct 2026 WIB); header Rev. 521, §11 kompakt changelog 116–520, §12 updated; HEAD 632bebb6824eee5ab8d3399af40aacad11ab5c2a (Rev. 521), 4 commits ahead origin_main), 4 / 0 (4 commits ahead origin_main). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run): **state stabil, tidak ada perubahan signifikan dari Rev. 521** (data terkonsisten). Build gate: **NOT RE-RUNABLE** — `node_modules/` **absent** (dihapus setelah Rev. 377; `npm ci` diperlukan untuk memulihkan); `.next/` masih ada (partial: `cache/` + `diagnostics/` + `package.json` + `server/` + `static/`, bukan production build). `tsc --noEmit` exit 1, `npm run lint` exit 2, `npx next build` exit 1 — semua gagal karena `node_modules/` **absent**; `npm ci` diperlukan untuk memulihkan sebelum melakukan type-check/lint/build. Database (dev.db): **tidak ada (absent)** — dihapus oleh commit HEAD \"Release: clean core files only\" (1dc891d) dan `.gitignore` mencantumkan `*.db`; seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` & `import_students_grades_clean.py` tidak ditemukan di working tree). **M02a (NFC):** field `uid_nfc` ada aktif di tabel students, semua 453 NULL (data ekspor NFC Tools belum tersedia). **Auth hardcode:** `src/components/Login.tsx` tetap `admin@pondokanbat.com` / `admin123` (typo domain `pondokanat.com`); produksi butuh bcrypt + session. **Beranda hardcode:** `src/components/Beranda.tsx` & `src/app/beranda/page.tsx` masih hardcoded `totalSantri` (belum fetch real-time dari DB). **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` sukses. **Status:** dokumen PRD **REVISI** — rev 522 = PRD fresh verification & konfirmasi stabilitas; seluruh data terkonsisten, tidak ada perubahan signifikan dari Rev. 521; branch 4 / 0 (4 commits ahead origin_main).\n"
)

c = c[:end_rev514] + rev522_s11 + c[end_rev514:]

# ---- 6. Add Rev. 522 entry to §12 (after last §12 entry, at end of file) ----
idx_rev521 = c.rfind("||- **Rev. 521 (final).** 24 Oktober 2026 (WIB): PRD fresh verification & stability confirmation (24 Oct 2026 WIB); HEAD `ea1ac69d39efdcf87346274f5ede6e5b55b714b5` (Rev. 519 commit")
assert idx_rev521 != -1, "§12 Rev. 521 entry not found"
end_rev521 = c.find("\n", idx_rev521)
assert end_rev521 != -1, "Rev. 521 entry end not found"

rev522_s12 = (
    "\n"
    "||- **Rev. 522 (final).** 24 Oktober 2026 (WIB): PRD fresh verification & stability confirmation (24 Oct 2026 WIB); HEAD `632bebb6824eee5ab8d3399af40aacad11ab5c2a` (Rev. 521 commit: PRD fresh verification & stability confirmation (24 Oct 2026 WIB); header Rev. 521, §11 kompakt changelog 116–520, §12 updated; HEAD 632bebb6824eee5ab8d3399af40aacad11ab5c2a (Rev. 521), 4 commits ahead origin_main), 4 / 0 (4 commits ahead origin_main). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run): **state stabil, tidak ada perubahan signifikan dari Rev. 521** (data terkonsisten). Build gate: **NOT RE-RUNABLE** — `node_modules/` **absent** (dihapus setelah Rev. 377; `npm ci` diperlukan untuk memulihkan); `.next/` masih ada (partial: `cache/` + `diagnostics/` + `package.json` + `server/` + `static/`, bukan production build). `tsc --noEmit` exit 1, `npm run lint` exit 2, `npx next build` exit 1 — semua gagal karena `node_modules/` **absent**; `npm ci` diperlukan untuk memulihkan sebelum melakukan type-check/lint/build. Database (dev.db): **tidak ada (absent)** — dihapus oleh commit HEAD \"Release: clean core files only\" (1dc891d) dan `.gitignore` mencantumkan `*.db`; seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` & `import_students_grades_clean.py` tidak ditemukan di working tree). **M02a (NFC):** field `uid_nfc` ada aktif di tabel students, semua 453 NULL (data ekspor NFC Tools belum tersedia). **Auth hardcode:** `src/components/Login.tsx` tetap `admin@pondokanbat.com` / `admin123` (typo domain `pondokanat.com`); produksi butuh bcrypt + session. **Beranda hardcode:** `src/components/Beranda.tsx` & `src/app/beranda/page.tsx` masih hardcoded `totalSantri` (belum fetch real-time dari DB). **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` sukses. **Status:** dokumen PRD **REVISI** — rev 522 = PRD fresh verification & konfirmasi stabilitas; seluruh data terkonsisten, tidak ada perubahan signifikan dari Rev. 521; branch 4 / 0 (4 commits ahead origin_main).\n"
)

c = c[:end_rev521] + rev522_s12 + c[end_rev521:]

# ---- 7. Verify ----
print("=== VERIFICATION ===")
print("File size:", len(c.encode("utf-8")), "bytes (was", len(orig.encode("utf-8")), ")")
print("'Rev. 522 (final)' count:", c.count("Rev. 522 (final)"))
print("'Rev. 521' remaining:", c.count("Rev. 521"))
print("'116–522' in §11:", "116–522 — 24 Oktober 2026 WIB" in c)
print("'468–522' in §12:", "468–522 — 24 Oktober 2026 WIB" in c)
print("'4 / 0 (4 commits ahead' in file:", "4 / 0 (4 commits ahead origin_main)" in c)
print("Header updated:", new_header[:60] in c)
print("§11 header updated:", new_s11 in c)
print("§12 header updated:", new_s12 in c)

with io.open(PATH, "w", encoding="utf-8") as f:
    f.write(c)

print("\nFile written successfully.")
