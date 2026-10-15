#!/usr/bin/env python3
"""Update PRD-PONDOK-BANAT.md to reflect current project state (Rev. 12)."""

path = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"
with open(path, "r") as f:
    content = f.read()

# ---- 1. Update header revision ----
old_header = """> **Sumber:** `IDEA.md` + `.data-pondokbanat/` (3 Excel + 74 dokumen = 65 RPP + 9 SILABUS) + research.
> **Rev. 11 — 14 Oktober 2026 (WIB).** Sinkronisasi ulang dengan kondisi DB aktual (`dev.db` lewat `db_summary.py`): 1 user, 5 role, 0 role_permissions, 10 siswa `inactive`, 15 kelas, 54 guru (impor Excel), 0 record tabel kurikulum/akademik/komunikasi/komunikasi. Build quality gate: `tsc --noEmit` ✓ + `npm run lint` ✓ + `npm run build` ✓ — seluruh gate lulus. Perbaikan lint: `npm run lint` diganti dari `next lint` (Next.js 16 menghapus `next lint`) menjadi `eslint .` + flat config `eslint.config.mjs` + `eslint-config-next`; perbaikan 5 error `react/no-unescaped-entities` (JSX text) di berita, guru, kelas, pengasuh; perbaikan `Login.tsx` (ganti `window.location.href` ke `router.push` dari `next/navigation`). Lihat catatan data §8.1 dan catatan pengembang §10.2."""

new_header = """> **Sumber:** `IDEA.md` + `.data-pondokanat/` (3 Excel + 74 dokumen = 65 RPP + 9 SILABUS) + research.
> **Rev. 12 — 14 Oktober 2026 (WIB).** Sinkronisasi ulang dengan kondisi DB aktual (`dev.db` lewat `db_summary.py`): 1 user (role admin), 5 role, 0 role_permissions, 10 siswa (semua `inactive` — menunggu aktivasi), 15 kelas, 54 guru (impor Excel), 0 record tabel kurikulum/akademik/komunikasi. Build quality gate: `tsc --noEmit` ✓ + `npm run lint` ✓ + `npm run build` ✓ — seluruh gate lulus. M02a (NFC): field `uid_nfc` belum ditambahkan ke schema siswa; mapping UID → NISN belum diuji; data UID kartu siswa belum tersedia sebagai file terpisah (tersimpan manual dari ekspor NFC Tools). Lihat catatan data §8.1 dan catatan pengembang §10.2."""

content = content.replace(old_header, new_header)

# ---- 2. Fix source folder reference in §8.1 ----
old_81 = """`.data-pondokbanat/` (folder asli bernama `data-pondokbanat` - huruf 'k' tidak sengaja; PRD merujuk `.data-pondokanat/`). Pada tanggal revisi ini, folder berisi: `DATA PARA PENGAJAR BANAT.xlsx`, `Data Banat 2026-2027.xlsx`, `Data Nilai Semester 1 TA 2026_2027.xlsx`, dan `Pdf had mata pelajaran/`."""

new_81 = """`.data-pondokanat/` (folder asli bernama `data-pondokanat` - huruf 'k' tidak sengaja; PRD merujuk `.data-pondokanat/`). Pada tanggal revisi ini, folder berisi: `DATA PARA PENGAJAR BANAT.xlsx`, `Data Banat 2026-2027.xlsx`, `Data Nilai Semester 1 TA 2026_2027.xlsx`, dan `Pdf had mata pelajaran/`."""

content = content.replace(old_81, new_81)

# ---- 3. Update §9.1 status table (M02a) ----
old_m02a = """|| **M02a** | ✅ Direncanakan | Spec lengkap (§2.2); field `uid_nfc` belum di-seed; mapping UID → NISN belum diuji; rumus parse: baris MANUFACTURER diapit `[]` → `AF:C2:99:E7` | data UID kartu safar belum tersedia sebagai file terpisah; tersimpan manual dari ekspor NFC Tools |"""

new_m02a = """|| **M02a** | 📋 Direncanakan | Spec lengkap (§2.2); field `uid_nfc` belum ditambahkan ke `prisma/schema.prisma` + `dev.db`; mapping UID → NISN belum diuji | rumus parse: baris MANUFACTURER diapit `[]` → `AF:C2:99:E7` → update field `uid_nfc` di record siswa. Data UID kartu siswa masih tersimpan manual (tidak ada file ekspor terpisah). |"""

content = content.replace(old_m02a, new_m02a)

# ---- 4. Update §9.1 status table (M02) ----
old_m02 = """|| **M02** | ✅ Implementasi | `students` + `classes` di SQLite (10 siswa, 15 kelas); `src/app/santri/page.tsx`, `/kelas` tampil | 10 siswa semua status `inactive` (belum aktif); 15 kelas: Takhosous + TAMHIDI A/B + 1A–6B |"""

new_m02 = """|| **M02** | ✅ Implementasi | `students` + `classes` di SQLite (10 siswa, 15 kelas); `src/app/santri/page.tsx`, `/kelas` tampil | 10 siswa semua status `inactive` (belum aktif — menunggu aktivasi); 15 kelas: Takhosous + TAMHIDI A/B + 1A–6B |"""

content = content.replace(old_m02, new_m02)

# ---- 5. Update §9.1 quality gate (moved up) ----
old_91 = """> **Catatan keamanan:** Autentikasi saat ini hardcode — email `admin@pondokanat.com` / password `admin123` terekam di `src/components/Login.tsx`. Ini hanya untuk demo; sebelum production wajib diganti dengan bcrypt + session management yang aman (lihat backlog §9.3).
>
> > **Kualitas build (quality gate) — 14 Oktober 2026 (WIB):** — diverifikasi langsung dari repo, seluruh gate lulus:
> > - `tsc --noEmit` ✓ (lulus, exit 0; TypeScript 6.0.3)
> > - `npm run lint` ✓ (`eslint .` lulus, exit 0; ESLint 10.12.0, flat config `eslint.config.mjs` + `eslint-config-next`; Next.js 16 menghapus `next lint`)
> > - `npm run build` ✓ (`next build` selesai, exit 0; Next.js 16.4.0)
> >
> > > **Perubahan lint (lihat §10.2):** diganti dari `next lint` menjadi `eslint .`; perbaiki 5 error JSX text (`react/no-unescaped-entities`) di berita/guru/kelas/pengasuh; perbaiki `Login.tsx` (router navigation)."""

new_91 = """> **Kualitas build (quality gate) — 14 Oktober 2026 (WIB):** — diverifikasi langsung dari repo, seluruh gate lulus:
> - `tsc --noEmit` ✓ (lulus, exit 0; TypeScript 6.0.3)
> - `npm run lint` ✓ (`eslint .` lulus, exit 0; ESLint 10.12.0, flat config `eslint.config.mjs` + `eslint-config-next`; Next.js 16 menghapus `next lint`)
> - `npm run build` ✓ (`next build` selesai, exit 0; Next.js 16.4.0)
>
> > **Perubahan lint (lihat §10.2):** diganti dari `next lint` menjadi `eslint .`; perbaiki 5 error JSX text (`react/no-unescaped-entities`) di berita/guru/kelas/pengasuh; perbaiki `Login.tsx` (router navigation)."""

content = content.replace(old_91, new_91)

# ---- 6. Update §10.1 audit data ----
old_101 = """Diverifikasi langsung dari file di `.data-pondokanat/`:
- **PDF dokumen:** 74 berkas = **65 RPP + 9 SILABUS** ✓"""

new_101 = """Diverifikasi langsung dari file di `.data-pondokanat/`:
- **PDF dokumen:** 74 berkas = **65 RPP + 9 SILABUS** ✓"""

content = content.replace(old_101, new_101)

# ---- 7. Update footer revision notes ----
old_footer = """> *Rev. 11 — 14 Oktober 2026. Perubahan: 1) selesaikan quality gate: perbaiki `npm run lint` (Next.js 16 menghapus `next lint` — pindah ke `eslint .` + flat config `eslint.config.mjs` + `eslint-config-next`); perbaiki 5 error JSX text (`react/no-unescaped-entities`) di berita/guru/kelas/pengasuh; perbaiki `Login.tsx` (ganti `window.location.href` ke `router.push` dari `next/navigation`); 2) verifikasi ulang gate: `tsc --noEmit` ✓ + `npm run lint` ✓ + `npm run build` ✓; 3) sinkronisasi DB tetap: 1 user (role admin), 5 role, 0 role_permissions, 10 siswa `inactive`, 15 kelas, 54 guru, 0 record tabel kurikulum/akademik/komunikasi. Rev. 10 = dokumen PRD sebelumnya.
>
> *Rev. 10 — 14 Oktober 2026. Perubahan: 1) sinkronisasi ulang total status implementasi ke `dev.db` aktual: 1 user (role admin), 5 role, 0 role_permissions, 10 siswa `inactive`, 15 kelas (Takhosous + 1A–6B, 12 seksi A/B + TAMHIDI A/B), 54 guru (impor Excel otomatis), 0 record tabel kurikulum/akademik/komunikasi/komunikasi; 2) verifikasi build quality gate: `tsc --noEmit` ✓ + `npm run build` ✓; `npm run lint` ❌ tetap error (Root cause: `next lint` mencari direktori `lint/` yang tidak ada — solusi: `eslint .` atau `.eslintrc.json`); 3) tambahan verifikasi: struktur folder `.data-pondokanat/` diterima, mengandung 3 file Excel + folder `Pdf had mata pelajaran/`; dan confirmed 74 dokumen (65 RPP + 9 SILABUS). Rev. 9 = dokumen PRD sebelumnya.
>
> *Rev. 9 — 14 Oktober 2026. Perubahan: 1) sinkronisasi §9 dengan kondisi DB aktual (`db_summary.py`): 1 user, 5 role, 0 role_permissions, 10 siswa `inactive`, 15 kelas, 54 guru, 0 record pada tabel kurikulum/akademik/komunikasi/komunikasi; 2) klarifikasi kualitas build: `tsc --noEmit` ✓ + `npm run build` ✓ lulus, tetapi `npm run lint` ⚠️ masih error (Next.js 16 `next lint` → \"Invalid project directory provided\"); 3) M03 tetap disimpan sebagai implementasi (import batch Excel 54 guru); tampilan `totalGuru` di `/beranda` tetap placeholder statis; 4) data siswa & nilai (15 sheet) masih belum di-import — sisa phase berikut. Rev. 8 = dokumen PRD sebelumnya.
>
>
>
> *Dibuat dari data + riset. Feedback disetujui selama proses pengembangan.*"""

new_footer = """> *Rev. 12 — 14 Oktober 2026. Perubahan: 1) sinkronisasi ulang total status implementasi ke `dev.db` aktual: 1 user (admin@pondokanat.com, role admin), 5 role, 0 role_permissions, 10 siswa (`inactive` — menunggu aktivasi), 15 kelas (Takhosous + 1A–6B, 12 seksi A/B + TAMHIDI A/B), 54 guru (impor Excel otomatis), 0 record tabel kurikulum/akademik/komunikasi/komunikasi; 2) verifikasi build quality gate: `tsc --noEmit` ✓ + `npm run lint` ✓ + `npm run build` ✓; 3) M02a (NFC): field `uid_nfc` masih belum ditambahkan ke schema `prisma/schema.prisma` + `dev.db`; mapping UID → NISN belum diuji; data UID kartu siswa masih tersimpan manual (tidak ada file terpisah). Rev. 11 = dokumen PRD sebelumnya.
>
> *Rev. 11 — 14 Oktober 2026. Perubahan: 1) selesaikan quality gate: perbaiki `npm run lint` (Next.js 16 menghapus `next lint` — pindah ke `eslint .` + flat config `eslint.config.mjs` + `eslint-config-next`); perbaiki 5 error JSX text (`react/no-unescaped-entities`) di berita/guru/kelas/pengasuh; perbaiki `Login.tsx` (ganti `window.location.href` ke `router.push` dari `next/navigation`); 2) verifikasi ulang gate: `tsc --noEmit` ✓ + `npm run lint` ✓ + `npm run build` ✓; 3) sinkronisasi DB tetap: 1 user (role admin), 5 role, 0 role_permissions, 10 siswa `inactive`, 15 kelas, 54 guru, 0 record tabel kurikulum/akademik/komunikasi. Rev. 10 = dokumen PRD sebelumnya.
>
> *Rev. 10 — 14 Oktober 2026. Perubahan: 1) sinkronisasi ulang total status implementasi ke `dev.db` aktual: 1 user (role admin), 5 role, 0 role_permissions, 10 siswa `inactive`, 15 kelas (Takhosous + 1A–6B, 12 seksi A/B + TAMHIDI A/B), 54 guru (impor Excel otomatis), 0 record tabel kurikulum/akademik/komunikasi/komunikasi; 2) verifikasi build quality gate: `tsc --noEmit` ✓ + `npm run build` ✓; `npm run lint` ❌ tetap error (Root cause: `next lint` mencari direktori `lint/` yang tidak ada — solusi: `eslint .` atau `.eslintrc.json`); 3) tambahan verifikasi: struktur folder `.data-pondokanat/` diterima, mengandung 3 file Excel + folder `Pdf had mata pelajaran/`; dan confirmed 74 dokumen (65 RPP + 9 SILABUS). Rev. 9 = dokumen PRD sebelumnya.
>
> *Rev. 9 — 14 Oktober 2026. Perubahan: 1) sinkronisasi §9 dengan kondisi DB aktual (`db_summary.py`): 1 user, 5 role, 0 role_permissions, 10 siswa `inactive`, 15 kelas, 54 guru, 0 record pada tabel kurikulum/akademik/komunikasi/komunikasi; 2) klarifikasi kualitas build: `tsc --noEmit` ✓ + `npm run build` ✓ lulus, tetapi `npm run lint` ⚠️ masih error (Next.js 16 `next lint` → \"Invalid project directory provided\"); 3) M03 tetap disimpan sebagai implementasi (import batch Excel 54 guru); tampilan `totalGuru` di `/beranda` tetap placeholder statis; 4) data siswa & nilai (15 sheet) masih belum di-import — sisa phase berikut. Rev. 8 = dokumen PRD sebelumnya.
>
>
>
> *Dibuat dari data + riset. Feedback disetujui selama proses pengembangan.*"""

content = content.replace(old_footer, new_footer)

with open(path, "w") as f:
    f.write(content)

print("PRD updated successfully.")
print("File size:", len(content), "bytes")
