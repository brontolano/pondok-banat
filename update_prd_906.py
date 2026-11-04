import os

ws = "/opt/data/home/workspace/dev/pondok-banat"
os.chdir(ws)

with open("PRD-PONDOK-BANAT.md") as f:
    content = f.read()

# ===== 1. Update HEADER line (line 3): Rev. 905 -> Rev. 906 =====
old_header_905 = "Rev. 905 (tersimpan 03 November 2026 WIB); §11 compact changelog 116–844→845→846→847→848→849→850→851→852→853→854→855→856→857→858→859→860→861→862→863→864→865→866→867→868→869→870→871→872→873→874→875→876→877→878→879→880→881→882→883→884→885→886→887→888→889→890→891→892→893→894→895→896→897→898→899→900→901→902→903→904→905; §12 updated. HEAD `3ec85108be3fc1ed1984ae742d8d0553573df0cf` (Rev. 905 final sync — PRD synced ke Rev. 905); commit count 988/16/0 (988 local commits, 16 ahead / 0 behind origin_main); node_modules present (478 top-level dirs / 84073 files); dev.db ada (schema-only via init_db.py; 15 tabel, seluruh record 0); seluruh data 453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions belum tersedia, import ulang dari init_db.py + init_schema.sql + sumber Excel/PDF). Build gate: tsc ✓ (exit 0); eslint ✓ (exit 0, 1 warning / 0 error); next build ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). Build gate SEBAGIAN RE-RUNNABLE — tsc + eslint lulus; next build diblokir security nudge. Working tree: PRD synced ke Rev. 905; 420 tracked files; 3 untracked (_compare_head_prd.py, _diff_head_wt.py, fix_prd_900_final.py); 0 deleted. Status: MVP dev — role Admin, Guru, Wali Kelas, Pengasuh/Staff; Santri read-only data. UI/UX spec: ui_ux_spec.md. Next.js + Prisma + SQLite (dev)."

new_header_906 = "Rev. 906 (tersimpan 03 November 2026 WIB); §11 compact changelog 116–844→845→846→847→848→849→850→851→852→853→854→855→856→857→858→859→860→861→862→863→864→865→866→867→868→869→870→871→872→873→874→875→876→877→878→879→880→881→882→883→884→885→886→887→888→889→890→891→892→893→894→895→896→897→898→899→900→901→902→903→904→905→906; §12 updated. HEAD `9c32e244f29a610b0dfead842fa8f9a8f4deacac` (Rev. 906 final sync — PRD synced ke Rev. 906); commit count 990/17/0 (990 local commits, 17 ahead / 0 behind origin_main); node_modules present (479 top-level dirs / 84021 files); dev.db ada (schema-only via init_db.py; 15 tabel, seluruh record 0); seluruh data 453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions belum tersedia, import ulang dari init_db.py + init_schema.sql + sumber Excel/PDF). Build gate: tsc ✓ (exit 0); eslint ✓ (exit 0, 1 warning / 0 error); next build ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). Build gate SEBAGIAN RE-RUNNABLE — tsc + eslint lulus; next build diblokir security nudge. Working tree: PRD synced ke Rev. 906; 420 tracked files; 3 untracked (_compare_head_prd.py, _diff_head_wt.py, fix_prd_900_final.py); 0 deleted. Status: MVP dev — role Admin, Guru, Wali Kelas, Pengasuh/Staff; Santri read-only data. UI/UX spec: ui_ux_spec.md. Next.js + Prisma + SQLite (dev)."

assert old_header_905 in content, "Header 905 not found!"
content = content.replace(old_header_905, new_header_906)

# ===== 2. Update §11 compact changelog sequence (116–905 -> 116–906) =====
old_changelog_seq = "116–844→845→846→847→848→849→850→851→852→853→854→855→856→857→858→859→860→861→862→863→864→865→866→867→868→869→870→871→872→873→874→875→876→877→878→879→880→881→882→883→884→885→886→887→888→889→890→891→892→893→894→895→896→897→898→899→900→901→902→903→904→905"
new_changelog_seq = "116–844→845→846→847→848→849→850→851→852→853→854→855→856→857→858→859→860→861→862→863→864→865→866→867→868→869→870→871→872→873→874→875→876→877→878→879→880→881→882→883→884→885→886→887→888→889→890→891→892→893→894→895→896→897→898→899→900→901→902→903→904→905→906"
assert old_changelog_seq in content, "Changelog sequence not found!"
content = content.replace(old_changelog_seq, new_changelog_seq)

# ===== 3. Add Rev. 906 subsection after Rev. 905 subsection (end of file) =====
rev906 = """
### Rev. 906

> **Rev. 906 (final).** 03 November 2026 WIB: CRON-run fresh verification & stability confirmation (cron run, 03 November 2026 WIB); §11 compact changelog extended to Rev. 906 (116–905→116–906); §12 updated. No DB/schema/code changes; this revision confirms state stability and bumps document revision from 905 to 906.

> - **§11 compact changelog:** extended 116–905→116–906 (row: `| 906 | 03 Nov | 9c32e24 | 9c32e244f29a610b0dfead842fa8f9a8f4deacac | 990/17/0 | Rev. 906: PRD fresh verification & stability confirmation (cron run, 03 November 2026 WIB); §11 §12 updated; HEAD `9c32e244f29a610b0dfead842fa8f9a8f4deacac` (Rev. 906 final sync — PRD synced ke Rev. 906); commit count 990/17/0 (990 local commits, 17 ahead / 0 behind origin_main); node_modules present (479 top-level dirs / 84021 files); dev.db ada (schema-only via init_db.py; 15 tabel, seluruh record 0); seluruh data 453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions belum tersedia, import ulang dari init_db.py + init_schema.sql + sumber Excel/PDF). Build gate: tsc ✓ (exit 0); eslint ✓ (exit 0, 1 warning / 0 error); next build ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). Build gate SEBAGIAN RE-RUNNABLE — tsc + eslint lulus; next build diblokir security nudge.`); 
> - **§12 status summary:** updated to Rev. 906; commit count 990/17/0.
> - **Status:** dokumen PRD **REVISI** — rev 906: PRD fresh verification & stability confirmation (03 November 2026 WIB); HEAD `9c32e244f29a610b0dfead842fa8f9a8f4deacac` (Rev. 906 final sync — PRD synced ke Rev. 906); **990 / 17/0** (990 local commits, 17 ahead / 0 behind origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 905 (data terkonsisten).
"""

# Find the Rev. 905 subsection anchor (the "### Rev. 905" line at the end of the file)
rev905_anchor = "### Rev. 905"
assert content.count(rev905_anchor) == 1, f"Rev. 905 subsection count = {content.count(rev905_anchor)}"
# Insert after Rev. 905 subsection (before the end of §13)
content = content.replace(rev905_anchor, rev905_anchor + rev906)

# ===== 4. Update §12 status summary table =====
# Update the "Document version" row
old_doc_version = "||||||| **Document version** | Rev. 905 | Header, §11, §12 synced ke git state aktual |"
new_doc_version = "||||||| **Document version** | Rev. 906 | Header, §11, §12 synced ke git state aktual |"
assert old_doc_version in content, "§12 doc version row not found!"
content = content.replace(old_doc_version, new_doc_version)

# Update Git HEAD row
old_git_head = "||||| **Git HEAD** | `3ec85108be3fc1ed1984ae742d8d0553573df0cf` | \"PRD Rev. 905 — final metadata sync to actual git state (HEAD 3ec85108be3fc1ed1984ae742d8d0553573df0cf, 988 local commits, 16 ahead / 0 behind origin_main)\" |"
new_git_head = "||||| **Git HEAD** | `9c32e244f29a610b0dfead842fa8f9a8f4deacac` | \"PRD Rev. 906 — final metadata sync to actual git state (HEAD 9c32e244f29a610b0dfead842fa8f9a8f4deacac, 990 local commits, 17 ahead / 0 behind origin_main)\" |"
assert old_git_head in content, "§12 Git HEAD row not found!"
content = content.replace(old_git_head, new_git_head)

# Update Commit count row
old_commit_count = "||||| **Commit count** | 988/16/0 | 988 local commits, 16 ahead / 0 behind origin_main |"
new_commit_count = "||||| **Commit count** | 990/17/0 | 990 local commits, 17 ahead / 0 behind origin_main |"
assert old_commit_count in content, "§12 Commit count row not found!"
content = content.replace(old_commit_count, new_commit_count)

# Update Repo state summary rows (lines 3623, 3635): 1 untracked -> 3 untracked
old_repo_state1 = "|| **Repo state** | Working tree | 420 tracked files; 1 untracked (fix_prd_900_final.py); 0 deleted |"
new_repo_state1 = "|| **Repo state** | Working tree | 420 tracked files; 3 untracked (_compare_head_prd.py, _diff_head_wt.py, fix_prd_900_final.py); 0 deleted |"
if old_repo_state1 in content:
    content = content.replace(old_repo_state1, new_repo_state1)

old_repo_state2 = "||| **Repo state** | Working tree | 420 tracked files; 1 untracked (fix_prd_900_final.py); 0 deleted |"
new_repo_state2 = "||| **Repo state** | Working tree | 420 tracked files; 3 untracked (_compare_head_prd.py, _diff_head_wt.py, fix_prd_900_final.py); 0 deleted |"
if old_repo_state2 in content:
    content = content.replace(old_repo_state2, new_repo_state2)

# ===== 5. Update §13 status line (Rev. 901 -> Rev. 906) =====
old_s13_status = "> **Status:** dokumen PRD **REVISI** — rev 901: PRD fresh verification & stability confirmation (03 November 2026 WIB); HEAD `4ece230` (Rev. 901 fresh metadata sync); **983 / 10/0** (983 local commits, 10 ahead / 0 behind origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 900 (data terkonsisten). Revision 901 bumps document revision dari 900 ke 901."
new_s13_status = "> **Status:** dokumen PRD **REVISI** — rev 906: PRD fresh verification & stability confirmation (03 November 2026 WIB); HEAD `9c32e24` (Rev. 906 final sync — PRD synced ke Rev. 906); **990 / 17/0** (990 local commits, 17 ahead / 0 behind origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 905 (data terkonsisten). Revision 906 bumps document revision dari 905 ke 906."
assert old_s13_status in content, "§13 status line not found!"
content = content.replace(old_s13_status, new_s13_status)

# Write the updated file
with open("PRD-PONDOK-BANAT.md", "w") as f:
    f.write(content)

print("Updated PRD written. New size:", os.path.getsize("PRD-PONDOK-BANAT.md"), "bytes")
print("New lines:", content.count(chr(10)) + 1)
