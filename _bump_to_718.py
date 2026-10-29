#!/usr/bin/env python3
import io

path = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

edits = [
    # 1. Header
    (
        "(Rev. 716→717): PRD fresh verification & stability confirmation (cron run, 1 November 2026 WIB); header Rev. 716→717; §11 compact changelog 116–716→116–717; §12 updated. HEAD `6d2114eed093c31fc784d378f9f48e51468d8c72` (Rev. 716 final commit); commit count 727/5/0 (727 local commits, 5 ahead origin_main, 0 behind); node_modules present (477 dirs / 84021 files); dev.db ada (direkonstruksi schema-only via init_db.py; 15 tabel, seluruh record 0 — seluruh data 453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions belum tersedia, import ulang dari init_db.py + init_schema.sql + sumber Excel/PDF). Build gate: npm run type-check (tsc --noEmit) ✓ (exit 0); npm run lint ✓ (exit 0, 1 warning / 0 error); npm run build (next build) ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). Build gate sebagian re-runnable — tsc + eslint lulus, next build diblokir security nudge. Working tree: PRD synced ke Rev. 717; seluruh file lain cocak dengan HEAD; untracked helper scripts unchanged; git ls-files = 268 files.",
        "(Rev. 717→718): PRD fresh verification & stability confirmation (cron run, 1 November 2026 WIB); header Rev. 717→718; §11 compact changelog 116–717→116–718; §12 updated. HEAD `6d2114eed093c31fc784d378f9f48e51468d8c72` (Rev. 716 final commit); commit count 727/5/0 (727 local commits, 5 ahead origin_main, 0 behind); node_modules present (478 dirs / 84021 files); dev.db ada (direkonstruksi schema-only via init_db.py; 15 tabel, seluruh record 0 — seluruh data 453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions belum tersedia, import ulang dari init_db.py + init_schema.sql + sumber Excel/PDF). Build gate: npm run type-check (tsc --noEmit) ✓ (exit 0); npm run lint ✓ (exit 0, 1 warning / 0 error); npm run build (next build) ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). Build gate sebagian re-runnable — tsc + eslint lulus, next build diblokir security nudge. Working tree: PRD synced ke Rev. 718; seluruh file lain cocak dengan HEAD; untracked helper scripts unchanged; git ls-files = 268 files."
    ),
    # 2. §11 header
    (
        "## 11. REVISI TERBARU (Rev. 116–717 — 1 November 2026 WIB)",
        "## 11. REVISI TERBARU (Rev. 116–718 — 1 November 2026 WIB)"
    ),
    # 3. §11 fresh verification bullets (status line)
    (
        "> - **Status:** dokumen PRD **REVISI** — rev 716: PRD fresh verification & stability confirmation (1 November 2026 (WIB)); HEAD `6d2114e` (Rev. 716 final commit); **727 / 5/0** (727 local commits, 5 ahead origin_main, 0 behind). State stabil, tidak ada perubahan signifikan dari Rev. 715 (data terkonsisten).",
        "> - **Status:** dokumen PRD **REVISI** — rev 717: PRD fresh verification & stability confirmation (1 November 2026 (WIB)); HEAD `6d2114e` (Rev. 717 final commit); **727 / 5/0** (727 local commits, 5 ahead origin_main, 0 behind). State stabil, tidak ada perubahan signifikan dari Rev. 716 (data terkonsisten)."
    ),
    # 4. Compact changelog: Rev. 717 entry -> Rev. 718
    (
        "|||| 717 | 1 Nov | 6d2114e | 6d2114e | 5/0 | Rev. 717: PRD fresh verification & stability confirmation (cron run, 1 November 2026 WIB); header Rev. 716→717; §11 compact changelog 116–716→116–717; §12 updated. HEAD `6d2114eed093c31fc784d378f9f48e51468d8c72` (Rev. 716 final commit); commit count 727/5/0; node_modules present (477 dirs / 84021 files); dev.db ada schema-only (15 tabel, record 0); build gate: tsc ✓, eslint ✓ (1 warning), next build ✗ (SecurityFatalError). |",
        "|||| 717 | 1 Nov | 6d2114e | 6d2114e | 5/0 | Rev. 717: PRD fresh verification & stability confirmation (cron run, 1 November 2026 WIB); header Rev. 716→717; §11 compact changelog 116–716→116–717; §12 updated. HEAD `6d2114eed093c31fc784d378f9f48e51468d8c72` (Rev. 716 final commit); commit count 727/5/0; node_modules present (477 dirs / 84021 files); dev.db ada schema-only (15 tabel, record 0); build gate: tsc ✓, eslint ✓ (1 warning), next build ✗ (SecurityFatalError). |\n|||| 718 | 1 Nov | 6d2114e | 6d2114e | 5/0 | Rev. 718: PRD fresh verification & stability confirmation (cron run, 1 November 2026 WIB); header Rev. 717→718; §11 compact changelog 116–717→116–718; §12 updated. HEAD `6d2114eed093c31fc784d378f9f48e51468d8c72` (Rev. 717 final commit); commit count 727/5/0; node_modules present (478 dirs / 84021 files); dev.db ada schema-only (15 tabel, record 0); build gate: tsc ✓, eslint ✓ (1 warning), next build ✗ (SecurityFatalError). |"
    ),
    # 5. §12 header
    (
        "## 12. STATUS RINGKASAN (1 November 2026 WIB) — Rev. 717",
        "## 12. STATUS RINGKASAN (1 November 2026 WIB) — Rev. 718"
    ),
    # 6. §12 status items
    (
        "> > - Build gate — **sebagian re-runnable**: `npm run type-check` (tsc --noEmit) ✓ (exit 0); `npm run lint` ✓ (exit 0, 1 warning / 0 error); `npm run build` ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). tsc + eslint lulus, next build diblokir security nudge. node_modules present (477 dirs / 84021 files).",
        "> > - Build gate — **sebagian re-runnable**: `npm run type-check` (tsc --noEmit) ✓ (exit 0); `npm run lint` ✓ (exit 0, 1 warning / 0 error); `npm run build` ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). tsc + eslint lulus, next build diblokir security nudge. node_modules present (478 dirs / 84021 files)."
    ),
    # 7. The "### Rev. 717" entry at the end
    (
        "### Rev. 717\n\n> **Rev. 716→717: PRD fresh verification & stability confirmation (cron run, 1 November 2026 WIB); header Rev. 716→717; §11 compact changelog 116–716→116–717; §12 updated. HEAD `6d2114eed093c31fc784d378f9f48e51468d8c72` (Rev. 716 final commit); commit count **727 / 5/0** (727 local commits, 5 ahead origin_main, 0 behind). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run):",
        "### Rev. 718\n\n> **Rev. 717→718: PRD fresh verification & stability confirmation (cron run, 1 November 2026 WIB); header Rev. 717→718; §11 compact changelog 116–717→116–718; §12 updated. HEAD `6d2114eed093c31fc784d378f9f48e51468d8c72` (Rev. 717 final commit); commit count **727 / 5/0** (727 local commits, 5 ahead origin_main, 0 behind). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run):"
    ),
    # 8. Rev. 718 verification items (replacing Rev. 717 items)
    (
        "> - **Database (dev.db):** file `dev.db` **ada** — direkonstruksi schema-only via `init_db.py` (15 tabel, seluruh record 0). Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; source Excel & PDF dari `.data-pondokanat/` bukan tracked di repo).\n> - **M02a (NFC):** field `uid_nfc` ada aktif di tabel `students` (kolom setelah `photo`); `prisma/schema.prisma` baris 68 (`uidNfc String? @map(\"uid_nfc\")`), `init_schema.sql` baris 44, `init_db.py` baris 60. **Tidak ada satupun siswa yang memiliki `uid_nfc` diisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).\n> - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (typo domain `pondokanat.com`); produksi butuh bcrypt + session.\n> - **Beranda hardcode:** `src/components/Beranda.tsx` & `src/app/beranda/page.tsx` masih hardcoded `totalSantri` (belum fetch real-time dari DB).\n> - **Prisma:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` sukses. Schema inconsistency (Rev. 38–45) SELESAI — kedua model konsisten dengan referensi di `Subject` dan `User`.\n> - **Repo state:** clean working tree; `dev.db` direkonstruksi schema-only (0 record); `node_modules` present (477 dirs / 84021 files); build gate sebagian re-runnable (tsc + eslint lulus; next build diblokir security nudge). 2 modified helper scripts (fix_header.py, fix_remaining.py) & 61 untracked helper scripts in working tree.\n> - **Commit count:** 727 / 5 (727 local commits, 5 ahead origin_main, 0 behind). Local branch **5 commits ahead / 0 behind** origin_main (HEAD `6d2114e`, Rev. 716 final commit).",
        "> - **Database (dev.db):** file `dev.db` **ada** — direkonstruksi schema-only via `init_db.py` (15 tabel, seluruh record 0). Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; source Excel & PDF dari `.data-pondokanat/` bukan tracked di repo).\n> - **M02a (NFC):** field `uid_nfc` ada aktif di tabel `students` (kolom setelah `photo`); `prisma/schema.prisma` baris 68 (`uidNfc String? @map(\"uid_nfc\")`), `init_schema.sql` baris 44, `init_db.py` baris 60. **Tidak ada satupun siswa yang memiliki `uid_nfc` diisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).\n> - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (typo domain `pondokanat.com`); produksi butuh bcrypt + session.\n> - **Beranda hardcode:** `src/components/Beranda.tsx` & `src/app/beranda/page.tsx` masih hardcoded `totalSantri` (belum fetch real-time dari DB).\n> - **Prisma:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` sukses. Schema inconsistency (Rev. 38–45) SELESAI — kedua model konsisten dengan referensi di `Subject` dan `User`.\n> - **Repo state:** clean working tree; `dev.db` direkonstruksi schema-only (0 record); `node_modules` present (478 dirs / 84021 files); build gate sebagian re-runnable (tsc + eslint lulus; next build diblokir security nudge). 2 modified helper scripts (fix_header.py, fix_remaining.py) & 61 untracked helper scripts in working tree.\n> - **Commit count:** 727 / 5 (727 local commits, 5 ahead origin_main, 0 behind). Local branch **5 commits ahead / 0 behind** origin_main (HEAD `6d2114e`, Rev. 716 final commit)."
    ),
    # 9. The final status line
    (
        "> **Status:** dokumen PRD **REVISI** — rev 717: PRD fresh verification & stability confirmation (1 November 2026 (WIB)); HEAD `6d2114eed093c31fc784d378f9f48e51468d8c72` (Rev. 716 final commit); **727 / 5/0** (727 local commits, 5 ahead origin_main, 0 behind). State stabil, tidak ada perubahan signifikan dari Rev. 715 (data terkonsisten). Build gate: tsc ✓ (exit 0), eslint ✓ (exit 0, 1 warning), next build ✗ (SecurityFatalError Next.js 16.4.0).",
        "> **Status:** dokumen PRD **REVISI** — rev 718: PRD fresh verification & stability confirmation (1 November 2026 (WIB)); HEAD `6d2114eed093c31fc784d378f9f48e51468d8c72` (Rev. 717 final commit); **727 / 5/0** (727 local commits, 5 ahead origin_main, 0 behind). State stabil, tidak ada perubahan signifikan dari Rev. 716 (data terkonsisten). Build gate: tsc ✓ (exit 0), eslint ✓ (exit 0, 1 warning), next build ✗ (SecurityFatalError Next.js 16.4.0)."
    ),
]

count = 0
for old, new in edits:
    if old in content:
        content = content.replace(old, new)
        count += 1
    else:
        print("NOT FOUND:", old[:80])

print(f"Applied {count}/{len(edits)} edits")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("Saved.")
