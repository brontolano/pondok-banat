import sqlite3, os

DB = "/opt/data/home/workspace/dev/pondok-banat/dev.db"
conn = sqlite3.connect(DB)
cur = conn.cursor()

print("=== STUDENTS TABLE COLUMNS ===")
cols = cur.execute("PRAGMA table_info(students)").fetchall()
for c in cols:
    print(f"  {c[1]}: {c[2]}")

print("\n=== STUDENTS PER CLASS ===")
rows = cur.execute(
    "SELECT jenjang, seksi, COUNT(*) FROM students GROUP BY jenjang, seksi ORDER BY jenjang, seksi"
).fetchall()
total = 0
for r in rows:
    print(f"  {r[0]} {r[1]}: {r[2]}")
    total += r[2]
print(f"  TOTAL: {total}")

print("\n=== STATUS ---")
active = cur.execute("SELECT COUNT(*) FROM students WHERE active = 1").fetchone()[0]
inactive = cur.execute("SELECT COUNT(*) FROM students WHERE active = 0").fetchone()[0]
nfc = cur.execute(
    "SELECT COUNT(*) FROM students WHERE uid_nfc IS NOT NULL AND trim(uid_nfc) != ''"
).fetchone()[0]
print(f"  active={active}, inactive={inactive}")
print(f"  uid_nfc filled: {nfc}")
conn.close()
