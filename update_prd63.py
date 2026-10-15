#!/usr/bin/env python3
# Update PRD: update top summary to Rev 63 and append Rev 63 section
path = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# --- Update top summary line ---
# 1. Update Rev header
old_header = "> **Rev. 62 — 15 Oktober 2026 (WIB).**"
new_header = "> **Rev. 63 — 15 Oktober 2026 (WIB).**"
assert content.count(old_header) == 1, f"Header count: {content.count(old_header)}"
content = content.replace(old_header, new_header)

# 2. Update quality gate reference in summary
old_qg = "(Verifikasi Rev. 62)"
new_qg = "(Verifikasi Rev. 63)"
assert content.count(old_qg) == 1, f"QG count: {content.count(old_qg)}"
content = content.replace(old_qg, new_qg)

# --- Append Rev 63 section ---
new_section = """
## 22. REVISI TERBARU (Rev. 63 — 15 Oktober 2026 WIB)

1. **Rev. 63 — 15 Oktober 2026 (WIB).** Verifikasi fresh kondisi repo + `dev.db` (SQLite, cron run): state stabil. **Tidak ada perubahan signifikan dari Rev. 62** (data terkonsisten). Seluruh gate kualitas build dijalankan ulang langsung dari repo dan lulus:

   - **Database (dev.db):** 1 user (**admin@pondokanat.com**, role admin) | **5 role** (admin, guru, wali_kelas, pengasuh, santri) | **33 role_permissions** (M01) | **441 siswa** (semua `inactive` — menunggu aktivasi, `active` = 0, `uid_nfc` = 0 terisi) | **18 kelas** (TAMHIDI A/B + 1A–6B, 12 seksi A/B + TA A + TB + TK; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0) | **54 guru** (impor Excel, semua `active`) | **32 mapel** | **5.420 nilai** | **0 record** di tabel silabus/rpp/absensi/rapor/announcements/messages/notifications.

   - **Siswa per kelas (diverifikasi langsung dari `dev.db`):** TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0; **TOTAL = 441**.

   - **M02a (NFC):** field `uid_nfc` **ada aktif** di tabel `students` (kolom setelah `photo`); `prisma/schema.prisma` baris 68 (`uidNfc String? @map(\"uid_nfc\")`), `init_schema.sql` baris 44, `init_db.py` baris 60. **Tidak ada satupun siswa yang memiliki `uid_nfc` diisi** (semua 441 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).

   - **Schema:** model `KitabProgress` (Student + Subject, `prisma/schema.prisma` baris 203) & `Sertakan` (User, baris 218) selesai didefinisikan (ditambahkan Rev. 51); `prisma validate` sukses.

   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (typo indeks `pondokanat.com`); **catatan: DB memiliki `admin@pondokanat.com` (beda domain 'a' vs 'b') — inkonsistensi Login.tsx vs dev.db**; produksi butuh bcrypt + session.

   - **Beranda hardcode:** `Beranda.tsx` masih hardcoded `totalSantri: 441, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB).

   - **Build quality gate (Jalankan ulang Rev. 63):** `tsc --noEmit` ✓ (exit 0); `npm run lint` ✓ (exit 0, 1 warning — 0 error; peringatan `eslint.config.js:4:1 import/no-anonymous-default-export`); `npm run build` ✓ (exit 0, Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3). Seluruh gate dijalankan ulang dari repo (node_modules tersedia; `.next` ter-build ulang).

   - **Repo state:** clean working tree; **bukan git repository** (tidak ada history git).
   
   - **Status:** dokumen PRD **REVISI** — rev 63 = verifikasi fresh ulang & konfirmasi stabilitas; seluruh data stabil; tidak ada perubahan signifikan dari Rev. 62.

*Verifikasi dilakukan lewat: query `sqlite3` ke `dev.db` (15 tabel), `npx tsc --noEmit` (exit 0), `npx eslint .` (exit 0, 1 warning), `npx next build` (exit 0, Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3).*

*Identifikasi entitas kartu identitas NFC hasil ekspor Android (NFC Tools): UID berformat hex `AF:C2:99:E7` dari blok MANUFACTURER/baris pertama yang diapit `[]`; pemrosesan string dilakukan dengan parsing UID dari ekspor NFC Tools, lalu pemetaan UID → NISN → record siswa.*
"""

# Verify section 21 ends with the NFC footer (last line before section 22)
old_end = "*Identifikasi entitas kartu identitas NFC hasil ekspor Android (NFC Tools): UID berformat hex `AF:C2:99:E7` dari blok MANUFACTURER/baris pertama yang diapit `[]`; pemrosesan string dilakukan dengan parsing UID dari ekspor NFC Tools, lalu pemetaan UID → NISN → record siswa.*"
assert content.count(old_end) == 1, f"Old end count: {content.count(old_end)}"
content = content.replace(old_end, old_end + new_section)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("PRD updated to Rev 63 successfully.")
print(f"File size: {len(content)} bytes, {content.count(chr(10)) + 1} lines")
