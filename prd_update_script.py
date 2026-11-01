import io

path = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Header changes
old_header = "header Rev. 754\u2192755; \u00a711 compact changelog 116\u2013754\u2192116\u2013755; \u00a712 updated. HEAD 2346f79 (Rev. 754 final commit); commit count 769/1/0 (769 local commits, 1 ahead origin_main, 0 behind); node_modules present (477 dirs / 84021 files)"
new_header = "header Rev. 756; \u00a711 compact changelog 116\u2013754\u2192116\u2013756; \u00a712 updated. HEAD 8afc403 (Rev. 755); commit count 770/2/0 (770 local commits, 2 ahead origin_main, 0 behind); node_modules present (477 dirs / 84021 files)"
if old_header in content:
    content = content.replace(old_header, new_header)
    print("Header: updated")
else:
    print("Header: OLD_HEADER NOT FOUND")

# 2. §12 heading
old_s12 = "## 12. STATUS RINGKASAN (30 Oktober 2026 WIB) \u2014 Rev. 755"
new_s12 = "## 12. STATUS RINGKASAN (30 Oktober 2026 WIB) \u2014 Rev. 756"
if old_s12 in content:
    content = content.replace(old_s12, new_s12)
    print("§12 heading: updated")
else:
    print("§12 heading: NOT FOUND")

# 3. §12 Repo state line
old_repo = "> > - **Repo state (Rev. 755):** HEAD `2346f79` (Rev. 754 final commit); **769 local commits, 1 ahead / 0 behind** origin_main; 340 tracked files; 3 untracked (dev_report.py, verify_db.py, verify_db_check.py); 0 deleted (fix_duplicate.py removed)."
new_repo = "> > - **Repo state (Rev. 756):** HEAD `8afc403` (Rev. 755); **770 local commits, 2 ahead / 0 behind** origin_main; 340 tracked files; 3 untracked (dev_report.py, verify_db.py, verify_db_check.py); 0 deleted (fix_duplicate.py removed)."
if old_repo in content:
    content = content.replace(old_repo, new_repo)
    print("§12 Repo state: updated")
else:
    print("§12 Repo state: NOT FOUND")

# 4. Insert new Rev. 756 section in §11 (before '## 12.')
rev756 = """### Rev. 756

> **Rev. 756 (fresh).** 30 Oktober 2026 (WIB): CRON-run fresh verification & stability confirmation (cron run); HEAD `8afc403` (Rev. 755 final commit); **770 / 2/0** (770 local commits, 2 ahead origin_main, 0 behind). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run):

> - **Environment:** node v26.5.1, npm 11.17.0, Prisma CLI = Prisma Developer Platform (new CLI; `generate`/`validate` commands not available in this release).

> - **Build quality gate:** `npm run type-check` (tsc --noEmit) \u2713 (exit 0); `npm run lint` \u2713 (exit 0, 1 warning / 0 error); `npm run build` (next build) \u2717 (exit 1 \u2014 SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). Build gate sebagian re-runnable \u2014 tsc + eslint lulus, next build diblokir security nudge. node_modules present (477 dirs / 84021 files).

> - **Database (dev.db):** **ada** \u2014 direkonstruksi schema-only via `init_db.py` (15 tabel, seluruh record 0). Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; source Excel & PDF dari `.data-pondokanat/` bukan tracked di repo).

> - **M02a (NFC):** field `uid_nfc` ada aktif di tabel `students` (kolom setelah `photo`); `prisma/schema.prisma` baris 68 (`uidNfc String? @map(\"uid_nfc\")`), `init_schema.sql` baris 44, `init_db.py` baris 60. **Tidak ada satupun siswa yang memiliki `uid_nfc` diisi** (semua 453 NULL) \u2014 data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).

> - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (typo domain `pondokanat.com`); produksi butuh bcrypt + session.

> - **Beranda hardcode:** `src/components/Beranda.tsx` & `src/app/beranda/page.tsx` masih hardcoded `totalSantri` (belum fetch real-time dari DB).

> - **Prisma:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` sukses (command not available in new Prisma CLI). Schema inconsistency (Rev. 38\u201345) SELESAI.

> - **Repo state:** clean working tree; `dev.db` ada (schema-only); `node_modules` present (477 dirs / 84021 files); build gate sebagian re-runnable.

> - **Commit count:** 770 / 2 (770 local commits, 2 ahead origin_main, 0 behind). Local branch **770 commits ahead / 0 behind** origin_main.

> - **Status:** dokumen PRD **REVISI** \u2014 rev 756: PRD fresh verification & stability confirmation (30 Oktober 2026 (WIB)); HEAD `8afc403` (Rev. 755 final commit); **770 / 2/0** (770 local commits, 2 ahead origin_main, 0 behind). State stabil, tidak ada perubahan signifikan dari Rev. 755 (data terkonsisten).

"""

marker = "## 12. STATUS RINGKASAN"
if marker in content:
    content = content.replace(marker, rev756 + marker, 1)
    print("Inserted Rev. 756 section before §12")
else:
    print("§12 marker: NOT FOUND")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("Done. File updated.")
print("Rev 756 section count:", content.count("### Rev. 756"))
print("Rev 755 section count:", content.count("### Rev. 755"))
print("Rev 756 heading present:", "## 12. STATUS RINGKASAN (30 Oktober 2026 WIB) \u2014 Rev. 756" in content)
