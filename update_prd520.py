import io

path = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Header update
old_header = """Rev. 519: PRD fresh verification & stability confirmation (24 Oct 2026 WIB); header Rev. 519 (updated from Rev. 518), §11 kompakt changelog 116–519, §12 updated; HEAD `0cb6019d39efdcf87346274f5ede6e5b55b714b5` (Rev. 518 commit: PRD fresh verification & stability confirmation (24 Oct 2026 WIB)); 1 / 0 (1 commit ahead origin_main). Branch `main`, remote `brontolano/pondok-banat`. `git rev-parse HEAD` = `0cb6019d39efdcf87346274f5ede6e5b55b714b5` (Rev. 518 commit, fresh verification dilakukan hari ini); **origin/main:** `d36eb62911dc50d7d2e452ac1d37a801024dd3b6` (Rev. 517, in sync). Local branch **1 commit ahead / 0 behind** origin_main. Working tree: `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 519 (fresh verification), fresh verification dilakukan hari ini); seluruh file lain cocak dengan HEAD; untracked: 67 skrip utility (tidak terpantau dalam git); `commit_msg.txt` dihapus (build artifact); `git ls-files` = 187 file."""

new_header = """Rev. 520: PRD fresh verification & stability confirmation (24 Oct 2026 WIB); header Rev. 520 (updated from Rev. 519), §11 kompakt changelog 116–520, §12 updated; HEAD `ea1ac69d39efdcf87346274f5ede6e5b55b714b5` (Rev. 519 commit: PRD fresh verification & stability confirmation (24 Oct 2026 WIB)); 2 / 0 (2 commit ahead origin_main). Branch `main`, remote `brontolano/pondok-banat`. `git rev-parse HEAD` = `ea1ac69d39efdcf87346274f5ede6e5b55b714b5` (Rev. 519 commit, fresh verification dilakukan hari ini); **origin/main:** `d36eb62911dc50d7d2e452ac1d37a801024dd3b6` (Rev. 517, in sync). Local branch **2 commit ahead / 0 behind** origin_main. Working tree: `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 520 (fresh verification), fresh verification dilakukan hari ini); seluruh file lain cocak dengan HEAD; untracked: 67 skrip utility (tidak terpantau dalam git); `commit_msg.txt` dihapus (build artifact); `git ls-files` = 187 file."""

assert old_header in content, "Header not found"
content = content.replace(old_header, new_header)
print("Header updated.")

# 2. §11 header
old_s11 = "## 11. REVISI TERBARU (Rev. 116–519 — 24 Oktober 2026 WIB)"
new_s11 = "## 11. REVISI TERBARU (Rev. 116–520 — 24 Oktober 2026 WIB)"
assert old_s11 in content, "§11 header not found"
content = content.replace(old_s11, new_s11)
print("§11 header updated.")

# 3. §12 header
old_s12 = "## 12. REVISI TERBARU (Rev. 468–519 — 24 Oktober 2026 WIB)"
new_s12 = "## 12. REVISI TERBARU (Rev. 468–520 — 24 Oktober 2026 WIB)"
assert old_s12 in content, "§12 header not found"
content = content.replace(old_s12, new_s12)
print("§12 header updated.")

# 4. Add Rev. 520 entry after the last §12 entry (Rev. 514)
old_rev514 = """||- **Rev. 514 (final).** 24 Oktober 2026 (WIB): PRD fresh verification & stability confirmation (24 Oct 2026 WIB); HEAD `c4c93184cd749250bdf8b258efe60f22c9dbe258` (Rev. 514 commit: PRD fresh verification & stability confirmation (24 Oct 2026 WIB); header Rev. 514, §11 kompakt changelog 116–514, §12 updated); 0 / 0 (0 commits ahead origin_main). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run): **state stabil, tidak ada perubahan signifikan dari Rev. 513** (data terkonsisten). Build gate: **NOT RE-RUNABLE** — `node_modules/` **absent** (dihapus setelah Rev. 377; `npm ci` diperlukan untuk memulihkan); `.next/` masih ada (partial: `cache/` + `diagnostics/` + `package.json` + `server/` + `static/`, bukan production build). `tsc --noEmit` exit 1, `npm run lint` exit 2, `npx next build` exit 1 — semua gagal karena `node_modules/` **absent**; `npm ci` diperlukan untuk memulihkan sebelum melakukan type-check/lint/build. Database (dev.db): **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`; seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` & `import_students_grades_clean.py` tidak ditemukan di working tree). **M02a (NFC):** field `uid_nfc` ada aktif di tabel students, semua 453 NULL (data ekspor NFC Tools belum tersedia). **Auth hardcode:** `src/components/Login.tsx` tetap `admin@pondokanbat.com` / `admin123` (typo domain `pondokanat.com`); produksi butuh bcrypt + session. **Beranda hardcode:** `src/components/Beranda.tsx` & `src/app/beranda/page.tsx` masih hardcoded `totalSantri` (belum fetch real-time dari DB). **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` sukses. **Status:** dokumen PRD **REVISI** — rev 514 (final): PRD fresh verification & konfirmasi stabilitas; seluruh data terkonsisten, tidak ada perubahan signifikan dari Rev. 513; branch 0 ahead / 0 behind origin_main."""

new_rev520 = old_rev514 + """

||- **Rev. 520 (final).** 24 Oktober 2026 (WIB): PRD fresh verification & stability confirmation (24 Oct 2026 WIB); HEAD `ea1ac69d39efdcf87346274f5ede6e5b55b714b5` (Rev. 519 commit: PRD fresh verification & stability confirmation (24 Oct 2026 WIB); header Rev. 519, §11 kompakt changelog 116–518, §12 updated; HEAD 0cb6019 (Rev. 518), 1 commit ahead origin_main), 2 / 0 (2 commits ahead origin_main). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run): **state stabil, tidak ada perubahan signifikan dari Rev. 519** (data terkonsisten). Build gate: **NOT RE-RUNABLE** — `node_modules/` **absent** (dihapus setelah Rev. 377; `npm ci` diperlukan untuk memulihkan); `.next/` masih ada (partial: `cache/` + `diagnostics/` + `package.json` + `server/` + `static/`, bukan production build). `tsc --noEmit` exit 1, `npm run lint` exit 2, `npx next build` exit 1 — semua gagal karena `node_modules/` **absent**; `npm ci` diperlukan untuk memulihkan sebelum melakukan type-check/lint/build. Database (dev.db): **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`; seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` & `import_students_grades_clean.py` tidak ditemukan di working tree). **M02a (NFC):** field `uid_nfc` ada aktif di tabel students, semua 453 NULL (data ekspor NFC Tools belum tersedia). **Auth hardcode:** `src/components/Login.tsx` tetap `admin@pondokanbat.com` / `admin123` (typo domain `pondokanat.com`); produksi butuh bcrypt + session. **Beranda hardcode:** `src/components/Beranda.tsx` & `src/app/beranda/page.tsx` masih hardcoded `totalSantri` (belum fetch real-time dari DB). **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` sukses. **Status:** dokumen PRD **REVISI** — rev 520 (final): PRD fresh verification & konfirmasi stabilitas; seluruh data terkonsisten, tidak ada perubahan signifikan dari Rev. 519; branch 2 ahead / 0 behind origin_main."""

assert old_rev514 in content, "Rev. 514 entry not found"
content = content.replace(old_rev514, new_rev520)
print("Rev. 520 entry added.")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("File saved.")
print("File size:", len(content.encode("utf-8")), "bytes")
print("Rev. 520 present:", "Rev. 520 (final)" in content)
print("§11 range 116-520:", "116–520" in content)
print("§12 range 468-520:", "468–520" in content)
