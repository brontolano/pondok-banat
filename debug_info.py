#!/usr/bin/env python3
import sqlite3
conn = sqlite3.connect('/opt/data/home/workspace/dev/pondok-banat/dev.db')
cur = conn.cursor()
print("=== students schema ===")
for row in cur.execute('PRAGMA table_info(students)').fetchall():
    print(row)
print("\n=== students sample ===")
for row in cur.execute('SELECT * FROM students LIMIT 5').fetchall():
    print(row)
print("\n=== classes sample ===")
for row in cur.execute('SELECT * FROM classes LIMIT 5').fetchall():
    print(row)
print("\n=== teachers sample ===")
for row in cur.execute('SELECT * FROM teachers LIMIT 3').fetchall():
    print(row)
conn.close()
