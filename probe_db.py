#!/usr/bin/env python3
import sqlite3, os

base = "/opt/data/home/workspace/dev/pondok-banat"
db_path = os.path.join(base, "dev.db")
conn = sqlite3.connect(db_path)
cur = conn.cursor()

tables = [
    "users", "roles", "role_permissions",
    "students", "classes", "teachers",
    "subjects", "silabus", "rpp",
    "absensi", "grades", "rapor",
    "announcements", "messages", "notifications",
]

for t in tables:
    try:
        cur.execute(f"SELECT COUNT(*) FROM {t}")
        n = cur.fetchone()[0]
        print(f"{t}: {n}")
    except Exception as e:
        print(f"{t}: ERROR {e}")

print()
# sample: classes
cur.execute("SELECT jenjang, seksi, COUNT(*) FROM classes GROUP BY 1,2 ORDER BY 1")
print("classes by jenjang/seksi:")
for r in cur.fetchall():
    print(r)

# Teacher jabatan count
cur.execute("SELECT jabatan, COUNT(*) FROM teachers GROUP BY jabatan ORDER BY 2 DESC")
print("teachers by jabatan:")
for r in cur.fetchall():
    print(r)

conn.close()
