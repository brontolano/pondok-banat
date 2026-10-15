path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'
with open(path, 'r') as f:
    lines = f.readlines()

# Find the "8. **Rev. 31" line (should be around line 409)
rev31_idx = None
for i, line in enumerate(lines):
    if line.startswith('8. **Rev. 31 — 14 Oktober 2026'):
        rev31_idx = i
        break

if rev31_idx is None:
    print("ERROR: Could not find '8. **Rev. 31' line")
else:
    print(f"Found '8. **Rev. 31' at line index {rev31_idx} (1-indexed: {rev31_idx + 1})")
    
    # The Rev. 31 entry includes the header line + detail lines until a blank line
    # Find the end of the details (the last non-blank line before a blank line)
    detail_end = rev31_idx + 1
    while detail_end < len(lines) and lines[detail_end].strip() != '':
        detail_end += 1
    
    print(f"Rev. 31 entry spans lines {rev31_idx + 1} to {detail_end} (1-indexed)")
    
    # Replace the header line
    lines[rev31_idx] = '7. **Rev. 30 — 14 Oktober 2026 (WIB).** Re-verifikasi final kondisi repo + `dev.db` (SQLite, cron run): **1 user (admin@pondokanat.com, role admin)** | **5 role** (admin, guru, wali_kelas, pengasuh, santri) | **33 role_permissions** (M01) | **441 siswa** (semua `inactive`; `uid_nfc` = 0 terisi) | **18 kelas** (TAMHIDI A/B + 1A–6B, 12 seksi A/B + TA A + TB + TK; TAMHIDI A/B/Takhosous = 0) | **54 guru** (impor Excel, semua `active`) | **32 mapel** | **5.420 nilai** | **0 record** tabel silabus/rpp/absensi/rapor/announcements/messages/notifications. **dev.db:** total 15 tabel (users, roles, role_permissions, students, classes, teachers, subjects, silabus, rpp, absensi, grades, rapor, announcements, messages, notifications). **Siswa per kelas:** TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosous=0; **TOTAL = 441**. **M02a (NFC):** field `uid_nfc` ada di tabel `students` (kolom setelah `photo`) namun **0 siswa** terisi (data ekspor NFC Tools belum tersedia — mapping UID → NISN tertunda). **Status:** dokumen PRD **FINAL**; state stabil, tidak ada perubahan dari Rev. 29.\n'
    
    # Replace the detail lines (rev31_idx+1 to detail_end-1) with the new Rev. 31 details
    new_rev31_details = [
        '8. **Rev. 31 — 14 Oktober 2026 (WIB).** Re-verification final kondisi repo + `dev.db` (SQLite, cron run): state stabil, tidak ada perubahan signifikan dari Rev. 30.\n',
        '   - **Database (dev.db):** 1 user (admin@pondokanat.com, role admin) | 5 role (admin, guru, wali_kelas, pengasuh, santri) | 33 role_permissions (M01, seed via .seed_users_roles.py) | 441 siswa (semua `inactive` — menunggu aktivasi, `active` = 0, `uid_nfc` = 0 terisi) | 18 kelas (TAMHIDI A/B + 1A–6B, 12 seksi A/B + TA A + TB + TK) | 54 guru (impor Excel, semua `active`) | 32 mapel | 5.420 nilai | 0 record di tabel silabus/rpp/absensi/rapor/announcements/messages/notifications.\n',
        '   - **Siswa per kelas:** TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosous=0; **TOTAL = 441**.\n',
        '   - **M02a (NFC):** field `uid_nfc` ada di tabel `students` (kolom setelah `photo`) namun **0 siswa** terisi (data ekspor NFC Tools belum tersedia — mapping UID → NISN tertunda).\n',
        '   - **KitabProgress:** masih *referenced* di `Subject` (`KitabProgress[]`) tetapi **tidak didefinisikan** di `prisma/schema.prisma` (baris 117) — perlu ditambahkan kalau fitur progress kitab dibangun.\n',
        '   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (typo indeks `pondokanbat.com`); produksi butuh bcrypt + session.\n',
        '   - **Beranda hardcode:** `Beranda.tsx` masih hardcoded `totalSantri: 441, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB).\n',
        '   - **Build quality gate:** `tsc --noEmit` OK (exit 0); `npm run lint` OK (exit 0, 6 warning / 0 error); `npm run build` OK (Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3).\n',
        '   - **Status:** dokumen PRD **FINAL**; state stabil; rev 31 = penutupan audit & konfirmasi stabilitas.\n',
    ]
    
    # Replace lines from rev31_idx+1 to detail_end with new details
    # The slice should replace lines[rev31_idx+1:detail_end] with new_rev31_details
    lines[rev31_idx+1:detail_end] = new_rev31_details
    
    with open(path, 'w') as f:
        f.writelines(lines)
    
    print(f"Fixed. Total lines now: {len(lines)}")

print("Done")
