import sqlite3

base = "/opt/data/home/workspace/dev/pondok-banat"
con = sqlite3.connect(base + "/dev.db")
cur = con.cursor()

# Get schema
print("=== Schema ===")
for row in cur.execute("SELECT sql FROM sqlite_master WHERE type='table'"):
    print(row[0])
    print()

# Check students columns
print("=== Students sample ===")
cols = [r[1] for r in cur.execute("PRAGMA table_info(students)")]
print("Columns:", cols)
rows = cur.execute("SELECT * FROM students LIMIT 3").fetchall()
print("Rows:", rows)
print("Count:", cur.execute("SELECT COUNT(*) FROM students").fetchone()[0])

print("\n=== Classes ===")
cols = [r[1] for r in cur.execute("PRAGMA table_info(classes)")]
print("Columns:", cols)
rows = cur.execute("SELECT * FROM classes LIMIT 5").fetchall()
print("Rows:", rows)
print("Count:", cur.execute("SELECT COUNT(*) FROM classes").fetchone()[0])

print("\n=== Teachers ===")
cols = [r[1] for r in cur.execute("PRAGMA table_info(teachers)")]
print("Columns:", cols)
rows = cur.execute("SELECT * FROM teachers LIMIT 3").fetchall()
print("Rows:", rows)
print("Count:", cur.execute("SELECT COUNT(*) FROM teachers").fetchone()[0])

print("\n=== Users ===")
cols = [r[1] for r in cur.execute("PRAGMA table_info(users)")]
print("Columns:", cols)
rows = cur.execute("SELECT * FROM users LIMIT 3").fetchall()
print("Rows:", rows)
print("Count:", cur.execute("SELECT COUNT(*) FROM users").fetchone()[0])

print("\n=== Roles ===")
cols = [r[1] for r in cur.execute("PRAGMA table_info(roles)")]
print("Columns:", cols)
rows = cur.execute("SELECT * FROM roles").fetchall()
print("Rows:", rows)
print("Count:", cur.execute("SELECT COUNT(*) FROM roles").fetchone()[0])

print("\n=== Role_permissions ===")
cols = [r[1] for r in cur.execute("PRAGMA table_info(role_permissions)")]
print("Columns:", cols)
rows = cur.execute("SELECT * FROM role_permissions").fetchall()
print("Rows:", rows)
print("Count:", cur.execute("SELECT COUNT(*) FROM role_permissions").fetchone()[0])

con.close()
