#!/usr/bin/env python3
"""Get student data from the database."""
import sqlite3
import os

base = "/opt/data/home/workspace/dev/pondok-banat"
db_path = os.path.join(base, "dev.db")
conn = sqlite3.connect(db_path)
cur = conn.cursor()
print("=== Students ===")
for row in cur.execute('SELECT id, nisn, name, status, kelas_id FROM students ORDER BY nisn'):
    print(row)
print()
print("=== Classes ===")
for row in cur.execute('SELECT kode, nama, seksi, jenjang, program FROM classes'):
    print(row)
conn.close()
