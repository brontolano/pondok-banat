import sqlite3
import os

db_path = '/opt/data/home/workspace/dev/pondok-banat/dev.db'
print('DB exists:', os.path.exists(db_path))
print('DB size:', os.path.getsize(db_path) if os.path.exists(db_path) else 'N/A')
print()

conn = sqlite3.connect(db_path)
cur = conn.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
tables = [r[0] for r in cur.fetchall()]
print('=== TABLES (', len(tables), ') ===')
for t in tables:
    cur.execute('SELECT COUNT(*) FROM "' + t + '"')
    cnt = cur.fetchone()[0]
    print(f'  {t}: {cnt} records')
conn.close()
