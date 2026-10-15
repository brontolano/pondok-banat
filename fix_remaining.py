#!/usr/bin/env python3
"""Fix remaining numbering issues in the PRD file."""
path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix "6. Struktur kode" under Rev. 19 -> "3. Struktur kode"
# The Rev. 19 block has: 1. Verifikasi DB, 2. Beranda placeholder, 6. Struktur kode, 7. Build quality gate
# We need: 1. Verifikasi DB, 2. Beranda placeholder, 3. Struktur kode, 4. Build quality gate
content = content.replace(
    '2. **Beranda placeholder:** `Beranda.tsx` (baris 26–28) & `page.tsx` (baris 14–16) **sudah diupdate** ke nilai DB aktual (441/54/18) — `grep` konfirmasi: `totalSantri: 441`, `totalGuru: 54`, `totalKelas: 18`. Perlu sinkronisasi ke DB (fetch real counts) untuk iterasi berikutnya.\n\n6. **Struktur kode:**',
    '2. **Beranda placeholder:** `Beranda.tsx` (baris 26–28) & `page.tsx` (baris 14–16) **sudah diupdate** ke nilai DB aktual (441/54/18) — `grep` konfirmasi: `totalSantri: 441`, `totalGuru: 54`, `totalKelas: 18`. Perlu sinkronisasi ke DB (fetch real counts) untuk iterasi berikutnya.\n\n3. **Struktur kode:**'
)

# Fix "7. Build quality gate" under Rev. 19 -> "4. Build quality gate"
content = content.replace(
    '3. **Struktur kode:** `src/app/*` = 13 halaman; `src/components` = Beranda.tsx + Login.tsx; `src/lib` = kosong (logic inline). Prisma schema (line 68) mendefinisikan `uidNfc` @map(`\"uid_nfc\"`) pada model `Student`.\n\n7. **Build quality gate:**',
    '3. **Struktur kode:** `src/app/*` = 13 halaman; `src/components` = Beranda.tsx + Login.tsx; `src/lib` = kosong (logic inline). Prisma schema (line 68) mendefinisikan `uidNfc` @map(`\"uid_nfc\"`) pada model `Student`.\n\n4. **Build quality gate:**'
)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Fixed remaining numbering")
