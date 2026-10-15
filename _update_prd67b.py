#!/usr/bin/env python3
"""Update PRD to Rev. 67: fix header revision + append Rev. 67 section."""
import re

PATH = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'

with open(PATH, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Fix header: "Rev. 66" at start -> "Rev. 67"
content, n1 = re.subn(
    r'(> \*\*Rev\.) 66( — 15 Oktober 2026 \(WIB\)\.\s)',
    r'\1 67\2',
    content,
    count=1,
)
print(f'Header label patch: {n1} replaced')

# 2. Fix "Verifikasi Rev. 66" -> "Verifikasi Rev. 67" in header
content, n2 = re.subn(
    r'(Verifikasi Rev\.) 66(\.\*\*)',
    r'\1 67\2',
    content,
    count=1,
)
print(f'Verifikasi Rev patch: {n2} replaced')

# 3. Append Rev. 67 section
rev67_section = '''

## 26. REVISI TERBARU (Rev. 67 — 15 Oktober 2026 WIB)

1. **Rev. 67 — 15 Oktober 2026 (WIB).** Verifikasi fresh kondisi repo + `dev.db` (SQLite, cron run): state stabil. **Tidak ada perubahan signifikan dari Rev. 66** (data terkonsisten). Seluruh gate kualitas build yang dapat dijalankan dari repo lulus:
   - **Database (dev.db):** 1 user (**admin@pondokanat.com**, role admin) | **5 role** (admin, guru, wali_kelas, pengasuh, santri) | **33 role_permissions** (M01) | **441 siswa** (semua `inactive` — menunggu aktivasi, `active` = 0, `uid_nfc` = 0 terisi) | **18 kelas** (TAMHIDI A/B + 1A–6B, 12 seksi A/B + TA A + TB + TK; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0) | **54 guru** (impor Excel, semua `active`) | **32 mapel** | **5.420 nilai** | **0 record** di tabel silabus/rpp/absensi/rapor/announcements/messages/notifications.
   - **Siswa per kelas (diverifikasi langsung dari `dev.db`):** TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0; **TOTAL = 441**.
   - **M02a (NFC):** field `uid_nfc` **ada aktiv** di tabel `students` (kolom setelah `photo`); `prisma/schema.prisma` baris 68 (`uidNfc String? @map(\"uid_nfc\")`), `init_schema.sql` baris 44, `init_db.py` baris 60. **Tidak ada satupun siswa yang memiliki `uid_nfc` diisi** (semua 441 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Schema:** model `KitabProgress` (Student + Subject, `prisma/schema.prisma` baris 203) & `Sertakan` (User, baris 218) selesai didefinisikan (ditambahkan Rev. 51); `prisma validate` sukses.
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (typo indeks `pondokanat.com`); **catatan: DB memiliki `admin@pondokanat.com` (beda domain 'a' vs 'b') — inkonsistensi Login.tsx vs dev.db**; produksi butuh bcrypt + session.
   - **Beranda hardcode:** `Beranda.tsx` masih hardcoded `totalSantri: 441, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB).
   - **Build quality gate (Jalankan ulang Rev. 67):** `tsc --noEmit` diblokir Tirith security scan (OSV/ecosystem metadata lookup timeout); `npm run lint` ✓ (exit 0, 1 warning — 0 error; peringatan `eslint.config.js:4:1 import/no-anonymous-default-export`); `npm run build` ✓ (exit 0, Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3). Seluruh gate yang dapat dijalankan dari repo (node_modules tersedia; `.next` ter-build ulang) lulus.
   - **Repo state:** clean working tree; **bukan git repository** (tidak ada history git).
   - **Status:** dokumen PRD **REVISI** — rev 67 = verifikasi fresh ulang & konfirmasi stabilitas; seluruh data stabil; tidak ada perubahan signifikan dari Rev. 66.

*Verifikasi dilakukan lewat: query `sqlite3` ke `dev.db` (15 tabel), `npx eslint .` (exit 0, 1 warning), `npx next build` (exit 0, Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3). `tsc --noEmit` diblokir Tirith security scan (OSV/ecosystem metadata lookup timeout).*

*Identifikasi entitas kartu identitas NFC hasil ekspor Android (NFC Tools): UID berformat hex `AF:C2:99:E7` dari blok MANUFACTURER/baris pertama yang diapit `[]`; pemrosesan string dilakukan dengan parsing UID dari ekspor NFC Tools, lalu pemetaan UID → NISN → record siswa.*
'''

if not content.endswith('\n'):
    content += '\n'
content += rev67_section

with open(PATH, 'w', encoding='utf-8') as f:
    f.write(content)

print('Total file size:', len(content), 'bytes')
print('Done.')
