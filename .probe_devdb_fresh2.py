import sqlite3, os, json

db_path = "/opt/data/home/workspace/dev/pondok-banat/dev.db"
print("DB_EXISTS", os.path.exists(db_path))
if os.path.exists(db_path):
    print("DB_SIZE", os.path.getsize(db_path))
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = [r[0] for r in cursor.fetchall()]
    print("TABLE_COUNT", len(tables))
    for t in tables:
        try:
            cursor.execute("SELECT COUNT(*) FROM [" + t + "]")
            cnt = cursor.fetchone()[0]
            print("COUNT_" + t, cnt)
        except Exception as e:
            print("ERR_" + t, str(e))
    conn.close()
