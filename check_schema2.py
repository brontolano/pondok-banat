import sqlite3

conn = sqlite3.connect('/opt/data/home/workspace/dev/pondok-banat/dev.db')
cur = conn.cursor()

# Print schema for key tables
for t in ['students','classes','users','roles','role_permissions','subjects','rpp','silabus','grades']:
    cur.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='" + t + "'")
    r = cur.fetchone()
    print('=== ' + t + ' ===')
    print(r[0] if r else 'NOT FOUND')
    print()
conn.close()
