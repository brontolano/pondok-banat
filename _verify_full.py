import sqlite3

DB = "/opt/data/home/workspace/dev/pondok-banat/dev.db"
conn = sqlite3.connect(DB)
cur = conn.cursor()

print("=== STUDENTS PER CLASS ===")
rows = cur.execute(
    """
    SELECT c.jenjang, c.seksi, c.kode, COUNT(s.id) as cnt
    FROM students s
    JOIN classes c ON s.kelas_id = c.id
    GROUP BY c.jenjang, c.seksi, c.kode
    ORDER BY c.jenjang, c.seksi, c.kode
    """
).fetchall()
total = 0
for r in rows:
    print(f"  {r[0]} {r[1]} ({r[2]}): {r[3]}")
    total += r[3]
print(f"  TOTAL: {total}")

print("\n=== STATUS ---")
active = cur.execute("SELECT COUNT(*) FROM students WHERE status = 'active'").fetchone()[0]
inactive = cur.execute("SELECT COUNT(*) FROM students WHERE status = 'inactive'").fetchone()[0]
nfc = cur.execute(
    "SELECT COUNT(*) FROM students WHERE uid_nfc IS NOT NULL AND trim(uid_nfc) != ''"
).fetchone()[0]
print(f"  active={active}, inactive={inactive}")
print(f"  uid_nfc filled: {nfc}")

print("\n=== CLASS SUMMARY ---")
class_totals = cur.execute(
    """
    SELECT c.jenjang, c.seksi, c.kode, COUNT(s.id)
    FROM classes c
    LEFT JOIN students s ON s.kelas_id = c.id
    GROUP BY c.jenjang, c.seksi, c.kode
    ORDER BY c.jenjang, c.seksi, c.kode
    """
).fetchall()
for r in class_totals:
    print(f"  {r[0]} {r[1]} ({r[2]}): {r[3]}")

print("\n=== COMPONENT COUNTS ---")
checks = [
    ("users", "users"),
    ("roles", "roles"),
    ("role_permissions", "role_permissions"),
    ("students", "students"),
    ("classes", "classes"),
    ("teachers", "teachers"),
    ("subjects", "subjects"),
    ("grades", "grades"),
    ("silabus", "silabus"),
    ("rpp", "rpp"),
    ("absensi", "absensi"),
    ("rapor", "rapor"),
    ("announcements", "announcements"),
    ("messages", "messages"),
    ("notifications", "notifications"),
]
for tbl, _ in checks:
    cnt = cur.execute(f"SELECT COUNT(*) FROM {tbl}").fetchone()[0]
    print(f"  {tbl}: {cnt}")

print("\n=== SAMPLES ===")
print("users:", cur.execute("SELECT * FROM users").fetchall())
print("roles:", cur.execute("SELECT * FROM roles").fetchall())
print("role_permissions:", cur.execute("SELECT * FROM role_permissions LIMIT 5").fetchall())
print("classes:", cur.execute("SELECT * FROM classes").fetchall())
conn.close()
