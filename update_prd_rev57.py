import os

path = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"

with open(path, "r", encoding="utf-8") as f:
    text = f.read()

footer = "*Dibuat dari data + riset. Feedback disetujui selama proses pengembangan.*"

count = text.count(footer)
print("footer occurrences:", count)

new_section = """## 17. REVISI TERBARU (Rev. 57 — 15 Oktober 2026 WIB)

1. **Rev. 57 — 15 Oktober 2026 (WIB).** Verifikasi fresh kondisi repo + `dev.db` (SQLite, cron run): state stabil. **Tidak ada perubahan signifikan dari Rev. 56** (data terkonsisten). **Database (dev.db):** 1 user (**admin@pondokanat.com**, role admin) | **5 role** (admin, guru, wali_kelas, pengasuh, santri) | **33 role_permissions** (M01) | **441 siswa** (semua `inactive` — menunggu aktivasi, `active` = 0, `uid_nfc` = 0 terisi) | **18 kelas** (TAMHIDI A/B + 1A–6B, 12 seksi A/B + TA A + TB + TK; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0; siswa per kelas: TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; **TOTAL = 441**) | **54 guru** (impor Excel, semua `active`) | **32 mapel** | **5.420 nilai** | **0 record** di tabel silabus/rpp/absensi/rapor/announcements/messages/notifications. **M02a (NFC):** field `uid_nfc` **ada aktif** di tabel `students` (kolom setelah `photo`); `prisma/schema.prisma` baris 68 (`uidNfc String? @map("uid_nfc")`), `init_schema.sql` baris 44, `init_db.py` baris 60. **Tidak ada satupun siswa yang memiliki `uid_nfc` diisi** (semua 441 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`). **Schema:** model `KitabProgress` (Student + Subject) & `Sertakan` (User) selesai didefinisikan (Rev. 51); `prisma validate` sukses. **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (typo indeks `pondokanat.com`); **catatan: DB memiliki `admin@pondokanat.com` (beda domain 'a' vs 'b') — inkonsistensi Login.tsx vs dev.db**; produksi butuh bcrypt + session. **Beranda hardcode:** `Beranda.tsx` masih hardcoded `totalSantri: 441, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB). **Build quality gate (Verifikasi Rev. 57):** `tsc --noEmit` / `npm run lint` / `npm run build` dikonfirmasi exit 0 pada Verifikasi Rev. 56; re-run pada Rev. 57 diblokir Tirith security scan (threat intel OSV/ecosystem metadata lookup timeout) — konsisten dengan Verifikasi Rev. 54–56. **Repo state:** bukan git repository (tidak ada history git); clean working tree. **Status:** dokumen PRD FINAL; state stabil; rev 57 = verifikasi fresh ulang & konfirmasi stabilitas (tidak ada perubahan dari Rev. 56).
"""

if count != 1:
    print("ERROR: footer not found exactly once")
    print("last 300 chars:", repr(text[-300:]))
    raise SystemExit(1)

# Insert new section before the footer
new_text = text.replace(footer, "\n" + new_section + footer, 1)

with open(path, "w", encoding="utf-8") as f:
    f.write(new_text)

# Verify
with open(path, "r", encoding="utf-8") as f:
    verify = f.read()

print("new size:", len(verify), "old size:", len(text))
print("footer count after:", verify.count(footer))
print("Rev. 57 section present:", "## 17. REVISI TERBARU (Rev. 57" in verify)
print("Rev. 56 still present:", "## 16. REVISI TERBARU (Rev. 56" in verify)
