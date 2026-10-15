path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

rev39 = '''> **Rev. 39 — 14 Oktober 2026 (WIB).** Verifikasi fresh kondisi repo + `dev.db` (SQLite, cron run) — state stabil, tidak ada perubahan signifikan dari Rev. 38 (data terverifikasi ulang).
> **Database (dev.db):** 1 user (admin@pondokanat.com, role admin) | 5 role (admin, guru, wali_kelas, pengasuh, santri) | 33 role_permissions (M01) | 441 siswa (semua `inactive` — menunggu aktivasi, `active` = 0, `uid_nfc` = 0 terisi) | 18 kelas (TAMHIDI A/B + 1A–6B, 12 seksi A/B + TA A + TB + TK) | 54 guru (impor Excel, semua `active`) | 32 mapel | 5.420 nilai | 0 record di tabel silabus/rpp/absensi/rapor/announcements/messages/notifications.
> **Siswa per kelas (diverifikasi langsung dari `dev.db`):** TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosous=0; **TOTAL = 441**.
> **M02a (NFC):** field `uid_nfc` ada di tabel `students` namun **0 siswa** terisi (data ekspor NFC Tools belum tersedia — mapping UID → NISN tertunda).
> **Schema inconsistency (dikonfirmasi fresh):** model `KitabProgress` (direferensikan di `Subject`) dan `Sertakan` (direferensikan di `User`) masih **tidak didefinisikan** di `prisma/schema.prisma` — perlu ditambahkan sebelum fitur yang mementuknya dibangun. (Konfirmasi: `grep -c "model KitabProgress"` = 0, `grep -c "model Sertakan"` = 0.)
> **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanat.com` / `admin123` (typo indeks `pondokanbat.com`); produksi butuh bcrypt + session.
> **Beranda hardcode:** `Beranda.tsx` masih hardcoded `totalSantri: 441, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB).
> **Build quality gate (verifikasi ulang):** `tsc --noEmit` ✓ (exit 0); `npm run lint` ✓ (exit 0, 6 warning / 0 error); `npm run build` ✓ (exit 0, Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3).
> **Status:** dokumen PRD **FINAL**; state stabil; rev 39 = verifikasi fresh & konfirmasi stabilitas.'''

anchor = 'catatan schema inconsistency.\n> **Rev. 30 — 14 Oktober 2026 (WIB).'
count = content.count(anchor)
assert count == 1, f"anchor count = {count}"
content = content.replace(anchor, rev39 + '\n' + anchor, 1)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("done; total chars:", len(content))
