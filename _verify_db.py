import sqlite3
import os

conn = sqlite3.connect('dev.db')
cur = conn.cursor()
tables = ['users','roles','role_permissions','students','classes','teachers','subjects','silabus','rpp','absensi','grades','rapor','announcements','messages','notifications']
for t in tables:
    cur.execute('SELECT COUNT(*) FROM ' + t)
    print(t + ': ' + str(cur.fetchone()[0]))
cur.execute('SELECT COUNT(*) FROM students WHERE status = 0')
print('students inactive: ' + str(cur.fetchone()[0]))
cur.execute('SELECT COUNT(*) FROM students WHERE uid_nfc IS NOT NULL AND uid_nfc != ""')
print('students uid_nfc filled: ' + str(cur.fetchone()[0]))
cur.execute("SELECT id, email, role FROM users")
for r in cur.fetchall():
    print('user: ' + str(r))
conn.close()
