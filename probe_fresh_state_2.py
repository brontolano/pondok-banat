import sqlite3

conn = sqlite3.connect('/opt/data/home/workspace/dev/pondok-banat/dev.db')
cur = conn.cursor()

print('=== users table schema ===')
cur.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='users'")
print(cur.fetchone()[0])

print()
print('=== values ===')
cur.execute('SELECT * FROM users')
cols = [description[0] for description in cur.description]
print('columns:', cols)
for r in cur.fetchall():
    print(r)

print()
print('=== classes table schema ===')
cur.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='classes'")
print(cur.fetchone()[0])

conn.close()
