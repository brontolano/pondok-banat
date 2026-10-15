import sqlite3
conn = sqlite3.connect('dev.db')
cursor = conn.cursor()
cursor.execute('PRAGMA table_info(classes)')
for row in cursor.fetchall():
    print(row)
cursor.execute('PRAGMA table_info(students)')
for row in cursor.fetchall():
    print(row)
cursor.execute('PRAGMA table_info(subjects)')
for row in cursor.fetchall():
    print(row)
cursor.execute('PRAGMA table_info(grades)')
for row in cursor.fetchall():
    print(row)