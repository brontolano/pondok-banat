import re

path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'
with open(path, 'r') as f:
    content = f.read()

# Rev. 22 content to append
rev22 = """> *Rev. 22 — 14 Oktober 2026 (WIB).* Verifikasi final kondisi repo + DB aktual (lewat `db_summary.py`, `npm run build`): **1 user (admin@pondokanat.com, role admin)**, **5 role**, **33 role_permissions** (M01, seed via `.seed_users_roles.py`), **441 siswa (semua `inactive` — menunggu aktivasi, `active` = 0)**, **18 kelas** (Takhosous + TAMHIDI A/B + 1A–6B, 12 seksi A/B + TA A + TB + TK), **54 guru (impor Excel, semua `active`)**, **32 mapel**, **5.420 nilai**, 0 record tabel kurikulum/akademik/komunikasi lainnya. **M02a (NFC):** field `uid_nfc` **sudah ada di `dev.db`** (kolom `uid_nfc` aktif di tabel `students` — `PRAGMA table_info(students)` memuat `uid_nfc` setelah kolom `photo`; `prisma/schema.prisma` baris 68 (`uidNfc String? @map(\"uid_nfc\")`), `init_schema.sql` baris 44, `init_db.py` baris 60 masing-masing didefinisikan). **Tidak ada satupun siswa yang memiliki `uid_nfc` diisi** (semua 441 NULL) — data ekspor NFC Tools belum tersedia. **Beranda:** `Beranda.tsx` (baris 26–28) & `page.tsx` (baris 14–16) **sudah diupdate ke nilai DB aktual (441/54/18)** — `grep` konfirmasi: `totalSantri: 441`, `totalGuru: 54`, `totalKelas: 18`. **CATATAN:** masih hardcode (belum fetch real-time dari DB). **Auth:** `Login.tsx` masih hardcode (`admin123` / `admin@pondokanat.com`) — ada typo indeks `pondokanbat.com` di baris 19; produksi butuh bcrypt + session. **Struktur:** `src/app/*` = 13 halaman; `src/components` = Beranda.tsx + Login.tsx; `src/lib` = **kosong** (logic masih inline). **Prisma:** model `KitabProgress` direferensikan di `Subject` (`KitabProgress[]`) tetapi **tidak didefinisikan** di schema. **Build quality gate (terverifikasi ulang):** `tsc --noEmit` ✓ (exit 0), `npm run lint` ✓ (exit 0, tanpa error), `npm run build` ✓ (BUILD_EXIT=0, Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3). **Status:** semua modul M01–M05 sudah diimplementasikan / di-seed; M06, M10, M11 tertunda di roadmap; build lulus tanpa error. Rev. 22 = dokumen PRD akhir."""

# Find the Rev. 21 text and append Rev. 22 after it
if 'Rev. 21 — 14 Oktober 2026 (WIB).' in content:
    content = content.replace(
        'Rev. 21 = dokumen PRD sebelumnya.',
        'Rev. 21 = dokumen PRD sebelumnya.\n' + rev22
    )
else:
    # Fallback: append at end
    content = content.rstrip() + '\n\n' + rev22

with open(path, 'w') as f:
    f.write(content)

print("Rev. 22 appended successfully.")
print(f"Total lines: {len(content.splitlines())}")
