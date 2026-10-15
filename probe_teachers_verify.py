import sqlite3
conn = sqlite3.connect("/opt/data/home/workspace/dev/pondok-banat/dev.db")
conn.row_factory = sqlite3.Row
print("=== teachers (sample) ===")
for r in conn.execute("SELECT id, nip, name, jabatan, kelas_id FROM teachers ORDER BY id LIMIT 12"):
    print(" ", r["nip"], "|", r["name"], "|", r["jabatan"], "| kelas_id=", r["kelas_id"])
print("=== teachers by jabatan ===")
for r in conn.execute("SELECT jabatan, COUNT(*) c FROM teachers GROUP BY jabatan ORDER BY c DESC"):
    print(" ", r["jabatan"], r["c"])
print("=== classes ===")
for r in conn.execute("SELECT id, kode, nama, jenjang FROM classes ORDER BY id"):
    print(" ", r["kode"], "|", r["nama"], "|", r["jenjang"])
print("=== teachers count by jenjang of kelas ===")
print("total teachers:", conn.execute("SELECT COUNT(*) FROM teachers").fetchone()[0])
conn.close()
