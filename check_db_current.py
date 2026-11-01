import sqlite3
import os

print("=== DATABASE QUERY ===")
print("dev.db exists:", os.path.exists('dev.db'))
if os.path.exists('dev.db'):
    conn = sqlite3.connect('dev.db')
    cur = conn.cursor()
    tables = [r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
    print("Number of tables:", len(tables))
    for t in tables:
        count = cur.execute('SELECT COUNT(*) FROM "{}"'.format(t)).fetchone()[0]
        print("  {}: {} records".format(t, count))
    conn.close()
