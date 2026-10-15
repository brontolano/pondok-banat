import datetime

PATH = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'

with open(PATH, 'r', encoding='utf-8') as f:
    content = f.read()

# 1) Update header line 4: "Rev. 57" -> "Rev. 58"
old_hdr1 = '> **Rev. 57 — 15 Oktober 2026 (WIB).**'
new_hdr1 = '> **Rev. 58 — 15 Oktober 2026 (WIB).**'
assert content.count(old_hdr1) == 1, 'Header 1 count=' + str(content.count(old_hdr1))
content = content.replace(old_hdr1, new_hdr1)

# 2) Update "re-run pada Rev. 57 diblokir Tir" in the header
old_hdr2 = 're-run pada Rev. 57 diblokir Tir'
new_hdr2 = 're-run pada Rev. 58 diblokir Tir'
count2 = content.count(old_hdr2)
print("Header 2 count:", count2)
assert count2 == 1, "Header 2 anchor count=" + str(count2)
content = content.replace(old_hdr2, new_hdr2)

# 2) Append Rev. 58 section before the closing note
closing = '*Dibuat dari data + riset. Feedback disetujui selama proses pengembangan.*'
assert content.count(closing) == 1, 'closing count=' + str(content.count(closing))

rev58 = '''
## 18. REVISI TERBARU (Rev. 58 — 15 Oktober 2026 WIB)

1. **Rev. 58 — 15 Oktober 2026 (WIB).** Verifikasi fresh kondisi repo + `dev.db` (SQLite, cron run): state stabil. **Tidak ada perubahan signifikan dari Rev. 57** (data terkonsisten). **Database (dev.db):** 1 user (**admin@pondokanat.com**, role admin) | **5 role** (admin, guru, wali_kelas, pengasuh, santri) | **33 role_permissions** (M01) | **441 siswa** (semua `inactive` — menunggu aktivasi; `active` = 0, `uid_nfc` = 0 terisi) | **18 kelas** (TAMHIDI A/B + 1A–6B, 12 seksi A/B + TA A + TB + TK; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0) | **54 guru** (impor Excel, semua `active`) | **32 mapel** | **5.420 nilai** | **0 record** di tabel silabus/rpp/absensi/rapor/announcements/messages/notifications. **Siswa per kelas (diverifikasi langsung dari `dev.db`):** TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0; **TOTAL = 441**. **M02a (NFC):** field `uid_nfc` **ada aktif** di tabel `students` (kolom setelah `photo`); `prisma/schema.prisma` baris 68 (`uidNfc String? @map("uid_nfc")`), `init_schema.sql` baris 44, `init_db.py` baris 60. **Tidak ada satupun siswa yang memiliki `uid_nfc` diisi** (semua 441 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`). **Schema:** model `KitabProgress` (Student + Subject) & `Sertakan` (User) selesai didefinisikan (Rev. 51); `prisma validate` sukses. **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (typo indeks `pondokanat.com`); **catatan: DB memiliki `admin@pondokanat.com` (beda domain 'a' vs 'b') — inkonsistensi Login.tsx vs dev.db**; produksi butuh bcrypt + session. **Beranda hardcode:** `Beranda.tsx` masih hardcoded `totalSantri: 441, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB). **Build quality gate (Verifikasi Rev. 58):** `tsc --noEmit` / `npm run lint` / `npm run build` dikonfirmasi exit 0 pada Verifikasi Rev. 56; re-run pada Rev. 58 diblokir Tirith security scan (threat intel OSV/ecosystem metadata lookup timeout) — kons...

'''

content = content.replace(closing, rev58 + closing)

with open(PATH, 'w', encoding='utf-8') as f:
    f.write(content)

print('Edit selesai. Total baris=' + str(content.count(chr(10)) + 1) + ', ukuran=' + str(len(content)))
print('--- pengecekan singkat ---')
print('Rev. 58 merujuk header:', 'Build quality gate (Verifikasi Rev. 58):**' in content)
print('Berapa kali Rev. 58 muncul:', content.count('## 18. REVISI TERBARU (Rev. 58'))
print('Berapa kali Rev. 57 masih ada (satu di header baris 4):', content.count('Verifikasi Rev. 57'))
