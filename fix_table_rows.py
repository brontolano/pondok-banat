#!/usr/bin/env python3
"""Fix missing M03 and M05 rows in status table"""
import os

base = "/opt/data/home/workspace/dev/pondok-banat"
prd = os.path.join(base, "PRD-PONDOK-BANAT.md")

with open(prd, encoding="utf-8") as f:
    txt = f.read()

# ---------------------------------------------------------------------------
# 1. Insert M03 row between M02a and M04
# ---------------------------------------------------------------------------
m02a_end = "| M02a | Integrasi NFC (UID) | 🔜 Direncanakan | Spec lengkap (utk §2.2); field `uid_nfc` belum di-seed; mapping UID → NISN belum diuji; rumus parse: baris MANUFACTURER diapit `[]` → `AF:C2:99:E7` |\n"

m03_row = """||| M03 | Master Data Guru & Staf | 📋 Implementasi (statis) | Schema Prisma lengkap (Teacher, Staff, Position) + dashboard `/guru` (statis, hardcoded 5 guru); data dari DB belum di-bind | > **Catatan:** 5 guru di `dev.db` (4 Wali Kelas + 1 Guru, semua active); sumber 60 baris (53 utama + 7 ganti/badal, 59 unik). Import batch dari Excel belum diimplementasikan |"""

if m02a_end in txt:
    txt = txt.replace(m02a_end, m02a_end + "\n" + m03_row)
    print("M03 row inserted")
else:
    print("M02a end not found")

# ---------------------------------------------------------------------------
# 2. Insert M05 row between M04 and M06
# ---------------------------------------------------------------------------
# Find the M04 row
old_m04 = "| M04 | Kurikulum & Kitab Kuning | 📋 Implementasi (statis) | Schema Prisma lengkap (Subject, Silabus, RPP + KitabProgress) + dashboard `/kelas` (statis, hardcoded 4 pelajaran: AG, BINDO, MAT, IPS); data dari DB belum di-bind | > **Catatan:** `subjects`, `silabus`, `rpp` masing-masing **0 record**; 17 mapel + 74 dokumen (65 RPP + 9 SILABUS) masih di Excel/PDF saja |"

# M05 row that should come after M04 (before M06)
old_m05 = "| M06 | Hifz/Quran Memorization | ❌ Tidak aktif (MVP) | Tidak ada schema/seed/release; tertunda di roadmap iterasi 2 |"

new_m05 = """| M05 | Akademik & Absensi | 📋 Implementasi (statis) | Schema Prisma lengkap (Grade, Absensi, Rapor) + dashboard `/nilai` (statis, contoh nilai manual); data dari DB belum di-bind | > **Catatan:** tabel `grades`, `absensi`, `rapor` masing-masing **0 record**; 15 sheet nilai masih di Excel saja (TK, TA A, TB, 1A–6B) |"""
if old_m04 in txt and old_m05 in txt:
    txt = txt.replace(old_m04, old_m04 + "\n" + new_m05)
    print("M05 row inserted after M04")
else:
    print("M04 or M05 not found")

# ---------------------------------------------------------------------------
# 3. Fix M02a row: add Catatan about NFC data not available as separate file
# ---------------------------------------------------------------------------
old_m02a = "| M02a | Integrasi NFC (UID) | 🔜 Direncanakan | Spec lengkap (utk §2.2); field `uid_nfc` belum di-seed; mapping UID → NISN belum diuji; rumus parse: baris MANUFACTURER diapit `[]` → `AF:C2:99:E7` |"

new_m02a = "| M02a | Integrasi NFC (UID) | 🔜 Direncanakan | Spec lengkap (utk §2.2); field `uid_nfc` belum di-seed; mapping UID → NISN belum diuji; rumus parse: baris MANUFACTURER diapit `[]` → `AF:C2:99:E7` | > **Catatan:** data UID kartu siswa belum tersedia sebagai file terpisah; tersimpan manual dari ekspor NFC Tools |"

if old_m02a in txt:
    txt = txt.replace(old_m02a, new_m02a)
    print("M02a row fixed")
else:
    print("M02a row pattern not found")

# ---------------------------------------------------------------------------
# 4. Write
# ---------------------------------------------------------------------------
with open(prd, "w", encoding="utf-8") as f:
    f.write(txt)

print()
print("=== PRD fixed ===")
print("Total lines:", txt.count(chr(10)) + 1)
print("Size:", len(txt), "bytes")
