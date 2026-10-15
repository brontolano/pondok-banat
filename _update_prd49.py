import sys

with open('PRD-PONDOK-BANAT.md', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update the header (Rev. 48 -> Rev. 49)
content = content.replace(
    '> **Rev. 48 — 15 Oktober 2026 (WIB).**',
    '> **Rev. 49 — 15 Oktober 2026 (WIB).**'
)
content = content.replace(
    '> **Tidak ada perubahan signifikan dari Rev. 47** (data terkonsisten).',
    '> **Tidak ada perubahan signifikan dari Rev. 48** (data terkonsisten).'
)
content = content.replace(
    '> Build quality gate (Verifikasi Rev. 48):',
    '> Build quality gate (Verifikasi Rev. 49):'
)
content = content.replace(
    '> **Status:** dokumen PRD **REVISI** — dokumen PRD diperbarui ke Rev. 48 sesuai verifikasi ulang fresh kondisi repo + dev.db (state stabil, tidak ada perubahan signifikan dari Rev. 47).',
    '> **Status:** dokumen PRD **REVISI** — dokumen PRD diperbarui ke Rev. 49 sesuai verifikasi ulang fresh kondisi repo + dev.db (state stabil, tidak ada perubahan signifikan dari Rev. 48).'
)

# 2. Add the new revision entry after the Rev. 48 history entry
rev49_entry = '''26. **Rev. 49 — 15 Oktober 2026 (WIB).** Fresh verification seluruh kondisi repo + `dev.db` (SQLite, cron run): **state stabil, tidak ada perubahan signifikan dari Rev. 48**. Build quality gate: `tsc --noEmit` ✓ (exit 0); `npm run lint` ✓ (exit 0, 1 warning / 0 error); `npm run build` ✓ (exit 0, Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3). Database (dev.db): 1 user (admin@pondokanat.com, role admin) | 5 role (admin, guru, wali_kelas, pengasuh, santri) | 33 role_permissions (M01, seed via .seed_users_roles.py) | 441 siswa (semua `inactive` — menunggu aktivasi) | 18 kelas (TAMHIDI A/B + 1A–6B, 12 seksi A/B + TA A + TB + TK; TAMHIDI A/B/Takhosours = 0) | 54 guru (impor Excel, semua `active`) | 32 mapel | 5.420 nilai | 0 record di tabel silabus/rpp/absensi/rapor/announcements/messages/notifications. **Siswa per kelas:** TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0; **TOTAL = 441**. **M02a (NFC):** field `uid_nfc` ada di tabel `students` (kolom setelah `photo`) namun **0 siswa** terisi (data ekspor NFC Tools belum tersedia — mapping UID → NISN tertunda). **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanat.com` / `admin123` (typo indeks `pondokanat.com`); produksi butuh bcrypt + session. **Beranda hardcode:** `Beranda.tsx` masih hardcoded `totalSantri: 441, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB). **KitabProgress & Sertakan:** keduanya **sudah didefinisikan** di `prisma/schema.prisma` (model `KitabProgress` di baris 203, model `Sertakan` di baris 218 — ditambahkan Rev. 51); `prisma validate` sukses. Progress kitab & relation User telah disiapkan untuk iterasi berikut. **Status:** dokumen PRD **REVISI** — dokumen PRD diperbarui ke Rev. 49 sesuai verifikasi ulang fresh kondisi repo + dev.db (state stabil, tidak ada perubahan signifikan dari Rev. 48).

'''

# Insert after the Rev. 48 history entry
old_rev48 = '25. **Rev. 48 — 15 Oktober 2026 (WIB).** Fresh verification seluruh kondisi repo + `dev.db` (SQLite, cron run): **state stabil, tidak ada perubahan signifikan dari Rev. 47**. Build quality gate: `tsc --noEmit` ✓ (exit 0); `npm run lint` ✓ (exit 0, 1 warning / 0 error); `npm run build` ✓ (exit 0, Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3). Database (dev.db): 1 user (admin@pondokanat.com, role admin) | 5 role (admin, guru, wali_kelas, pengasuh, santri) | 33 role_permissions (M01, seed via .seed_users_roles.py) | 441 siswa (semua `inactive` — menunggu aktivasi) | 18 kelas (TAMHIDI A/B + 1A–6B, 12 seksi A/B + TA A + TB + TK; TAMHIDI A/B/Takhosours = 0) | 54 guru (impor Excel, semua `active`) | 32 mapel | 5.420 nilai | 0 record di tabel silabus/rpp/absensi/rapor/announcements/messages/notifications. **Siswa per kelas:** TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0; **TOTAL = 441**. **M02a (NFC):** field `uid_nfc` ada di tabel `students` (kolom setelah `photo`) namun **0 siswa** terisi (data ekspor NFC Tools belum tersedia — mapping UID → NISN tertunda). **KitabProgress & Sertakan:** keduanya **sudah didefinisikan** di `prisma/schema.prisma` (model `KitabProgress` di baris 203, model `Sertakan` di baris 218 — ditambahkan Rev. 51); `prisma validate` sukses. Progress kitab & relation User telah disiapkan untuk iterasi berikut. **Status:** dokumen PRD **REVISI** — dokumen PRD diperbarui ke Rev. 48 sesuai verifikasi ulang fresh kondisi repo + dev.db (state stabil, tidak ada perubahan signifikan dari Rev. 47).'

if old_rev48 in content:
    content = content.replace(old_rev48, old_rev48 + '\n' + rev49_entry)
    print("Added Rev. 49 entry")
else:
    print("ERROR: Could not find Rev. 48 history entry")
    sys.exit(1)

with open('PRD-PONDOK-BANAT.md', 'w', encoding='utf-8') as f:
    f.write(content)

print("File updated successfully")
print(f"New line count: {len(content.split(chr(10)))}")
