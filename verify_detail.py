import sqlite3
con = sqlite3.connect('dev.db')
sc = [r[1] for r in con.execute('PRAGMA table_info(students)')]
cc = [r[1] for r in con.execute('PRAGMA table_info(classes)')]
print('students cols:', sc)
print('classes cols:', cc)
rows = con.execute("SELECT c.nama, COUNT(s.id) FROM students s JOIN classes c ON s.kelas_id=c.id GROUP BY c.nama ORDER BY c.id")
total = 0
for row in rows:
    print(row)
    total += row[1]
print("TOTAL:", total)
print("=== Role count ===")
print("roles:", con.execute('SELECT COUNT(*) FROM roles').fetchone()[0])
print("=== role_permissions ===")
print("role_permissions:", con.execute('SELECT COUNT(*) FROM role_permissions').fetchone()[0])
