import os
import sqlite3

base = '/opt/data/home/workspace/dev/pondok-banat'

print("=== File timestamps ===")
for f in ['init_db.py', 'init_schema.sql', 'prisma/schema.prisma', 'dev.db', 'check_nfc.py']:
    path = os.path.join(base, f)
    if os.path.exists(path):
        mtime = os.path.getmtime(path)
        import datetime
        dt = datetime.datetime.fromtimestamp(mtime)
        print(f"  {f}: {dt}")
    else:
        print(f"  {f}: NOT FOUND")

print()
print("=== Database check ===")
conn = sqlite3.connect(os.path.join(base, 'dev.db'))
c = conn.cursor()
c.execute('PRAGMA table_info(students)')
cols = c.fetchall()
print("Students columns:", [r[1] for r in cols])
c.execute('SELECT COUNT(*) FROM students')
print("Students count:", c.fetchone()[0])
conn.close()
