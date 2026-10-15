#!/usr/bin/env python3
"""Get actual user email from dev.db."""
import sqlite3, os

DB = "/opt/data/home/workspace/dev/pondok-banat/dev.db"
conn = sqlite3.connect(DB)
cur = conn.cursor()
rows = cur.execute("SELECT id, email, name, role, status FROM users").fetchall()
for r in rows:
    print("user:", r)

# Also check the actual prisma schema for uidNfc definition
schema = open("/opt/data/home/workspace/dev/pondok-banat/prisma/schema.prisma").read()
print("\n--- Schema uidNfc / Sertakan ---")
for i, line in enumerate(schema.split('\n'), 1):
    if 'uidNfc' in line or 'Sertakan' in line:
        print(f"{i}: {line}")

conn.close()
