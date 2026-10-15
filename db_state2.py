#!/usr/bin/env python3
import sqlite3, os

root = '/opt/data/home/workspace/dev/pondok-banat'
db_path = os.path.join(root, 'dev.db')
con = sqlite3.connect(db_path)
cur = con.cursor()

# students with status
cur.execute("SELECT status, COUNT(*) FROM students GROUP BY status ORDER BY status")
print("=== students status counts ===")
for r in cur.fetchall():
    print(r)

# students sample with actual columns
print("\n=== students sample (all columns) ===")
cur.execute("SELECT * FROM students LIMIT 3")
for r in cur.fetchall():
    print(r)

# classes
print("\n=== classes ===")
cur.execute("SELECT * FROM classes LIMIT 20")
for r in cur.fetchall():
    print(r)

# teachers
print("\n=== teachers sample (first 3) ===")
cur.execute("SELECT * FROM teachers LIMIT 3")
for r in cur.fetchall():
    print(r)

# subjects
print("\n=== subjects count ===")
cur.execute("SELECT COUNT(*) FROM subjects")
print(cur.fetchone()[0])

# grades
print("\n=== grades count ===")
cur.execute("SELECT COUNT(*) FROM grades")
print(cur.fetchone()[0])

# users
print("\n=== users ===")
cur.execute("SELECT * FROM users LIMIT 5")
for r in cur.fetchall():
    print(r)

# roles
print("\n=== roles ===")
cur.execute("SELECT * FROM roles LIMIT 10")
for r in cur.fetchall():
    print(r)

# role_permissions
print("\n=== role_permissions ===")
cur.execute("SELECT * FROM role_permissions LIMIT 5")
for r in cur.fetchall():
    print(r)
