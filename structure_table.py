#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Restructure the §9.1 modul table in PRD-PONDOK-BANAT.md into a clean
4-column table and move inline 'Catatan' notes to footnotes."""

PATH = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'
NL = chr(10)

# Clean 4-column table + footnotes (replaces lines 294..314 exclusive in 0-based)
NEW_TABLE = [
    '| Modul | Status | Keterangan | Notes |',
    '|---|---|---|---|',
    '| **M01** | \u2705 Implementasi | `prisma/schema.prisma` (model User, Role, RolePermission) + `src/app/login/page.tsx`; 1 user admin seed otomatis via `init_db.py`; authorization masih hardcode di React | tabel `role_permissions` didefinisikan tapi **0 record** \u2014 perizinan modul belum di-enforce di API; auth masih hardcode (`admin@pondokanat.com` / `admin123`) |',
    '| **M02** | \u2705 Implementasi | `students` + `classes` di SQLite (10 siswa, 15 kelas); `src/app/santri/page.tsx`, `/kelas` tampil | 10 siswa semua status `inactive` (belum aktif); 15 kelas: Takhosous + TAMHIDI A/B + 1A\u20136B |',
    '| **M02a** | \u2705 Direncanakan | Spec lengkap (\u00a72.2); field `uid_nfc` belum di-seed; mapping UID \u2192 NISN belum diuji; rumus parse: baris MANUFACTURER diapit `[]` \u2192 `AF:C2:99:E7` | data UID kartu safar belum tersedia sebagai file terpisah; tersimpan manual dari ekspor NFC Tools |',
    '| **M03** | \U0001f4cb Implementasi | Schema Prisma lengkap (Teacher, Staff, Position) + dashboard `/guru`; **impor batch Excel otomatis** | impor dari `DATA PARA PENGAJAR BANAT.xlsx` > `TAHUN 2026-2027` \u2192 **54 guru** di `dev.db` (sumber 60 baris: 53 utama + 7 ganti/badal, 59 nama unik); via `import_excel.py` |',
    '| **M04** | \U0001f4cb Implementasi (statis) | Schema Prisma lengkap (Subject, Silabus, RPP) + dashboard `/kelas` (statis, hardcoded 4 pelajaran: AG, BINDO, MAT, IPS); data dari DB belum di-bind | `subjects`, `silabus`, `rpp` masing-masing **0 record**; 17 mapel + 74 dokumen (65 RPP + 9 SILABUS) masih di Excel/PDF saja |',
    '| **M05** | \U0001f4cb Implementasi (statis) | Schema Prisma lengkap (Grade, Absensi, Rapor) + dashboard `/nilai` (statis, contoh nilai manual); data dari DB belum di-bind | tabel `grades`, `absensi`, `rapor` masing-masing **0 record**; 15 sheet nilai masih di Excel saja (TK, TA A, TB, 1A\u20136B) |',
    '| **M06** | \u274c Tidak aktif (MVP) | Tidak ada schema/seed/release; tertunda di roadmap iterasi 2 | \u2014 |',
    '| **M07** | \u2705 Direncanakan | Schema Prisma tidak ada; `src/app/ruang-kegiatan/page.tsx` ada tapi konten statis (ruangan, kegiatan) | \u2014 |',
    '| **M08** | \u2705 Direncanakan | Schema Prisma (Announcement, Message, Notification) tetapi **belum di-seed**; dashboard `/berita` ada (statis) | \u2014 |',
    '| **M09** | \u2705 Direncanakan | UI `/laporan/page.tsx` punya tombol ekspor; **generative PDF belum ada** | \u2014 |',
    '| **M10** | \u274c Tidak aktif (MVP) | Tertunda roadmap iterasi 3 | \u2014 |',
    '| **M11** | \u274c Tidak aktif (MVP) | Gatsby mobile \u2014 tidak termasuk MVP; tertunda | \u2014 |',
    '',
    '> **Catatan:** Komponen `Beranda` menunjukkan `totalSantri: 42`, `totalGuru: 27` (placeholder statis), tidak mencerminkan jumlah sesungguhnya di `dev.db` (10 siswa `inactive`, 54 guru, 15 kelas). Display `totalGuru` di `/beranda` masih hardcode; akan disinkronkan ke DB.',
    '',
    '> **Catatan Prisma:** model `KitabProgress` hanya direferensikan di `Subject` (`KitabProgress[]`) tetapi **tidak didefinisikan** di schema; perlu ditambahkan jika fitur progress kitab akan dibangun.',
]

def main():
    with open(PATH, encoding='utf-8') as f:
        lines = f.read().splitlines()

    # Boundary checks
    assert lines[294] == '', 'boundary[294] mismatch: %r' % lines[294]
    assert lines[295].startswith('| Modul | Status'), 'start mismatch: %r' % lines[295]
    assert lines[313].startswith('| M11 |'), 'end mismatch: %r' % lines[313]

    old_region = lines[294:314]
    print('Replaced region (%d lines):' % len(old_region))
    for ln in old_region:
        print('  ' + ln)

    lines[294:314] = NEW_TABLE

    with open(PATH, 'w', encoding='utf-8') as f:
        f.write(NL.join(lines))

    print('Written OK.')

    # Verify
    v = open(PATH, encoding='utf-8').read().splitlines()
    print('--- verify: new table + footnotes (first 15) ---')
    for i in range(294, min(310, len(v))):
        print('%d: %s' % (i, v[i]))

if __name__ == '__main__':
    main()
