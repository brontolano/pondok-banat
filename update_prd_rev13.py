#!/usr/bin/env python3
"""Update PRD-PONDOK-BANAT.md to Rev 13."""
path = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"

with open(path, "r") as f:
    c = f.read()

# 1. Header
old_h = """> **Sumber:** `IDEA.md` + `.data-pondokanat/` (3 Excel + 74 dokumen = 65 RPP + 9 SILABUS) + research.
> **Rev. 12 — 14 Oktober 2026 (WIB).** Sinkronisasi ulang dengan kondisi DB aktual (`dev.db` lewat `db_summary.py`): 1 user (role admin), 5 role, 0 role_permissions, 10 siswa (semua `inactive` — menunggu aktivasi), 15 kelas, 54 guru (impor Excel), 0 record tabel kurikulum/akademik/komunikasi. Build quality gate: `tsc --noEmit` ✓ + `npm run lint` ✓ + `npm run build` ✓ — seluruh gate lulus. M02a (NFC): field `uid_nfc` belum ditambahkan ke schema siswa; mapping UID → NISN belum diuji; data UID kartu siswa belum tersedia sebagai file terpisah (tersimpan manual dari ekspor NFC Tools). Lihat catatan data §8.1 dan catatan pengembang §10.2."""

new_h = """> **Sumber:** `IDEA.md` + `.data-pondokanat/` (3 Excel + 74 dokumen = 65 RPP + 9 SILABUS) + research.
> **Rev. 13 — 15 Oktober 2026 (WIB).** Sinkronisasi ulang dengan kondisi DB aktual (`dev.db` lewat `db_summary.py`): 1 user (role admin), 5 role, 0 role_permissions, 10 siswa (semua `inactive` — menunggu aktivasi), 15 kelas, 54 guru (impor Excel), 0 record tabel kurikulum/akademik/komunikasi. Build quality gate (terverifikasi ulang): `tsc --noEmit` ✓ (exit 0) + `npm run lint` ✓ (exit 0, 6 warning — tanpa error) + `npm run build` ✓ (exit 0). M02a (NFC): field `uid_nfc` masih belum ditambahkan ke schema siswa; mapping UID → NISN belum diuji; data UID kartu siswa masih tersimpan manual (tidak ada file ekspor terpisah). Tidak ada modul baru yang diimplementasikan sejak Rev. 12. Lihat catatan data §8.1 dan catatan pengembang §10.2."""

assert old_h in c, "header not found"
c = c.replace(old_h, new_h)

# 2. Footer - add Rev 13
old_f11 = """> *Rev. 11 — 14 Oktober 2026. Perubahan: 1) selesaikan quality gate: perbaiki `npm run lint` (Next.js 16 menghapus `next lint` — pindah ke `eslint .` + flat config `eslint.config.mjs` + `eslint-config-next`); perbaiki 5 error JSX text (`react/no-unescaped-entities`) di berita/guru/kelas/pengasuh; perbaiki `Login.tsx` (ganti `window.location.href` ke `router.push` dari `next/navigation`); 2) verifikasi ulang gate: `tsc --noEmit` ✓ + `npm run lint` ✓ + `npm run build` ✓; 3) sinkronisasi DB tetap: 1 user (role admin), 5 role, 0 role_permissions, 10 siswa `inactive`, 15 kelas, 54 guru, 0 record tabel kurikulum/akademik/komunikasi. Rev. 10 = dokumen PRD sebelumnya."""

new_f11 = """> *Rev. 13 — 15 Oktober 2026 (WIB). Perubahan: 1) Sinkronisasi ulang status implementasi ke `dev.db` aktual (state tidak berubah): 1 user (admin@pondokanat.com, role admin), 5 role, 0 role_permissions, 10 siswa (`inactive` — menunggu aktivasi), 15 kelas (Takhosous + 1A–6B, 12 seksi A/B + TAMHIDI A/B), 54 guru (impor Excel otomatis), 0 record tabel kurikulum/akademik/komunikasi/komunikasi; 2) Verifikasi ulang build quality gate: `tsc --noEmit` ✓ (exit 0); `npm run lint` ✓ (exit 0, 6 warning tanpa error: unused vars di halaman beranda/santri/sekolah dan komponen Beranda); `npm run build` ✓ (exit 0, next build selesai); 3) M02a (NFC): field `uid_nfc` masih belum ditambahkan ke schema `prisma/schema.prisma` + `dev.db`; mapping UID → NISN belum diuji; data UID kartu siswa masih tersimpan manual (tidak ada file terpisah). Semua modul M01–M11 tetap dalam status sesuai Rev. 12. Rev. 12 = dokumen PRD sebelumnya.
>
> *Rev. 12 — 14 Oktober 2026 (WIB). Perubahan: Sinkronisasi ulang dengan kondisi DB aktual (`dev.db` lewat `db_summary.py`): 1 user (role admin), 5 role, 0 role_permissions, 10 siswa (semua `inactive` — menunggu aktivasi), 15 kelas, 54 guru (impor Excel), 0 record tabel kurikulum/akademik/komunikasi. Build quality gate: `tsc --noEmit` ✓ + `npm run lint` ✓ + `npm run build` ✓ — seluruh gate lulus. M02a (NFC): field `uid_nfc` belum ditambahkan ke schema siswa; mapping UID → NISN belum diuji; data UID kartu siswa belum tersedia sebagai file terpisah (tersimpan manual dari ekspor NFC Tools). Lihat catatan data §8.1 dan catatan pengembang §10.2.
>
> *Rev. 11 — 14 Oktober 2026. Perubahan: 1) selesaikan quality gate: perbaiki `npm run lint` (Next.js 16 menghapus `next lint` — pindah ke `eslint .` + flat config `eslint.config.mjs` + `eslint-config-next`); perbaiki 5 error JSX text (`react/no-unescaped-entities`) di berita/guru/kelas/pengasuh; perbaiki `Login.tsx` (ganti `window.location.href` ke `router.push` dari `next/navigation`); 2) verifikasi ulang gate: `tsc --noEmit` ✓ + `npm run lint` ✓ + `npm run build` ✓; 3) sinkronisasi DB tetap: 1 user (role admin), 5 role, 0 role_permissions, 10 siswa `inactive`, 15 kelas, 54 guru, 0 record tabel kurikulum/akademik/komunikasi. Rev. 10 = dokumen PRD sebelumnya."""

assert old_f11 in c, "footer11 not found"
c = c.replace(old_f11, new_f11)

with open(path, "w") as f:
    f.write(c)

print("PRD updated to Rev 13")
print("Size:", len(c))
