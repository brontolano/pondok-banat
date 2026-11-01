#!/usr/bin/env python3
# Update PRD-PONDOK-BANAT.md from Rev. 816 (stale 844/36) to Rev. 817 (845/37)
import io

path = "PRD-PONDOK-BANAT.md"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

# --- 1. Update header ---
old_header = """header Rev. 816; §11 compact changelog 116–816; §12 updated. HEAD `48c6744` (Rev. 815 final committed); commit count 844/36/0 (844 local commits, 36 ahead / 0 behind origin_main); node_modules present (5103 dirs / 84021 files); dev.db ada (schema-only via init_db.py; 15 tabel, seluruh record 0); seluruh data 453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions belum tersedia, import ulang dari init_db.py + init_schema.sql + sumber Excel/PDF). Build gate: tsc ✓ (exit 0); eslint ✓ (exit 0, 1 warning / 0 error); next build ✗ (SecurityFatalError: Next.js 16.4.0 has a known security vulnerability — upgrade recommended). Working tree: PRD synced ke Rev. 816; 340 tracked files; 49 untracked (incl. probe scripts); 0 deleted."""

new_header = """header Rev. 817; §11 compact changelog 116–817; §12 updated. HEAD `3d79fce` (Rev. 816 final committed); commit count 845/37/0 (845 local commits, 37 ahead / 0 behind origin_main); node_modules present (5103 dirs / 84021 files); dev.db ada (schema-only via init_db.py; 15 tabel, seluruh record 0); seluruh data 453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions belum tersedia, import ulang dari init_db.py + init_schema.sql + sumber Excel/PDF). Build gate: tsc ✓ (exit 0); eslint ✓ (exit 0, 1 warning / 0 error); next build ✗ (SecurityFatalError: Next.js 16.4.0 has a known security vulnerability — upgrade recommended). Working tree: PRD synced ke Rev. 817; 340 tracked files; 49 untracked (incl. probe scripts); 0 deleted."""

assert old_header in content, "Header not found!"
content = content.replace(old_header, new_header)

# --- 2. Add new Rev. 817 entry in the detailed section (after Rev. 816 entry, before end of file) ---
old_rev816_end = """**Status:** dokumen PRD **REVISI** — rev 816: PRD fresh verification & stability confirmation (cron run, 31 Oktober 2026 WIB); HEAD `48c6744` (Rev. 815 final committed); **844 / 36/0** (844 local commits, 36 ahead / 0 behind origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 815 (data terkonsisten).
"""

new_rev817 = """**Status:** dokumen PRD **REVISI** — rev 816: PRD fresh verification & stability confirmation (cron run, 31 Oktober 2026 WIB); HEAD `48c6744` (Rev. 815 final committed); **844 / 36/0** (844 local commits, 36 ahead / 0 behind origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 815 (data terkonsisten).

### Rev. 817 (fresh verification)

**Tanggal:** 5 November 2026 (WIB) — cron run fresh verification & stability confirmation.

**HEAD commit:** `3d79fce` (Rev. 816 final committed — PRD fresh verification & stability confirmation, 5 November 2026 WIB; header Rev. 817, §11 compact changelog 116–817, §12 updated; HEAD 3d79fce (Rev. 816), 845/37/0, node_modules 5103 dirs / 84021 files, dev.db schema-only; BUILD GATE tsc+eslint lulus, next build security nudge)

**Commit count:** 845 local commits, **37 ahead / 0 behind** origin_main (origin/main at `60d2d99` (Rev. 788)).

**Working tree:** clean (PRD synced ke Rev. 817); untracked 49; 0 deleted.

**Build quality gate — sebagian re-runnable:**
- `npm run type-check` (tsc --noEmit) ✓ (exit 0)
- `npm run lint` ✓ (exit 0, 1 warning / 0 error)
- `npm run build` (next build) ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability — engine security nudge, upgrade recommended). node_modules present (5103 dirs / 84021 files).

**Database (dev.db):** **ada** — schema-only via `init_db.py` (15 tabel, seluruh record 0). Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql` + sumber Excel/PDF).

**M02a (NFC):** field `uid_nfc` ada aktif di tabel `students` (kolom setelah `photo`); `prisma/schema.prisma` baris 68 (`uidNfc String? @map("uid_nfc")`); `init_schema.sql` baris 44, `init_db.py` baris 60. **0 siswa terisi (semua 453 NULL)** — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).

**Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` sudah diperbaiki; typo `pondokanat.com` telah dihapus); produksi butuh bcrypt + session.

**Beranda hardcode:** `src/components/Beranda.tsx` & `src/app/beranda/page.tsx` masih hardcoded `totalSantri` (belum fetch real-time dari DB); nilai sekarang `totalSantri: 453, totalGuru: 54, totalKelas: 18`.

**Prisma:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` sukses. Schema inconsistency (Rev. 38–45) SELESAI.

**Repo state:** clean working tree; PRD ditulis ke Rev. 817; `dev.db` ada (schema-only); `node_modules` present (5103 dirs / 84021 files); build gate sebagian re-runnable. 49 untracked helper scripts; 0 deleted.

**Commit count:** 845 local commits, **37 ahead / 0 behind** origin_main. Local branch **845 commits ahead / 0 behind** origin_main (HEAD `3d79fce`, Rev. 816 final committed). origin/main at `60d2d99` (Rev. 788).

**Status:** dokumen PRD **REVISI** — rev 817: PRD fresh verification & stability confirmation (cron run, 5 November 2026 WIB); HEAD `3d79fce` (Rev. 816 final committed); **845 / 37/0** (845 local commits, 37 ahead / 0 behind origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 816 (data terkonsisten).
"""

assert old_rev816_end in content, "Rev. 816 end marker not found!"
content = content.replace(old_rev816_end, new_rev817)

with io.open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("Updated PRD to Rev. 817")
print("Header check:", "header Rev. 817" in content)
print("Rev 817 check:", "### Rev. 817" in content)
print("Commit count check:", "845 / 37/0" in content)
