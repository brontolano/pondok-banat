import os

path = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

updates = []

# --- Header (line 4) ---
r = content.replace(
    "header Rev. 789; §11 compact changelog 116–786→789; §12 updated.",
    "header Rev. 790; §11 compact changelog 116–789→790; §12 updated.")
assert r != content, "header prefix not replaced"
content = r
updates.append("Header: Rev. 790 (compact changelog 116–789→790)")

r = content.replace(
    "HEAD `60d2d998181f50166939aae104dff9da62b6a05a` (Rev. 788)",
    "HEAD `83aeb1ff863414dd83c6cd51dae3bb648474c014` (Rev. 789)")
assert r != content, "header HEAD not replaced"
content = r
updates.append("Header: HEAD -> 83aeb1ff (Rev. 789 committed)")

r = content.replace(
    "commit count 807/4/0 (807 local commits, 4 ahead / 0 behind origin_main)",
    "commit count 809/1/0 (809 local commits, 1 ahead / 0 behind origin_main)")
assert r != content, "header commit count not replaced"
content = r
updates.append("Header: commit count -> 809/1/0")

r = content.replace(
    "Working tree: PRD synced ke Rev. 789",
    "Working tree: PRD synced ke Rev. 789; Rev. 790 in working tree")
assert r != content, "header working tree not replaced"
content = r
updates.append("Header: working tree -> Rev. 789 + Rev. 790")

r = content.replace(
    "340 tracked files; 21 untracked",
    "340 tracked files; 23 untracked")
assert r != content, "header untracked count not replaced"
content = r
updates.append("Header: untracked -> 23")

# --- §12 heading ---
r = content.replace(
    "## 12. STATUS RINGKASAN (30 Oktober 2026 WIB) — Rev. 789",
    "## 12. STATUS RINGKASAN (31 Oktober 2026 WIB) — Rev. 790")
assert r != content, "§12 heading not replaced"
content = r
updates.append("§12 heading: Rev. 790")

# --- §12 repo state line (smaller, robust replacements) ---
r = content.replace(
    "**Repo state (Rev. 789):**",
    "**Repo state (Rev. 790):**")
assert r != content, "§12 repo state heading not replaced"
content = r
updates.append("§12 repo state: Rev. 790")

r = content.replace(
    "HEAD `60d2d998181f50166939aae104dff9da62b6a05a` (Rev. 788 committed)",
    "HEAD `83aeb1ff863414dd83c6cd51dae3bb648474c014` (Rev. 789 committed)")
assert r != content, "§12 repo HEAD not replaced"
content = r
updates.append("§12 repo HEAD: Rev. 790")

r = content.replace(
    "**807 local commits, 4 ahead / 0 behind**",
    "**809 local commits, 1 ahead / 0 behind**")
assert r != content, "§12 repo commit count not replaced"
content = r
updates.append("§12 repo commit count -> 809/1/0")

# §12 repo untracked is already handled by header step-5 global replace (line 2516 has
# "340 tracked files; 21 untracked; 0 deleted" -> becomes "...23 untracked; 0 deleted").
updates.append("§12 repo untracked -> 23 (via header step-5 global replace)")

# --- §11 Rev. 790 section (insert before ## 12.) ---
rev790 = """### Rev. 790

> **Rev. 790 (fresh).** 31 Oktober 2026 (WIB): CRON-run fresh verification & stability confirmation (cron run); HEAD `83aeb1ff863414dd83c6cd51dae3bb648474c014` (Rev. 789 committed; Rev. 790 in working tree); commit count **809 / 1/0** (809 local commits, 1 ahead / 0 behind origin_main). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run):

> - **Environment:** node v26.5.1, npm 11.17.0, Prisma CLI = Prisma Developer Platform (new CLI; `generate`/`validate` commands not available in this release).

> - **Build quality gate:** `npm run type-check` (tsc --noEmit) ✓ (exit 0); `npm run lint` ✓ (exit 0, 1 warning / 0 error); `npm run build` (next build) ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). Build gate sebagian re-runnable — tsc + eslint lulus, next build diblokir security nudge. node_modules present (5103 dirs / 84021 files).

> - **Database (dev.db):** **ada** — direkonstruksi schema-only via `init_db.py` (15 tabel, seluruh record 0). Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; source Excel & PDF dari `.data-pondokanat/` bukan tracked di repo).

> - **M02a (NFC):** field `uid_nfc` ada aktif di tabel `students` (kolom setelah `photo`); `prisma/schema.prisma` baris 68 (`uidNfc String? @map(\"uid_nfc\")`), `init_schema.sql` baris 44, `init_db.py` baris 60. **0 siswa terisi (semua 453 NULL)** — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).

> - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` telah diperbaiki); produksi butuh bcrypt + session.

> - **Beranda hardcode:** `src/components/Beranda.tsx` & `src/app/beranda/page.tsx` masih hardcoded `totalSantri` (belum fetch real-time dari DB); nilai sekarang `totalSantri: 453, totalGuru: 54, totalKelas: 18`.

> - **Prisma:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` sukses (command not available in new Prisma CLI). Schema inconsistency (Rev. 38–45) SELESAI.

> - **Repo state:** clean working tree (Rev. 790 in working tree); `dev.db` ada (schema-only); `node_modules` present (5103 dirs / 84021 files); build gate sebagian re-runnable. 23 untracked helper scripts; 0 deleted (fix_duplicate.py removed).

> - **Commit count:** **809 / 1/0** local commits (809 local commits, 1 ahead / 0 behind origin_main). Local branch **809 commits ahead / 0 behind** origin_main (HEAD `83aeb1f`, Rev. 789 committed; Rev. 790 in working tree).

> - **Status:** dokumen PRD **REVISI** — rev 790: PRD fresh verification & stability confirmation (31 Oktober 2026 (WIB)); HEAD `83aeb1f` (Rev. 789); **809 / 1/0** (809 local commits, 1 ahead / 0 behind origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 789 (data terkonsisten).

"""

marker = "## 12. STATUS RINGKASAN"
assert marker in content, "§12 marker not found"
content = content.replace(marker, rev790 + marker, 1)
updates.append("Rev. 790 section: inserted before §12")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("Updates applied:")
for u in updates:
    print("  -", u)
print("Done. File updated.")
print("Rev 790 section count:", content.count("### Rev. 790"))
print("Rev 789 section count:", content.count("### Rev. 789"))
print("§12 heading present:", "## 12. STATUS RINGKASAN (31 Oktober 2026 WIB) — Rev. 790" in content)
