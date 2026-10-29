import io

path = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"
s = io.open(path, encoding="utf-8").read()

# === 1. Update HEADER (line 4) ===
old_header = """> **Sumber:** `IDEA.md` + `.data-pondokanat/` (3 Excel + 74 dokumen = 65 RPP + 9 SILABUS) + research.
> Rev. 624: PRD fresh verification & stability confirmation (cron run, 27 Oktober 2026 WIB); header Rev. 624→625; §11 compact changelog 116–624→116–625; §12 updated; HEAD `03133044d385c34810ca2b0e2639510340e4aa37` (Rev. 624 final commit); commit count **627 / 6/0** (627 local commits, 6 ahead origin_main, 0 behind); working tree: PRD-PONDOK-BANAT.md cocak dengan HEAD (revisi terbaru = Rev. 625, commit 03133044d385c34810ca2b0e2639510340e4aa37); seluruh file lain cocak dengan HEAD; untracked: 12 (correct_sha.py, fix_line713.py, fix_stale.py, table_fix.py, update_prd.py, update_prd603.py, update_prd609.py, update_prd616.py, update_prd619.py, update_prd619_sha.py, update_prd620.py, update_prd_sha2.py); git ls-files = 268 files."""

new_header = """> **Sumber:** `IDEA.md` + `.data-pondokanat/` (3 Excel + 74 dokumen = 65 RPP + 9 SILABUS) + research.
> Rev. 625: PRD fresh verification & stability confirmation (cron run, 27 Oktober 2026 WIB); header Rev. 625→626; §11 compact changelog 116–625→116–626; §12 updated; HEAD `3c93b709f685603363ce77dad198e869df59866f` (Rev. 625 final commit); commit count **628 / 7/0** (628 local commits, 7 ahead origin_main, 0 behind); working tree: PRD-PONDOK-BANAT.md cocak dengan HEAD (revisi terbaru = Rev. 626, commit 3c93b709f685603363ce77dad198e869df59866f); seluruh file lain cocak dengan HEAD; untracked: 12 (correct_sha.py, fix_line713.py, fix_stale.py, table_fix.py, update_prd.py, update_prd603.py, update_prd609.py, update_prd616.py, update_prd619.py, update_prd619_sha.py, update_prd620.py, update_prd_sha2.py); git ls-files = 268 files."""

assert s.count(old_header) == 1, f"Header count: {s.count(old_header)}"
s = s.replace(old_header, new_header)

# === 2. Update Rev. 625 section (lines 811, 822) ===
old_625 = """### Rev. 625

> **Rev. 625 (fresh).** 27 Oktober 2026 (WIB): CRON-run fresh verification & stability confirmation (cron run); HEAD `03133044d385c34810ca2b0e2639510340e4aa37` (Rev. 624 final commit); **6 / 0** (6 commits ahead origin_main, 0 behind). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run):"""
new_625 = """### Rev. 625

> **Rev. 625 (fresh).** 27 Oktober 2026 (WIB): CRON-run fresh verification & stability confirmation (cron run); HEAD `3c93b709f685603363ce77dad198e869df59866f` (Rev. 625 final commit); **7 / 0** (7 commits ahead origin_main, 0 behind). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run):"""
assert s.count(old_625) == 1, f"Rev.625 section count: {s.count(old_625)}"
s = s.replace(old_625, new_625)

old_625b = """> - **Status:** dokumen PRD **REVISI** — rev 625: PRD fresh verification & stability confirmation (27 Oktober 2026 (WIB)); HEAD `03133044d385c34810ca2b0e2639510340e4aa37` (Rev. 624 final commit); **6 / 0** (6 commits ahead origin_main, 0 behind). State stabil, tidak ada perubahan signifikan dari Rev. 624 (data terkonsisten)."""
new_625b = """> - **Status:** dokumen PRD **REVISI** — rev 625: PRD fresh verification & stability confirmation (27 Oktober 2026 (WIB)); HEAD `3c93b709f685603363ce77dad198e869df59866f` (Rev. 625 final commit); **7 / 0** (7 commits ahead origin_main, 0 behind). State stabil, tidak ada perubahan signifikan dari Rev. 625 (data terkonsisten)."""
assert s.count(old_625b) == 1, f"Rev.625b count: {s.count(old_625b)}"
s = s.replace(old_625b, new_625b)

# === 3. Update §12 (line 851) ===
old_12 = """> > - Commit count: **627 / 6/0** (627 local commits, 6 ahead origin_main, 0 behind). Local branch 627 commits ahead / 0 behind origin_main (HEAD 03133044d385c34810ca2b0e2639510340e4aa37, Rev. 624 final commit)."""
new_12 = """> > - Commit count: **628 / 7/0** (628 local commits, 7 ahead origin_main, 0 behind). Local branch 628 commits ahead / 0 behind origin_main (HEAD 3c93b709f685603363ce77dad198e869df59866f, Rev. 625 final commit)."""
assert s.count(old_12) == 1, f"§12 count: {s.count(old_12)}"
s = s.replace(old_12, new_12)

# === 4. Add Rev. 625 row to changelog (after the Rev. 624 row) ===
# Use partial match to avoid special character issues
old_row_partial = """|||| 624 | 27 Okt | ff7a89b667fa202ae3508511356aab93b8898de4 | ff7a89b667fa202ae3508511356aab93b8898de4 | 5/0 | Rev. 624: PRD fresh verification & stability confirmation (cron run, 27 Oktober 2026 WIB); header Rev. 623→624; §11 compact changelog 116–623→116–624; §12 updated. HEAD ff7a89b667fa202ae3508511356aab93b8898de4 (Rev. 623 final commit); commit count 626 / 5/0"""
new_row = old_row_partial + """ (626 local commits, 5 ahead origin_main, 0 behind). Build gate: tsc ✓ (exit 0), eslint ✓ (exit 0, 1 warning/0 error); next build ✓ (exit 0 — build sukses tanpa SecurityFatalError). node_modules present (5103 dirs / 84021 files); dev.db absent; M02a NFC field uid_nfc aktif, 0 siswa terisi; Auth & Beranda hardcode; Prisma KitabProgress & Sertakan terdefinisi. |

||||| 625 | 27 Okt | 3c93b709f685603363ce77dad198e869df59866f | 3c93b709f685603363ce77dad198e869df59866f | 7/0 | Rev. 625: PRD fresh verification & stability confirmation (cron run, 27 Oktober 2026 WIB); header Rev. 624→625; §11 compact changelog 116–624→116–625; §12 updated; HEAD 3c93b70 (Rev. 625 final commit); commit count 628/7/0; node_modules present (477 dirs / 84021 files); dev.db absent; M02a NFC field uid_nfc aktif, 0 siswa terisi; Auth & Beranda hardcode; Prisma KitabProgress & Sertakan terdefinisi. |"""

if s.count(old_row_partial) == 1:
    s = s.replace(old_row_partial, new_row)
    print("Changelog row added")
else:
    print(f"Changelog row not found: {s.count(old_row_partial)}")
    # Try alternative: search for unique substring
    idx = s.find("|||| 624 | 27 Okt | ff7a89b")
    if idx >= 0:
        print(f"Found at position {idx}")
        # Show the exact text around the position
        print(repr(s[idx:idx+200]))

# Write the file
io.open(path, "w", encoding="utf-8").write(s)
print("Done. File written.")
print(f"File size: {len(s)} chars, {s.count(chr(10))} lines")
