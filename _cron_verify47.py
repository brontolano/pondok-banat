import sqlite3
conn = sqlite3.connect('/opt/data/home/workspace/dev/pondok-banat/dev.db')
cur = conn.cursor()
tables = [r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
print("TABLES:", tables)
for t in tables:
    cnt = cur.execute("SELECT COUNT(*) FROM \"" + t + "\"").fetchone()[0]
    print("  %s: %d" % (t, cnt))
print("\n--- siswa per kelas ---")
for row in cur.execute("SELECT kelas_id, COUNT(*) FROM students GROUP BY kelas_id"):
    print(" ", row)
print("\nuid_nfc filled:", cur.execute("SELECT COUNT(*) FROM students WHERE uid_nfc IS NOT NULL AND uid_nfc != ''").fetchone()[0])
conn.close()
