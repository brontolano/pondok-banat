import os

prd_path = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"

with open(prd_path, "r") as f:
    lines = f.readlines()

# Line 4 (index 3) is the header — needs to be replaced with Rev. 28
new_header = """> **Rev. 28 — 14 Oktober 2026 (WIB).** Verifikasi final kondisi repo + dev.db (lewat Python `sqlite3` + `npm run build`): **1 user (admin@pondokanat.com, role admin)**, **5 role** (admin, guru, wali_kelas, pengasuh, santri), **33 role_permissions** (M01, seed via `.seed_users_roles.py`), **441 siswa** (semua `inactive` — menunggu aktivasi, `active` = 0, `uid_nfc` = 0 siswa terisi), **18 kelas** (TAMHIDI A/B + 1A–6B, 12 seksi A/B + TA A + TB + TK), **54 guru** (impor Excel, semua `active`), **32 mapel**, **5.420 nilai**, **0 record** di tabel silabus/rpp/absensi/rapor/announcements/messages/notifications. **Siswa per kelas (diverifikasi langsung dari `dev.db`):** TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosous=0; **TOTAL = 441**. **M02a (NFC):** field `uid_nfc` **ada aktif** di tabel `students` (kolom setelah `photo`); `prisma/schema.prisma` baris 68 (`uidNfc String? @map(\\\"uid_nfc\\\")`), `init_schema.sql` baris 44, `init_db.py` baris 60. **Tidak ada satupun siswa yang memiliki `uid_nfc` diisi** (semua 441 NULL) — data ekspor NFC Tools belum tersedia. **Beranda:** `Beranda.tsx` (baris 26–28) & `page.tsx` (baris 14–16) **sudah diupdate** ke nilai DB aktual (441/54/18). **CATATAN:** masih hardcode (belum fetch real-time dari DB). **Auth:** `Login.tsx` masih hardcode (`admin123` / `admin@pondokanat.com`) — ada typo indeks `pondokanbat.com` di baris 19; produksi butuh bcrypt + session. **Struktur:** `src/app/*` = 13 halaman; `src/components` = Beranda.tsx + Login.tsx; `src/lib` = **kosong** (logic masih inline). `prisma/schema.prisma` baris 68 mendefinisikan `uidNfc` @map(\\\"uid_nfc\\\") pada model `Student`. Model `KitabProgress` direferensikan di `Subject` (`KitabProgress[]`) tetapi **tidak didefinisikan** di schema. **Build quality gate (verifikasi akhir):** `npm run type-check` (tsc --noEmit) ✓ (exit 0); `npm run lint` ✓ (exit 0, 6 warning / 0 error); `npm run build` (next build) ✓ (exit 0, Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3). **Status:** semua modul M01–M05 sudah diimplementasikan / di-seed; M06, M10, M11 tertunda di roadmap; build lulus tanpa error. Rev. 28 = dokumen PRD final (kondisi stabil, tidak ada perubahan dari Rev. 27).\\n"""

# Replace line 4 (index 3)
lines[3] = new_header

with open(prd_path, "w") as f:
    f.writelines(lines)

print("File updated. Total lines:", len(lines))
print("Line 4 first 80 chars:", lines[3][:80])
