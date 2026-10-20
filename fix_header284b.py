# Fix the header: remove leftover old header text after the new Rev. 284 header.
# The new header ends with "init_schema.sql: 15 tabel."
# The old header continuation starts with "Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Git HEAD (local): `8217a6167574989fa6b9108ce12876ff1085a48b`"
# We need to remove everything from the start of the old header continuation up to (but not including) the old header's final "init_schema.sql: 15 tabel."

path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# The old header text starts right after "init_schema.sql: 15 tabel." (end of new header)
# and continues with "Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Git HEAD (local): `8217a616...` \"Rev. 282: PRD fresh verification & stability confirmation ...\" ..."
#
# The old header's full continuation is:
old_continuation = ('Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. '
                    'Git HEAD (local): `8217a6167574989fa6b9108ce12876ff1085a48b` "Rev. 282: PRD fresh verification & stability confirmation (19 Oct 2026 WIB); updated header to Rev. 282 + added section 60" '
                    '(branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `8217a6167574989fa6b9108ce12876ff1085a48b`). '
                    'Git HEAD (origin/main): `03fe91a913233ca207008ac82516d9d2d7a6dcd1` (Rev. 279) — berbeda dengan local HEAD (local 3 commit ahead). '
                    'Working tree: PRD mencakup perubahan lokal (revisi terbaru = Rev. 283, belum dicomit). Local branch **3 commit ahead**, **0 commit behind** origin/main. '
                    'Database (dev.db): file dev.db saat ini tidak ada (absent) — dihapus oleh commit "Release: clean core files only" (1dc891d) dan .gitignore mencantumkan *.db; '
                    'seluruh record (453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) tidak tersedia dan harus di-import ulang menggunakan skrip semula '
                    '(init_db.py, init_schema.sql; import_excel.py dan import_students_grades_clean.py tidak ditemukan di working tree). '
                    'Build quality gate: NO LONGER RE-RUNABLE — node_modules/absent (0 package; .bin tidak ada); .next ada (partial: cache + diagnostics + package.json + server + static + trace + trace-build + turbopack + types, bukan production build). '
                    'tsc --noEmit, npm run lint, npm run build memerlukan npm instal ulang sebelum dapat dijalankan. '
                    'M02a (NFC): field uid_nfc masih di schema Prisma, init_schema.sql baris 44, init_db.py baris 60, namun 0 siswa terisi (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format AF:C2:99:E7). '
                    'Auth hardcode: src/components/Login.tsx masih pakai admin@pondokanbat.com / admin123 (domain pondokanbat.com (sesuai nama \'Pondok Banat\')); produksi butuh bcrypt + session. '
                    'Beranda: src/app/page.tsx (login page) masih hardcode; belum ada dashboard utama yang terhubung ke DB. '
                    'Prisma: 17 model terdefinisi (termasuk KitabProgress, Sertakan — ditambahkan Rev. 51). init_schema.sql: 15 tabel.')

# Replace the combination of new header end + old continuation with just the new header end
# i.e. "init_schema.sql: 15 tabel." + old_continuation -> "init_schema.sql: 15 tabel."
fix = 'init_schema.sql: 15 tabel. ' + old_continuation

if fix in content:
    content = content.replace(fix, 'init_schema.sql: 15 tabel.', 1)
    print('Fixed! Old header continuation removed.')
    remaining = content.count(old_continuation)
    print(f'Remaining old continuation count: {remaining}')
else:
    print('Old continuation NOT found exactly. Trying partial...')
    partial = 'Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Git HEAD (local): `8217a6167574989fa6b9108ce12876ff1085a48b`'
    print(f'Partial match: {content.count(partial)}')
    # Find the position of the new header end
    new_end = content.find('init_schema.sql: 15 tabel.')
    while new_end != -1:
        pos = new_end + len('init_schema.sql: 15 tabel.')
        if pos < len(content) and content[pos:pos+5] == ' Verif':
            print(f'Found new header end at position {new_end}, next char is space + "Verif"')
            print(f'Context: {repr(content[pos-20:pos+100])}')
        new_end = content.find('init_schema.sql: 15 tabel.', new_end + 1)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f'Final file size: {len(content)} chars')
