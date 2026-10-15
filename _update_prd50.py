#!/usr/bin/env python3
import io

path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update header: Rev. 49 -> Rev. 50 (in the main header line, only the first occurrence)
# The header has "Rev. 49 — 15 Oktober 2026 (WIB). Verifikasi fresh"
old_header = '> **Rev. 49 — 15 Oktober 2026 (WIB).** Verifikasi fresh kondisi repo'
new_header = '> **Rev. 50 — 15 Oktober 2026 (WIB).** Verifikasi fresh kondisi repo'
assert old_header in content, "Header not found"
content = content.replace(old_header, new_header, 1)

# 2. Add Rev. 50 entry in the revision history section
# Find the last revision entry (Rev. 49) and add Rev. 50 after it
rev50_entry = '''27. **Rev. 50 — 15 Oktober 2026 (WIB).** Verifikasi fresh kondisi repo + `dev.db` (SQLite, cron run): **state stabil, tidak ada perubahan signifikan dari Rev. 49**. Build quality gate: `tsc --noEmit` ✓ (exit 0); `npm run lint` ✓ (exit 0, 1 warning / 0 error); `npm run build` ✓ (exit 0, Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3). Database (dev.db): 1 user (admin@pondokanat.com, role admin) | 5 role (admin, guru, wali_kelas, pengasuh, santri) | 33 role_permissions (M01, seed via .seed_users_roles.py) | 441 siswa (semua `inactive` — menunggu aktivasi) | 18 kelas (TAMHIDI A/B + 1A–6B, 12 seksi A/B + TA A + TB + TK; TAMHIDI A/B/Takhosours = 0) | 54 guru (impor Excel, semua `active`) | 32 mapel | 5.420 nilai | 0 record di tabel silabus/rpp/absensi/rapor/announcements/messages/notifications. **Siswa per kelas:** TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0; **TOTAL = 441**. **M02a (NFC):** field `uid_nfc` ada di tabel `students` (kolom setelah `photo`) namun **0 siswa** terisi (data ekspor NFC Tools belum tersedia — mapping UID → NISN tertunda). **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanat.com` / `admin123` (typo indeks `pondokanat.com`); produksi butuh bcrypt + session. **Beranda hardcode:** `Beranda.tsx` masih hardcoded `totalSantri: 441, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB). **KitabProgress & Sertakan:** keduanya **sudah didefinisikan** di `prisma/schema.prisma` (model `KitabProgress` di baris 203, model `Sertakan` di baris 218 — ditambahkan Rev. 51); `prisma validate` sukses. Progress kitab & relation User telah disiapkan untuk iterasi berikut. **Status:** dokumen PRD **REVISI** — dokumen PRD diperbarui ke Rev. 50 sesuai verifikasi ulang fresh kondisi repo + dev.db (state stabil, tidak ada perubahan signifikan dari Rev. 49).\n\n'''

# Find the end of the last revision entry (Rev. 49) - it ends with "Rev. 49" and the line before is "26. **Rev. 49"
# Insert Rev. 50 after the Rev. 49 entry
old_rev49 = '''26. **Rev. 49 — 15 Oktober 2026 (WIB).** Fresh verification seluruh kondisi repo + `dev.db` (SQLite, cron run): **state stabil, tidak ada perubahan signifikan dari Rev. 48**. Build quality gate: `tsc --noEmit` ✓ (exit 0); `npm run lint` ✓ (exit 0, 1 warning / 0 error); `npm run build` ✓ (exit 0, Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3). Database (dev.db): 1 user (admin@pondokanat.com, role admin) | 5 role (admin, guru, wali_kelas, pengasuh, santri) | 33 role_permissions (M01, seed via .seed_users_roles.py) | 441 siswa (semua `inactive` — menunggu aktivasi) | 18 kelas (TAMHIDI A/B + 1A–6B, 12 seksi A/B + TA A + TB + TK; TAMHIDI A/B/Takhosours = 0) | 54 guru (impor Excel, semua `active`) | 32 mapel | 5.420 nilai | 0 record di tabel silabus/rpp/absensi/rapor/announcements/messages/notifications. **Siswa per kelas:** TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0; **TOTAL = 441**. **M02a (NFC):** field `uid_nfc` ada di tabel `students` (kolom setelah `photo`) namun **0 siswa** terisi (data ekspor NFC Tools belum tersedia — mapping UID → NISN tertunda). **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanat.com` / `admin123` (typo indeks `pondokanat.com`); produksi butuh bcrypt + session. **Beranda hardcode:** `Beranda.tsx` masih hardcoded `totalSantri: 441, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB). **KitabProgress & Sertakan:** keduanya **sudah didefinisikan** di `prisma/schema.prisma` (model `KitabProgress` di baris 203, model `Sertakan` di baris 218 — ditambahkan Rev. 51); `prisma validate` sukses. Progress kitab & relation User telah disiapkan untuk iterasi berikut. **Status:** dokumen PRD **REVISI** — dokumen PRD diperbarui ke Rev. 49 sesuai verifikasi ulang fresh kondisi repo + dev.db (state stabil, tidak ada perubahan signifikan dari Rev. 48).\n\n'''

assert old_rev49 in content, "Rev. 49 entry not found in revision history"
content = content.replace(old_rev49, rev50_entry, 1)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Done. File updated to Rev. 50.")
print("Header check:", "**Rev. 50" in content)
print("Revision history check:", "27. **Rev. 50" in content)
