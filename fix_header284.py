import io

path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old_leftover = 'init_schema.sql: 15 tabel. Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Git HEAD (local): `8217a6167574989fa6b9108ce12876ff1085a48b`'
new_fixed = 'init_schema.sql: 15 tabel.'

if old_leftover in content:
    content = content.replace(old_leftover, new_fixed, 1)
    print(f'Fixed. Old leftover remaining: {content.count(old_leftover)}')
else:
    print(f'Old leftover NOT found')
    partial = 'Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Git HEAD (local): `8217a6167574989fa6b9108ce12876ff1085a48b`'
    print(f'Partial match (Verifikasi fresh kondisi): {content.count("Verifikasi fresh kondisi")}')
    print(f'Count of "8217a616": {content.count("8217a616")}')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f'New file size: {len(content)} chars')
