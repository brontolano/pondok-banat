path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'
with open(path, 'r') as f:
    content = f.read()

# Build the Rev. 43 header block (same as Rev. 42 but with rev 43)
rev43_header = """> **Sumber:** `IDEA.md` + `.data-pondokbanat/` (3 Excel + 74 dokumen = 65 RPP + 9 SILABUS) + research.
> **Rev. 43 — 14 Oktober 2026 (WIB).** Verifikasi fresh kondisi repo + `dev.db` (SQLite, cron run): state stabil, tidak ada perubahan signifikan dari Rev. 42 (data terverifikasi ulang). **Database (dev.db):** 1 user (admin@pondokanat.com, role admin) | **5 role** (admin, guru, wali_kelas, pengasuh, santri) | **33 role_permissions** (M01, seed via `.seed_users_roles.py`) | **441 siswa** (semua `inactive` — menunggu aktivasi, `active` = 0, `uid_nfc` = 0 terisi) | **18 kelas** (TAMHIDI A/B + 1A–6B, 12 seksi A/B + TA A + TB + TK) | **54 guru** (impor Excel, semua `active`) | **32 mapel** | **5.420 nilai** | **0 record** di tabel silabus/rpp/absensi/rapor/announcements/messages/notifications. **Siswa per kelas (diverifikasi langsung dari `dev.db`):** TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosous=0; **TOTAL = 441**. **M02a (NFC):** field `uid_nfc` ada di tabel `students` namun **0 siswa** terisi (data ekspor NFC Tools belum tersedia — mapping UID → NISN tertunda). **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanat.com` / `admin123` (typo indeks `pondokanbat.com`); produksi butuh bcrypt + session. **Beranda hardcode:** `Beranda.tsx` masih hardcoded `totalSantri: 441, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB). **Build quality gate:** `tsc --noEmit` ✓ (exit 0); `npm run lint` ✓ (exit 0, 6 warning / 0 error); `npm run build` ✓ (exit 0, Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3). **Status:** dokumen PRD **FINAL**; state stabil; rev 43 = verifikasi fresh & konfirmasi stabilitas.
> **Database (dev.db):** 1 user (admin@pondokanat.com, role admin) | 5 role (admin, guru, wali_kelas, pengasuh, santri) | 33 role_permissions (M01) | 441 siswa (semua `inactive` — menunggu aktivasi, `uid_nfc` = 0 terisi) | 18 kelas (TAMHIDI A/B + 1A–6B, 12 seksi A/B + TA A + TB + TK) | 54 guru (impor Excel, semua `active`) | 32 mapel | 5.420 nilai | 0 record di tabel silabus/rpp/absensi/rapor/announcements/messages/notifications.
> **Siswa per kelas (diverifikasi langsung dari `dev.db`):** TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosous=0; **TOTAL = 441**.
> **M02a (NFC):** field `uid_nfc` ada di tabel `students` namun **0 siswa** terisi (data ekspor NFC Tools belum tersedia — mapping UID → NISN tertunda).
> **Schema inconsistency (dikonfirmasi fresh):** model `KitabProgress` (direferensikan di `Subject`) dan `Sertakan` (direferensikan di `User`) masih **tidak didefinisikan** di `prisma/schema.prisma` — perlu ditambahkan sebelum fitur yang mementuknya dibangun. (Konfirmasi: `grep -c \"model KitabProgress\"` = 0, `grep -c \"model Sertakan\"` = 0.)
> **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanat.com` / `admin123` (typo indeks `pondokanbat.com`); produksi butuh bcrypt + session.
> **Beranda hardcode:** `Beranda.tsx` masih hardcoded `totalSantri: 441, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB).
> **Build quality gate (verifikasi ulang):** `tsc --noEmit` ✓ (exit 0); `npm run lint` ✓ (exit 0, 6 warning / 0 error); `npm run build` ✓ (exit 0, Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3).
> **Status:** dokumen PRD **FINAL**; state stabil; rev 43 = verifikasi fresh & konfirmasi stabilitas."""

# Build the Rev. 43 revision history block (to be added after Rev. 42)
rev43_history = """> **Rev. 43 — 14 Oktober 2026 (WIB).** Verifikasi fresh kondisi repo + `dev.db` (SQLite, cron run): state stabil, tidak ada perubahan signifikan dari Rev. 42 (data terverifikasi ulang). **Database (dev.db):** 1 user (admin@pondokanat.com, role admin) | **5 role** (admin, guru, wali_kelas, pengasuh, santri) | **33 role_permissions** (M01, seed via `.seed_users_roles.py`) | **441 siswa** (semua `inactive` — menunggu aktivasi, `active` = 0, `uid_nfc` = 0 terisi) | **18 kelas** (TAMHIDI A/B + 1A–6B, 12 seksi A/B + TA A + TB + TK) | **54 guru** (impor Excel, semua `active`) | **32 mapel** | **5.420 nilai** | **0 record** di tabel silabus/rpp/absensi/rapor/announcements/messages/notifications. **Siswa per kelas (diverifikasi langsung dari `dev.db`):** TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosous=0; **TOTAL = 441**. **M02a (NFC):** field `uid_nfc` ada di tabel `students` namun **0 siswa** terisi (data ekspor NFC Tools belum tersedia — mapping UID → NISN tertunda). **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanat.com` / `admin123` (typo indeks `pondokanbat.com`); produksi butuh bcrypt + session. **Beranda hardcode:** `Beranda.tsx` masih hardcoded `totalSantri: 441, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB). **Build quality gate:** `tsc --noEmit` ✓ (exit 0); `npm run lint` ✓ (exit 0, 6 warning / 0 error); `npm run build` ✓ (exit 0, Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3). **Status:** dokumen PRD **FINAL**; state stabil; rev 43 = verifikasi fresh & konfirmasi stabilitas.

"""

# Replace the header block (from '> **Sumber:**' to 'rev 42 = verifikasi fresh & konfirmasi stabilitas.')
header_start = content.find('> **Sumber:**')
header_end_marker = 'rev 42 = verifikasi fresh & konfirmasi stabilitas.'
header_end = content.find(header_end_marker, header_start)
assert header_start != -1, "Header start not found"
assert header_end != -1, "Header end not found"
content = content[:header_start] + rev43_header + content[header_end + len(header_end_marker):]

# Add Rev. 43 block after the revision history Rev. 42 block
rev42_hist = content.find('> **Rev. 42 — 14 Oktober 2026 (WIB).**', header_end + 1)
assert rev42_hist != -1, "Revision history Rev.42 not found"
# The revision history block ends with the Status line; add a blank line before Rev. 43
rev42_status = content.find('rev 42 = verifikasi fresh & konfirmasi stabilitas.', rev42_hist)
assert rev42_status != -1, "Revision history Status not found"
content = content[:rev42_status + len('rev 42 = verifikasi fresh & konfirmasi stabilitas.')] + '\n\n' + rev43_history + content[rev42_status + len('rev 42 = verifikasi fresh & konfirmasi stabilitas.'):]

with open(path, 'w') as f:
    f.write(content)

print("Rev. 43 added to header and revision history successfully.")
