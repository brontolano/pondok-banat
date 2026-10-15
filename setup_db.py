import sqlite3, os

base = '/opt/data/home/workspace/dev/pondok-banat'
db_path = os.path.join(base, 'dev.db')

if os.path.exists(db_path):
    os.remove(db_path)

# Read SQL from file
with open('/opt/data/home/workspace/dev/pondok-banat/init_schema.sql', 'r') as f:
    sql_content = f.read()

conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.executescript(sql_content)
conn.commit()
conn.close()
print("Database created:", db_path)
print("Tables:", cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name").fetchall())
