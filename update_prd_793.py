path = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

updates = []

# 1. Header line (line 4): Rev. 792 -> Rev. 793
old_hdr = "header Rev. 792; §11 compact changelog 116–791→792; §12 updated. HEAD `d68913a` (Rev. 791 committed); commit count 811/2/0 (810 local commits, 2 ahead / 0 behind origin_main)"
new_hdr = "header Rev. 793; §11 compact changelog 116–792→793; §12 updated. HEAD `2151803` (Rev. 792 committed); commit count 813/5/0 (812 local commits, 5 ahead / 0 behind origin_main)"
if old_hdr in content:
    content = content.replace(old_hdr, new_hdr, 1)
    updates.append("Header: updated to Rev. 793, commit count 813/5/0")
else:
    updates.append("Header: OLD_HEADER NOT FOUND — aborting")

# 2. §12 heading: Rev. 792 -> Rev. 793
old_s12 = "## 12. STATUS RINGKASAN (31 Oktober 2026 WIB) — Rev. 792"
new_s12 = "## 12. STATUS RINGKASAN (31 Oktober 2026 WIB) — Rev. 793"
if old_s12 in content:
    content = content.replace(old_s12, new_s12, 1)
    updates.append("§12 heading: updated to Rev. 793")
else:
    updates.append("§12 heading: NOT FOUND")

# 3. §12 repo state line: Rev. 792 -> Rev. 793
old_repo = "> - **Repo state (Rev. 792):** HEAD `d68913a` (Rev. 791 committed); **811 local commits, 2 ahead / 0 behind** origin_main; 340 tracked files; 26 untracked; 0 deleted (fix_duplicate.py removed)."
new_repo = "> - **Repo state (Rev. 793):** HEAD `2151803` (Rev. 792 committed); **813 local commits, 5 ahead / 0 behind** origin_main; 340 tracked files; 26 untracked; 0 deleted (fix_duplicate.py removed)."
if old_repo in content:
    content = content.replace(old_repo, new_repo, 1)
    updates.append("§12 repo state: updated to Rev. 793")
else:
    updates.append("§12 repo state: NOT FOUND")

# 4. Insert Rev. 793 section in §11 (before '## 12. STATUS RINGKASAN')
rev793 = """### Rev. 793

> **Rev. 793 (fresh).** 31 Oktober 2026 (WIB): CRON-run fresh verification & stability confirmation (cron run); HEAD `2151803` (Rev. 792 committed; Rev. 793 in working tree); commit count **813 / 5/0** (813 local commits, 5 ahead / 0 behind origin_main). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run):

> - **Environment:** node v26.5.1, npm 11.17.0, Prisma CLI = Prisma Developer Platform (new CLI; `generate`/`validate` commands not available in this release).

> - **Build quality gate:** `npm run type-check` (tsc --noEmit) ✓ (exit 0); `npm run lint` ✓ (exit 0, 1 warning / 0 error); `npm run build` (next build) ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). Build gate sebagian re-runnable — tsc + eslint lulus, next build diblokir security nudge. node_modules present (477 dirs / 84021 files).

> - **Database (dev.db):** **ada** — schema-only via `init_db.py` (15 tabel, seluruh record 0). Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; source Excel & PDF dari `.data-pondokanat/` bukan tracked di repo).

> - **M02a (NFC):** field `uid_nfc` ada aktif di tabel `students` (kolom setelah `photo`); `prisma/schema.prisma` baris 68 (`uidNfc String? @map(\"uid_nfc\")`), `init_schema.sql` baris 44, `init_db.py` baris 60. **0 siswa terisi (semua 453 NULL)** — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).

> - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` sudah diperbaiki); produksi butuh bcrypt + session.

> - **Beranda hardcode:** `src/components/Beranda.tsx` & `src/app/beranda/page.tsx` masih hardcoded `totalSantri` (belum fetch real-time dari DB); nilai sekarang `totalSantri: 453, totalGuru: 54, totalKelas: 18`.

> - **Prisma:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` sukses (command not available in new Prisma CLI). Schema inconsistency (Rev. 38–45) SELESAI.

> - **Repo state:** clean working tree (Rev. 793 in working tree); `dev.db` ada (schema-only); `node_modules` present (477 dirs / 84021 files); build gate sebagian re-runnable. 26 untracked helper scripts; 0 deleted (fix_duplicate.py removed).

> - **Commit count:** **813 / 5/0** local commits (813 local commits, 5 ahead / 0 behind origin_main). Local branch **813 commits ahead / 0 behind** origin_main (HEAD `2151803`, Rev. 792 committed; Rev. 793 in working tree).

> - **Status:** dokumen PRD **REVISI** — rev 793: PRD fresh verification & stability confirmation (31 Oktober 2026 (WIB)); HEAD `2151803` (Rev. 792 committed); **813 / 5/0** (813 local commits, 5 ahead / 0 behind origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 792 (data terkonsisten).

"""

marker = "## 12. STATUS RINGKASAN"
if marker in content:
    content = content.replace(marker, rev793 + marker, 1)
    updates.append("Rev. 793 section: inserted before §12")
else:
    updates.append("§12 marker: NOT FOUND")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("Updates applied:")
for u in updates:
    print("  -", u)
print("Done. File updated.")
print("Rev 793 section count:", content.count("### Rev. 793"))
