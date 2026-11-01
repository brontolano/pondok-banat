path = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

updates = []

# 1. Header line (line 4): Rev. 791 -> Rev. 792
old_hdr = "header Rev. 791; §11 compact changelog 116–790→791; §12 updated. HEAD `c603cf6` (Rev. 790); commit count 810/2/0"
new_hdr = "header Rev. 792; §11 compact changelog 116–791→792; §12 updated. HEAD `d68913a` (Rev. 791 committed); commit count 811/2/0"
if old_hdr in content:
    content = content.replace(old_hdr, new_hdr, 1)
    updates.append("Header: updated to Rev. 792, commit count 811/2/0")
else:
    updates.append("Header: OLD_HEADER NOT FOUND")

# 2. §12 heading: Rev. 791 -> Rev. 792
old_s12 = "## 12. STATUS RINGKASAN (31 Oktober 2026 WIB) — Rev. 791"
new_s12 = "## 12. STATUS RINGKASAN (31 Oktober 2026 WIB) — Rev. 792"
if old_s12 in content:
    content = content.replace(old_s12, new_s12, 1)
    updates.append("§12 heading: updated to Rev. 792")
else:
    updates.append("§12 heading: NOT FOUND")

# 3. §12 repo state line: Rev. 791 -> Rev. 792
old_repo = "> - **Repo state (Rev. 791):** HEAD `c603cf6` (Rev. 790 committed); **810 local commits, 2 ahead / 0 behind** origin_main; 340 tracked files; 23 untracked; 0 deleted (fix_duplicate.py removed)."
new_repo = "> - **Repo state (Rev. 792):** HEAD `d68913a` (Rev. 791 committed); **811 local commits, 2 ahead / 0 behind** origin_main; 340 tracked files; 25 untracked; 0 deleted (fix_duplicate.py removed)."
if old_repo in content:
    content = content.replace(old_repo, new_repo, 1)
    updates.append("§12 repo state: updated to Rev. 792")
else:
    updates.append("§12 repo state: NOT FOUND")

# 4. Insert Rev. 792 section in §11 (before '## 12.')
rev792 = """### Rev. 792

> **Rev. 792 (fresh).** 31 Oktober 2026 (WIB): CRON-run fresh verification & stability confirmation (cron run); HEAD `d68913a` (Rev. 791 committed; Rev. 792 in working tree); commit count **811 / 2/0** (811 local commits, 2 ahead / 0 behind origin_main). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run):

> - **Environment:** node v26.5.1, npm 11.17.0, Prisma CLI = Prisma Developer Platform (new CLI; `generate`/`validate` commands not available in this release).
>
> - **Build quality gate:** `npm run type-check` (tsc --noEmit) ✓ (exit 0); `npm run lint` ✓ (exit 0, 1 warning / 0 error); `npm run build` (next build) ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). Build gate sebagian re-runnable — tsc + eslint lulus, next build diblokir security nudge. node_modules present (477 dirs / 84021 files).
>
> - **Database (dev.db):** **ada** — schema-only via `init_db.py` (15 tabel, seluruh record 0). Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; source Excel & PDF dari `.data-pondokanat/` bukan tracked di repo).
>
> - **M02a (NFC):** field `uid_nfc` ada aktif di tabel `students` (kolom setelah `photo`); `prisma/schema.prisma` baris 68 (`uidNfc String? @map(\\"uid_nfc\\")`), `init_schema.sql` baris 44, `init_db.py` baris 60. **0 siswa terisi (semua 453 NULL)** — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
>
> - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` sudah diperbaiki); produksi butuh bcrypt + session.
>
> - **Beranda hardcode:** `src/components/Beranda.tsx` & `src/app/beranda/page.tsx` masih hardcoded `totalSantri` (belum fetch real-time dari DB); nilai sekarang `totalSantri: 453, totalGuru: 54, totalKelas: 18`.
>
> - **Prisma:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` sukses (command not available in new Prisma CLI). Schema inconsistency (Rev. 38–45) SELESAI.
>
> - **Repo state:** clean working tree (Rev. 792 in working tree); `dev.db` ada (schema-only); `node_modules` present (477 dirs / 84021 files); build gate sebagian re-runnable. 25 untracked helper scripts; 0 deleted (fix_duplicate.py removed).
>
> - **Commit count:** **811 / 2/0** local commits (811 local commits, 2 ahead / 0 behind origin_main). Local branch **811 commits ahead / 0 behind** origin_main (HEAD `d68913a`, Rev. 791 committed; Rev. 792 in working tree).
>
> - **Status:** dokumen PRD **REVISI** — rev 792: PRD fresh verification & stability confirmation (31 Oktober 2026 (WIB)); HEAD `d68913a` (Rev. 791 committed); **811 / 2/0** (811 local commits, 2 ahead / 0 behind origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 791 (data terkonsisten).

"""

marker = "## 12. STATUS RINGKASAN"
if marker in content:
    content = content.replace(marker, rev792 + marker, 1)
    updates.append("Rev. 792 section: inserted before §12")
else:
    updates.append("§12 marker: NOT FOUND")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("Updates applied:")
for u in updates:
    print("  -", u)
print("Done. File updated.")
print("Rev 792 section count:", content.count("### Rev. 792"))
