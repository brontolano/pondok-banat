# Update PRD-PONDOK-BANAT.md to current state
import io

path = 'PRD-PONDOK-BANAT.md'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

replacements = [
    # --- Header ---
    (
        "header Rev. 818; §11 compact changelog 116–818; §12 updated. HEAD `ab0c5c0` (Rev. 817 final committed); commit count 849/41/0 (849 local commits, 41 ahead / 0 behind origin_main); node_modules present (479 dirs / 84021 files); dev.db ada (schema-only via init_db.py; 15 tabel, seluruh record 0); seluruh data 453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions belum tersedia, import ulang dari init_db.py + init_schema.sql + sumber Excel/PDF). Build gate: tsc ✓ (exit 0); eslint ✓ (exit 0, 1 warning / 0 error); next build ✗ (SecurityFatalError: Next.js 16.4.0 has a known security vulnerability — upgrade recommended). Working tree: PRD synced ke Rev. 818; 340 tracked files; 49 untracked (incl. probe scripts); 0 deleted.",
        "header Rev. 818; §11 compact changelog 116–818; §12 updated. HEAD `2a048a6` (Rev. 818 final committed — header commit-count sync); commit count 850/42/0 (850 local commits, 42 ahead / 0 behind origin_main); node_modules present (477 dirs / 84021 files); dev.db ada (schema-only via init_db.py; 15 tabel, seluruh record 0); seluruh data 453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions belum tersedia, import ulang dari init_db.py + init_schema.sql + sumber Excel/PDF). Build gate: tsc ✓ (exit 0); eslint ✓ (exit 0, 1 warning / 0 error); next build ✗ (SecurityFatalError: Next.js 16.4.0 has a known security vulnerability — upgrade recommended). Working tree: PRD synced ke Rev. 818; 340 tracked files; 51 untracked (incl. probe scripts); 0 deleted."
    ),
    # --- Rev. 818 section ---
    (
        "**Tanggal:** 7 November 2026 (WIB) — cron run fresh verification & stability confirmation.\n\n**HEAD commit:** `ab0c5c0` (Rev. 817 final committed — PRD fresh verification & stability confirmation, 5 November 2026 WIB; header Rev. 817, §11 compact changelog 116–817, §12 updated; HEAD 3d79fce (Rev. 816), 845/37/0, node_modules 5103 dirs / 84021 files, dev.db schema-only; BUILD GATE tsc+eslint lulus, next build security nudge)",
        "**Tanggal:** 7 November 2026 (WIB) — cron run fresh verification & stability confirmation.\n\n**HEAD commit:** `2a048a6f13d00c9fbdbcc13939fa293afd188add` (Rev. 818 final committed — header commit-count sync, 5 November 2026 WIB; header Rev. 818, §11 compact changelog 116–818, §12 updated; HEAD 2a048a6 (Rev. 818), 850/42/0, node_modules 477 dirs / 84021 files, dev.db schema-only; BUILD GATE tsc+eslint lulus, next build security nudge)"
    ),
    (
        "**Commit count:** 846 local commits, **38 ahead / 0 behind** origin_main (origin/main at `60d2d99` (Rev. 788)).",
        "**Commit count:** 850 local commits, **42 ahead / 0 behind** origin_main (origin/main at `60d2d99` (Rev. 788))."
    ),
    (
        "**Working tree:** clean (PRD synced ke Rev. 818); untracked 49; 0 deleted.",
        "**Working tree:** clean (PRD synced ke Rev. 818); untracked 51; 0 deleted."
    ),
    (
        "`npm run build` (next build) ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability — engine security nudge, upgrade recommended). node_modules present (479 dirs / 84021 files).",
        "`npm run build` (next build) ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability — engine security nudge, upgrade recommended). node_modules present (477 dirs / 84021 files)."
    ),
    (
        "**Repo state:** clean working tree; PRD ditulis ke Rev. 818; `dev.db` ada (schema-only); `node_modules` present (479 dirs / 84021 files); build gate sebagian re-runnable. 49 untracked helper scripts; 0 deleted.",
        "**Repo state:** clean working tree; PRD ditulis ke Rev. 818; `dev.db` ada (schema-only); `node_modules` present (477 dirs / 84021 files); build gate sebagian re-runnable. 51 untracked helper scripts; 0 deleted."
    ),
    (
        "**Commit count:** 847 local commits, **39 ahead / 0 behind** origin_main. Local branch **847 commits ahead / 0 behind** origin_main (HEAD `ab0c5c0`, Rev. 817 final committed). origin/main at `60d2d99` (Rev. 788).",
        "**Commit count:** 850 local commits, **42 ahead / 0 behind** origin_main. Local branch **850 commits ahead / 0 behind** origin_main (HEAD `2a048a6`, Rev. 818 final committed). origin/main at `60d2d99` (Rev. 788)."
    ),
]

for old, new in replacements:
    if old in content:
        content = content.replace(old, new, 1)
    else:
        print("NOT FOUND:", old[:80])

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("DONE")
