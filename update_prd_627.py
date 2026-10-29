import io

path = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"
s = io.open(path, encoding="utf-8").read()
modified = 0

def repl(old, new):
    global s, modified
    c = s.count(old)
    assert c == 1, f"Found {c} occurrences of: {old[:80]}..."
    s = s.replace(old, new)
    modified += 1

# === 1. Update HEADER (line 4) ===
old_header = """> Rev. 625: PRD fresh verification & stability confirmation (cron run, 27 Oktober 2026 WIB); header Rev. 625→626; §11 compact changelog 116–625→116–626; §12 updated; HEAD `3c93b709f685603363ce77dad198e869df59866f` (Rev. 625 final commit); commit count **628 / 7/0** (628 local commits, 7 ahead origin_main, 0 behind); working tree: PRD-PONDOK-BANAT.md cocak dengan HEAD (revisi terbaru = Rev. 626, commit 3c93b709f685603363ce77dad198e869df59866f); seluruh file lain cocak dengan HEAD; untracked: 12 (correct_sha.py, fix_line713.py, fix_stale.py, table_fix.py, update_prd.py, update_prd603.py, update_prd609.py, update_prd616.py, update_prd619.py, update_prd619_sha.py, update_prd620.py, update_prd_sha2.py); git ls-files = 268 files."""
new_header = """> Rev. 626: PRD fresh verification & stability confirmation (cron run, 27 Oktober 2026 WIB); header Rev. 626→627; §11 compact changelog 116–626→116–627; §12 updated; HEAD `55625dd2f62fad15eb382a4ca86bffc1e4eed911` (Rev. 626 final commit); commit count **629 / 8/0** (629 local commits, 8 ahead origin_main, 0 behind); working tree: PRD-PONDOK-BANAT.md cocak dengan HEAD (revisi terbaru = Rev. 627, commit 55625dd2f62fad15eb382a4ca86bffc1e4eed911); seluruh file lain cocak dengan HEAD; untracked: 13 (correct_sha.py, fix_line713.py, fix_stale.py, table_fix.py, update_prd.py, update_prd603.py, update_prd609.py, update_prd616.py, update_prd619.py, update_prd619_sha.py, update_prd620.py, update_prd_626.py, update_prd_sha2.py); git ls-files = 268 files."""
repl(old_header, new_header)

# === 2. Update §11 compact changelog: add Rev. 627 row after Rev. 625 row ===
old_changelog_row = """||||| 625 | 27 Okt | 3c93b709f685603363ce77dad198e869df59866f | 3c93b709f685603363ce77dad198e869df59866f | 7/0 | Rev. 625: PRD fresh verification & stability confirmation (cron run, 27 Oktober 2026 WIB); header Rev. 624→625; §11 compact changelog 116–624→116–625; §12 updated; HEAD 3c93b70 (Rev. 625 final commit); commit count 628/7/0; node_modules present (477 dirs / 84021 files); dev.db absent; M02a NFC field uid_nfc aktif, 0 siswa terisi; Auth & Beranda hardcode; Prisma KitabProgress & Sertakan terdefinisi. |"""
new_changelog_row = old_changelog_row + """
|||||| 627 | 27 Okt | 55625dd2f62fad15eb382a4ca86bffc1e4eed911 | 55625dd2f62fad15eb382a4ca86bffc1e4eed911 | 8/0 | Rev. 627: PRD fresh verification & stability confirmation (cron run, 27 Oktober 2026 WIB); header Rev. 626→627; §11 compact changelog 116–626→116–627; §12 updated. HEAD 55625dd (Rev. 626 final commit); commit count 629/8/0; node_modules present (479 dirs / 84021 files); dev.db absent; M02a NFC field uid_nfc aktif, 0 siswa terisi; Auth & Beranda hardcode; Prisma KitabProgress & Sertakan terdefinisi. |"""
repl(old_changelog_row, new_changelog_row)

# === 3. Update §12 (line 853) ===
old_12 = """> > - Commit count: **628 / 7/0** (628 local commits, 7 ahead origin_main, 0 behind). Local branch 628 commits ahead / 0 behind origin_main (HEAD 3c93b709f685603363ce77dad198e869df59866f, Rev. 625 final commit)."""
new_12 = """> > - Commit count: **629 / 8/0** (629 local commits, 8 ahead origin_main, 0 behind). Local branch 629 commits ahead / 0 behind origin_main (HEAD 55625dd2f62fad15eb382a4ca86bffc1e4eed911, Rev. 626 final commit)."""
repl(old_12, new_12)

io.open(path, "w", encoding="utf-8").write(s)
print(f"Done. File written. Modifications: {modified}")
print(f"File size: {len(s)} chars, {s.count(chr(10))} lines")
