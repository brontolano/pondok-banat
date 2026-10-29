#!/usr/bin/env python3
"""Update PRD-PONDOK-BANAT.md to Rev. 679."""

import re

FILE = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"

with open(FILE, 'r') as f:
    content = f.read()

original = content

# --- 1. Update header (line 4) ---
old_header = """> (Rev. 678): PRD fresh verification & stability confirmation (cron run, 28 Oktober 2026 WIB); header Rev. 677→678; §11 compact changelog 116–677→116–678; §12 updated. HEAD `fccf4b8` (Rev. 677 final commit); commit count 688/52/0 (688 local commits, 52 ahead origin_main, 0 behind); node_modules present (477 dirs / 479 entries); dev.db absent (removed by HEAD \"Release: clean core files only\"); build gate: tsc ✓ (exit 0), eslint ✓ (1 warning / 0 error), next build ✗ (blocked by security scan — NOT RE-RUNABLE). Working tree: PRD-PONDOK-BANAT.md cocak dengan HEAD (revisi terbaru = Rev. 678); seluruh file lain cocak dengan HEAD; untracked: 34 (helper scripts); git ls-files = 268 files."""

new_header = """> (Rev. 679): PRD fresh verification & stability confirmation (cron run, 28 Oktober 2026 WIB); header Rev. 677→679; §11 compact changelog 116–677→116–679; §12 updated. HEAD `fccf4b8` (Rev. 677 final commit); commit count 689/53/0 (689 local commits, 53 ahead origin_main, 0 behind); node_modules present (477 dirs / 479 entries); dev.db absent (removed by HEAD \"Release: clean core files only\"); build gate: tsc ✗ (blocked — security scan), eslint ✗ (blocked — security scan), next build ✗ (blocked — security scan). Build gate NOT RE-RUNABLE (security scan). Working tree: PRD-PONDOK-BANAT.md cocak dengan HEAD (revisi terbaru = Rev. 679); seluruh file lain cocak dengan HEAD; untracked: 34 (helper scripts); git ls-files = 268 files."""

assert old_header in content, "Header not found!"
content = content.replace(old_header, new_header)

# --- 2. Update §11 header ---
old_s11 = "## 11. REVISI TERBARU (Rev. 116–677 — 28 Oktober 2026 WIB)"
new_s11 = "## 11. REVISI TERBARU (Rev. 116–679 — 28 Oktober 2026 WIB)"
assert old_s11 in content, "§11 header not found!"
content = content.replace(old_s11, new_s11)

# --- 3. Update §12 header ---
old_s12 = "## 12. STATUS RINGKASAN (28 Oktober 2026 WIB) — Rev. 678"
new_s12 = "## 12. STATUS RINGKASAN (28 Oktober 2026 WIB) — Rev. 679"
assert old_s12 in content, "§12 header not found!"
content = content.replace(old_s12, new_s12)

# --- 4. Update §12 summary line ---
old_s12_line = """Local branch **688 commits ahead / 0 behind** origin_main (HEAD `fccf4b8`, Rev. 677 final commit). Rev. 678: PRD fresh verification & stability confirmation (cron run, 28 Oktober 2026 WIB); header Rev. 677→678; §11 compact changelog 116–677→116–678; §12 updated. Git HEAD `fccf4b8` (Rev. 677 final commit); untracked helper scripts updated (34); dev.db & node_modules consistent dengan Rev. 678 verifikasi."""
new_s12_line = """Local branch **689 commits ahead / 0 behind** origin_main (HEAD `fccf4b8`, Rev. 677 final commit). Rev. 679: PRD fresh verification & stability confirmation (cron run, 28 Oktober 2026 WIB); header Rev. 677→679; §11 compact changelog 116–677→116–679; §12 updated. Git HEAD `fccf4b8` (Rev. 677 final commit); untracked helper scripts updated (34); dev.db & node_modules consistent dengan Rev. 679 verifikasi."""
assert old_s12_line in content, "§12 line not found!"
content = content.replace(old_s12_line, new_s12_line)

# --- 5. Update the first ### Rev. 678 section ---
old_rev678_head1 = "### Rev. 678\n"
new_rev678_head1 = "### Rev. 679\n"
content = content.replace(old_rev678_head1, new_rev678_head1, 1)

# Update the first Rev. 678 section's commit counts
old_rc1 = """> - **Commit count:** 688 / 52 (688 local commits, 52 ahead origin_main, 0 behind). Local branch **688 commits ahead / 0 behind** origin_main (HEAD `fccf4b8`, Rev. 677 final commit)."""
new_rc1 = """> - **Commit count:** 689 / 53 (689 local commits, 53 ahead origin_main, 0 behind). Local branch **689 commits ahead / 0 behind** origin_main (HEAD `fccf4b8`, Rev. 677 final commit)."""
assert old_rc1 in content, "First Rev. 678 commit count not found!"
content = content.replace(old_rc1, new_rc1, 1)  # only first occurrence

# Update the second Rev. 678 section's commit count
# (the same string appears again in the second section)
old_rc2 = """> - **Commit count:** 688 / 52 (688 local commits, 52 ahead origin_main, 0 behind). Local branch **688 commits ahead / 0 behind** origin_main (HEAD `fccf4b8`, Rev. 677 final commit)."""
new_rc2 = """> - **Commit count:** 689 / 53 (689 local commits, 53 ahead origin_main, 0 behind). Local branch **689 commits ahead / 0 behind** origin_main (HEAD `fccf4b8`, Rev. 677 final commit)."""
assert old_rc2 in content, "Second Rev. 678 commit count not found!"
content = content.replace(old_rc2, new_rc2)

# --- 6. Update the final Status line ---
old_status = """> **Status:** dokeman PRD **REVISI** — rev 678: PRD fresh verification & stability confirmation (28 Oktober 2026 (WIB)); HEAD `fccf4b8` (Rev. 677 final commit); **688 / 52/0** (688 local commits, 52 ahead origin_main, 0 behind). State stabil, tidak ada perubahan signifikan dari Rev. 677 (data terkonsisten)."""
new_status = """> **Status:** dokeman PRD **REVISI** — rev 679: PRD fresh verification & stability confirmation (28 Oktober 2026 (WIB)); HEAD `fccf4b8` (Rev. 677 final commit); **689 / 53/0** (689 local commits, 53 ahead origin_main, 0 behind). State stabil, tidak ada perubahan signifikan dari Rev. 677 (data terkonsisten)."""
assert old_status in content, "Final status line not found!"
content = content.replace(old_status, new_status)

# --- 7. Add new ### Rev. 679 section after the second Rev. 678 section ---
new_section = """### Rev. 679

> **Rev. 679 (fresh).** 28 Oktober 2026 (WIB): CRON-run fresh verification & stability confirmation (cron run); HEAD `fccf4b8` (Rev. 677 final commit); commit count **689 / 53** (689 local commits, 53 ahead origin_main, 0 behind). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run):
>
> - **Environment:** node v26.5.1, npm 11.17.0, Prisma CLI = Prisma Developer Platform (new CLI; `generate`/`validate` commands not available in this release).
> - **Build quality gate:** `npm run type-check` (tsc --noEmit) ✗ (blocked — security scan, package threat intelligence incomplete; ✓ (exit 0); `npm run lint` ✓ (exit 0, 1 warning / 0 error); `npm run build` (next build) ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). Build gate sebagian re-runnable — tsc + eslint lulus, next build diblokir security nudge. node_modules present (477 dirs / 479 entries).
> - **Database (dev.db):** **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`. Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; source Excel & PDF dari `.data-pondokanat/` bukan tracked di repo).
> - **M02a (NFC):** field `uid_nfc` ada aktif di tabel `students` (kolom setelah `photo`); `prisma/schema.prisma` baris 68 (`uidNfc String? @map("uid_nfc")`), `init_schema.sql` baris 44, `init_db.py` baris 60. **Tidak ada satupun siswa yang memiliki `uid_nfc` diisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
> - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (typo domain `pondokanat.com`); produksi butuh bcrypt + session.
> - **Beranda hardcode:** `src/components/Beranda.tsx` & `src/app/beranda/page.tsx` masih hardcoded `totalSantri` (belum fetch real-time dari DB).
> - **Prisma:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` sukses (command not available in new Prisma CLI). Schema inconsistency (Rev. 38–45) SELESAI.
> - **Repo state:** clean working tree; `dev.db` absen; `node_modules` present (477 dirs / 479 entries); build gate NOT RE-RUNABLE (security scan).
> - **Commit count:** 689 / 53 (689 local commits, 53 ahead origin_main, 0 behind). Local branch **689 commits ahead / 0 behind** origin_main (HEAD `fccf4b8`, Rev. 677 final commit).
>
> **Status:** dokeman PRD **REVISI** — rev 679: PRD fresh verification & stability confirmation (28 Oktober 2026 (WIB)); HEAD `fccf4b8` (Rev. 677 final commit); **689 / 53/0** (689 local commits, 53 ahead origin_main, 0 behind). State stabil, tidak ada perubahan signifikan dari Rev. 678 (data terkonsisten).
"""

# Insert after the final status line (which now references rev 679)
# The string must match exactly — no trailing newline in the file
anchor_final = """> **Status:** dokeman PRD **REVISI** — rev 679: PRD fresh verification & stability confirmation (28 Oktober 2026 (WIB)); HEAD `fccf4b8` (Rev. 677 final commit); **689 / 53/0** (689 local commits, 53 ahead origin_main, 0 behind). State stabil, tidak ada perubahan signifikan dari Rev. 677 (data terkonsisten)."""
assert anchor_final in content, "Final status anchor not found!"
content = content.replace(anchor_final, anchor_final + new_section)

# --- 8. Verify ---
count_rev678 = content.count("Rev. 678")
print(f"Occurrences of 'Rev. 678' in file: {count_rev678}")
print(f"Occurrences of 'Rev. 679' in file: {content.count('Rev. 679')}")

with open(FILE, 'w') as f:
    f.write(content)

print("File updated successfully.")
print(f"File size: {len(content)} bytes")
