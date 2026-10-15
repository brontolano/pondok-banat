path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'

with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Line 4 (index 3) is the header — needs to be replaced with Rev. 59
# Use the correct Rev. 59 header
new_header = """> **Rev. 59 — 15 Oktober 2026 (WIB).** Verifikasi fresh kondisi repo + `dev.db` (SQLite, cron run): state stabil. **Tidak ada perubahan signifikan dari Rev. 58** (data terkonsisten). Database (dev.db): 1 user (**admin@pondokanat.com**, role admin) | **5 role** (admin, guru, wali_kelas, pengasuh, santri) | **33 role_permissions** (M01) | **441 siswa** (semua `inactive` — menunggu aktivasi, `active` = 0, `uid_nfc` = 0 terisi) | **18 kelas** (TAMHIDI A/B + 1A–6B, 12 seksi A/B + TA A + TB + TK; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0) | **54 guru** (impor Excel, semua `active`) | **32 mapel** | **5.420 nilai** | **0 record** di tabel silabus/rpp/absensi/rapor/announcements/messages/notifications. **Siswa per kelas (diverifikasi langsung dari `dev.db`):** TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0; **TOTAL = 441**. **M02a (NFC):** field `uid_nfc` **ada aktif** di tabel `students` (kolom setelah `photo`); `prisma/schema.prisma` baris 68 (`uidNfc String? @map(\"uid_nfc\")`), `init_schema.sql` baris 44, `init_db.py` baris 60. **Tidak ada satupun siswa yang memiliki `uid_nfc` diisi** (semua 441 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`). **Schema:** model `KitabProgress` (Student + Subject) & `Sertakan` (User) selesai didefinisikan (Rev. 51); `prisma validate` sukses. **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (typo indeks `pondokanat.com`); **catatan: DB memiliki `admin@pondokanat.com` (beda domain 'a' vs 'b') — inkonsistensi Login.tsx vs dev.db**; produksi butuh bcrypt + session. **Beranda hardcode:** `Beranda.tsx` masih hardcoded `totalSantri: 441, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB). **Build quality gate (Verifikasi Rev. 59):** `tsc --noEmit` ✓ (exit 0); `npm run lint` ✓ (exit 0, 1 warning — 0 error; peringatan `eslint.config.js:4:1 import/no-anonymous-default-export`); `npm run build` ✓ (exit 0, Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3). **Repo state:** clean working tree; **bukan git repository** (tidak ada history git). **Status:** dokumen PRD **REVISI** — rev 59 = verifikasi fresh ulang; seluruh data stabil; tidak ada perubahan signifikan dari Rev. 58."""

lines[3] = new_header + "\n"

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("File updated. Total lines:", len(lines))
print("Line 4 first 120 chars:", lines[3][:120])
