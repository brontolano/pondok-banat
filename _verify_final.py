import sqlite3, os, sys

DB = os.path.join(os.path.dirname(__file__), "dev.db")
conn = sqlite3.connect(DB)
cur = conn.cursor()

print("=== PRD FINAL VERIFICATION (cron run) ===")
print(f"DB file: {DB} ({os.path.getsize(DB)} bytes)")

tables = [r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
print(f"TOTAL TABLES: {len(tables)}")
for t in tables:
    cnt = cur.execute(f'SELECT COUNT(*) FROM "{t}"').fetchone()[0]
    print(f"  {t}: {cnt}")

print("\n--- Students per class ---")
rows = cur.execute(
    "SELECT jenjang, seksi, COUNT(*) FROM students GROUP BY jenjang, seksi ORDER BY jenjang, seksi"
).fetchall()
total = 0
for r in rows:
    print(f"  {r[0]} {r[1]}: {r[2]}")
    total += r[2]
print(f"  TOTAL: {total}")

print("\n--- Status ---")
active = cur.execute("SELECT COUNT(*) FROM students WHERE active = 1").fetchone()[0]
inactive = cur.execute("SELECT COUNT(*) FROM students WHERE active = 0").fetchone()[0]
nfc = cur.execute(
    "SELECT COUNT(*) FROM students WHERE uid_nfc IS NOT NULL AND trim(uid_nfc) != ''"
).fetchone()[0]
print(f"  active={active}, inactive={inactive}")
print(f"  uid_nfc filled: {nfc}")

print("\n--- Core counts ---")
print(f"  users: {cur.execute('SELECT COUNT(*) FROM users').fetchone()[0]}")
print(f"  roles: {cur.execute('SELECT COUNT(*) FROM roles').fetchone()[0]}")
print(f"  role_permissions: {cur.execute('SELECT COUNT(*) FROM role_permissions').fetchone()[0]}")
print(f"  students: {cur.execute('SELECT COUNT(*) FROM students').fetchone()[0]}")
print(f"  classes: {cur.execute('SELECT COUNT(*) FROM classes').fetchone()[0]}")
print(f"  teachers: {cur.execute('SELECT COUNT(*) FROM teachers').fetchone()[0]}")
print(f"  subjects: {cur.execute('SELECT COUNT(*) FROM subjects').fetchone()[0]}")
print(f"  grades: {cur.execute('SELECT COUNT(*) FROM grades').fetchone()[0]}")
print(f"  silabus: {cur.execute('SELECT COUNT(*) FROM silabus').fetchone()[0]}")
print(f"  rpp: {cur.execute('SELECT COUNT(*) FROM rpp').fetchone()[0]}")
print(f"  announcements: {cur.execute('SELECT COUNT(*) FROM announcements').fetchone()[0]}")
print(f"  messages: {cur.execute('SELECT COUNT(*) FROM messages').fetchone()[0]}")
print(f"  notifications: {cur.execute('SELECT COUNT(*) FROM notifications').fetchone()[0]}")
print(f"  absensi: {cur.execute('SELECT COUNT(*) FROM absensi').fetchone()[0]}")
print(f"  rapor: {cur.execute('SELECT COUNT(*) FROM rapor').fetchone()[0]}")

conn.close()
print("\n=== VERIFICATION COMPLETE ===")
