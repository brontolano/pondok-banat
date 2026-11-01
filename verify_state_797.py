import sqlite3, os

conn = sqlite3.connect('/opt/data/home/workspace/dev/pondok-banat/dev.db')
cur = conn.cursor()

# List all tables
cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
tables = [r[0] for r in cur.fetchall()]
print(f"TABLE_COUNT: {len(tables)}")

# Count records per table
total_records = 0
for t in tables:
    cur.execute(f'SELECT COUNT(*) FROM "{t}"')
    cnt = cur.fetchone()[0]
    total_records += cnt
    print(f"  {t}: {cnt}")

print(f"TOTAL_RECORDS: {total_records}")
conn.close()

# node_modules stats
nm = '/opt/data/home/workspace/dev/pondok-banat/node_modules'
if os.path.isdir(nm):
    dirs = sum([len(d) for d in os.walk(nm)])
    files = sum([len(f) for _, _, f in os.walk(nm)])
    print(f"NODE_MODULES_DIRS: {dirs}")
    print(f"NODE_MODULES_FILES: {files}")

# dev.db size
db_path = '/opt/data/home/workspace/dev/pondok-banat/dev.db'
print(f"DEV_DB_SIZE: {os.path.getsize(db_path)}")
