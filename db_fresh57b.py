import sqlite3

con = sqlite3.connect("dev.db")
cur = con.cursor()

print("students schema (cols):")
for r in cur.execute("PRAGMA table_info(students)"):
    print("  ", r[1], r[2])

print("\nuid_nfc non-null:", cur.execute("SELECT COUNT(*) FROM students WHERE uid_nfc IS NOT NULL AND TRIM(uid_nfc)!=''").fetchone()[0])
print("uid_nfc sample:", cur.execute("SELECT uid_nfc FROM students WHERE uid_nfc IS NOT NULL LIMIT 3").fetchall())
print("students distinct kelas (sample):", cur.execute("SELECT DISTINCT kelas FROM students LIMIT 5").fetchall())
print("classes sample:")
for r in cur.execute("SELECT id,kode,nama,seksi,jenjang,program FROM classes LIMIT 5").fetchall():
    print("  ", r)
print("teacher count:", cur.execute("SELECT COUNT(*) FROM teachers").fetchone()[0])
print("grade count:", cur.execute("SELECT COUNT(*) FROM grades").fetchone()[0])
print("admin:", cur.execute("SELECT id,email,role FROM users LIMIT 1").fetchone())
print("role sample:", cur.execute("SELECT id,name FROM roles LIMIT 5").fetchall())
print("role_permission sample:", cur.execute("SELECT COUNT(*) FROM role_permissions").fetchone()[0])

con.close()
