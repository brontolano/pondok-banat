#!/usr/bin/env python3
"""Inspect actual dev.db schema."""
import sqlite3, os

DB = "/opt/data/home/workspace/dev/pondok-banat/dev.db"
conn = sqlite3.connect(DB)
cur = conn.cursor()

print("=== TABLES ===")
rows = cur.execute("SELECT name, sql FROM sqlite_master WHERE type='table' ORDER BY name").fetchall()
for name, sql in rows:
    print(f"\n--- {name} ---")
    print(sql)

print("\n=== PRAGMA table_info for students ---")
for row in cur.execute("PRAGMA table_info(students)").fetchall():
    print(row)

conn.close()
