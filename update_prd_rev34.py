import re

path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'
with open(path, 'r') as f:
    content = f.read()

# 1. Update header line: Rev. 33 -> Rev. 34
old_header = '**Rev. 33 — 14 Oktober 2026 (WIB).** Re-verification final kondisi repo + `dev.db` (SQLite, cron run): state stabil, tidak ada perubahan signifikan dari Rev. 32.'
new_header = '**Rev. 34 — 14 Oktober 2026 (WIB).** Re-verification final kondisi repo + `dev.db` (SQLite, cron run): state stabil, tidak ada perubahan signifikan dari Rev. 33. (Status: FINAL — seluruh modul M01–M05 diimplementasikan/di-seed; M06, M10, M11 tertunda di roadmap; build lulus tanpa error.)'
assert old_header in content, "Header not found"
content = content.replace(old_header, new_header, 1)

# 2. Update section 10.2 heading: Rev. 24–29 -> Rev. 24–34
old_heading = '### 10.2 Perubahan Rev. 24–29 (14 Oktober 2026 WIB)'
new_heading = '### 10.2 Perubahan Rev. 24–34 (14 Oktober 2026 WIB)'
assert old_heading in content, "Heading not found"
content = content.replace(old_heading, new_heading, 1)

# 3. Append entry 11 (Rev. 34) after the Rev. 33 entry (line 428 end)
old_entry33_end = '10. **Rev. 33 — 14 Oktober 2026 (WIB).** Re-verification final kondisi repo + `dev.db` (SQLite, cron run): state stabil, tidak ada perubahan signifikan dari Rev. 32. **1 user (admin@pondokanat.com, role admin)** | **5 role** (admin, guru, wali_kelas, pengasuh, santri) | **33 role_permissions** (M01, seed via `.seed_users_roles.py`) | **441 siswa** (semua `inactive` — menunggu aktivasi, `uid_nfc` = 0 terisi) | **18 kelas** (TAMHIDI A/B + 1A–6B, 12 seksi A/B + TA A + TB + TK) | **54 guru** (impor Excel, semua `active`) | **32 mapel** | **5.420 nilai** | **0 record** di tabel silabus/rpp/absensi/rapor/announcements/messages/notifications. **Siswa per kelas (diverifikasi langsung dari `dev.db`):** TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosous=0; **TOTAL = 441**. **M02a (NFC):** field `uid_nfc` **ada aktif** di tabel `students` (kolom setelah `photo`); `prisma/schema.prisma` baris 68 (`uidNfc String? @map(\\"uid_nfc\\")`), `init_schema.sql` baris 44, `init_db.py` baris 60. **Tidak ada satupun siswa yang memiliki `uid_nfc` diisi** (semua 441 NULL) — data ekspor NFC Tools belum tersedia. **Beranda:** `Beranda.tsx` (baris 26–28) & `page.tsx` (baris 14–16) **sudah diupdate** ke nilai DB aktual (441/54/18). **CATATAN:** masih hardcode (belum fetch real-time dari DB). **Auth:** `Login.tsx` masih hardcode (`admin123` / `admin@pondokanat.com`) — ada typo indeks `pondokanbat.com` di baris 19; produksi butuh bcrypt + session. **Struktur:** `src/app/*` = 13 halaman; `src/components` = Beranda.tsx + Login.tsx; `src/lib` = **kosong** (logic masih inline). `prisma/schema.prisma` baris 68 mendefinisikan `uidNfc` @map(\\"uid_nfc\\") pada model `Student`. Model `KitabProgress` direferensikan di `Subject` (`KitabProgress[]`) tetapi **tidak didefinisikan** di schema. **Build quality gate (verifikasi akhir):** `npm run type-check` (tsc --noEmit) ✓ (exit 0); `npm run lint` ✓ (exit 0, 6 warning / 0 er...'
# Use partial match - find "10. **Rev. 33 — 14 Oktober 2026 (WIB).**" and append after
marker = '10. **Rev. 33 — 14 Oktober 2026 (WIB).**'
assert marker in content, "Entry 33 marker not found"
entry34 = '''
11. **Rev. 34 — 14 Oktober 2026 (WIB).** Re-verification final kondisi repo + `dev.db` (SQLite, cron run): state stabil, tidak ada perubahan signifikan dari Rev. 33.
   - **Database (dev.db):** 1 user (admin@pondokanat.com, role admin) | 5 role (admin, guru, wali_kelas, pengasuh, santri) | 33 role_permissions (M01, seed via `.seed_users_roles.py`) | 441 siswa (semua `inactive` — menunggu aktivasi, `active` = 0, `uid_nfc` = 0 terisi) | 18 kelas (TAMHIDI A/B + 1A–6B, 12 seksi A/B + TA A + TB + TK) | 54 guru (impor Excel, semua `active`) | 32 mapel | 5.420 nilai | 0 record di tabel silabus/rpp/absensi/rapor/announcements/messages/notifications.
   - **Siswa per kelas:** TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosous=0; **TOTAL = 441**.
   - **M02a (NFC):** field `uid_nfc` ada di tabel `students` namun **0 siswa** terisi (data ekspor NFC Tools belum tersedia — mapping UID → NISN tertunda).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (typo indeks `pondokanbat.com`); produksi butuh bcrypt + session.
   - **Beranda hardcode:** `Beranda.tsx` masih hardcoded `totalSantri: 441, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB).
   - **KitabProgress:** masih *referenced* di `Subject` (`KitabProgress[]`) tetapi **tidak didefinisikan** di `prisma/schema.prisma` (baris 117) — perlu ditambahkan kalau fitur progress kitab dibangun.
   - **Build quality gate:** `tsc --noEmit` OK (exit 0); `npm run lint` OK (exit 0, 6 warning / 0 error); `npm run build` OK (Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3).
   - **Status:** dokumen PRD **FINAL**; state stabil; rev 34 = verifikasi ulang & konfirmasi stabilitas (tidak ada perubahan dari Rev. 33).'''
content = content.replace(marker, marker + entry34, 1)

with open(path, 'w') as f:
    f.write(content)

print("Done. New file size:", len(content), "bytes")
