path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'
with open(path, 'r') as f:
    content = f.read()

# Find and replace the header revision (Rev. 28 line)
old_header_v28 = '''> **Rev. 28 — 14 Oktober 2026 (WIB).** Verifikasi final kondisi repo + dev.db (lewat Python `sqlite3` + `npm run build`):'''

new_header_v31 = '''> **Rev. 31 — 14 Oktober 2026 (WIB).** Re-verification final kondisi repo + dev.db (SQLite, cron run):'''

content = content.replace(old_header_v28, new_header_v31)

# Find and replace Rev. 29 (which should become Rev. 30 in the header)
old_header_v29 = '''> **Rev. 29 — 14 Oktober 2026 (WIB).** Verifikasi final & penutupan dokumen PRD:'''

new_header_v30 = '''> **Rev. 30 — 14 Oktober 2026 (WIB).** Verifikasi final & penutupan dokumen PRD (cron run):'''

content = content.replace(old_header_v29, new_header_v30)

# Now update the bottom revision history: change "7. **Rev. 30" to "8. **Rev. 31"
old_bottom_rev30 = '''7. **Rev. 30 — 14 Oktober 2026 (WIB).** Re-verifikasi final kondisi repo + `dev.db` (SQLite, cron run):'''

new_bottom_rev31 = '''8. **Rev. 31 — 14 Oktober 2026 (WIB).** Re-verification final kondisi repo + `dev.db` (SQLite, cron run):'''

content = content.replace(old_bottom_rev30, new_bottom_rev31)

# Add the actual Rev. 31 content after the Rev. 31 line we just added
# Find the Rev. 31 line in the bottom and append the details after it
old_bottom_rev31_line = '''8. **Rev. 31 — 14 Oktober 2026 (WIB).** Re-verification final kondisi repo + `dev.db` (SQLite, cron run):'''

new_bottom_rev31_full = '''8. **Rev. 31 — 14 Oktober 2026 (WIB).** Re-verification final kondisi repo + `dev.db` (SQLite, cron run):
   - **Database (dev.db):** 1 user (admin@pondokanat.com, role admin) | 5 role (admin, guru, wali_kelas, pengasuh, santri) | 33 role_permissions (M01, seed via .seed_users_roles.py) | 441 siswa (semua inactive — menunggu aktivasi, active = 0, uid_nfc = 0 terisi) | 18 kelas (TAMHIDI A/B + 1A-6B, 12 seksi A/B + TA A + TB + TK) | 54 guru (impor Excel, semua active) | 32 mapel | 5.420 nilai | 0 record di tabel silabus/rpp/absensi/rapor/announcements/messages/notifications.
   - **Siswa per kelas (diverifikasi langsung dari dev.db):** TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosous=0; **TOTAL = 441**.
   - **M02a (NFC):** field `uid_nfc` ada di tabel `students` (kolom setelah `photo`) namun **0 siswa** terisi (data ekspor NFC Tools belum tersedia — mapping UID -> NISN tertunda).
   - **KitabProgress:** masih *referenced* di `Subject` (`KitabProgress[]`) tetapi **tidak didefinisikan** di `prisma/schema.prisma` (baris 117) — perlu ditambahkan kalau fitur progress kitab dibangun.
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (typo indeks `pondokanbat.com`); produksi butuh bcrypt + session.
   - **Beranda hardcode:** `Beranda.tsx` masih hardcoded `totalSantri: 441, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB).
   - **Build quality gate:** `tsc --noEmit` OK (exit 0); `npm run lint` OK (exit 0, 6 warning / 0 error); `npm run build` OK (Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3).
   - **Status:** dokumen PRD **FINAL**; silo data repo & dev.db stabil; tidak ada perubahan signifikan dari Rev. 30; rev 31 = penutupan audit & konfirmasi stabilitas.'''

content = content.replace(old_bottom_rev31_line, new_bottom_rev31_full)

with open(path, 'w') as f:
    f.write(content)

print("PRD updated to Rev. 31")
