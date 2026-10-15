import sqlite3

conn = sqlite3.connect('/opt/data/home/workspace/dev/pondok-banat/dev.db')
c = conn.cursor()

# Check if uid_nfc column exists in students table
c.execute("PRAGMA table_info(students)")
cols = c.fetchall()
print("Students table columns:")
for col in cols:
    print(f"  {col[1]}: {col[2]}")
print()

# Check count of uid_nfc populated
c.execute("SELECT COUNT(*) FROM students WHERE uid_nfc IS NOT NULL AND uid_nfc != ''")
print("Students with uid_nfc populated:", c.fetchone()[0])

# Check sample
c.execute("SELECT nisn, name, uid_nfc FROM students WHERE uid_nfc IS NOT NULL AND uid_nfc != '' LIMIT 5")
print("Sample rows with uid_nfc:")
for row in c.fetchall():
    print(f"  {row[0]} | {row[1]} | {row[2]}")

conn.close()
