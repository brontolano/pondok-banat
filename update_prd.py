#!/usr/bin/env python3
import sqlite3, os, re

base = "/opt/data/home/workspace/dev/pondok-banat"
prd = os.path.join(base, "PRD-PONDOK-BANAT.md")
with open(prd, encoding="utf-8") as f:
    txt = f.read()

# ---- Build the new implementation-status section ----
new_section = """
## 9. STATUS IMPLEMENTASI SAAT INI

> Rencana di Praktik: codebase Next.js 16 + React 19 + TypeScript, UI sudah tampil untuk keempat role, SQLite (dev.db) telah di-seed MVP. Bagian ini memetakan tiap modul M01–M11 dari PRD ke keadaan nyata di repo (date: 14 Oktober 2026).

### 9.1 Ringkasan

|| Modul | Status | Keterangan |
|---|---|---|---|
| M01 | Admin & User Management | ✅ Implementasi | `prisma/schema.prisma` (model User, Role, RolePermission) + `src/app/login/page.tsx`; 1 user admin seed otomatis via `init_db.py`; authorization masih hardcode di React |
| M02 | Master Data Santri | ✅ Implementasi | `students` + `classes` di SQLite (10 siswa, 13 kelas); `src/app/santri/page.tsx`, `/kelas` tampil |
| M03 | Master Data Guru & Staf | ✅ Implementasi | `teachers` di SQLite (5 seed); `src/app/guru/page.tsx`, filter jabatan |
| M04 | Kurikulum & Kitab Kuning | 🔜 Direncanakan | Schema Prisma lengkap (Subject, Silabus, RPP + KitabProgress) tetapi **belum di-seed** data mapel/silabus/rpp dari PDF/xlsx |
| M05 | Akademik & Absensi | 🔜 Direncanakan | Schema Prisma lengkap (Grade, Absensi, Rapor) tetapi **belum di-seed** data nilai; komponen `src/app/nilai/page.tsx` siap tapi kosong |
| M06 | Hifz/Quran Memorization | ❌ Tidak aktif (MVP) | Tidak ada schema/seed/release; tertunda di roadmap iterasi 2 |
| M07 | Kesiswaan & Tunggangan | 🔜 Direncanakan | Schema Prisma tidak ada; `src/app/ruang-kegiatan/page.tsx` belum dibangun |
| M08 | Komunikasi & Notifikasi | 🔜 Direncanakan | Schema Prisma (Announcement, Message, Notification) tetapi **belum di-seed**; `src/app/berita/page.tsx` ada tapi statis |
| M09 | Laporan & Analytics | 🔜 Direncanakan | UI `/laporan/page.tsx` punya tombol ekspor, **generative PDF belum ada** |
| M10 | Payment/Keuangan | ❌ Tidak aktif (MVP) | Tertunda roadmap iterasi 3 |
| M11 | Mobile & Offline | ❌ Tidak aktif (MVP) | Gatsby mobile — tidak termasuk MVP; tertunda |

### 9.2 Build & Database

- **Build:** `next build` → `.next/` (export-ready). Script `build` didefinisikan di `package.json`.
- **Database:** SQLite `dev.db` di-seed oleh `init_db.py` (MVP tables: users, roles, role_permissions, students, classes, teachers, + akademik/umum lain).
  - Saat ini: 1 user, 5 role, 10 siswa, 13 kelas, 5 guru.
- **Prisma:** schema `prisma/schema.prisma` (SQLite) mendefinisikan model M01–M05 + M08; driver client `prisma-client-js` (anggotakan `prisma` ^8.0.0-rc.22).
- **UI:** `src/app/*` berisi halaman berbasis route; komponen kecil `Beranda`, `Login`.

### 9.3 Open / Backlog (dari `docs/todolist.md`)

- Online mode (API routes)
- Password hashing (bcrypt) — Prisma `password` teks belum di-hash
- Export/backup/restore (Excel, PDF)
- Testing (unit + integration)
- Production deployment (Vercel, Docker)
- Input/import data sosial (santri, nilai, guru, dokumen) otomatis dari `.data-pondokanat/`
- Wali Santri portal (M08)
- PDF generation (M09)

---

## 10. CATATAN PENGEMBANG (DITAMBAHKAN 14 OKT 2026)

### 10.1 Audit data sumber (§8.1 diperbaiki)

Diverifikasi langsung dari file di `.data-pondokanat/`:

- **PDF dokumen:** 74 berkas = **65 RPP + 9 SILABUS** ✓
- **Pelajaran (mapel):** 17, dari nama file RPP (`Fiqih, Nahwu, Sharaf/Al-Qur'an, Hadits, Imla', Mahfudzhot, Mantiq, Siroh, Sorof, Tafsir, Tajwid, Tasawuf, Tawhid, Balagoh, Faraoid, Ulumul Hadits, Ulumul Qur'an`)
- **Nilai:** 15 sheet di `Data Nilai Semester 1 TA 2026_2027.xlsx` = TK, TA A, TB, 1A–6B ✓
- **Guru/Staf:** `DATA PARA PENGAJAR BANAT.xlsx` punya beberapa sheet:
  - `TAHUN 2026-2027`: 56 data baris
  - `Table 1`: 61 data baris, 60 nama unik
  - Angka **"58 guru/staff (51 utama + 7 ganti/badal)"** adalah hasil interpretasi tim; catat bahwa sheet mentah tidak membagi 'utama' vs 'ganti/badal' secara eksplisit. Untuk produksi, disarankan membaca `TAHUN 2026-2027` sebagai master utama, dan `Table 1` sebagai daftar ganti/badal.
- **Kelas:** 6 jenjang + Takhosous; 12 seksi A/B (1A–6B) sesuai PRD ✓

### 10.2 Penamaan

- Nama file folder asli adalah `Pdf had mata pelajaran` (tiap spasi). Tidak ada masalah.

---

*Rev. 2 — 14 Oktober 2026. Perubahan: 1) ditambah §9 Status Implementasi Saat Ini; 2) ditambah §10 Catatan Pengembang & audit data; 3) diperhalus klarifikasi §8.1. Rev. 1 = dokumen PRD asli.*
""".lstrip("\n")

# ---- Insert §9 and §10 before the footer line ----
# Split: keep everything up to (not including) the "*Dibuat dari data + riset." footer
footer_marker = "*Dibuat dari data + riset. Feedback disetujui selama proses pengembangan.*"
assert footer_marker in txt

head = txt.split(footer_marker)[0]
tail = footer_marker + "\n"

# fix the already-present §8.1 teacher note text: replace the ambiguous line
txt_head = head.replace(
    "- 58 guru/staff (DATA PARA PENGAJAR BANAT.xlsx: 51 utama + 7 ganti/badal).",
    "- 58 guru/staff (DATA PARA PENGAJAR BANAT.xlsx: 51 utama + 7 ganti/badal). *Lihat §10.1 audit sheet raw.*"
)

new_full = txt_head + "\n" + new_section + tail
new_full = new_full.replace(
    "- 58 guru/staff (DATA PARA PENGAJAR BANAT.xlsx: 51 utama + 7 ganti/badal).",
    "- 58 guru/staff (DATA PARA PENGAJAR BANAT.xlsx: 51 utama + 7 ganti/badal). *Lihat §10.1 audit sheet raw.*"
)

with open(prd, "w", encoding="utf-8") as f:
    f.write(new_full)

# ---- Report summary ----
print("=== New PRD line count:", new_full.count(chr(10)) + 1)
for marker in ["## 9. STATUS", "## 10. CATATAN", "10.1 Audit data", "10.2 Penamaan"]:
    print(marker, "->", marker in new_full)
# sanity: no double insertion
print("occurrences of '## 9.' :", new_full.count("## 9."))
