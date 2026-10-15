#!/usr/bin/env python3
"""Get a summary of student data in the Data Nilai Excel file and the current database."""
import sqlite3
import openpyxl

base = "/opt/data/home/workspace/dev/pondok-banat"
db_path = f"{base}/dev.db"

# Database students
conn = sqlite3.connect(db_path)
cur = conn.cursor()
print("=== DB Students (10) ===")
for row in cur.execute("SELECT id, nisn, name, status, kelas_id FROM students"):
    print(dict(row))
conn.close()

# Excel student count from Data Nilai
wb = openpyxl.load_workbook(f"{base}/.data-pondokanat/Data Nilai Semester 1 TA 2026_2027.xlsx", read_only=True)
print("\n=== Excel Data Nilai sheets ===")
print("Sheets:", wb.sheetnames)
for name in wb.sheetnames:
    ws = wb[name]
    # Count data rows (skip header rows)
    data_rows = 0
    for row in ws.iter_rows(values_only=True):
        if row[0] is not None and isinstance(row[0], (int, float)) and row[0] > 0:
            data_rows += 1
    print(f"  {name}: ~{data_rows} data rows")
wb.close()

# Excel student count from Data Banat
wb2 = openpyxl.load_workbook(f"{base}/.data-pondokanat/Data Banat 2026-2027.xlsx", read_only=True)
print("\n=== Data Banat 2026-2027 sheets ===")
print("Sheets:", wb2.sheetnames)
for name in wb2.sheetnames:
    ws = wb2[name]
    print(f"  {name}: {ws.max_row} rows x {ws.max_column} cols")
wb2.close()
