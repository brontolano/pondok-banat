import sqlite3

conn = sqlite3.connect('dev.db')
cur = conn.cursor()

print('--- teachers schema ---')
cur.execute('PRAGMA table_info(teachers)')
for r in cur.fetchall():
    print(r)

print('--- teachers status breakdown ---')
cur.execute('SELECT status, COUNT(*) FROM teachers GROUP BY status')
for r in cur.fetchall():
    print(r)

print('--- users schema ---')
cur.execute('PRAGMA table_info(users)')
for r in cur.fetchall():
    print(r)

print('--- classes schema ---')
cur.execute('PRAGMA table_info(classes)')
for r in cur.fetchall():
    print(r)

print('--- grades schema ---')
cur.execute('PRAGMA table_info(grades)')
for r in cur.fetchall():
    print(r)

conn.close()
