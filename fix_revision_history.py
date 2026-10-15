path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'
with open(path, 'r') as f:
    lines = f.readlines()

# Find the line "8. **Rev. 31 — 14 Oktober 2026 (WIB).** Re-verification final kondisi repo + `dev.db` (SQLite, cron run):"
# and the following lines until the blank line before the footer
rev31_start = None
rev31_end = None
for i, line in enumerate(lines):
    if line.startswith('8. **Rev. 31 — 14 Oktober 2026'):
        rev31_start = i
        break

if rev31_start is not None:
    # The Rev. 31 entry ends at the blank line after the Rev. 31 content
    # Find the end of the Rev. 31 content (the last non-empty line before a blank line)
    j = rev31_start + 1
    while j < len(lines) and lines[j].strip() != '':
        j += 1
    rev31_end = j  # exclusive end index
    
    # Extract the original Rev. 30 content from the end of the Rev. 31 entry
    rev31_content_lines = lines[rev31_start:rev31_end]
    
    # Find the line that has the original Rev. 30 content (starts with "1 user (admin@pondokanat.com")
    orig_rev30_content = None
    for k in range(len(rev31_content_lines) - 1, -1, -1):
        if rev31_content_lines[k].strip().startswith('1 user (admin@pondokanat.com'):
            orig_rev30_content = rev31_content_lines[k].strip()
            break
    
    if orig_rev30_content:
        # Replace the Rev. 31 entry with just the Rev. 31 summary line (no details)
        # The details should be removed since we're adding proper Rev. 30 and Rev. 31 entries
        lines[rev31_start] = '8. **Rev. 31 — 14 Oktober 2026 (WIB).** Re-verification final kondisi repo + `dev.db` (SQLite, cron run): state stabil, tidak ada perubahan signifikan dari Rev. 30.\n'
        # Remove the detail lines
        del lines[rev31_start+1:rev31_end]
        
        # Now insert a proper Rev. 30 entry before line 409 (index of "8. **Rev. 31")
        # Find the index of the "8. **Rev. 31" line (which is now rev31_start)
        idx8 = rev31_start
        rev30_entry = [
            '7. **Rev. 30 — 14 Oktober 2026 (WIB).** Re-verifikasi final kondisi repo + `dev.db` (SQLite, cron run): **1 user (admin@pondokanat.com, role admin)** | **5 role** (admin, guru, wali_kelas, pengasuh, santri) | **33 role_permissions** (M01) | **441 siswa** (semua `inactive`; `uid_nfc` = 0 terisi) | **18 kelas** (TAMHIDI A/B + 1A–6B, 12 seksi A/B + TA A + TB + TK; TAMHIDI A/B/Takhosous = 0) | **54 guru** (impor Excel, semua `active`) | **32 mapel** | **5.420 nilai** | **0 record** tabel silabus/rpp/absensi/rapor/announcements/messages/notifications. **dev.db:** total 15 tabel (users, roles, role_permissions, students, classes, teachers, subjects, silabus, rpp, absensi, grades, rapor, announcements, messages, notifications). **Siswa per kelas:** TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosous=0; **TOTAL = 441**. **M02a (NFC):** field `uid_nfc` ada di tabel `students` (kolom setelah `photo`) namun **0 siswa** terisi (data ekspor NFC Tools belum tersedia — mapping UID → NISN tertunda). **Status:** dokumen PRD **FINAL**; state stabil, tidak ada perubahan dari Rev. 29.\n'
        ]
        lines[idx8:idx8] = rev30_entry

with open(path, 'w') as f:
    f.writelines(lines)

print("Bottom revision history fixed")
print(f"Total lines: {len(lines)}")
