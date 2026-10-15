import sqlite3

base = "/opt/data/home/workspace/dev/pondok-banat"
con = sqlite3.connect(base + "/dev.db")
cur = con.cursor()

print("=== TEACHERS TABLE ===")
cols = [r[1] for r in cur.execute('PRAGMA table_info(teachers)')]
print("columns:", cols)
for r in cur.execute('SELECT * FROM teachers LIMIT 5'):
    print(r)

print("\n=== CLASSES TABLE ===")
cols = [r[1] for r in cur.execute('PRAGMA table_info(classes)')]
print("columns:", cols)
for r in cur.execute('SELECT * FROM classes LIMIT 5'):
    print(r)

print("\n=== STUDENTS SAMPLE ===")
cols = [r[1] for r in cur.execute('PRAGMA table_info(students)')]
print("columns:", cols)
for r in cur.execute('SELECT * FROM students LIMIT 3'):
    print(r)

print("\n=== ROLES ===")
for r in cur.execute('SELECT * FROM roles'):
    print(r)

print("\n=== ROLE_PERMISSIONS ===")
for r in cur.execute('SELECT * FROM role_permissions LIMIT 5'):
    print(r)

con.close()
