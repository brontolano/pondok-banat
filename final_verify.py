#!/usr/bin/env python3
"""Final verification of PRD"""
with open('/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md', 'r') as f:
    content = f.read()

# Check key elements
checks = [
    ("Revision footer Rev 7", "Rev. 7 — 14 Oktober 2026" in content),
    ("M01 row", "| M01 | Admin & User Management | ✅ Implementasi" in content),
    ("M02 row", "| M02 | Master Data Santri | ✅ Implementasi" in content),
    ("M02a row", "| M02a | Integrasi NFC (UID)" in content),
    ("M03 row (new)", "| M03 | Master Data Guru & Staf | 📋 Implementasi" in content),
    ("M04 row", "| M04 | Kurikulum & Kitab Kuning | 📋 Implementasi" in content),
    ("M05 row", "| M05 | Akademik & Absensi | 📋 Implementasi" in content),
    ("M06 row", "| M06 | Hifz/Quran Memorization" in content),
    ("M07 row", "| M07 | Kesiswaan & Tunggangan" in content),
    ("M08 row", "| M08 | Komunikasi & Notifikasi" in content),
    ("M09 row", "| M09 | Laporan & Analytics" in content),
    ("M10 row", "| M10 | Payment/Keuangan" in content),
    ("M11 row", "| M11 | Mobile & Offline" in content),
    ("DB block - role_permissions empty", "tabel `role_permissions` didefinisikan tapi **0 record**" in content),
    ("DB block - 10 siswa", "10 siswa (`inactive`)" in content),
    ("DB block - 13 kelas", "13 kelas (Takhosous + 1A–6B)" in content),
    ("DB block - 5 guru", "5 guru (semua Wali Kelas)" in content),
    ("Beranda static data note", "totalSantri: 42` dan `totalGuru: 27" in content),
    ("Data source folder", ".data-pondokanat" in content),
    ("Audit: 65 RPP + 9 SILABUS", "65 RPP + 9 SILABUS" in content),
    ("Audit: 17 mapel", "17, dari nama file RPP" in content),
    ("Audit: 15 sheet nilai", "15 sheet di `Data Nilai" in content),
    ("Audit: 59 nama unik", "59 nama unik" in content),
    ("Module M03 status", "| 📋 Implementasi (statis)" in content),
    ("Senior note about static UI", "Beranda` menunjukkan" in content),
]

all_pass = True
for name, result in checks:
    status = "✓" if result else "✗ FAIL"
    if not result:
        all_pass = False
    print(f"  [{status}] {name}")

print()
print("All checks passed!" if all_pass else "SOME CHECKS FAILED!")
