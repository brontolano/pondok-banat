import sqlite3, re
con = sqlite3.connect('/opt/data/home/workspace/dev/pondok-banat/dev.db')
cur = con.cursor()
# Verify role_permissions content
print("--- role_permissions (role_id, module, read/write/export/admin) ---")
for r in cur.execute("SELECT role_id, module, read_access, write_access FROM role_permissions ORDER BY role_id").fetchall():
    print("  ", r)
print()
print("--- students sample (id,nisn,name,jk,kelas_id,status,uid_nfc) ---")
for r in cur.execute("SELECT id,nisn,name,jk,kelas_id,status,uid_nfc FROM students LIMIT 3").fetchall():
    print("  ", r)
print()
print("--- users sample ---")
for r in cur.execute("SELECT id,email,password,role,status FROM users").fetchall():
    print("  ", r)
print()
print("--- grades sample ---")
for r in cur.execute("SELECT * FROM grades LIMIT 2").fetchall():
    print("  ", r)
