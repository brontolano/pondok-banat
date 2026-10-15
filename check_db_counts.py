import sqlite3

conn = sqlite3.connect("dev.db")
cur = conn.cursor()

print("=== users ===")
for row in cur.execute("SELECT id, email, password, name, role, status FROM users"):
    print(row)

print("\n=== roles ===")
for row in cur.execute("SELECT id, name, display_name, permissions FROM roles"):
    print(row)

print("\n=== role_permissions ===")
for row in cur.execute("SELECT id, role_id, permission FROM role_permissions"):
    print(row)

print("\n=== counts ===")
for table in ["students", "teachers", "classes", "subjects", "silabus", "rpp", "grades", "rapor", "announcements", "messages", "notifications"]:
    print(table, cur.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0])

print("\n=== all tables ===")
for row in cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"):
    print(row)

conn.close()
