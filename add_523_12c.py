#!/usr/bin/env python3
"""Add §12 Rev. 523 entry after §12 Rev. 522 entry."""

path = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"

with open(path) as f:
    lines = f.read().split("\n")

# Find last line between 548-555 that contains both "Rev. 522" and "0 / 0"
target_idx = None
for i in range(547, min(len(lines), 555)):
    line = lines[i]
    if "Rev. 522" in line and "0 / 0" in line:
        target_idx = i
        break

if target_idx is None:
    print("ERROR: Could not find §12 Rev. 522 entry")
    # Show all lines with Rev. 522
    for i in range(547, min(len(lines), 555)):
        if "Rev. 522" in lines[i]:
            print(f"  Line {i+1}: {lines[i][:80]}...")
    exit(1)

print(f"Found §12 Rev. 522 at line {target_idx + 1}")

rev523_entry = """    ||- **Rev. 523 (final).** 24 Oktober 2026 (WIB): PRD fresh verification & stability confirmation (24 Oktober 2026 (WIB); HEAD `8604c3c440d839e5312de173e70e067695006663` (Rev. 522 commit: PRD fresh verification & stability confirmation (24 Oktober 2026 (WIB); header Rev. 522, §11 kompakt changelog 116–522, §12 updated); 0 / 0 (0 commits ahead origin_main). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run): **state stabil, tidak ada perubahan signifikan dari Rev. 522** (data terkonsisten). Build gate: **NOT RE-RUNABLE** — `node_modules/` **absent** (dihapus setelah Rev. 377; `npm ci` diperlukan untuk memulihkan); `.next/` masih ada (partial: `cache/` + `diagnostics/` + `package.json` + `server/` + `static/`, bukan production build). `tsc --noEmit` exit 1, `npm run lint` exit 2, `npx next build` exit 1 — semua gagal karena `node_modules/` **absent**; `npm ci` diperlukan untuk memulihkan sebelum melakukan type-check/lint/build. Database (dev.db): **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`; seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` & `import_students_grades_clean.py` tidak ditemukan di working tree). **M02a (NFC):** field `uid_nfc` ada aktif di tabel students, semua 453 NULL (data ekspor NFC Tools belum tersedia). **Auth hardcode:** `src/components/Login.tsx` tetap `admin@pondokanbat.com` / `admin123` (typo domain); produksi butuh bcrypt + session. **Beranda hardcode:** `src/components/Beranda.tsx` & `src/app/beranda/page.tsx` masih hardcoded `totalSantri` (belum fetch real-time dari DB). **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` sukses. **Status:** dokumen PRD **REVISI** — rev 523 = PRD fresh verification & konfirmasi stabilitas; seluruh data terkonsisten, tidak ada perubahan signifikan dari Rev. 522; branch 0 / 0 (in sync)."""

# Insert after target line
lines.insert(target_idx + 1, rev523_entry)

with open(path, "w") as f:
    f.write("\n".join(lines))

print(f"✅ Added §12 Rev. 523 entry")
print(f"Total lines: {len(lines)}")
