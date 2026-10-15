import sqlite3
base = "/opt/data/home/workspace/dev/pondok-banat"
conn = sqlite3.connect(base + "/dev.db")
cur = conn.cursor()
print("===== students =====")
for row in cur.execute("SELECT id, nisn, name, jk, ttl, kelas_id, status, no_hp FROM students ORDER BY kelas_id, nisn"):
    print(row)
print()
print("===== classes =====")
for row in cur.execute("SELECT id, kode, nama, seksi, jenjang, program, wali_kelas_id FROM classes ORDER BY jenjang, seksi, kode"):
    print(row)
print()
print("===== teachers =====")
for row in cur.execute("SELECT id, nip, name, jk, jabatan, status, kelas_id, no_hp, email FROM teachers ORDER BY jabatan, name"):
    print(row)
print()
print("===== users =====")
for row in cur.execute("SELECT id, email, password, name, role, status FROM users"):
    print(row)
conn.close()
