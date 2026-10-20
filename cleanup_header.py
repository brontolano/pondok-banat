# Clean up leftover old header text after the new Rev. 284 header in line 4
path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'

with open(path, 'r') as f:
    content = f.read()

# Check for leftover old header text
import re

# The new header ends with "init_schema.sql: 15 tabel."
# The leftover old header text starts with "Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil"
# and includes the old git hash references.

# Find the pattern: new header end + leftover old text
# The old header text is: "Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Git HEAD (local): `8217a6167574989fa6b9108ce12876ff1085a48b` \"Rev. 282: PRD fresh verification & stability confirmation (19 Oct 2026 WIB); updated header to Rev. 282 + added section 60\" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `8217a6167574989fa6b9108ce12876ff1085a48b`). Git HEAD (origin/main): `03fe91a913233ca207008ac82516d9d2d7a6dcd1` (Rev. 279) — berbeda dengan local HEAD (local 3 commit ahead). Working tree: PRD mencakup perubahan lokal (revisi terbaru = Rev. 283, belum dicomit). Local branch **3 commit ahead**, **0 commit behind** origin/main. Database (dev.db): file dev.db saat ini tidak ada (absent) — dihapus oleh commit \"Release: clean core files only\" (1dc891d) dan .gitignore mencantumkan *.db; seluruh record (453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) tidak tersedia dan harus di-import ulang menggunakan skrip semula (init_db.py, init_schema.sql; import_excel.py dan import_students_grades_clean.py tidak ditemukan di working tree). Build quality gate: NO LONGER RE-RUNABLE — node_modules/absent (0 package; .bin tidak ada); .next ada (partial: cache + diagnostics + package.json + server + static + trace + trace-build + turbopack + types, bukan production build). tsc --noEmit, npm run lint, npm run build memerlukan npm instal ulang sebelum dapat dijalankan. M02a (NFC): field uid_nfc masih di schema Prisma, init_schema.sql baris 44, init_db.py baris 60, namun 0 siswa terisi (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format AF:C2:99:E7). Auth hardcode: src/components/Login.tsx masih pakai admin@pondokanbat.com / admin123 (domain pondokanbat.com (sesuai nama 'Pondok Banat')); produksi butuh bcrypt + session. Beranda: src/app/page.tsx (login page) masih hardcode; belum ada dashboard utama yang terhubung ke DB. Prisma: 17 model terdefinisi (termasuk KitabProgress, Sertakan — ditambahkan Rev. 51). init_schema.sql: 15 tabel."

# Simpler approach: find the leftover text pattern and remove it
# The leftover starts with " Verifikasi fresh kondisi repo + dev.db" (note the leading space)
# and ends with "init_schema.sql: 15 tabel." (duplicate)

# Let's check what's there
old_leftover = " Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Git HEAD (local): `8217a6167574989fa6b9108ce12876ff1085a48b` \"Rev. 282: PRD fresh verification & stability confirmation (19 Oct 2026 WIB); updated header to Rev. 282 + added section 60\" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `8217a6167574989fa6b9108ce12876ff1085a48b`). Git HEAD (origin/main): `03fe91a913233ca207008ac82516d9d2d7a6dcd1` (Rev. 279) — berbeda dengan local HEAD (local 3 commit ahead). Working tree: PRD mencakup perubahan lokal (revisi terbaru = Rev. 283, belum dicomit). Local branch **3 commit ahead**, **0 commit behind** origin/main. Database (dev.db): file dev.db saat ini tidak ada (absent) — dihapus oleh commit \"Release: clean core files only\" (1dc891d) dan .gitignore mencantumkan *.db; seluruh record (453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) tidak tersedia dan harus di-import ulang menggunakan skrip semula (init_db.py, init_schema.sql; import_excel.py dan import_students_grades_clean.py tidak ditemukan di working tree). Build quality gate: NO LONGER RE-RUNABLE — node_modules/absent (0 package; .bin tidak ada); .next ada (partial: cache + diagnostics + package.json + server + static + trace + trace-build + turbopack + types, bukan production build). tsc --noEmit, npm run lint, npm run build memerlukan npm instal ulang sebelum dapat dijalankan. M02a (NFC): field uid_nfc masih di schema Prisma, init_schema.sql baris 44, init_db.py baris 60, namun 0 siswa terisi (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format AF:C2:99:E7). Auth hardcode: src/components/Login.tsx masih pakai admin@pondokanbat.com / admin123 (domain pondokanbat.com (sesuai nama 'Pondok Banat')); produksi butuh bcrypt + session. Beranda: src/app/page.tsx (login page) masih hardcode; belum ada dashboard utama yang terhubung ke DB. Prisma: 17 model terdefinisi (termasuk KitabProgress, Sertakan — ditambahkan Rev. 51). init_schema.sql: 15 tabel."

if old_leftover in content:
    print("Found old leftover text (full match)")
    content = content.replace(old_leftover, "")
else:
    # Try partial match
    # Find the old leftover start
    old_start = "Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil."
    if old_start in content:
        print("Found old leftover start")
        idx = content.find(old_start)
        # Find the end (the second "init_schema.sql: 15 tabel.")
        # The new header ends with "init_schema.sql: 15 tabel."
        # So we need to remove from idx to the second occurrence
        first = content.find("init_schema.sql: 15 tabel.", idx)
        second = content.find("init_schema.sql: 15 tabel.", first + 1)
        if second != -1:
            print("Found old leftover in range", first, second)
            content = content[:first] + content[second:]
        else:
            print("Could not find end")
    else:
        print("Old leftover start not found")

with open(path, 'w') as f:
    f.write(content)

print("File size:", len(content))
