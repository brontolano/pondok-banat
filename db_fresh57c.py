import sqlite3

con = sqlite3.connect("dev.db")
cur = con.cursor()

print("admin:", cur.execute("SELECT id, email, role FROM users LIMIT 1").fetchall())
print("\nClasses program distribution (from classes table):")
for r in cur.execute("SELECT program, COUNT(*) FROM classes GROUP BY program ORDER BY program").fetchall():
    print("  ", r)

print("\nStudent count per kelas_id (join classes):")
for r in cur.execute("SELECT c.program, COUNT(s.id) FROM students s JOIN classes c ON s.kelas_id = c.id GROUP BY c.program ORDER BY c.program").fetchall():
    print("  ", r)

print("\ngrades distinct kelas_id (sample):", cur.execute("SELECT DISTINCT kelas_id FROM grades LIMIT 3").fetchall())
print("grade ranges:", cur.execute("SELECT MIN(nilai), MAX(nilai) FROM grades").fetchone())

con.close()
