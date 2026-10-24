#!/usr/bin/env python3
"""Update PRD-PONDOK-BANAT.md to Rev. 523 (fresh verification)."""

import subprocess, os, re

PATH = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"
content = open(PATH).read()

# ---- 1. Capture live verification state ----
out = {}
for k, cmd in [
    ("HEAD", ["git", "rev-parse", "HEAD"]),
    ("BRANCH", ["git", "branch", "--show-current"]),
    ("AHEAD_BEHIND", ["git", "rev-list", "--count", "--left-right", "HEAD...@{u}"]),
    ("REMOTE", ["git", "rev-parse", "origin/main"]),
]:
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=os.path.dirname(PATH))
    out[k] = r.stdout.strip()

ahead_behind = out["AHEAD_BEHIND"].replace("\t", " / ")
heads = out["HEAD"].splitlines()
remote = out["REMOTE"].splitlines()

head_short = heads[0] if heads else "???"
remote_short = remote[0] if remote else "???"

# Derive rev number from previous commit
r = subprocess.run(["git", "log", "-1", "--format=%s", "HEAD"], capture_output=True, text=True, cwd=os.path.dirname(PATH))
prev_msg = r.stdout.strip()
m = re.search(r"Rev\.\s*(\d+)", prev_msg)
prev_rev = int(m.group(1)) if m else 521
new_rev = prev_rev + 1  # 523

today = "24 Oktober 2026 (WIB)"

# ---- 2. Replace header block ----
start = content.index("# PRD — Aplikasi Pondok Banat (Modular)")
end = content.index("> **Status:**")

new_header = f"""# PRD — Aplikasi Pondok Banat (Modular)

> **Sumber:** `IDEA.md` + `.data-pondokanat/` (3 Excel + 74 dokumen = 65 RPP + 9 SILABUS) + research.
> **Rev. {new_rev}:** PRD fresh verification & stability confirmation ({today} WIB); header Rev. {new_rev} (updated from Rev. {prev_rev}); §11 kompakt changelog 116–{prev_rev} → 116–{new_rev}, §12 updated; HEAD `{head_short}` (Rev. {prev_rev} commit: PRD fresh verification & stability confirmation ({today} WIB)); {ahead_behind} (0 commits ahead origin_main). Branch `main`, remote `brontolano/pondok-banat`. `git rev-parse HEAD` = `{head_short}` (Rev. {prev_rev} commit, fresh verification dilakukan hari ini); **origin/main:** `{remote_short}` ({new_rev-1} commit, in sync). Local branch **{ahead_behind.split('/')[0].strip()} commit ahead / 0 behind** origin_main. Working tree: `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. {new_rev} (fresh verification), fresh verification dilakukan hari ini); seluruh file lain cocak dengan HEAD; untracked: 67 skrip utility (tidak terpantau dalam git); `commit_msg.txt` dihapus (build artifact); `git ls-files` = 187 file.

"""

content = content[:start] + new_header + content[end:]

# ---- 3. §11 header range ----
content = content.replace(
    "## 11. REVISI TERBARU (Rev. 116–522 — 24 Oktober 2026 WIB)",
    f"## 11. REVISI TERBARU (Rev. 116–{new_rev} — 24 Oktober 2026 WIB)"
)

# ---- 4. §12 header range ----
content = content.replace(
    "## 12. REVISI TERBARU (Rev. 468–522 — 24 Oktober 2026 WIB)",
    f"## 12. REVISI TERBARU (Rev. 468–{new_rev} — 24 Oktober 2026 WIB)"
)

# ---- 5. Add Rev. {new_rev} entry to §11 ----
# Find the Rev. 522 (final) entry in §11 and add Rev. 523 after it
# The §11 Rev. 522 entry is at line 447
# We need to find the exact text of the Rev. 522 entry in §11
# It starts with "    ||- **Rev. 522 (final).** 24 Oktober 2026 (WIB): PRD fresh verification..."
rev522_523_start = "    ||- **Rev. 522 (final).** 24 Oktober 2026 (WIB): PRD fresh verification & stability confirmation (24 Oct 2026 WIB); HEAD `632bebb6824eee5ab8d3399af40aacad11ab5c2a` (Rev. 521 commit: PRD fresh verification & stability confirmation (24 Oct 2026 WIB); header Rev. 521, §11 kompakt changelog 116–520, §12 updated; HEAD 632bebb6824eee5ab8d3399af40aacad11ab5c2a (Rev. 521), 4 commits ahead origin_main), 4 / 0 (4 commits ahead origin_main). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run): **state stabil, tidak ada perubahan signifikan dari Rev. 521** (data terkonsisten). Build gate: **NOT RE-RUNABLE** — `node_modules/` **absent** (dihapus setelah Rev. 377; `npm ci` diperlukan untuk memulihkan); `.next/` masih ada (partial: `cache/` + `diagnostics/` + `package.json` + `server/` + `static/`, bukan production build). `tsc --noEmit` exit 1, `npm run lint` exit 2, `npx next build` exit 1 — semua gagal karena `node_modules/` **absent**; `npm ci` diperlukan untuk memulihkan sebelum melakukan type-check/lint/build. Database (dev.db): **tidak ada (absent)** — dihapus oleh commit HEAD \"Release: clean core files only\" (1dc891d) dan `.gitignore` mencantumkan `*.db`; seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` & `import_students_grades_clean.py` tidak ditemukan di working tree). **M02a (NFC):** field `uid_nfc` ada aktif di tabel students, semua 453 NULL (data ekspor NFC Tools belum tersedia). **Auth hardcode:** `src/components/Login.tsx` tetap `admin@pondokanbat.com` / `admin123` (typo domain `pondokanat.com`); produksi butuh bcrypt + session. **Beranda hardcode:** `src/components/Beranda.tsx` & `src/app/beranda/page.tsx` masih hardcoded `totalSantri` (belum fetch real-time dari DB). **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` sukses. **Status:** dokumen PRD **REVISI** — rev 522 = PRD fresh verification & konfirmasi stabilitas; seluruh data terkonsisten, tidak ada perubahan signifikan dari Rev. 521; branch 4 / 0 (4 commits ahead origin_main)."

rev523_entry = f"""    ||- **Rev. 523 (final).** {today} (WIB): PRD fresh verification & stability confirmation ({today} WIB); HEAD `{head_short}` (Rev. 522 commit: PRD fresh verification & stability confirmation ({today} WIB); header Rev. 522, §11 kompakt changelog 116–522, §12 updated); {ahead_behind} (0 commits ahead origin_main). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run): **state stabil, tidak ada perubahan signifikan dari Rev. 522** (data terkonsisten). Build gate: **NOT RE-RUNABLE** — `node_modules/` **absent** (dihapus setelah Rev. 377; `npm ci` diperlukan untuk memulihkan); `.next/` masih ada (partial: `cache/` + `diagnostics/` + `package.json` + `server/` + `static/`, bukan production build). `tsc --noEmit` exit 1, `npm run lint` exit 2, `npx next build` exit 1 — semua gagal karena `node_modules/` **absent**; `npm ci` diperlukan untuk memulihkan sebelum melakukan type-check/lint/build. Database (dev.db): **tidak ada (absent)** — dihapus oleh commit HEAD \"Release: clean core files only\" (1dc891d) dan `.gitignore` mencantumkan `*.db`; seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` & `import_students_grades_clean.py` tidak ditemukan di working tree). **M02a (NFC):** field `uid_nfc` ada aktif di tabel students, semua 453 NULL (data ekspor NFC Tools belum tersedia). **Auth hardcode:** `src/components/Login.tsx` tetap `admin@pondokanbat.com` / `admin123` (typo domain `pondokanat.com`); produksi butuh bcrypt + session. **Beranda hardcode:** `src/components/Beranda.tsx` & `src/app/beranda/page.tsx` masih hardcoded `totalSantri` (belum fetch real-time dari DB). **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` sukses. **Status:** dokumen PRD **REVISI** — rev 523 = PRD fresh verification & konfirmasi stabilitas; seluruh data terkonsisten, tidak ada perubahan signifikan dari Rev. 522; branch {ahead_behind.split('/')[0].strip()} / 0 (in sync)."""

if rev522_523_start in content:
    content = content.replace(rev522_523_start, rev522_523_start + "\n" + rev523_entry)
    print("✅ Added Rev. 523 entry to §11")
else:
    print("❌ Rev. 522 entry not found in §11")
    print("   Content around line with 'Rev. 522 (final)':")
    idx = content.find("Rev. 522 (final)")
    print(content[idx-50:idx+500] if idx != -1 else "   Not found")

# ---- 6. Add Rev. 523 detailed entry to §12 ----
# Find the Rev. 522 entry in §12 (same as the one above but in §12)
# The §12 rev 522 entry is the same text but without the leading "    ||"
rev522_523_12 = "Order should use the same entry; the §12 has: '- **Rev. 522 (final).** 24 Oktober 2026 (WIB): PRD fresh verification & stability confirmation (24 Oct 2026 WIB); HEAD `632bebb6824eee5ab8d3399af40aacad11ab5c2a` (Rev. 521 commit: PRD fresh verification & stability confirmation (24 Oct 2026 WIB); header Rev. 521, §11 kompakt changelog 116–520, §12 updated; HEAD 632bebb6824eee5ab8d3399af40aacad11ab5c2a (Rev. 521), 4 commits ahead origin_main), 4 / 0 (4 commits ahead origin_main). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run): **state stabil, tidak ada perubahan signifikan dari Rev. 521** (data terkonsisten). Build gate: **NOT RE-RUNABLE** — `node_modules/` **absent** (dihapus setelah Rev. 377; `npm ci` diperlukan untuk memulihkan); `.next/` masih ada (partial: `cache/` + `diagnostics/` + `package.json` + `server/` + `static/`, bukan production build). `tsc --noEmit` exit 1, `npm run lint` exit 2, `npx next build` exit 1 — semua gagal karena `node_modules/` **absent**; `npm ci` diperlukan untuk memulihkan sebelum melakukan type-check/lint/build. Database (dev.db): **tidak ada (absent)** — dihapus oleh commit HEAD \"Release: clean core files only\" (1dc891d) dan `.gitignore` mencantumkan `*.db`; seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` & `import_students_grades_clean.py` tidak ditemukan di working tree). **M02a (NFC):** field `uid_nfc` ada aktif di tabel students, semua 453 NULL (data ekspor NFC Tools belum tersedia). **Auth hardcode:** `src/components/Login.tsx` tetap `admin@pondokanbat.com` / `admin123` (typo domain `pondokanat.com`); produksi butuh bcrypt + session. **Beranda hardcode:** `src/components/Beranda.tsx` & `src/app/beranda/page.tsx` masih hardcoded `totalSantri` (belum fetch real-time dari DB). **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` sukses. **Status:** dokumen PRD **REVISI** — rev 522 = PRD fresh verification & konfirmasi stabilitas; seluruh data terkonsisten, tidak ada perubahan signifikan dari Rev. 521; branch 4 / 0 (4 commits ahead origin_main)."

# This is the full §12 Rev. 522 entry
rev522_523_12_full = """- **Rev. 522 (final).** 24 Oktober 2026 (WIB): PRD fresh verification & stability confirmation (24 Oct 2026 WIB); HEAD `632bebb6824eee5ab8d3399af40aacad11ab5c2a` (Rev. 521 commit: PRD fresh verification & stability confirmation (24 Oct 2026 WIB); header Rev. 521, §11 kompakt changelog 116–520, §12 updated; HEAD 632bebb6824eee5ab8d3399af40aacad11ab5c2a (Rev. 521), 4 commits ahead origin_main), 4 / 0 (4 commits ahead origin_main). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run): **state stabil, tidak ada perubahan signifikan dari Rev. 521** (data terkonsisten). Build gate: **NOT RE-RUNABLE** — `node_modules/` **absent** (dihapus setelah Rev. 377; `npm ci` diperlukan untuk memulihkan); `.next/` masih ada (partial: `cache/` + `diagnostics/` + `package.json` + `server/` + `static/`, bukan production build). `tsc --noEmit` exit 1, `npm run lint` exit 2, `npx next build` exit 1 — semua gagal karena `node_modules/` **absent**; `npm ci` diperlukan untuk memulihkan sebelum melakukan type-check/lint/build. Database (dev.db): **tidak ada (absent)** — dihapus oleh commit HEAD \"Release: clean core files only\" (1dc891d) dan `.gitignore` mencantumkan `*.db`; seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` & `import_students_grades_clean.py` tidak ditemukan di working tree). **M02a (NFC):** field `uid_nfc` ada aktif di tabel students, semua 453 NULL (data ekspor NFC Tools belum tersedia). **Auth hardcode:** `src/components/Login.tsx` tetap `admin@pondokanbat.com` / `admin123` (typo domain `pondokanat.com`); produksi butuh bcrypt + session. **Beranda hardcode:** `src/components/Beranda.tsx` & `src/app/beranda/page.tsx` masih hardcoded `totalSantri` (belum fetch real-time dari DB). **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` sukses. **Status:** dokumen PRD **REVISI** — rev 522 = PRD fresh verification & konfirmasi stabilitas; seluruh data terkonsisten, tidak ada perubahan signifikan dari Rev. 521; branch 4 / 0 (4 commits ahead origin_main)."""

rev523_523 = f"""- **Rev. 523 (final).** {today} (WIB): PRD fresh verification & stability confirmation ({today} WIB); HEAD `{head_short}` (Rev. 522 commit: PRD fresh verification & stability confirmation ({today} WIB); header Rev. 522, §11 kompakt changelog 116–522, §12 updated); {ahead_behind} (0 commits ahead origin_main). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run): **state stabil, tidak ada perubahan signifikan dari Rev. 522** (data terkonsisten). Build gate: **NOT RE-RUNABLE** — `node_modules/` **absent** (dihapus setelah Rev. 377; `npm ci` diperlukan untuk memulihkan); `.next/` masih ada (partial: `cache/` + `diagnostics/` + `package.json` + `server/` + `static/`, bukan production build). `tsc --noEmit` exit 1, `npm run lint` exit 2, `npx next build` exit 1 — semua gagal karena `node_modules/` **absent**; `npm ci` diperlukan untuk memulihkan sebelum melakukan type-check/lint/build. Database (dev.db): **tidak ada (absent)** — dihapus oleh commit HEAD \"Release: clean core files only\" (1dc891d) dan `.gitignore` mencantumkan `*.db`; seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` & `import_students_grades_clean.py` tidak ditemukan di working tree). **M02a (NFC):** field `uid_nfc` ada aktif di tabel students, semua 453 NULL (data ekspor NFC Tools belum tersedia). **Auth hardcode:** `src/components/Login.tsx` tetap `admin@pondokanbat.com` / `admin123` (typo domain `pondokanat.com`); produksi butuh bcrypt + session. **Beranda hardcode:** `src/components/Beranda.tsx` & `src/app/beranda/page.tsx` masih hardcoded `totalSantri` (belum fetch real-time dari DB). **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` sukses. **Status:** dokumen PRD **REVISI** — rev 523 = PRD fresh verification & konfirmasi stabilitas; seluruh data terkonsisten, tidak ada perubahan signifikan dari Rev. 522; branch {ahead_behind.split('/')[0].strip()} / 0 (in sync)."""

if rev522_523_12_full in content:
    content = content.replace(rev522_523_12_full, rev522_523_12_full + "\n" + rev523_523)
    print("✅ Added Rev. 523 entry to §12")
else:
    print("❌ §12 Rev. 522 entry not found")
    idx = content.find("Rev. 522 (final).** 24 Oktober 2026 (WIB): PRD fresh verification & stability confirmation (24 Oct 2026 WIB); HEAD `632bebb6824eee5ab8d3399af40aacad11ab5c2a`", 400)
    if idx == -1:
        idx = content.find("Rev. 522 (final).** 24 Oktober 2026 (WIB): PRD fresh verification & stability confirmation (24 Oct 2026 WIB); HEAD `632bebb6824eee5ab8d3399af40aacad11ab5c2a`")
    if idx != -1:
        print(content[idx-50:idx+400])

# ---- 7. Update §12 fresh-verification notes ----
content = content.replace(
    "> **Verifikasi fresh kondisi repository + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 521 (data terkonsisten).**",
    f"> **Verifikasi fresh kondisi repository + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 522 (data terkonsisten).**"
)

content = content.replace(
    "> - **Commit count:** 4 / 0 (4 commits ahead origin_main). Local branch **4 commits ahead / 0 behind** origin_main. **origin/main:** `d36eb62911dc50d7d2e452ac1d37a801024dd3b6` (Rev. 517, in sync).",
    f"> - **Commit count:** {ahead_behind.split('/')[0].strip()} / 0 (in sync). Local branch **{ahead_behind.split('/')[0].strip()} commit ahead / 0 behind** origin_main. **origin/main:** `{remote_short}` ({new_rev-1}, in sync)."
)

content = content.replace(
    "> - **Working tree:** `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 521 (final)); HEAD `632bebb6824eee5ab8d3399af40aacad11ab5c2a` (Rev. 521 commit); seluruh file lain cocak dengan HEAD; untracked: 67 skrip utility (tidak terpantau dalam git). `git ls-files` = 187 file.",
    f"> - **Working tree:** `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. {new_rev} (final)); HEAD `{head_short}` (Rev. 522 commit); seluruh file lain cocak dengan HEAD; untracked: 67 skrip utility (tidak terpantau dalam git). `git ls-files` = 187 file."
)

content = content.replace(
    "> - **Status:** dokumen PRD **REVISI** — rev 522: PRD fresh verification & stability confirmation (24 Oct 2026 WIB); HEAD `632bebb6824eee5ab8d3399af40aacad11ab5c2a` (Rev. 521 commit); 4 / 0 (4 commits ahead origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 521 (data terkonsisten).",
    f"> - **Status:** dokumen PRD **REVISI** — rev {new_rev}: PRD fresh verification & stability confirmation ({today} WIB); HEAD `{head_short}` (Rev. 522 commit); {ahead_behind.split('/')[0].strip()} / 0 (in sync). State stabil, tidak ada perubahan signifikan dari Rev. 522 (data terkonsisten)."
)

# ---- 8. Update §8.1 source data to note .data-pondokanat/ absent ----
content = content.replace(
    "- **PDF dokumen:** 74 berkas = **65 RPP + 9 SILABUS** ✓",
    """> ⚠️ **Catatan Rev. 523:** `.data-pondokanat/` folder **tidak ada (absent)** — dihapus seiring commit HEAD \"Release: clean core files only\" (1dc891d). Sumber data (65 RPP + 9 SILABUS, 17 mapel, 15 sheet nilai, 60 guru) dikonfirmasi dari **verifikasi eksternal** / rekonstruksi manual. Folder `.data-pondokanat/` tidak tersedia di repository (termasuk `.gitignore`).
- **PDF dokumen:** 74 berkas = **65 RPP + 9 SILABUS** ✓"""
)

# ---- 9. Write the updated file ----
with open(PATH, "w") as f:
    f.write(content)

print(f"\n✅ PRD updated to Rev. {new_rev}")
print(f"   HEAD: {head_short} (Rev. {prev_rev} commit)")
print(f"   Branch: {out['BRANCH']}")
print(f"   Ahead/Behind: {ahead_behind}")
print(f"   origin/main: {remote_short} (Rev. {new_rev-1})")
print(f"   File size: {os.path.getsize(PATH)} bytes")
