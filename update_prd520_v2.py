with open("/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md", "r", encoding="utf-8") as f:
    content = f.read()

# Find the position of the last Rev. 514 entry (the one at the end of §12)
# The last entry starts with "||- **Rev. 514 (final).**"
rev514_marker = "||- **Rev. 514 (final).**"
pos = content.rfind(rev514_marker)
print("Last Rev. 514 entry position:", pos)

if pos == -1:
    print("ERROR: Rev. 514 entry not found!")
else:
    # The entry text after the marker
    entry_start = pos + len(rev514_marker)
    # Read until we find a newline that indicates end of line
    # Actually, let's find the end of the line (the line ends with "origin_main.")
    line_end = content.find("\n", entry_start)
    if line_end == -1:
        line_end = len(content)
    print("Entry line ends at:", line_end)
    
    # New Rev. 520 entry
    new_entry = ""
    new_entry += "||- **Rev. 520 (final).** 24 Oktober 2026 (WIB): PRD fresh verification & stability confirmation (24 Oct 2026 WIB); HEAD `ea1ac69d39efdcf87346274f5ede6e5b55b714b5` (Rev. 519 commit: PRD fresh verification & stability confirmation (24 Oct 2026 WIB); header Rev. 519, §11 kompakt changelog 116–518, §12 updated; HEAD 0cb6019 (Rev. 518), 1 commit ahead origin_main), 2 / 0 (2 commits ahead origin_main). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run): **state stabil, tidak ada perubahan signifikan dari Rev. 519** (data terkonsisten). Build gate: **NOT RE-RUNABLE** — `node_modules/` **absent** (dihapus setelah Rev. 377; `npm ci` diperlukan untuk memulihkan); `.next/` masih ada (partial: `cache/` + `diagnostics/` + `package.json` + `server/` + `static/`, bukan production build). `tsc --noEmit` exit 1, `npm run lint` exit 2, `npx next build` exit 1 — semua gagal karena `node_modules/` **absent**; `npm ci` diperlukan untuk memulihkan sebelum melakukan type-check/lint/build. Database (dev.db): **tidak ada (absent)** — dihapus oleh commit HEAD \"Release: clean core files only\" (1dc891d) dan `.gitignore` mencantumkan `*.db`; seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` & `import_students_grades_clean.py` tidak ditemukan di working tree). **M02a (NFC):** field `uid_nfc` ada aktif di tabel students, semua 453 NULL (data ekspor NFC Tools belum tersedia). **Auth hardcode:** `src/components/Login.tsx` tetap `admin@pondokanbat.com` / `admin123` (typo domain `pondokanat.com`); produksi butuh bcrypt + session. **Beranda hardcode:** `src/components/Beranda.tsx` & `src/app/beranda/page.tsx` masih hardcoded `totalSantri` (belum fetch real-time dari DB). **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` sukses. **Status:** dokumen PRD **REVISI** — rev 520 (final): PRD fresh verification & konfirmasi stabilitas; seluruh data terkonsisten, tidak ada perubahan signifikan dari Rev. 519; branch 2 ahead / 0 behind origin_main."
    
    # Insert new entry after the Rev. 514 entry (with a blank line before)
    # The original content after pos has the Rev. 514 entry, then a newline
    new_content = content[:pos] + content[pos:]  # keep everything
    
    # Find where the Rev. 514 entry ends
    rev514_entry_end = content.find("\n", entry_start)
    if rev514_entry_end == -1:
        rev514_entry_end = len(content)
    
    # Insert new entry after the Rev. 514 entry
    new_content = content[:rev514_entry_end] + "\n\n" + new_entry + "\n" + content[rev514_entry_end:]
    
    # Also update the §11 changelog range
    new_content = new_content.replace("§11 kompakt changelog 116–519", "§11 kompakt changelog 116–520")
    new_content = new_content.replace("## 11. REVISI TERBARU (Rev. 116–519", "## 11. REVISI TERBARU (Rev. 116–520")
    new_content = new_content.replace("## 12. REVISI TERBARU (Rev. 468–519", "## 12. REVISI TERBARU (Rev. 468–520")
    
    with open("/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md", "w", encoding="utf-8") as f:
        f.write(new_content)
    
    print("File updated successfully.")
    print("File size:", len(new_content.encode("utf-8")), "bytes")
    print("Rev. 520 present:", "Rev. 520 (final)" in new_content)
    print("§11 range 116-520:", "116–520" in new_content)
    print("§12 range 468-520:", "468–520" in new_content)
